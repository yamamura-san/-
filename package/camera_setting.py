import PySimpleGUI as sg
import configparser

def setting():

    # iniファイル読み込み
    config = configparser.ConfigParser()
    config.read("package/config.ini")
    cfg_read_1 = config["Data"]["videotime"]
    cfg_read_2 = config["Data"]["exposuretime"]
    cfg_read_3 = config["Data"]["fps"]
    cfg_read_4 = config["Data"]["gain"]
    cfg_read_5 = config["Data"]["x_min"]
    cfg_read_6 = config["Data"]["x_max"]
    cfg_read_7 = config["Data"]["y_min"]
    cfg_read_8 = config["Data"]["y_max"]

    # GUI設定
    sg.theme('Dark Blue 3')
    layout = [
        [sg.Text('撮影設定を入力してください')],
        [sg.Text('撮影時間 [s]', size=(20, 1)), sg.InputText(cfg_read_1)],      
        [sg.Text('露光時間(19 um≧) [us]', size=(20, 1)), sg.InputText(cfg_read_2)],
        [sg.Text('フレームレート [fps]', size=(20, 1)), sg.InputText(cfg_read_3)],
        [sg.Text('ゲイン(≦48 dB) [dB]', size=(20, 1)), sg.InputText(cfg_read_4)],
        [sg.Text('トリムx_min [pix]', size=(20, 1)), sg.InputText(cfg_read_5)],      
        [sg.Text('トリムx_max [pix]', size=(20, 1)), sg.InputText(cfg_read_6)],
        [sg.Text('トリムy_min [pix]', size=(20, 1)), sg.InputText(cfg_read_7)],
        [sg.Text('トリムy_max [pix]', size=(20, 1)), sg.InputText(cfg_read_8)],
        [sg.Submit(button_text='設定完了')]
        ]

    window = sg.Window('撮影条件設定', layout)

    while True:
        event, values = window.read()
        if event is None:
            print('exit')
            break

        if event == '設定完了':
            show_message = "撮影時間は{0} [s]\n".format(values[0])
            show_message += "露光時間は{0} [us]\n".format(values[1])
            show_message += "フレームレートは{0} [fps]\n".format(values[2])
            show_message += "ゲインは{0} [dB]\n".format(values[3])
            val0, val1, val2, val3, val4, val5, val6, val7= int(values[0]), int(values[1]) ,int(values[2]),int(values[3]), int(values[4]), int(values[5]) ,int(values[6]),int(values[7])
            sg.popup(show_message)
            break

    # configの各項目に上書き
    config["Data"]["videotime"] = values[0]
    config["Data"]["exposuretime"]= values[1]
    config["Data"]["fps"] = values[2]
    config["Data"]["gain"] = values[3]
    config["Data"]["x_min"] = values[4]
    config["Data"]["x_max"]= values[5]
    config["Data"]["y_min"] = values[6]
    config["Data"]["y_max"] = values[7]

    # config.iniファイルに上書き
    with open("package/config.ini", "w") as f:
        config.write(f)


    window.close()
    return val0, val1, val2, val3, val4, val5, val6, val7

if __name__ == "__main__":
    print(setting())