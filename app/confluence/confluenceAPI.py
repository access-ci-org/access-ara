import os
from dotenv import load_dotenv
from atlassian import Confluence
from io import StringIO
import pandas as pd

class ConfluenceAPI:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("confluence_url")
        self.atlas_user = os.getenv("atlassian_username")
        self.conf_token = os.getenv("confluence_token")
        self.conf = Confluence(url=self.url, username=self.atlas_user, password=self.conf_token)
        self.space = os.getenv("confluence_space")
        self.parent_id = os.getenv("parent_page_id")
    
    def create_page(self, title, body, parent_id=None, space= os.getenv("confluence_space")):
        try:
            if parent_id is None:
                parent_id = self.parent_id
            self.conf.create_page(space=space, title=title, body=body, parent_id=parent_id, type='page',
                                  representation='storage',editor='v2',full_width=False)
        except Exception as e:
            print(e)
    
    def update_or_create_page(self, title, body, representation='storage', full_width=False):
        try:
            self.conf.update_or_create(parent_id=self.parent_id, title=title, body=body, representation=representation, full_width=full_width)
        except Exception as e:
            print(e)

    def get_page_children_ids(self, page_id=None):
        if page_id is None:
            page_id = self.parent_id
        page_children = self.conf.get_page_child_by_type(page_id=page_id, type='page')
        child_page_ids = [page['id'] for page in page_children]
        return child_page_ids

    def get_tabulated_page_data(self, page_id):
        page = self.conf.get_page_by_id(page_id, expand='body.view')
        page_content = page['body']['view']['value']
        page_title = page['title']
        page_content_io = StringIO(page_content)
        tables = pd.read_html(page_content_io)
        return tables, page_title
