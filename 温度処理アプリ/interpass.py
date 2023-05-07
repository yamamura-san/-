import PySimpleGUI as sg
import pandas as pd
import datetime
import glob
from natsort import natsorted
import os
import configparser

# tracelogとtemplogからパス間温度を計算する。簡易GUI上で処理できるように
def main():
    # テーマ設定
    sg.theme("SystemDefault ")

    # PHの機械座標の設定値を読み出し、iniファイルに保存しておきいつでもデフォルト値を変えられるように
    config = configparser.ConfigParser()
    config.read("setting.ini")
    value1 = config["Data"]["z_position"]

    # ウィンドウのレイアウト定義
    layout = [[sg.Text("tracelogフォルダ", size = (15, 1)), sg.InputText(key = "foldername1", size = (20, 1)), sg.FolderBrowse("フォルダ読込",target = "foldername1", size = (15, 1))],
              [sg.Text("温度logファイル", size = (15, 1)), sg.InputText(key = "filename1", size = (20, 1)), sg.FileBrowse("フォルダ読込",target = "filename1", size = (15, 1))],
              [sg.Text("gcodeファイル", size = (15, 1)), sg.InputText(key = "filename2", size = (20, 1)), sg.FileBrowse("ファイル読込",target = "filename2", size = (15, 1))],
              [sg.Text("退避機械座標", size = (15, 1)), sg.InputText(value1, key = "position", size = (20, 1))],
              [sg.Button("パス間温度計算実行", key = "bt1")]]
    
    window = sg.Window("パス間温度計算ツール", layout)

    while True:
        event, values = window.read()

        # ウィンドウ閉じる処理、ループから抜ける
        if event == sg.WIN_CLOSED:
            break

        # 変換ボタンを押したときに変換関数を呼び出し、ポップアップを表示する処理
        if event == "bt1":
            print("処理を開始します。")
            # 温度ログの前処理
            folderpath_temp = values["filename1"]
            data_temp, process_folder, output_folder  = templog_prepro(folderpath_temp)
            print("温度処理完了")
            # マージしたいtracelog格納フォルダを選択し、マージを行う
            folderpath_merge = values["foldername1"]
            # マージ処理
            data_merge = tracelog_merge(folderpath_merge, process_folder)
            print("マージ処理完了")

            # 造形している部分とウェイトかかっている位置のログを抽出
            filepath_gcode = values["filename2"]
            pos = values["position"]
            data_merge_pathtime = wait_time(data_merge, filepath_gcode, pos, process_folder)
            print("ウェイト時刻処理完了")

            # パス間温度計算処理
            path_temp(data_merge_pathtime, data_temp, output_folder)
            print("処理完了")

            # ポップアップ表示
            sg.popup("計算完了")
    
    window.close()    


# tracelogのマージ処理。長い造形だと複数ログにまたがってしまうため。
def tracelog_merge(input_folder, output_folder):
    # マージ後のファイル名
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    filename = "tracelog_merge_" + current_time +".csv" 
    filepath = output_folder + "/" + filename

    # 指定フォルダのcsvファイルを読み込み
    log_list = glob.glob(input_folder + "/*csv")
    log_list = natsorted(log_list)

    # 一つ目のcsvファイルを読み込む
    df = pd.read_csv(log_list[0], converters={'JobName':str, 'DateTime':str})

    # ログが2つ以上ある場合は以降のループ処理でログをマージさせる
    # 初期値定義
    i = 1
    # フォルダ内のログの数が1より大きい場合はループを実行
    while i < len(log_list):
        # 昇順で並び変えたcsvファイルを一次的に格納する
        df_tmp = pd.read_csv(log_list[i], converters={'JobName':str, 'DateTime':str})
        # もとのdfとのマージ
        df = pd.concat([df, df_tmp])
        i = i + 1
    
    df.to_csv(filepath)

    return filepath


