import hashlib
import os
import re
from itertools import combinations


def __get_all_axioms_from_text(text: str):
    axiom_pattern = re.compile(r'^.+\.$', flags=re.MULTILINE)
    axioms = axiom_pattern.findall(text)
    return axioms


def __identify_axioms_by_first_variable_used(axioms: list) -> list:
    identified_axioms = list()
    variable_pattern = re.compile(r'X\d+')
    atomic_count = 0
    for axiom in axioms:
        first_variable = variable_pattern.search(axiom)
        if first_variable is None:
            atomic_count += 1
            identified_axiom = axiom.replace('sos', 'axiom_' + str(atomic_count))
        else:
            identified_axiom = axiom.replace('sos', 'axiom_with_first_variable_' + first_variable.group())
        identified_axioms.append(identified_axiom)
    return identified_axioms


def __check_subaxioms(axioms: list, depth: int):
    sub_axioms_tuples = combinations(axioms, len(axioms) - depth)
    for sub_axioms_tuple in sub_axioms_tuples:
        sub_axioms = list(sub_axioms_tuple)
        sub_axioms.sort()
        axiom_text = '\n'.join(sub_axioms)
        axioms_file_content_hash = str(hashlib.md5(axiom_text.encode()).hexdigest())
        axioms_file_name = 'in/' + axioms_file_content_hash + '.in'
        axioms_file = open(axioms_file_name, 'w')
        axioms_file.write(axiom_text)
        axioms_file.close()
        
        cmd_to_run_vampire = \
            'Resources/vampire_rel_master_6172 ' + \
            ' --mode casc_sat ' + \
            axioms_file_name + \
            ' > out/' + axioms_file_content_hash + '.out'
        
        vampire_result = os.system(cmd_to_run_vampire)  # returns the exit status
        vampire_has_decided = vampire_result == 0
        if vampire_has_decided:
            print('Vampire decided about ' + axioms_file_content_hash)
      
            
if __name__ == '__main__':
    axioms_in_text_file = open('Resources/bfo.tptp')
    axioms_text = axioms_in_text_file.read()
    axioms_in_text = __get_all_axioms_from_text(text=axioms_text)
    identified_axioms_in_text = __identify_axioms_by_first_variable_used(axioms=axioms_in_text)
    identified_axioms_in_text.sort()
    __check_subaxioms(axioms=identified_axioms_in_text, depth=1)
else:
    axioms_in_text_file = open('Resources/bfo.tptp')
    axioms_text = axioms_in_text_file.read()
    axioms_in_text = __get_all_axioms_from_text(text=axioms_text)
    identified_axioms_in_text = __identify_axioms_by_first_variable_used(axioms=axioms_in_text)
    identified_axioms_in_text.sort()
    __check_subaxioms(axioms=identified_axioms_in_text, depth=1)
