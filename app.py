import datetime
import logging
import logging.handlers
from flask import Flask
from flask import render_template
from flask import session as ses
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "hogehoge"

# db 接続
USER_NAME = "admin"
PASSWORD = "PkYKANK2w6s7M3H"
HOST = "develop.ckpyo7l7ljdb.ap-northeast-1.rds.amazonaws.com"
DB_NAME = ""
DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    USER_NAME,
    PASSWORD,
    HOST,
    DB_NAME
)
ENGINE = create_engine(DATABASE, encoding="utf-8", echo=True)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

# ログ設定
LOGFILE = "test.log"
app.logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(LOGFILE)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
app.logger.addHandler(fh)


@app.route('/')
def hello_world():
    app.logger.info("処理開始")

    val1 = "■ webサーバ現在日時：%s" \
           % datetime.datetime.now()
    val2 = "■ db サーバ現在日時：%s" \
           % session.execute("select now()").next()[0]

    if not ses.get("init"):
        ses["init"] = True
        ses["sid"] = datetime.datetime.now().strftime("%y%m%d%H%M%S")
        val3 = "■ セッション新規作成：%s" % ses.get("sid")
        print(ses.items())
    else:
        val3 = "■ セッション既存利用：%s" % ses.get("sid")
        print(ses.items())
    values = {"val1": val1, "val2": val2, "val3": val3}

    app.logger.info("処理終了")
    return render_template('index.html', values=values)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
