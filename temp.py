import pandas as pd
import glob

def temp_log(folder):
    # 前処理後の保存ファイル名
    filename = "temp_time.csv"

    # glob関数でデータ取得 ファイル名は変わるからのファイル名に依存しないこの処理がいいか
    filepath = glob.glob(folder + "/*csv")[0]

    # ログデータの列名を作成、列名と列数に特に意味はない。この列を作ってあげないとpandasがエラーを吐く。とりあえず１０列用意
    col_name = range(1,10,1)

    # 定義したカラム名でデータを読み込む
    df = pd.read_csv(filepath, names = col_name, encoding = "shift-jis", index_col=0)

    # "Time"以下の行をスライスで読み込み
    df = df.loc["Time": ]

    # 欠損値のある列を削除する。10列分仮で用意したが、おそらく2列分程度しかデータは取らないと思うから除去してあげる
    df= df.dropna(how = "all", axis = 1)

    # 保存 前処理のために作成した列名は削除する
    df.to_csv(filename, header=False)

    return filename

if __name__ == "__main__":
    temp_log("temp")