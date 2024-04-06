import os
from models import db
from models.rps import RPS
from models.gui import GUI
from models.rpGUI import RpGUI
from models.rpMemory import RpMemory
from models.researchField import ResearchFields
from models.rpResearchField import RpResearchField
from models.software import Software
from models.rpSoftware import RpSoftware
from confluence.confluenceAPI import ConfluenceAPI
from confluence.APIValidation import validate_storage_table, validate_suitability, validate_memory_table

def get_rp_storage_data(storageTable):
    """
    sourceTable: pandas data table containing the storage information for the rp
    returns: dictionary of storage information

    This function assumes that the storageTable is valid (validate using validate_storage_table before calling this)
    This function is used to get the storage information from the storage table and 
    return it in a dictionary format that can be used to update the database
    The index of the storageTable is directly related to the columns as seen on the confluence page
    """
    scratch_tb = storageTable.iloc[0,0]
    longterm_tb = storageTable.iloc[0,1]
    storageData = {'scratch_tb': scratch_tb,
                'longterm_tb': longterm_tb,}
    return storageData

def get_rp_memory_data(memoryTable, rp):
    """
    memoryTable: pandas data table containing the memory information for the rp
    rp: rps object

    returns: list of dictionaries containing the memory information

    This function assumes that the memoryTable is valid (validate using validate_memory_table before calling this)
    This function is used to get the memory information from the memory table and
    return it in a dictionary format that can be used to update the database
    The index of the storageTable is directly related to the columns as seen on the confluence page
    """
    node_type = memoryTable.columns[0]
    per_node_memory_gb = memoryTable.columns[1]
    memoryData = []
    for i in range(0, len(memoryTable.index)):
        row = memoryTable.iloc[[i]]
        memoryData.append({'rp':rp,
                        'node_type': row[node_type].to_string(index=False),
                        'per_node_memory_gb':row[per_node_memory_gb].to_string(index=False)})
    return(memoryData)

def get_rp_functionality_data(funcTable):
    """
    funcTable: pandas data table containing the functionality information for the rp
    returns: dictionary of functionality information

    This function assumes that the funcTable is valid (validate using validate_suitability before calling this)
    This function is used to get the functionality information from the functionality table and
    return it in a dictionary format that can be used to update the database
    The index of the funcTable is directly related to the columns as seen on the confluence page
    """
    graphical = funcTable.iloc[0,1]
    gpu = funcTable.iloc[1,1]
    virtual_machine = funcTable.iloc[2,1]
    funcData = {'graphical':graphical,
                'gpu':gpu,
                'virtual_machine':virtual_machine}
    return funcData

