import sys
import os
from confluence.confluenceAPI import get_conf, get_page_children_ids
from logic.softwares import get_softwares
from createConfPages import get_rp_software_tables


###
# Mainly for updating software data
# Get software data from conf, combine the software data from conf and local data
# create new table from combined data
# push table to rp data page
##


def get_software_from_conf(pageId, pageName):
    pass


def combine_software_data(conf_sftw, local_sftw):
    pass

def update_rp_software_page(rp_name, page_data):

    conf = get_conf()

    parent_page = os.getenv("parent_page_id")

    child_pages = get_page_children_ids(conf, parent_page)

    for 

    conf_sftw = get_software_from_conf()

    pass


if __name__ == '__main__':
    try:

        # can be three different items: rps, softwares, all

        whichData = sys.argv[1]

        if whichData == '':
            pass

    except Exception as e:
        print(e)