from .APIValidation import *
from .confluenceAPI import get_conf, get_tabulated_page_data

def check_page(pageId):

    """
    Checks a given confluence page for errors.
    This is meant to be used by RPs when making changes to their page to ensure that the page is valid.
    If new tables are added to the page, this function will need to be updated to check those tables as well.
    Similarly if existing tables are changed or removed, this function will need to be updated.
    """
    conf = get_conf()
    tables, pageName = get_tabulated_page_data(conf, pageId)

    messages = []

    storageTableIsValid, msg = validate_storage_table(tables[0])
    if not storageTableIsValid:
        messages.append(msg)
    
    memoryDataIsValid, msg = validate_memory_table(tables[1])
    if not memoryDataIsValid:
        messages.append(msg)

    funcTableIsValid, msg = validate_suitability(tables[2])
    if not funcTableIsValid:
        messages.append("Issue with Functionality table. "+msg)
    
    guiTableIsValid, msg = validate_suitability(tables[3])
    if not guiTableIsValid:
        messages.append("Issue with GUI table. "+ msg)
    
    fieldsTableIsValid, msg = validate_suitability(tables[4])
    if not fieldsTableIsValid:
        messages.append("Issue with Research Field table. "+msg)

    jobClassIsValid, msg = validate_suitability(tables[5])
    if not jobClassIsValid:
        messages.append("Issue with Job Class table. "+msg)
    
    return messages, pageName

    


    