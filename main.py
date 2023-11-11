from flask import Flask
from flask import render_template
from flask import request
from yt_dlp import YoutubeDL
import os

# from mega import Mega
from flask import make_response
import datetime
import uuid
import json

# const
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  #カレントディレクトリ取得 (./)
VIDEO_LIST_PATH = os.path.join(CURRENT_DIR ,"log", "video_list.txt")
LOG_PATH = os.path.join(CURRENT_DIR,"log", "log.txt")
VIDEO_FOLDER_PATH = os.path.join(CURRENT_DIR ,"video")

### 関数定義
def read_log(video_list_path):
  video_list = []
  with open(video_list_path) as f:
    for s_line in f:
      video_list.append(s_line)
  return video_list


## log書き込み
def write_log(file_path, log):
  with open(file_path, mode='a', encoding='utf_8') as f:
    f.writelines("\n"+log)

## 行を削除
def delete_line(file_path, del_text):
  with open(file_path, mode='r+') as f:
    size = os.path.getsize(file_path)

    if size == 0:  #リストがからの場合
      pass
    else:
      for i, line in enumerate(f):
        l = f.readlines()
        if del_text in line:  #一致する文字列を削除
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
        video_path = video_path.replace("\n", "")  #改行コードを削除
        print(video_path)
        os.remove(video_path)  # ファイルを削除
        delete_line(video_list_path, str(video_path))  #video_list.txtの行を削除
        print("deleteしたっす: " + video_path)

    except FileNotFoundError:
      print("#### FileNotFoundError エラーっす")
      delete_line(video_list_path, str(video_path))  #video_list.txtの行を削除
      delete_file(video_list_path)  #エラーが無くなるまで再起呼び出し


app = Flask(__name__)  #インスタンス作成

## templateを使用するやり方
@app.route('/')
def index():
  #return name
  return render_template('index.html')  #変更


## POSTリクエストが来た時の処理
@app.route('/', methods=['POST'])  #indexページにてPOSTが来た
def post():
  
  # video_list_path = current_dir + "/log/video_list.txt"
  # log_path = current_dir + "/log/log.txt"
  # video_folder_path = current_dir + "/video/"

  # ファイル削除
  delete_file(VIDEO_LIST_PATH)

  yt_url = request.form.get('url')  #nameがurlの要素を取得
  format_name = ".mp3"
 

  uuid_4 = str(uuid.uuid4())
  # オプション設定
  ydl_opts = {
      'outtmpl':  os.path.join(VIDEO_FOLDER_PATH , uuid_4 + '%(id)s' + format_name),  #/video/ファイル名.mp4 (uuidをファイル名の頭につけて被らないようにしている)
      'title': '%(title)s',
      'format': 'bestaudio',
      'playlistreverse': True,  #プレイリストの古い順に取得
      'max_filesize': 700000000,  #最大ファイルサイズを指定(bytes), 現状は700MBまで許容
      # 'max_downloads' : '1', #最大ダウンロード数
  }

  ## infoを取り出す
  with YoutubeDL() as ydl:
    print("##### ビデオ情報")
    info = ydl.extract_info(yt_url, download=False)

    #### テスト用 #TODO 再生リストに対応させる！
    #### print("プレイリストかどうか：", info.get('_type')) 
    # if info.get('_type') == 'None': #1動画
    # elif info.get('_type') == 'playlist': #プレイリスト
    # else: #例外


  ## ダウンロード
  with YoutubeDL(ydl_opts) as ydl:

    info = ydl.extract_info(yt_url, download=False)
    video_id = info.get('id', None)
    video_title = info.get('title', None)
    file_path =  os.path.join(VIDEO_FOLDER_PATH , uuid_4 + video_id + format_name)
    print(video_title)
    print(file_path)
    print("#########")
    ydl.download(yt_url) #ダウンロード

    ## 記録用
    dt_now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    log = dt_now_jst.strftime(
        '%Y-%m-%d %H:%M:%S') + ", " + video_title + ", " + yt_url  #ログの内容
    write_log(VIDEO_LIST_PATH, file_path)  #削除処理記録用
    write_log(LOG_PATH, str(log))  #個人的な記録用

    ## json書き出しテスト
    # json_path =  os.path.join(CURRENT_DIR , "log","json.txt")
    # write_log(json_path, json.dumps(info, indent=2, ensure_ascii=False))  #個人的な記録用

  MIMETYPE = 'audio/mpeg'

  # ダウンロード処理
  res = make_response()
  res.data = open(file_path, "rb").read()
  res.headers['Content-Type'] = MIMETYPE
  res.headers[
      'Content-Disposition'] = 'attachment; filename=' + video_title.encode(
      ).decode('unicode-escape') + format_name
  return res


if __name__ == "__main__":
  from waitress import serve
  ## ファイル新規作成
  if not os.path.isfile(VIDEO_LIST_PATH):
    with open(VIDEO_LIST_PATH, mode='w') as f:
      pass
  
  ## flask run
  serve(app, host="0.0.0.0", port=3000)

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
