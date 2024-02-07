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
            sd = ''
            for idx in range(idx1 + len(sub1), idx2):
                sd = sd + line[idx]
            return 'Short Description', sd.strip()

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
            if line.startswith("whatis"):
                result = parse_whatis_line(line)
                if result:
                    key, value = result
                    parsed_details[key] = value
            elif line.startswith("prepend_path"):
                result = parse_path_line(line)
                if result:
                    key, value = result
                    parsed_details[key] = value
            elif line.startswith("setenv"):
                result = parse_setenv_line(line)
                if result:
                    key, value = result
                    parsed_details[key] = value
         details.append(parsed_details)
         
    # Convert the parsed data to a JSON-formatted string
    json_string = json.dumps(parsed_details, indent=2)

    # Print the JSON string
    for element in details:
         print(json.dumps(element))
         print()

if __name__ == "__main__":
     get_module_details('../software_details/expanse_modules_details.txt')