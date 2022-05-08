from ast import Str
import dbaccess
import json
import pkg_resources
import sys
import subprocess
from urllib import request
# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import requests
import base64
# import l

installed_packages = {
    d.project_name: d.version for d in pkg_resources.working_set}


class check:
    def checkpackages():
        lsres = dbaccess.dbaccessdetails.frameworkdetails()
        data = json.loads(lsres.data)
        # print(data['result'])
        # print("installed_packages", installed_packages)
        
        for fetch in data['result']:
            lsreponame = fetch['repositoriename']
            url = "https://api.github.com/repos/"+ fetch['accountname'] +"/"+ lsreponame +"/contents/requirementsjson.txt?ref="+ fetch['branchname'] +""
            payload={}
            headers = {
              'Authorization': 'token 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'
            }            
            strresponse = requests.request("GET", url, headers=headers, data=payload)
            print(strresponse.text)
            jsres = json.loads(strresponse.text)
            lscon = jsres['content']
            lscon = base64.b64decode(lscon)
            print(lscon)

            lsreqjson = json.loads(lscon)
            for k in lsreqjson:
                print(k, lsreqjson[k])
                # for line in lscon.splitlines():
                #   print(line)
                #   lineResult = libLAPFF.parseLine(line)
                # lspac = fetch['packagename']
                lspac = k
                lsinstalledver = installed_packages[lspac]
                lsvercheck = bool(lsinstalledver and not lsinstalledver.isspace())
                url = f'https://pypi.python.org/pypi/{lspac}/json'
                releases = json.loads(request.urlopen(url).read())['info']
                lsversion = str(releases["version"])
                lssummary = releases["summary"]
                lsrelease = releases["release_url"]
                lsinstpack = lspac + " " +lsversion
                lsintlatestver = int(lsversion.replace(".", ""))
                if(lsvercheck):
                    lsinttblver = int(lsinstalledver.replace(".", ""))
                else:
                    lsinttblver = 0
                if(lsinttblver <= lsintlatestver):
                    # implement pip as a subprocess:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', lspac])
                    # process output with an API in the subprocess module:
                    # reqs = subprocess.check_output(
                    #     [sys.executable, '-m', 'pip', lspac])
                    # summary
                #  lsres = dbaccess.dbaccessdetails.updateframwork(lspac,lsversion)
                    check.mailsend(lsreponame,lspac,lsinstalledver,lsversion,lsrelease,lssummary)
                    print("Successfully installed")
                else:
                    print(lsinstpack, "Already installed latest")
        return lsres

    def mailsend(reponame,pspackage,currver, latestver, releaseurl, psdescription):
        #   label = subprocess.check_output(["git", "describe"]).strip()
        #   print("git user details: ", label)
        # create message object instance
        msg = MIMEMultipart()
        message = "<h1>Installed the package version Details: </h1><b><p>Repo name: "+ reponame +"</p><b><p>Package name: "+ pspackage +"</p><b><p>Current used version: "+ currver +"</p><b><p>Available latest version: "+ latestver +"</p><b><p>Relase URL: "+ releaseurl +"</p><b>"
        # setup the parameters of the message
        password = "@gk8072721917@"
        msg['From'] = "pgopalakrishnan1996@gmail.com"
        msg['To'] = "Gopalakrishnan.palanisamy@saama.com"
        msg['Cc'] = "Gopalakrishnan.palanisamy@saama.com"
        msg['Subject'] = "Subscription"
        # add in the message body
    #   msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(message, 'html'))
        # create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("successfully sent email to %s:" % (msg['To']))