# tracelogから造形を実施している部分だけのデータを抽出し、ウェイトがかかる時刻を計算する処理。それ以外の情報は不要なので除去
def wait_time(file_tracelog, file_gcode, wait_Z, process_folder):

    # マージしたtracelogのcsvファイルの読み込み
    data = pd.read_csv(file_tracelog, converters={'JobName':str, 'DateTime':str})

    # 必要な情報だけを抜き出し保存するファイル名、パス
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    filename = "interpass_time_" + current_time + ".csv"
    filepath =  process_folder+ "/" + filename
    
    # gcode名とtracelogのjob名が一致する行だけを抽出
    # gcodeファイルからから拡張子gcodeの除去
    file_gcode = os.path.splitext(os.path.basename(file_gcode))[0]
    # 加工を行っている部分だけを取り出すため、jobnameと一致するJobが投入されている箇所を抽出
    data = data[data["JobName"] == file_gcode]
    
    # 不要な列の除去
    # 抽出リスト
    data_list = ["JobName", "DateTime", "CNC_MAC_POS_Z"]
    # リストをもとにdfを整理
    data = data[data_list]
    print(data.head())

    # Zがウェイト位置から下降する位置を判定するための前進差分計算(Time_n - Time_n+1) 正の値を持つ場合、次の時刻でZが下降しているということ
    data["diff_POS_Z"] = data["CNC_MAC_POS_Z"].diff(-1)
    print(data.head())

    # ウェイトしている最終時刻だけを抽出する。機械座標が引数指定の位置でかつ、前進差分値が正ならば、そのときの時刻はウェイトの最終時刻ということ
    data = data[(data["CNC_MAC_POS_Z"] == wait_Z) & (data["diff_POS_Z"] > 0)]

    # パス数の計算
    num_layer = len(data)
    print(num_layer)
    # 1~最終パス番号までのリストを準備
    list_layer = list(range(1, num_layer + 1))
    # 0列目にレイヤー番号を入れる処理
    data.insert(0, "Layer", list_layer)

    # 必要なのは層情報、時刻データだけなので他は除去
    data_list2 = ["Layer", "DateTime"]
    data = data[data_list2]

    # 保存
    data.to_csv(filepath, index=False)

    return filepath


# 温度ログの処理、設定情報等が最初の10数行にわたって記述してあるのでそれらを取り除く処理
def templog_prepro(file):

    # 温度データ格納先のフォルダ定義
    # 温度データ格納先フォルダ抽出
    data_temp_folder = os.path.dirname(file)
    # 各種ログ処理時の途中データ保存するフォルダのパス定義
    process_folder = data_temp_folder + "/interpass_process"
    # フォルダ作成
    os.makedirs(process_folder, exist_ok= True)

    # 前処理後の保存ファイル名
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    filename = "temperature_prepro_" + current_time + ".csv"
    filepath = process_folder +"/"+ filename

    # ログデータの列名を作成、列名と列数に特に意味はない。ただこの列を作ってあげないとpandas側でエラーを吐く。とりあえず１０列用意
    col_name = range(1,10,1)

    # 上記で定義したカラム名でデータを読み込む
    df = pd.read_csv(file, names = col_name, encoding = "shift-jis", index_col=0)

    # "Time"以下の行をスライスで読み込みを行う。Timeより前のデータはカメラの設定値情報だからカット
    df = df.loc["Time": ]

    # 欠損値のある列を削除する。10列分仮で用意したが、おそらく2列分程度しかデータは取らないと思うから除去してあげる
    df= df.dropna(how = "all", axis = 1)

    # 保存 前処理のために作成した列名は削除する
    df.to_csv(filepath, header=False)

    return filepath, process_folder, data_temp_folder

# ウェイトがかかる時刻に最も近い温度データを抜き出す処理
def path_temp(interpass_time, temperature, output_folder):
    # 出力先ファイル名
    now = datetime.datetime.now()
    current_time = now.strftime("%Y-%m-%d-%H-%M")
    filename = "interpass_temp_ "+ current_time + ".csv"
    filepath = output_folder +"/"+ filename

    # データの読み込み
    df_trace = pd.read_csv(interpass_time)
    df_temp = pd.read_csv(temperature)

    # str型の時刻をdatetime型に変換
    df_temp["Time"] = pd.to_datetime(df_temp["Time"], format='%Y-%m-%d %H:%M:%S')
    # インデックスを"Time"に変換する
    df_temp = df_temp.set_index("Time")

    # 空のリストを用意,とりあえず4つ分観察エリアの温度データを格納できるように
    list1 = []

    # 無数の温度データの中から、パス間とする時刻（加工ヘッドが停止した時刻）に最も近い温度時刻を抽出する処理
    # パス間の時刻を基にループ
    for wait_time in df_trace["DateTime"]:
        # 探索処理
        target = df_temp.index[df_temp.index.get_loc(pd.to_datetime(wait_time), 'nearest')]

        list1.append(df_temp.loc[target][0])

    df_trace["No1"] = list1

    df_trace.to_csv(filepath, index = False)


if __name__ == "__main__":
    main()