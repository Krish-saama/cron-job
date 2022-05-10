from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from sqlalchemy import text
import tables


class dbaccessdetails:
    def frameworkdetails():
        try:
            sql = text(
                "select * from repositoriesdetails where activestatus = TRUE")
            result = tables.db.engine.execute(sql)
            print(result)
            return jsonify({'result': [dict(row) for row in result]})
        except Exception as e:
            print("FRAMEWORKDETAILS FUN EXCEPTION : ", e)

    def updateframwork(pspackagename, psversion):
        try:
            sql = text("update packagesdetails set version = '" +
                       psversion + "' where packagename = '" + pspackagename + "'")
            result = tables.db.engine.execute(sql)
            print(result)
            return jsonify({'result': [dict(row) for row in result]})
        except Exception as e:
            print("UPDATEFRAMWORK FUN EXCEPTION : ", e)
