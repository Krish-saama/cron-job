import dbaccess
import json
import pkg_resources
from urllib import request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import base64
import os

installed_packages = {
    d.project_name: d.version for d in pkg_resources.working_set}


class check:
    def checkpackages():
        try:
            lsres = dbaccess.dbaccessdetails.frameworkdetails()
            data = json.loads(lsres.data)
            for fetch in data['result']:
                lsreponame = fetch['repositoriename']
                lsrepomail = fetch["repomail"]
                url = os.getenv('GIT_BASE_URL') + \
                    fetch['accountname'] + "/" + lsreponame + \
                    "/contents/requirements.txt?ref=" + \
                    fetch['branchname'] + ""
                payload = {}
                headers = {
                    'Authorization': 'token ' + os.getenv('GIT_AUTH_TOKEN')
                }
                strresponse = requests.request(
                    "GET", url, headers=headers, data=payload)
                jsres = json.loads(strresponse.text)
                lscon = jsres['content']
                lscon = base64.b64decode(lscon)
                for line in lscon.splitlines():
                    lspacname = line.decode()
                    lssplitval = lspacname.split("==")
                    lspac = lssplitval[0].strip()
                    lsstrver = lssplitval[1].strip()
                    lsinstalledver = lsstrver.replace(".", "")
                    res = [str(i)
                           for i in lsinstalledver.split() if i.isdigit()]
                    lsinstalledver = ""
                    for ele in res:
                        lsinstalledver += ele
                    lsinttblver = int(lsinstalledver)
                    url = os.getenv('PYPI_URL').replace("#pack#", lspac)
                    releases = json.loads(request.urlopen(url).read())['info']
                    lsversion = str(releases["version"])
                    lssummary = releases["summary"]
                    lsrelease = releases["release_url"]
                    lsinstpack = lspac + " " + lsversion
                    lsintlatestver = int(lsversion.replace(".", ""))
                    if(lsinttblver < lsintlatestver):
                        # we need using for auto install logic currently disabled
                        # implement pip as a subprocess:
                        # subprocess.check_call([sys.executable, '-m', 'pip', 'install', lspac])
                        # process output with an API in the subprocess module:
                        # reqs = subprocess.check_output(
                        #     [sys.executable, '-m', 'pip', lspac])
                        # summary
                        #  lsres = dbaccess.dbaccessdetails.updateframwork(lspac,lsversion)
                        check.mailsend(lsrepomail, lsreponame, lspac, lsstrver,
                                       lsversion, lsrelease, lssummary)
                    else:
                        print(lsinstpack, "Already installed latest")
            return lsres
        except Exception as e:
            print("CHECKPAKAGES FUN EXCEPTION : ", e)

    def mailsend(repomail, reponame, pspackage, lsstrver, latestver, releaseurl, psdescription):
        try:
            msg = MIMEMultipart()
            message = "<h1>Installed the package version Details: </h1><b><p>Repo name: " + reponame + "</p><b><p>Package name: " + pspackage + \
                "</p><b><p>Current used version: " + lsstrver + "</p><b><p>Available latest version: " + \
                latestver + "</p><b><p>Relase URL: " + releaseurl + "</p><b>"
            # setup the parameters of the message
            password = os.getenv('PASSWORD')
            msg['From'] = os.getenv('MAIL_FROM')
            msg['To'] = repomail
            msg['Cc'] = os.getenv('CC')
            msg['Subject'] = os.getenv('SUBJECT')
            # add in the message body
            # msg.attach(MIMEText(message, 'plain'))
            msg.attach(MIMEText(message, 'html'))
            # create server
            server = smtplib.SMTP(os.getenv('SMTP'))
            server.starttls()
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            print("successfully sent email to %s:" % (msg['To']))
        except Exception as e:
            print("MAILSEND FUN EXCEPTION : ", e)
