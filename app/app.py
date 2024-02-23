from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import json
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/")
def software_search():
    df = pd.read_csv('./softwareInfo.csv',na_filter=False)
    print(type(df))
    table = df.to_html(classes='table-striped" id = "softwareTable',index=False,border=1)

    return render_template("software_search.html",table=table)


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)