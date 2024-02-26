import pandas as pd


rp_urls={
    'aces':'https://hprc.tamu.edu/software/aces/',
    'anvil': 'https://www.rcac.purdue.edu/index.php/knowledge/applications/',
    'bridges-2': 'https://www.psc.edu/resources/software/',
    'darwin': 'https://docs.hpc.udel.edu/software/',
    'delta': '',
    'expanse':'',
    'faster':'https://hprc.tamu.edu/software/faster/',
    'jetstream2':'',
    'kyric':'',
    'ookami':'',
    'rockfish':'',
    'stampede-2':'https://tacc.utexas.edu/use-tacc/software-list/',
    'ranch':'https://tacc.utexas.edu/use-tacc/software-list/',
    'osg':'',
    'osn':''
}

def create_full_url(rp_names, software_name):
    has_individual_software_page = ['anvil','bridges-2','darwin']
    rp_names_list = rp_names.split(',')

    urls=[]
    for rp_name in rp_names_list:
        rp_name_l = rp_name.strip().lower()
        base_url = rp_urls.get(rp_name_l,'')

        if rp_name_l in has_individual_software_page and base_url:
            full_url=f"{rp_name}: {base_url}{software_name.lower()}"
            if rp_name_l == 'darwin':
                full_url=f"{full_url}/{software_name.lower()}"
        elif base_url:
            full_url = f"{rp_name}: {base_url}"
        else:
            full_url=''
        
        if full_url:
            urls.append(full_url)

    combined_urls = ' , '.join(urls)
    return combined_urls

def create_static_table():
    df = pd.read_csv('./staticSearch/softwareInfo.csv',na_filter=False)
    df['RP Software Documentation'] = df.apply(lambda row: create_full_url(row['RP Name'],row['Software']), axis=1)
    empty_columns = ['Example Software Use (link)', 'Area-specific Examples', 'Containerized Version of Software',
                     'RP Documentations for Software', 'Pathing', 'RP Name.1','RP Full Software Doc']
    
    df.drop(empty_columns,axis=1,inplace=True)
    df.to_csv('./staticSearch/staticTable.csv',index=False)
    return(df)


if __name__ == "__main__":
    df = create_static_table()