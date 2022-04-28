from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from sqlalchemy import text

db = SQLAlchemy()

class dbaccessdetails:
    def frameworkdetails():
        sql = text("select * from packagesdetails")
        result = db.engine.execute(sql)
        print(result)
        return jsonify({'result': [dict(row) for row in result]})

    def updateframwork(pspackagename,psversion):
        sql = text("update packagesdetails set version = '"+ psversion +"' where packagename = '"+ pspackagename +"'")
        result = db.engine.execute(sql)
        print(result)
        return jsonify({'result': [dict(row) for row in result]})    
