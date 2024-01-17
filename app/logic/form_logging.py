import logging

#Initialize query logger
input_logger = logging.getLogger(__name__)

#Override default logging level
input_logger.setLevel('INFO')

#Handler/Formatter for query logs. Send to query.logs
input_handler = logging.FileHandler("formInfo.log", mode='a')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
input_handler.setFormatter(formatter)
input_logger.addHandler(input_handler)

def log_form_data(formData):
    #Q: (HPC Use)
    hpcUse = formData.get('hpc-use')
    response = swap_val_to_text(hpcUse)
    input_logger.info("User Input - HPC Use - %s", response)

    #Q: (ACCESS RPs familiarity)
    accessFamiliar = formData.get("access-familiarity")
    response = swap_val_to_text(accessFamiliar)
    input_logger.info("User Input - Familiar with ACCESS RPs - %s", response)

    #Q: (RPs User is Familiar With)
    usedRPs = formData.get("used-hpc")
    input_logger.info("User Input - RPs Used:\n%s", usedRPs)

    #Q: (User Experience)
    userExp = formData.get("hpc-experience")
    input_logger.info("User Input - Amount of Experience - %s", userExp)

    #Q: (Need GUI)
    needGui = formData.get('gui-needed')
    response = swap_val_to_text(needGui)
    input_logger.info("User Input - Need Gui - %s", response)

    #Q: (GUI Familiarity)
    usedGui = formData.get('used-gui')
    input_logger.info("User Input - Familiar GUIs:\n%s", usedGui)

    #Q: (Field of Research)
    fields = formData.get("research-field")
    fieldList = fields.split(",")
    input_logger.info("User Input - Field(s) of Research:\n%s", fieldList)

    #Q: (Fields Tags Added)
    addFields = formData.get("add-field-tags")
    addFieldsList = addFields.split(",")
    input_logger.info("User Input - Research Field Tags Added:\n%s", addFieldsList)

    #Q: (Storage)
    storage = formData.get("storage")
    response = swap_val_to_text(storage)
    input_logger.info("User Input - Storage Needed - %s", response)

    #Q: (File Count)
    numFiles = formData.get("num-files")
    input_logger.info("User Input - # of Files Needed - %s", numFiles)

    #Q: (Long Term Storage)
    longTermStorageNeeded = formData.get("long-term-storage")
    input_logger.info("User Input - Long Term Storage - %s", longTermStorageNeeded)

    #Q: (Temp Storage)
    scratchStorageNeeded = formData.get("temp-storage")
    input_logger.info("User Input - Scratch Storage - %s", scratchStorageNeeded)

    #Q: (Memory)
    memoryNeeded = formData.get("memory")
    input_logger.info("User Input - Memory Needed - %s", memoryNeeded)

    #Q: (Software)
    softwares = formData.get("software")
    softwareList = softwares.split(",")
    input_logger.info("User Input - Softwares:\n%s", softwareList)

    #Q: (Add Software)
    addSoftware = formData.get("add-software-tags")
    addSoftwareList = addSoftware.split(",")
    input_logger.info("User Input - Software Tags Added:\n%s", addSoftwareList)

    #Q: (Graphical Component)
    graphicsNeeded = formData.get("graphics")
    response = swap_val_to_text(graphicsNeeded)
    input_logger.info("User Input - Graphical Component - %s", response)

    #Q: (CPU/GPU Parallel)
    cpuGpuParallelNeeded = formData.get("cpu-gpu-parallel")
    response = swap_val_to_text(cpuGpuParallelNeeded)
    input_logger.info("User Input - CPU/GPU Parallel - %s", response)

    #Q: (Always On)
    alwaysRunningNeeded = formData.get("job-run")
    response = swap_val_to_text(alwaysRunningNeeded)
    input_logger.info("User Input - Always Running - %s", response)

    #Q: (Virtual Machine)
    vmNeeded = formData.get("vm")
    response = swap_val_to_text(vmNeeded)
    input_logger.info("User Input - VM Needed - %s", response)

def swap_val_to_text(radioVal):
    if radioVal == None:
        return 'No input from user'
    if (radioVal == '0'):
        return 'No'
    elif (radioVal == '1'):
        return 'Yes'
    else:
        return 'unsure'