import pandas as pd
import datetime

def path_temp(csv_trace, csv_temp):
    # マージ先ファイル名
    filename = "interpass_temp.csv"

    # データの読み込み
    df_trace = pd.read_csv(csv_trace)
    df_temp = pd.read_csv(csv_temp)

    # str型の時刻をdatetime型に変換
    df_temp["Time"] = pd.to_datetime(df_temp["Time"], format='%Y-%m-%d %H:%M:%S')
    # インデックスを"Time"に変換する
    df_temp = df_temp.set_index("Time")

    # 空のリストを用意,とりあえず4つ分観察エリアの温度データを格納できるように
    list1 = []
    list2 = []

    # 無数の温度データの中から、パス間とする時刻（加工ヘッドが停止した時刻）に最も近い温度時刻を抽出する処理
    # パス間の時刻を基にループ
    for wait_time in df_trace["DateTime"]:
        # 探索処理
        target = df_temp.index[df_temp.index.get_loc(pd.to_datetime(wait_time), 'nearest')]

        list1.append(df_temp.loc[target][0])
        list2.append(df_temp.loc[target][1])

    df_trace["No1"] = list1
    df_trace["No2"] = list2

    df_trace.to_csv(filename, index = False)

if __name__ == "__main__":
    path_temp("path_time.csv", "temp_time.csv")