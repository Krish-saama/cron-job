# import imp
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
# from importlib.abc import Traversable
from flask import Flask
import threading
import json
import sys
from urllib import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, true
import process
from pkg_resources import parse_version
import dbaccess
import sched
import time
# from shared.db import db
s = sched.scheduler(time.time, time.sleep)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1/item?user=postgres&password=postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dbaccess.db.init_app(app)
app = dbaccess
app.appcon
# with app.app_context():
#     dbaccess.db.create_all()


# def schedulerclass():
    

def do_something():
    print("Doing stuff...")
    process.check.checkpackages()
    # do your stuff
    s.enter(1, 1, do_something, (s,))
if __name__ == '__main__':
    # create_app()
    app.run(debug=True,port=3000)

# schedulerclass()



@app.route('/hello', methods=['GET', 'POST'])
def welcome():
    # process.check.mailsend()
    lsres = process.check.checkpackages()
    print(lsres)
    return "Hello World!"


@app.route('/versions/<pkg_name>', methods=['GET', 'POST'])
def versions(pkg_name):
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    # print(releases)
    return sorted(releases, key=parse_version, reverse=True)


scheduler = BackgroundScheduler()
scheduler.add_job(func=do_something, trigger="interval", seconds=5)
scheduler.start()   
atexit.register(lambda: scheduler.shutdown())

