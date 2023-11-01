from flask import Flask
from flask import render_template
from flask import request
from yt_dlp import YoutubeDL
import os
# from mega import Mega 
from flask import  make_response
import datetime



### 関数定義 
def read_log(video_list_path):
    video_list = []
    with open(video_list_path) as f:
        for s_line in f:
            video_list.append(s_line)
    return video_list

## log書き込み
def write_log(file_path, log):
    with open(file_path, encoding='shift_jis') as f:
        l = f.readlines()

    l.insert(0, log+'\n')

    with open(file_path, mode='w',encoding='shift_jis') as f:
        f.writelines(l)


## 行を削除
def delete_line(file_path, del_text):
    with open(file_path, mode='r+') as f:
        size = os.path.getsize(file_path)

        if size == 0: #リストがからの場合
            pass
        else:
            for i, line in enumerate(f):
                l = f.readlines()
                if del_text in line: #一致する文字列を削除
                    l.insert(i, '')
                    with open(file_path, mode='w') as f:
                        f.writelines(l)



## ファイル削除関数
def delete_file(video_list_path):
    video_list = read_log(video_list_path)
    if len(video_list) < 1:
        pass
    else:
        try:
            for video_path in video_list:
                video_path = video_path.replace("\n", "") #改行コードを削除
                os.remove(video_path) # ファイルを削除
                delete_line(video_list_path, str(video_path)) #video_list.txtの行を削除

        except FileNotFoundError:
            print("#### FileNotFoundError エラーっす")
            delete_line(video_list_path, str(video_path))  #video_list.txtの行を削除
            delete_file(video_list_path)  #エラーが無くなるまで再起呼び出し



app = Flask(__name__) #インスタンス作成
## templateを使用するやり方
@app.route('/')
def index():
    #return name
    return render_template('index.html') #変更

## POSTリクエストが来た時の処理
@app.route('/', methods=['POST']) #indexページにてPOSTが来た
def post():
    # 前処理
    current_dir = os.path.dirname(os.path.abspath(__file__)) #カレントディレクトリ取得(venv/src)
    venv_dir = os.path.abspath(os.path.join(current_dir, os.pardir)) #1つ上のディレクトリを取得(/venv)
    project_dir = os.path.abspath(os.path.join(venv_dir, os.pardir)) #1つ上のディレクトリを取得(venvの一つ上)
    video_list_path = venv_dir + "/src/static/video_list.txt"
    log_path = venv_dir + "/src/static/log.txt"
    print(venv_dir)
    print(project_dir)

    # 最初にファイルが残っていたら削除
    delete_file(video_list_path)

    yt_url = request.form.get('url') #nameがurlの要素を取得
    format_name = ".mp3"

    # オプション設定
    ydl_opts = {
        'outtmpl' : '%(id)s'+ format_name,
        'title': '%(title)s',
        'format' : 'bestaudio',
        'playlistreverse':True, #プレイリストの古い順に取得
        'max_filesize':700000000, #最大ファイルサイズを指定(bytes), 現状は700MBまで許容
        # 'max_downloads' : '1', #最大ダウンロード数
    }
    
    ### youtube からダウンロード
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(yt_url) 
        print("##### ビデオ情報")
        info = ydl.extract_info(yt_url, download=False)
        video_id = info.get('id', None)
        video_title = info.get('title', None)
        # file_path = current_dir + "/" + video_id + format_name #repl.t用
        file_path = project_dir + "/" + video_id + format_name
        print(video_title)
        print(file_path)
        print("#########")

        ## 記録用
        dt_now = datetime.datetime.now()
        log = dt_now.strftime('%Y-%m-%d %H:%M:%S')+ ", " + video_title + ", " + yt_url  #ログの内容
        write_log(video_list_path, file_path) #削除処理記録用
        write_log(log_path, str(log)) #個人的な記録用

    MIMETYPE = 'audio/mpeg'

    # クライアント側へダウンロードさせる処理
    res = make_response()
    res.data  = open(file_path, "rb").read()
    res.headers['Content-Type'] = MIMETYPE
    res.headers['Content-Disposition'] = 'attachment; filename=' + video_title.encode().decode('unicode-escape') + format_name
    return res



if __name__ == "__main__":
    app.run()


## 本番用
# if __name__ == "__main__":
#   from waitress import serve
#   serve(app, host="0.0.0.0", port=3000)


# # Storageにアップロード(MEGA無料ストレージを使用)
# mega = Mega()
# email = ""
# password = ""
# m = mega.login(email,password)
# file = m.upload(file_path)

# # Storageのパスを返す
# storage_path = m.get_upload_link(file)
# print(storage_path)

# # Strageからdownloadさせる
# m.download_url(storage_path) 

