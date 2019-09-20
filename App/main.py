# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import logging

from flask import Flask
import pymysql
import time

from flask import request, render_template, redirect, url_for
import pandas as pd


app = Flask(__name__, template_folder='template')
UPLOAD_FOLDER = '/path/to/the/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024


@app.route('/')
def hello():
    # prepare a cursor object using cursor() method
    db = pymysql.connect("remotemysql.com", "gbxDvsOVi9", "1ZHZ7XXr3y", "gbxDvsOVi9" )
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute("SELECT VERSION()")
    # Fetch a single row using fetchone() method.
    data = cursor.fetchone()
    print ("Database version : %s " % data)
    # disconnect from server
    db.close()
    return render_template('ack.html', db = "Database version : %s " % data)


@app.route('/goto')
def goto():
    return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        #feild validations
        if 'file' not in request.files:
            return render_template('error.html',msg = "Error: No file uploaded")
        file = request.files.get('file')
        if file.filename == '' or file.filename.split(".")[1].lower()!='csv':
            return render_template('error.html',msg = "Error: No file uploaded, Please upload CSV")
        #connecttion
        db = pymysql.connect("remotemysql.com", "gbxDvsOVi9", "1ZHZ7XXr3y", "gbxDvsOVi9" )
        df = pd.read_csv(file)
        if len(df.columns) >= 4 or df.shape[0] >= 500000 or df.shape[0] == 0:
            return render_template('error.html',msg = "Error: Number of Columns greater than 5 or number of rows greater than 5 lacs")
        try:
            start = time.time()
            cursor = db.cursor()
            cursor.execute("DROP TABLE IF EXISTS SUB")
            # Create table as per requirement
            sql = """CREATE TABLE SUB( """
            for j in df.columns:
                sql += "_".join(j.lower().split())+" VARCHAR(100),"
            sql = sql[:-1]
            sql += ")"
            cursor.execute(sql)
            col = " , ".join(["_".join(j.lower().split()) for j in df.columns])
            st = ",".join(('%s '*df.shape[1]).split())
            sql = """INSERT INTO SUB( {} ) VALUES ({})""".format(col, st)
            cursor.executemany(sql, df.values.tolist())
            db.commit()
            end = time.time()
        except Exception:
            return render_template('error.html', msg = "Error: DBException")
            db.rollback()
        finally:
            db.close()
        return render_template('upload.html', shape=df.shape, status=True, t= end - start)
    else:
        return render_template('upload.html')
    return render_template('upload.html', status=False)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template('error.html',msg = "Error: File Too Large , Please upload less than 10 MB"), 413


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]
