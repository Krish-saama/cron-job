from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from flask import Flask
import json
from urllib import request
import process
from pkg_resources import parse_version
import tables
import sched
import time
from dotenv import load_dotenv
load_dotenv()
s = sched.scheduler(time.time, time.sleep)


app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True, port=3000)


def do_something():
    print("Doing stuff...")
    app = tables.create_app()
    app.app_context().push()
    process.check.checkpackages()
    s.enter(1, 1, do_something, (s,))


@app.route('/hello', methods=['GET', 'POST'])
def welcome():
    print(tables.db.engine)
    lsres = process.check.checkpackages()
    print(lsres)
    return "Hello World!"


@app.route('/versions/<pkg_name>', methods=['GET', 'POST'])
def versions(pkg_name):
    url = f'https://pypi.python.org/pypi/{pkg_name}/json'
    releases = json.loads(request.urlopen(url).read())['releases']
    return sorted(releases, key=parse_version, reverse=True)


scheduler = BackgroundScheduler()
scheduler.add_job(func=do_something, trigger="interval", seconds=120)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
