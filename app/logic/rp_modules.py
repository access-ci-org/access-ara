import re
def get_modules_and_versions(file,allModulesAndVersions={}):
    """
    params:
        file: path to a file
        allModulesAndVersions: a dictionary of with module names as keys and versions as values
    
    returns:
        currentModules: a list of module names in the given file
        allModulesAndVersions: the param dict updated with the data from the file

    reference the module/software section of the readme for info on the file format
    """
    with open(file) as f:
            content = f.read()
    mods = re.split('\s{2,}|\n',content)    #separate things with more than 2 spaces or a newline
    if 'Where:' in mods:
        desc = mods.index('Where:')
        mods = mods[:desc]
    stringsToRemove = ['(','---','/opt']
    # remove all items that contain string that should be removed
    mods = [mod for mod in mods if not any(string in mod for string in stringsToRemove)]
    currentModules = []
    for mod in mods:
        if mod:
            if "/" in mod:
                moduleName, moduleVersion = mod.split("/", 1)
                moduleName = moduleName.strip()
                if moduleName not in currentModules:
                    currentModules.append(moduleName)
                if (moduleName in allModulesAndVersions) and (moduleVersion not in allModulesAndVersions[moduleName]):
                    allModulesAndVersions[moduleName] += f", {moduleVersion}"
                else:
                    allModulesAndVersions[moduleName] = moduleVersion
            else:
                # If the module has no versions
                if mod not in currentModules:
                    currentModules.append(mod)
                if (mod not in allModulesAndVersions):
                    allModulesAndVersions[mod] = ''
    return(allModulesAndVersions, currentModules)
