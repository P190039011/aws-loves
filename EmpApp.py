from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'student'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('AddEmp.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addstdnt", methods=['POST'])
def AddStdnt():
    reg_id = request.form['reg_id']
    full_name = request.form['first_name']
    cert_name = request.form['cert_name']
    verifi_num = request.form['verifi_num']
    specialisation = request.form['specialisation']
    stdnt_pdf_file = request.files['stdnt_pdf_file']

    insert_sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (reg_id, full_name, certi_name, verifi_num, specialisation))
        db_conn.commit()
        stdnt_name = "" + full_name
        # Uplaod image file in S3 #
        stdnt_pdf_file_name_in_s3 = "reg-id-" + str(reg_id) + "_pdf_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=stdnt_pdf_file_name_in_s3, Body=stdnt_pdf_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                stdnt_pdf_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=stdnt_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
