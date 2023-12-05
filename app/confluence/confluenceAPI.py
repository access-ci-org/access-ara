import os
from dotenv import load_dotenv
from atlassian import Confluence
import pandas as pd

def get_conf():

    load_dotenv() # Load the .env file

    url = os.getenv("confluence_url")
    altas_user = os.getenv("atlassian_username")
    conf_token = os.getenv("confluence_token")

    # The URL endpoint
    conf = Confluence(url=url, username=altas_user, password=conf_token)
    return conf

def create_conf_page(conf,title,body,parent_id=None,space=os.getenv("confluence_space")):
   try:
        conf.create_page(space=space,title=title,
                            body=body,parent_id=parent_id,
                            type='page',representation='storage',
                            editor='v2', full_width=False )
   except Exception as e:
        print(e)

def get_page_children_ids(conf,pageID):
    """
    conf: confluence object
    pageID: id of the page to retrieve
    returns: list of ids of the children of the page
    """
    page = conf.get_page_by_id(page_id=pageID)
    pageChildren = conf.get_page_child_by_type(page_id=pageID, type='page')
    childPageIds=[]
    for page in pageChildren:
        childPageIds.append(page['id'])
    return(childPageIds)

def get_tabulated_page_data(conf, pageID):
   """
    conf: confluence object
    pageID: id of the page to retrieve

    returns: list of tables (pandas data tables) in the page
             and the title of the page being accessed
   """
   page = conf.get_page_by_id(pageID, expand='body.view')
   pageContent = page['body']['view']['value'] 
   pageTitle = page['title']
   table = pd.read_html(pageContent)
   
   return table, pageTitle
   

