# デプロイ実験用サンプルプログラム

新しく環境作成した際に、試しに実行できるようなサンプル

* 実行環境での現在日時
* DBでの現在日時(MYSQL)
* セッションの利用
* ログ出力

あたりをやっている。

## 簡単デプロイ方法

* 仮想環境作成
```
# gitから取得 & venv作成
cd /home/ec2-user/
git clone https://github.com/re-24/deploySampleFlask
python3 -m venv ./venv

# 環境切り替え
. venv/bin/activate

# パッケージインストール
pip install -r requirements.txt
pip install uwsgi
```

* nginx インストール
```
sudo yum install nginx
```
※ http://<IPアドレス>/ で nginxのwelcomeページが表示されるの確認

* nginx 設定を修正(/etc/nginx/nginx.conf)
```
#user nginx; # flask実行するユーザに合わせて修正
user ec2-user;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;
・・・・
```

* nginx 設定を新規追加修正(/etc/nginx/config.d/uwsgi.conf)
```
server {

    listen       80;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ec2-user/uwsgi.sock;
    }
}
```

* uwsgi 設定ファイル作成(/home/ec2-user/deploySampleFlask/app.ini)
```
[uwsgi]
module = app
callable = app
master = true
processes = 1
socket = /home/ec2-user/uwsgi.sock
chmod-socket = 666
vacuum = true
die-on-term = true
wsgi-file = /home/ec2-user/deploySampleFlask/app.py
logto = /home/ec2-user/deploySampleFlask/app.log
```

## 他の参考サイトの通りやって嵌った事柄
* tmp直下は、private tmp(?)になるらしく、uwsgiから見れない
  (tmpに作られるファイルがマスタリングされる)
* nginxとuwsgiの実行ユーザが一致していないとpermission denied