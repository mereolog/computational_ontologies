import re
import sys, os

root = "Resources/TUpper/"
iri_regex = re.compile(r'(http://colore.oor.net/)(.+)')

for path, subdirs, file_names in os.walk(root):
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        file = open(file_path, 'r')
        if file_name.endswith('clif'):
            file_content = file.read()
            file.close()
            file = open(file_path, 'w')
            new_file_content = file_content.replace('http://colore.oor.net/','https://raw.githubusercontent.com/mereolog/computational_ontologies/main/TUpper/')
            file.write(new_file_content)
            file.close()
        