def update_rp_table_form_conf(tables,pageName):
    """
    tables: list of pandas data tables in the page
    pageName: name of the page the data came from
    
    This function is used to update the database from the confluence pages

    Each index in the tables list corresponds to the order in which the data is being displayed on the confluence page

    """

    messages = []
    rpName = pageName[:pageName.rfind(" ")] # get the rp name from the page name (page names are '<RP Name> Data')
    if RPS.select().count() == 0:   # check if the rp exists in the database
        rp = None
    else:
        rp = RPS.get_or_none(RPS.name == rpName)    # get the rp object from the database
        print(f"\nGetting data for {rpName}")

    # get the data for the rps tables
    # validate the data and get the data in the correct format
    storageTable = tables[0]
    storageTableIsValid, msg = validate_storage_table(storageTable)
    if storageTableIsValid:
        storageData = get_rp_storage_data(storageTable)
    else:
        messages.append(msg+(". Storage data was not updated."))
        print(msg+(". Storage data was not updated."))

    functionalityTable = tables[2]
    funcTableIsValid, msg = validate_suitability(functionalityTable)
    if funcTableIsValid:
        funcData = get_rp_functionality_data(functionalityTable)
    else:
        messages.append(msg+(". Functionality data was not updated."))
        print(msg+(". Functionality data was not updated."))

    if not rp:  # if the rp table does not exist, create it and add the data
        print(f"RP '{rpName}' not found")
        if not (funcTableIsValid and storageTableIsValid):
            print(f'Unable to create new RP {rpName}.')
            messages.append(f'Unable to create new RP {rpName}.')
            return
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                rpTableData['name'] = rpName
                rpTableData.update(storageData)
                rpTableData.update(funcData)
                rp = RPS.create(**rpTableData)
                print(f"Rp {rpName} created")
            except Exception as e:
                msg = f"Error while trying to create RP {rpName}"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    else:   # if the rp table exists, update it with the new data
        with db.atomic() as transaction:
            try:
                rpTableData = {}
                if storageTableIsValid:
                    rpTableData.update(storageData)
                if funcTableIsValid:
                    rpTableData.update(funcData)
                RPS.update(**rpTableData).where(RPS.name==rpName).execute()
                print(f'RP {rpName} updated')
            except Exception as e:
                msg = f"Error while trying to update RP {rpName}"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    
    # get the data for rpMemory table, validate it, delete the current table, and create a new one with the new data
    memoryTable = tables[1]
    memoryDataIsValid, msg = validate_memory_table(memoryTable)

    if memoryDataIsValid:
        memoryData = get_rp_memory_data(memoryTable,rp)
        if memoryData:
            with db.atomic() as transaction:
                try:
                    delRpMem = RpMemory.delete().where(RpMemory.rp == rp)
                    delRpMem.execute()
                    createRpMem = RpMemory.insert_many(memoryData).on_conflict_replace()
                    createRpMem.execute()
                    print(f"Memory info successfully updated for {rpName}")
                except Exception as e:
                    msg = f"Error while trying to update {rpName} memory"
                    print(f"{msg} : \n", e)
                    messages.append(msg)
                    transaction.rollback()
    else:
        messages.append(msg+("Memory data was not updated."))
        print(msg+("Memory data was not updated."))
    
    # get the data for the guiTable tables, validate it, delete the current table, and create a new one with the new data
    guiTable = tables[3]
    guiTableIsValid = validate_suitability(guiTable)
    if guiTableIsValid:
        guiTable.fillna(1, inplace=True) #replace na with 1
        guiTuple = guiTable.itertuples(index=False)
        with db.atomic() as transaction:
            try:
                RpGUI.delete().where(RpGUI.rp == rp).execute()
                for item in guiTuple:
                    gui, guiCreated = GUI.get_or_create(gui_name = item[0])
                    rpGuiData =  {'rp':rp,'gui':gui,'suitability':item[1]}
                    rpGui = RpGUI.create(**rpGuiData)
            except Exception as e:
                msg = f"Error while trying to update {rpName} GUI"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()

    # get the data for the researchFields tables, validate it, delete the current table, and create a new one with the new data
    fieldsTable = tables[4]
    fieldsTableIsValid,msg = validate_suitability(fieldsTable)
    if fieldsTableIsValid:
        fieldsTuple = fieldsTable.itertuples(index=False)
        with db.atomic() as transaction:
            try:
                RpResearchField.delete().where(RpResearchField.rp == rp).execute()
                for item in fieldsTuple:
                    field, fieldCreated = ResearchFields.get_or_create(field_name=item[0])
                    researchFieldData = {'rp':rp,'research_field':field,'suitability':item[1]}
                    RpResearchField.create(**researchFieldData)
            except Exception as e:
                msg = f"Error while trying to update {rpName} research fields"
                print(f"{msg} : \n", e)
                messages.append(msg)
                transaction.rollback()
    else:
        messages.append(msg+(". Fields data was not updated."))
        print(msg+(". Fields data was not updated."))

    print("Errors: ", messages)

def update_rps_from_conf():
    """
    This function is used to update all rp information in the database from the confluence pages
    """
    conf_api = ConfluenceAPI()

    parent_id = os.getenv("parent_page_id")
    pageIds = conf_api.get_page_children_ids(parent_id)
    for id in pageIds:
        # get the page name and the tables in the page
        tables, pageName = conf_api.get_tabulated_page_data(page_id=id)
        if ('Data' in pageName):    # if the page name contains 'Data', then it is a data page
            update_rp_table_form_conf(tables,pageName)

def update_software_from_conf():
    """
    This function is used to update all rp software information in the database from the confluence pages
    """
    conf_api = ConfluenceAPI()
    pageIds = conf_api.get_page_children_ids()
    for id in pageIds:
        table, pageName = conf_api.get_tabulated_page_data(page_id=id)
        rp_name = pageName.split()[0]
        if "Software" in pageName and "All RP Software" != pageName:
            # read the data from table (its a pandas df)
            software_list = table[0].iloc[:,0].dropna().tolist()

            # get the rp object based on rp_name
            rp  = RPS.get_or_none(RPS.name == rp_name)
            if rp:
                with db.atomic():
                    try:
                        # create or get Software objects
                        software_objs = [Software.get_or_create(software_name=name)[0] for name in software_list]

                        # create RpSoftware entries
                        rp_software_data = [{'rp':rp, 'software':software} for software in software_objs]
                        RpSoftware.insert_many(rp_software_data).on_conflict_replace().execute()
                    except Exception as e:
                        print(f"Error while updating software for RP {rp_name}: {str(e)}")
                        db.rollback()
            else:
                print(f"RP {rp_name} not found")

if __name__ == '__main__':
    update_rps_from_conf()
    update_software_from_conf()
    
