from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from softwareStatic import create_static_table
import os
import re
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def software_search():
    try:
        df = pd.read_csv("./staticSearch/staticTable.csv", keep_default_na=False)
    except FileNotFoundError as e:

        df = create_static_table()
        print(e)
    
    table = df.to_html(classes='table-striped" id = "softwareTable',index=False,border=1)

    return render_template("software_search.html",table=table)

@app.route("/dynamic")
def software_search_dynamic():
    df = pd.read_csv('./dynamicSearch/combined_data.csv',keep_default_na=False)
    df.insert(9,"Example Use",np.nan)
    df.fillna('',inplace=True)
    table = df.to_html(classes='table-striped" id = "softwareTableDynamic',index=False,border=1)
    return render_template("software_search.html", table=table)

@app.route("/example_use/<software_name>")
def get_example_use(software_name):

    if software_name == '7-Zip':
        software_name = '7z'

    file_directory = "./dynamicSearch/softwareUse/"
    
    normalize_software_name = re.escape(software_name).lower()

    pattern = re.compile(normalize_software_name, re.IGNORECASE)

    try:
        for filename in os.listdir(file_directory):
            if pattern.search(filename):
                with open(os.path.join(file_directory,filename),'r') as file:
                    file_content = file.read()
                    return(jsonify({"use": file_content}))
        return jsonify({"use": '**Unable to find use case record**'})
    except Exception as e:
        print(e)
        return(jsonify({"use": '**Unable to find use case record**'})), 500


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)