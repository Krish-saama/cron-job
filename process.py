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

installed_packages = {
    d.project_name: d.version for d in pkg_resources.working_set}


class check:
    def checkpackages():
        lsres = dbaccess.dbaccessdetails.frameworkdetails()
        data = json.loads(lsres.data)
        # print(data['result'])
        print("installed_packages", installed_packages)
        for fetch in data['result']:
            print(fetch['packagename'])
            lspac = fetch['packagename']
            lstblpackversion = fetch['version']
            lsinstalledver = installed_packages[lspac]
            lsvercheck = bool(lsinstalledver and not lsinstalledver.isspace())
            url = f'https://pypi.python.org/pypi/{lspac}/json'
            releases = json.loads(request.urlopen(url).read())['info']
            lsversion = str(releases["version"])
            lssummary = releases["summary"]
            print("lsversion", lsversion)
            print("lssummary", lssummary)
            lsinstpack = lspac + lsversion
            lsintlatestver = int(lsversion.replace(".", ""))
            if(lsvercheck):
                lsinttblver = int(lsinstalledver.replace(".", ""))
            else:
                lsinttblver = 0
            if(lsinttblver < lsintlatestver):
                # implement pip as a subprocess:
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', lsinstpack])
                # process output with an API in the subprocess module:
                reqs = subprocess.check_output(
                    [sys.executable, '-m', 'pip', lsinstpack])
                # summary
            #  lsres = dbaccess.dbaccessdetails.updateframwork(lspac,lsversion)
                print(releases)
            else:
                print(lsinstpack, "Already installed latest")

        # print(releases)
        # return sorted(releases, key=parse_version, reverse=True)
        return lsres

    def mailsend():
      label = subprocess.check_output(["git", "describe"]).strip() 
      print("git user details: ", label) 
        # create message object instance
      msg = MIMEMultipart()
      message = "Thank you"
      # setup the parameters of the message
      password = "@gk8072721917"
      msg['From'] = "pgopalakrishnan1996@gmail.com"
      msg['To'] = "gopalakrishnan.palanisamy@saama.com"
      msg['Subject'] = "Subscription"
      # add in the message body
      msg.attach(MIMEText(message, 'plain'))
      # create server
      server = smtplib.SMTP('smtp.gmail.com: 587')
      server.starttls()
      # Login Credentials for sending the mail
      server.login(msg['From'], password)
      # send the message via the server.
      server.sendmail(msg['From'], msg['To'], msg.as_string())
      server.quit()
      print("successfully sent email to %s:" % (msg['To']))
