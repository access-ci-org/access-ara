from flask import Flask, render_template, request
from dotenv import load_dotenv
import json
from .models.rps import RPS
from .models.gui import GUI
from .models.researchField import ResearchFields
from .models.jobClass import JobClass
from .models.software import Software
from .models.rpInfo import RpInfo
from .logic.form_logging import log_form_data
from .logic.recommendation import get_recommendations
from .confluence.checkPage import check_page

app = Flask(__name__)

@app.route("/")
def recommender_page():

    rps = RPS.select()
    research_fields = ResearchFields.select().order_by(ResearchFields.field_name)
    guis = GUI.select()
    return render_template("questions.html", 
                           rps = rps, 
                           research_fields = research_fields,
                           guis = guis)

@app.route("/get_research_fields")
def get_research_fields():
    research_fields = ResearchFields.select().order_by(ResearchFields.field_name)
    return([field.field_name for field in research_fields])

@app.route("/get_job_classes")
def get_job_classes():
    job_classes = JobClass.select().order_by(JobClass.class_name)
    return([job.class_name for job in job_classes])
    
@app.route("/get_software")
def get_software():
    softwares = Software.select().order_by(Software.software_name)
    softwares_and_versions = [f"{software.software_name}" for software in softwares]

    return softwares_and_versions

@app.route("/get_score", methods=['POST'])
def get_score():
    data = request.get_json()
    log_form_data(data)
    recommendations = get_recommendations(data)
    return json.dumps(recommendations, sort_keys=True)
    
# get_info function pulls from the rpInfo database to get blurbs, links, and documentation links
@app.route("/get_info", methods=['POST'])
def get_info():
    info = RpInfo.select()
    blurbs_links = {
        "rp": [f"{info.rp.name}" for info in info],
        "blurb": [f"{info.blurb}" for info in info],
        "hyperlink": [f"{info.link}" for info in info],
        "documentation": [f"{info.documentation}" for info in info]
    }
    return blurbs_links
    

@app.route("/check_conf_page/<pageId>",methods=['GET'])
def check_conf_page(pageId):
    messages, pageName = check_page(pageId=pageId)
    return render_template("check_page.html",
                           messages=messages,
                           pageName=pageName)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)