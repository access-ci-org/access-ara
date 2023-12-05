from models.rps import RPS
from models.rpMemory import RpMemory
from logic.research import get_research_fields
from logic.jobClass import get_job_classes
from logic.softwares import get_softwares 
from logic.gui import get_guis
from confluence.confluenceAPI import get_conf, create_conf_page
import pandas as pd

#####################
# This page is for creating the pages for the RP data and RP software tables
# The data is pulled from the database and then converted to html tables
# The tables are then added to the body of the page
# The pages are then created in Confluence
# The pages are created under the 'Data for RP Recommendations' page
# This code is not used in the app, but is used to create the pages in Confluence
# The pages already exist in Confluence, so this code is not needed for production use
#####################

def get_rp_data_tables(rpNamesList):
    """
    rpNamesList: list of rp names
    returns: dictionary of rp data tables

    each section of the code follows the same pattern:
    1. get the data from the database
    2. convert the data to a dataframe
    3. add the dataframe to the dictionary (tablesDict)

    This code is being used for the <RP Name> Data pages
    The specific order in which the data is added to the dictionary is important
    it reflects the order in which the data will be displayed on the page
    """
    tablesDict = {}
    for rpName in rpNamesList:
        tablesDict[rpName] = []
        rp = RPS.select().where(RPS.name == rpName)[0] # get the rp object from the database
        
        # storage information
        rpHardware = {'Temp Storage (TB)': [rp.scratch_tb],
                      'Long-Term Storage (TB)':[rp.longterm_tb]}
        df = pd.DataFrame(data=rpHardware)
        tablesDict[rpName].append(df)

        # memory (RAM) information
        nodeTypes = []
        memAmount = []
        for row in RpMemory.select().where(RpMemory.rp==rp):
            nodeTypes.append(row.node_type)
            memAmount.append(row.per_node_memory_gb)
        rpMemory = {'Memory (RAM) Node': nodeTypes,
                    'Amount (GB)': memAmount}
        df = pd.DataFrame(data=rpMemory)

        tablesDict[rpName].append(df)  

        # functionality information
        rpSupports = {
                        'Functionality':['Supports jobs that have a graphical component',
                                                'CPU and GPU run in Parallel',
                                                'Job is always active',
                                                'Has a virtual machine or supports virtualization'],
                        'Suitability':[rp.graphical,
                                       rp.parallel,
                                       rp.always_running,
                                       rp.virtual_machine]
                    }
        df = pd.DataFrame(data=rpSupports)
        tablesDict[rpName].append(df)
        
        # GUI information
        guis = get_guis(rpName)
        rpGui = {'GUI':[gui.gui.gui_name for gui in guis],
                 'Suitability': ''}
        df = pd.DataFrame(data=rpGui)
        tablesDict[rpName].append(df)

        # research fields information
        researchFields = get_research_fields(rpName)
        rpResearch = {'Field':[field.research_field.field_name for field in researchFields],
                      'Suitability':[field.suitability for field in researchFields]
                      }
        df = pd.DataFrame(data=rpResearch)
        tablesDict[rpName].append(df)

        # job class information
        jobClasses = get_job_classes(rpName)
        rpJob = {'Job Class': [jobClass.job_class.class_name for jobClass in jobClasses],
                 'Suitability':[jobClass.suitability for jobClass in jobClasses]}
        df = pd.DataFrame(data=rpJob)
        tablesDict[rpName].append(df)

    return(tablesDict)

def get_rp_software_tables(rpNamesList):
    """
    rpNamesList: list of rp names
    returns: dictionary of rp software tables

    For each rp, get the software packages that are installed on that rp

    The code is being used for the <RP Name> Software pages
    """

    tablesDict = {}
    for rpName in rpNamesList:
        tablesDict[rpName] = []
        softwares = get_softwares(rpName)
        rpSoftware={'Software Packages': [software.software.software_name for software in softwares]}
        df = pd.DataFrame(data=rpSoftware)
        tablesDict[rpName].append(df)
    return tablesDict


def create_rp_data_conf_pages(conf, rpNamesList):
    dataTablesDict = get_rp_data_tables(rpNamesList)
    parent_id = 245202949   # id of the parent page ('Data for RP Recommendations' page)
    for rpName in rpNamesList:

        title = f'{rpName} Data' # title of the page to be created
        body = ''

        # convert each dataframe table to html table and add to body of the page
        for table in dataTablesDict[rpName]:
            body += table.to_html(index=False,classes='confluenceTable')

        create_conf_page(conf,title=title,body=body,parent_id=parent_id)

def create_rp_softwares_conf_pages(conf, rpNamesList):
    softwareTablesDict = get_rp_software_tables(rpNamesList)
    parent_id = 245202949 # id of the parent page ('Data for RP Recommendations' page)
    for rpName in rpNamesList:
        title = f'{rpName} Software' # title of the page to be created
        body = ''

        # convert each dataframe table to html table and add to body of the page
        for table in softwareTablesDict[rpName]:
            body += table.to_html(index=False,classes='confluenceTable')
        create_conf_page(conf,title=title,body=body,parent_id=parent_id)

def create_all_rp_conf_pages():
    conf = get_conf()

    # get all the RP names
    rps = RPS.select().order_by(RPS.name)
    rpNamesList = [rp.name for rp in rps]

    create_rp_data_conf_pages(conf,rpNamesList)
    create_rp_softwares_conf_pages(conf,rpNamesList)

