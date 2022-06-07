import re
import sys, os

root = "Resources/TUpper/"
iri_regex = re.compile(r'(http://colore.oor.net/)(.+)')

for path, subdirs, file_names in os.walk(root):
    for file_name in file_names:
        file_path = os.path.join(path, file_name)
        file = open(file_path, 'r')
        if file_name == '.DS_Store':
            continue
        file_content = file.read()
        file.close()
        new_file_content = iri_regex.sub(repl='\1 ala_ma_kota', string=file_content)
        file = open(file_path, 'w')
        file.write(new_file_content)
        file.close()
        