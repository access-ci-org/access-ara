from confluence.confluenceAPI import ConfluenceAPI
from logic.softwares import get_softwares
import pandas as pd

###
# Used for updating software data from conf
# Get software data from conf, combine the software data from conf and local data
# create new table from combined data
# push table to rp software page
##


def get_local_software(rp_name):
    software = get_softwares(rp_name)
    
    # print([s for s in software])

    sftw = [s.software.software_name for s in software]
    return sftw


def combine_software_data(conf_sftw, local_sftw):

    if conf_sftw is None:
        return local_sftw
    
    conf_sftw_set = set(conf_sftw)
    local_sftw_set = set(local_sftw)

    combined_sftw_set = conf_sftw_set.union(local_sftw_set)

    combined_sftw = list(combined_sftw_set)
    print(combined_sftw)
    combined_sftw.sort()

    return combined_sftw

def update_rp_software_page(conf_api, rp_name, page_data):

    title = f"{rp_name} Software"
    body = page_data.to_html(index=False, classes='confluenceTable')

    conf_api.update_or_create_page(title=title, body=body)

if __name__ == '__main__':
    try:
        conf_api = ConfluenceAPI()

        child_page_ids = conf_api.get_page_children_ids()

        for id in child_page_ids:
            page_data, page_name = conf_api.get_tabulated_page_data(child_page_ids[2])
            if "Software" in page_name and "All RP Software" != page_name:
                rp_name = page_name.split()[0]
                local_sftw = get_local_software(rp_name=rp_name)
                conf_sftw = page_data[0].iloc[:, 0].dropna().tolist()
                combined_sftw = combine_software_data(conf_sftw=conf_sftw, local_sftw=local_sftw)
                sftw_table = pd.DataFrame({'Software Packages': combined_sftw}).to_html(index=False,classes='confluenceTable')
                conf_api.update_or_create_page(title=page_name,body=sftw_table)

    except Exception as e:
        print(e)