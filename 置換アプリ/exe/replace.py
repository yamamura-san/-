import PySimpleGUI as sg
import os
import configparser

# GUI処理
def gui():
    # テーマ設定
    sg.change_look_and_feel("DarkAmber")

    # PHの機械座標の設定値を読み出し、iniファイルに保存しておきいつでもデフォルト値を変えられるように
    config = configparser.ConfigParser()
    config.read("setting.ini")
    value1 = config["Data"]["z_position"]

    # レイアウト設定、ファイルの選択とｍ座標指定と実行ボタンがあれば十分、退避座標は基本的に変更がないのでiniファイルに標準値を入れておく
    layout = [[sg.Text("ファイル選択"), sg.InputText(key = "filename", size = (20, 1)), sg.FileBrowse("ファイル読込",target = "filename")],
              [sg.Text("退避機械座標"), sg.InputText(value1, key = "position", size = (20, 1))],
              [sg.Button("変換実行", key = "bt1")]]

    window = sg.Window("パス変換ツール", layout)

    while True:
        event, values = window.read()

        # ウィンドウ閉じる処理、ループから抜ける
        if event == sg.WIN_CLOSED:
            break

        # 変換ボタンを押したときに変換関数を呼び出し、ポップアップを表示する処理
        if event == "bt1":
            # 辞書からfilenameを取り出す
            filepath = values["filename"]
            pos = values["position"]

            # 変換関数を実行
            replace_gcode(filepath, pos)

            # ポップアップ表示
            sg.popup("変換完了")
    
    window.close()


# 加工パス修正処理
def replace_gcode(filename, pos):
    # 置換前のファイル読み込み
    with open(filename) as file:
        content = file.read()
    
    # 置換処理
    content = content.replace(";MESH:NONMESH", ";TTTTTTTTTT")

    # 置換ファイル保存
    # 保存先のディレクトリ指定
    dir = os.path.dirname(filename)
    # 返還前のファイル名取得
    ori_name = os.path.basename(filename).split('.', 1)[0]
    # 保存ファイル名指定
    dst_name = dir + "/" + ori_name + "_ams7010.gcode"
    print(dst_name)
    with open(dst_name, "w") as dst_file:
        dst_file.write(content)

if __name__ == "__main__":
    gui()