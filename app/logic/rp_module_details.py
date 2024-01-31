import re
import json

def parse_whatis_line(line):
        match = re.match(r'whatis\("(.*?) : (.*?)"\)', line)
        if match:
            return match.group(1).strip(), match.group(2).strip()
        return None

def parse_path_line(line):
    match = re.match(r'prepend_path\("(\w+)","(.*?)"\)', line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None

def parse_setenv_line(line):
    match = re.match(r'setenv\("(.*?)","(.*?)"\)', line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None

def get_module_details(file):
    """
    params:
        file: path to a file
    
    returns:
        json_string: json dump of all module details

    reference the module/software section of the readme for info on the file format
    """
    with open(file) as f:
            content = f.read()

    # Initialize an empty dictionary to store the key-value pairs
    parsed_details = {}

    # Process each line of the input data
    for line in content.split('\n'):
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

    # Convert the parsed data to a JSON-formatted string
    json_string = json.dumps(parsed_details, indent=2)

    # Print the JSON string
    print(json_string)
        
        
    #return(json_string)

if __name__ == "__main__":
     get_module_details('../software_details/expanse_modules_details.txt')