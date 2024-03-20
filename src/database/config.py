from configparser import ConfigParser
import os

path_to_ini = os.path.join('src', 'database', 'database.ini')
def config(filename=path_to_ini, section='postgresql'):
    
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
            
    else:
        raise Exception(f'Section {0} is not found in the {1} file.'.format(section, filename))
    
    return db
