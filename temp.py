import pandas as pd
import os
import glob
from natsort import natsorted


def merge(folder):
    # マージ後のファイル名
    merge_name = "tracelog_merge.csv"

    # 指定フォルダのcsvファイルを読み込み
    log_list = glob.glob(folder + "/*csv")
    log_list = natsorted(log_list)

    # 一つ目のcsvファイルを読み込む
    df = pd.read_csv(log_list[0])

    # ログが2つ以上ある場合は次のループ処理でログをマージさせる
    # 初期値定義
    i = 1
    # フォルダ内のログの数が1より大きい場合はループを実行
    while i < len(log_list):
        # 昇順で並び変えたcsvファイルを一次的に格納する
        df_tmp = pd.read_csv(log_list[i])
        # もとのdfとのマージ
        df = pd.concat([df, df_tmp])
        i = i + 1
    
    df.to_csv(merge_name)

    return merge_name


def temp(filename, jobname, wait_Z):
    # csvファイルの読み込み
    data = pd.read_csv(filename)
    
    # gcode名とjob名が一致する行だけを抽出
    # jobnameから拡張子gcodeの除去
    jobname = os.path.splitext(os.path.basename(jobname))[0]
    # 加工を行っている部分だけを取り出すため、jobnameと一致するJobが投入されている箇所を抽出
    data = data[data["JobName"] == jobname]
    
    # 不要な列の除去
    # 抽出リスト
    data_list = ["JobName", "DateTime", "CNC_MAC_POS_Z"]
    # リストをもとにdfを整理
    data = data[data_list]

    # Zがウェイト位置から下降する位置を判定するための前進差分計算 正の値を持つ場合、次の時刻でZが下降しているということ
    data["diff_POS_Z"] = data["CNC_MAC_POS_Z"].diff(-1)
    
    # 機械座標が引数指定の位置でかつ、前進差分値が正ならば、そのときの時刻はウェイトの最終時刻ということ
    data = data[(data["CNC_MAC_POS_Z"] == wait_Z) & (data["diff_POS_Z"] > 0)]

    num_layer = len(data)
    list_layer = list(range(1, num_layer + 1))
    data.insert(0, "Layer", list_layer)

    # 必要なのは層情報、時刻データだけなので他は除去
    data_list2 = ["Layer", "DateTime"]
    data = data[data_list2]

    # 保存
    data.to_csv("path_time.csv", index=False)

if __name__ == "__main__":
    log_name = merge("trace")
    temp(log_name, "test.test.gcode", 220)