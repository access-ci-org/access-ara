import re
import json

def parse_whatis_line(line):
    match = re.match(r'whatis\("(.*?) : (.*?)"\)', line) #software details contain multiple lines of 'whatis' with key value pairs
    if match:
        return match.group(1).strip(), match.group(2).strip()
    else: #software detail only contains one line of 'whatis', which is the short description
        sub1 = 'whatis("'
        idx1 = line.index('whatis("')
        idx2 = line.index('")')
        sd_value = ''
        for idx in range(idx1 + len(sub1), idx2):
            sd_value = sd_value + line[idx]
        return 'Short Description', sd_value.strip()

    
def parse_path_line(line): #returns type of path (key) and the respective path (value)
    match = re.match(r'prepend_path\("(\w+)","(.*?)"\)', line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None

def parse_setenv_line(line): #returns environment variable (key) and its value
    match = re.match(r'setenv\("(.*?)","(.*?)"\)', line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None

def parse_depends_line(line): #returns "dependencies" as key and software depencency as str value
    sub1 = 'depends_on("'
    idx1 = line.index('depends_on("')
    idx2 = line.index('")')
    depends_on_value = ''
    for idx in range(idx1 + len(sub1), idx2):
        depends_on_value = depends_on_value + line[idx]
    return 'Depends On', depends_on_value.strip()

def get_module_details(file):
    """
    params:
        file: path to a file
    
    returns:
        detail: array of json strings of all module details
    """
    with open(file) as f:
            content = f.read()
    
    list_of_software = re.split('\n{2,}', content)

    # Initialize an empty dictionary to store the key-value pairs
    details = []

    for software in list_of_software:
         lines = software.split('\n')
         parsed_details = {}

         for line in lines:
            if line.startswith("whatis"): #parse lines beginning with "whatis"
                result = parse_whatis_line(line)
                if result:
                    key, value = result
                    parsed_details[key] = value
            elif line.startswith("prepend_path") or line.startswith("append_path"): #parse lines beginning with "append_path"
                result = parse_path_line(line)
                if result:
                    key, value = result
                    if key in parsed_details:
                        if isinstance(parsed_details[key], list): #if certain path key has multiple values, store them in a list. otherwise, key->str
                            parsed_details[key].append(value)
                        else:
                            parsed_details[key] = [parsed_details[key], value]
                    else:
                        parsed_details[key] = value
            elif line.startswith("setenv"): #parse lines beginning with "setenv"
                result = parse_setenv_line(line)
                if result:
                    key, value = result
                    parsed_details[key] = value
            elif line.startswith("depends_on"): #parse lines beginning with "depends_on"
                result = parse_depends_line(line)
                if result:
                    key, value = result
                    if key in parsed_details: #if multiple dependencies, store them in a list
                        if isinstance(parsed_details[key], list):
                            parsed_details[key].append(value)
                        else:
                            parsed_details[key] = [parsed_details[key], value]
                    else:
                        parsed_details[key] = value
         if(parsed_details != {}): #don't include empty information
            details.append(parsed_details)
         
    # Convert the parsed data to a JSON-formatted string
    json_string = json.dumps(parsed_details)

    # Print the JSON string
    for element in details:
         print(json.dumps(element))
         print()

if __name__ == "__main__":
     get_module_details('../software_details/anvil_modules_details.txt')