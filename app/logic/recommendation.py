from ..models.rpGUI import RpGUI
from ..models.gui import GUI
from ..models.researchField import ResearchFields
from ..models.rpResearchField import RpResearchField
from ..models.rps import RPS
from ..models.software import Software
from ..models.rpSoftware import RpSoftware
from ..models.rpMemory import RpMemory
import operator
from functools import reduce
import logging

#Initialize query logger
query_logger = logging.getLogger(__name__)

#Override default logging level
query_logger.setLevel('INFO')

#Handler/Formatter for query logs. Send to query.logs
query_handler = logging.FileHandler("queryInfo.log", mode='a')
rec_handler = logging.FileHandler("formInfo.log", mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
query_handler.setFormatter(formatter)
query_logger.addHandler(query_handler)

def calculate_points(currentPoints, suitability=1):
    """
    Calculates how many points should be given based on suitability
    This functions is called by the other 'calculate_score_' functions
    """
    if suitability>0:
        points = currentPoints + (suitability*1)
    else:
        points = currentPoints + 0.5

    return points

def calculate_score_rf(researchFieldList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the researchFieldList
    researchFieldList: list of research fields the user selected
    scoreBoard: dict with RPs as keys and their scores as values
                if RP has not been assigned a value yet then it will not be in the dict
    return: returns the updated scoreboard
    """
    # Set the parameters used to filter the table
    filter = []
    for researchField in researchFieldList:
        filter.append((ResearchFields.field_name == f"{researchField}"))
    
    # Combine the RpResearchField and ResearchFields tables, and 
    # Only select the ones that match the filter
    rpWithFieldTable = (RpResearchField.select()
                                       .join(ResearchFields, on=(RpResearchField.research_field==ResearchFields.id))
                                       .where(reduce(operator.or_,filter))).select()
    query_logger.info("SQLite Query - Research Fields:\n%s", rpWithFieldTable)
    for row in rpWithFieldTable:
        rp = row.rp.name
        suitability = row.suitability
        if rp in scoreBoard:
            scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
            scoreBoard[rp]['reasons'].append(row.research_field.field_name)
        else:
            scoreBoard[rp] = {'score': max(1,suitability), 'reasons': [row.research_field.field_name]}
    return scoreBoard

def calculate_score_software(softwareList,scoreBoard):
    """
    Calculates and gives points to rps based on the items in the softwareList
    softwareList: list of softwares the user selected
    scoreBoard: dict with RPs as keys and their scores as values
                if RP has not been assigned a value yet then it will not be in the dict
    return: returns the updated scoreboard
    """
    # Set the parameters used to filter the table
    filter = []
    for software in softwareList:
        filter.append((Software.software_name == f"{software}"))
    
    # Combine the RpSoftware and Software tables, and 
    # Only select the ones that match the filter
    rpWithSoftware = (RpSoftware.select()
                                .join(Software, on=(RpSoftware.software==Software.id))
                                .where(reduce(operator.or_,filter))).select()
    query_logger.info("SQLite Query - Softwares:\n%s", rpWithSoftware)
    for row in rpWithSoftware:
        rp = row.rp.name
        suitability = 10         # Prioritize softwares more than hardwares or GUIs
        if rp in scoreBoard:
            scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
            scoreBoard[rp]['reasons'].append(row.software.software_name)
        else:
            scoreBoard[rp] = {'score': max(1,suitability), 'reasons': [row.software.software_name]}

    return(scoreBoard)

def classify_rp_storage(storageType):
    """
    Classifies RPs into three categories: less-than-1, 1-10, more-than-10,
        based on their storage (in TB)
    (These categories directly correspond to the values gotten from the form)
    storageType: must be "long-term" or "scratch" for what type of storage needs to be classified
    returns a dict with each category as the key as a list of RP names that fit
        that categories as the values
    """
    
    classifiedRps = {}
    
    if storageType == "long-term":
        ltOneTb = RPS.select().where(RPS.longterm_tb < 1.0)
        oneToTenTb = RPS.select().where((RPS.longterm_tb >= 1.0) & (RPS.longterm_tb< 10.0))
        mtTenTb = RPS.select().where(RPS.longterm_tb >= 10.0)

    elif storageType == "scratch":
        ltOneTb = RPS.select().where(RPS.scratch_tb < 1.0)
        oneToTenTb = RPS.select().where((RPS.scratch_tb >= 1.0) & (RPS.scratch_tb< 10.0))
        mtTenTb = RPS.select().where(RPS.scratch_tb >= 10.0)

    classifiedRps["less-than-1"] = [rp.name for rp in ltOneTb]
    classifiedRps["1-10"] = [rp.name for rp in oneToTenTb]
    classifiedRps["more-than-10"] = [rp.name for rp in mtTenTb]

    return classifiedRps

def get_recommendations(formData):
    scoreBoard = {}
    yes = '1'

    # If user has used ACCESS hpc
    if formData.get("used-hpc"):
        # increase score for all ACCESS RPs user has experience with
        for rp in formData.get("used-hpc"):
            if rp in scoreBoard:
                scoreBoard[rp]['score'] += 1
                scoreBoard[rp]['reasons'].append("User Experience")
            else:
                scoreBoard[rp] = {'score': 1, 'reasons': ["User Experience"]}

    #If user needs a system with a GUI
    if (formData.get("gui-needed") == '1'):
        rpsWithGui = RpGUI.select()

        #If user selects specific GUI give points to only RPs with that GUI
        if formData.get('used-gui'):
            for rp in rpsWithGui:
                if rp.gui.gui_name in formData.get('used-gui'):
                    suitability = rp.suitability
                    if rp.rp.name in scoreBoard:
                        scoreBoard[rp.rp.name]['score'] += calculate_points(scoreBoard[rp.rp.name]['score'],suitability)
                        scoreBoard[rp.rp.name]['reasons'].append(rp.gui.gui_name)
                    else:
                        scoreBoard[rp.rp.name] = {'score': max(1,suitability), 'reasons': [rp.gui.gui_name]}
                        
        #If user does not select any specific GUIs give points to every RP with a GUI
        else:
            rpsWithGui = RpGUI.select()
            rpNames = list({rp.rp.name for rp in rpsWithGui})
            # increase score for all rps with a GUI
            for rp in rpNames:
                suitability = 1
                if rp in scoreBoard:
                    scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'],suitability)
                    scoreBoard[rp]['reasons'].append("GUI")
                else:
                    scoreBoard[rp] = {'score': max(1,suitability), 'reasons': ["GUI"]}
            
    
    # Research Field
    researchFields = formData.get("research-field")
    researchFieldList = researchFields.split(",")

    if researchFieldList:
        scoreBoard = calculate_score_rf(researchFieldList,scoreBoard)

    # Storage
    storageNeeded = formData.get("storage")
    if storageNeeded:
        
        longTermStorageNeeded = formData.get("long-term-storage")
        scratchStorageNeeded = formData.get("temp-storage")

        if (longTermStorageNeeded != "unsure" and longTermStorageNeeded) :
            storageType = "long-term"
            classifiedRpsLt = classify_rp_storage(storageType)
            for rp in classifiedRpsLt[longTermStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                    scoreBoard[rp]['reasons'].append("Long Term Storage")
                else:
                    scoreBoard[rp] = {'score': 1, 'reasons': ["Long Term Storage"]}

        if (scratchStorageNeeded and scratchStorageNeeded != "unsure"):
            storageType = "scratch"
            classifiedRpsScratch = classify_rp_storage(storageType)
            for rp in classifiedRpsScratch[scratchStorageNeeded]:
                if rp in scoreBoard:
                    scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                    scoreBoard[rp]['reasons'].append("Temporary Storage")
                else:
                    scoreBoard[rp] = {'score': 1, 'reasons': ["Scratch Storage"]}
    # Memory (RAM)
    memoryNeeded = formData.get("memory")
    # TODO: add scoring system after the memory data has been added to the db
    if memoryNeeded:
        if memoryNeeded == 'less-than-64':
            rpMems = RpMemory.select().where(RpMemory.per_node_memory_gb < 64)
            for rpMem in rpMems:
                rpName = rpMem.rp.name
                if rpName in scoreBoard:
                    if 'Memory' in scoreBoard[rpName]['reasons']:
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                    else:
                        scoreBoard[rpName]['score'] = calculate_points(scoreBoard[rpName]['score'])
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                else:
                    scoreBoard[rpName] = {'score': 1, 'reasons': [f"{rpMem.per_node_memory_gb} GB Memory"]}

        elif memoryNeeded == '64-512':
            rpMems = RpMemory.select().where((RpMemory.per_node_memory_gb > 64) & (RpMemory.per_node_memory_gb <512))
            for rpMem in rpMems:
                rpName = rpMem.rp.name
                if rpName in scoreBoard:
                    if 'Memory' in scoreBoard[rpName]['reasons']:
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                    else:
                        scoreBoard[rpName]['score'] = calculate_points(scoreBoard[rpName]['score'])
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                else:
                    scoreBoard[rpName] = {'score': 1, 'reasons': [f"{rpMem.per_node_memory_gb} GB Memory"]}
        elif memoryNeeded == 'more-than-512':
            rpMems = RpMemory.select().where(RpMemory.per_node_memory_gb > 512)
            for rpMem in rpMems:
                rpName = rpMem.rp.name
                if rpName in scoreBoard:
                    if 'Memory' in scoreBoard[rpName]['reasons']:
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                    else:
                        scoreBoard[rpName]['score'] = calculate_points(scoreBoard[rpName]['score'])
                        scoreBoard[rpName]['reasons'].append(f"{rpMem.per_node_memory_gb} GB Memory")
                else:
                    scoreBoard[rpName] = {'score': 1, 'reasons': [f"{rpMem.per_node_memory_gb} GB Memory"]}


    # Software
    softwares = formData.get("software")
    if softwares:
        softwareList = softwares.split(",")
        if softwareList:
            scoreBoard = calculate_score_software(softwareList, scoreBoard)

    # Graphics
    graphicsNeeded = formData.get("graphics")
    # TODO: add scoring after the graphics data has been added to the db
    if graphicsNeeded == yes:
        graphicalRps = RPS.select().where(RPS.graphical > 0)
        for rp in graphicalRps:
            suitability = rp.graphical
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score['] = calculate_points(scoreBoard[rp.name]['score'], suitability)
                scoreBoard[rp.name]['reasons'].append("Graphics")
            else:
                scoreBoard[rp.name] = {'score': max(suitability,1), 'reasons': ["Graphics"]}

    # GPU
    GPUNeeded = formData.get("gpu")
    if (GPUNeeded and GPUNeeded == yes):
        gpuRPs = RPS.select().where(RPS.gpu > 0)
        gpuRPNames = [rp.name for rp in gpuRPs]
        for rp in gpuRPNames:
            if rp in scoreBoard:
                scoreBoard[rp]['score'] = calculate_points(scoreBoard[rp]['score'])
                scoreBoard[rp]['reasons'].append("GPU")
            else:
                scoreBoard[rp] = {'score': 1, 'reasons': ["GPU"]} 

    # Job needs to be running always
    alwaysRunningNeeded = formData.get("job-run")
    if alwaysRunningNeeded == yes:
        arRps = RPS.select().where(RPS.always_running > 0)
        for rp in arRps:
            suitability = 10        # Prioritize always running to bring Jetstream2 up
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score'] = calculate_points(scoreBoard[rp.name]['score'],suitability)
                scoreBoard[rp.name]['reasons'].append("Always Running")
            else:
                scoreBoard[rp.name] = {'score': max(suitability,1), 'reasons': ["Always Running"]}

    # Virtual machine
    VmNeeded = formData.get("vm")
    if VmNeeded == yes:
        vmRps = RPS.select().where(RPS.virtual_machine > 0)
        for rp in vmRps:
            suitability = 10        # Prioritize VM to bring Jetstream2 up
            if rp.name in scoreBoard:
                scoreBoard[rp.name]['score'] = calculate_points(scoreBoard[rp.name]['score'],suitability)
                scoreBoard[rp.name]['reasons'].append("Virtual Machine")
            else:
                scoreBoard[rp.name] = {'score': max(suitability,1), 'reasons': ["Virtual Machine"]}
    query_logger.addHandler(rec_handler)
    query_logger.info('Recommendation Scoreboard:\n%s', scoreBoard)
    query_logger.removeHandler(rec_handler)

    return scoreBoard

