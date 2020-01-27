import sys
sys.path.append("..")
from classes.parsing import Parsing
from classes.knowledge_graph import KnowledgeGraph
import spacy
from spacy.matcher import Matcher

'''
THESE IMPORTS ARE TEMPORARY
'''

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

'''
THESE IMPORTS ARE TEMPORARY
'''

def main():

    file_name = str(sys.argv[1])
    opt = sys.argv[2]
    output_name = str(sys.argv[3])

    p = Parsing(file_name, output_name)

    if opt == '1':
        p.perform_remove_white()
    elif opt == '2':
        sub_str = input("Enter a substring: ")
        p.perform_remove_substring(sub_str)
    elif opt == '3':
        r_str = input("Enter a substring to remove: ")
        p_str = input("Enter a substring to replace it with: ")
        p.perform_replace_substring(r_str, p_str)

    print("COMPLETE => Find output in ../data/" + output_name)
    p.perform_extract_all()

    data = pd.DataFrame({'subj': ['Bob', 'Ricky', 'The day', 'Bob', 'Michael',
                                  'Bob', 'Bob', 'Nibraas', 'Arif', 'Donny', 'Bob'],
                         'subj_ques': ['Who', 'Who', 'When', 'Who', 'Who', 'Who',
                                       'Who', 'Who','Who', 'Who','Who'],
                         'relations': ['has a', 'drives to the', 'always', 'usually hits',
                                       'puts up', 'eats', 'writes', 'is obsessed with', 'always',
                                       'likes to play', 'turned his apartment into a'],
                         'obj': ['car', 'store', 'cycles', 'targets', 'carts', 'peanut butter',
                                 'fragments', 'Daniel Caesar', 'smells bad', 'sports', 'mansion'],
                         'obj_ques': ['What', 'Where', 'What', 'What', 'What', 'What',
                                      'What', 'Who', 'How', 'What', 'What']
                         })

    print('DATA =>\n', data)

    # test = [["Bob", "car"],
    #         ["Ricky", "store"],
    #         ["Don", "Store"],
    #         ["The day", "cycles"],
    #         ["Bob", "targets"],
    #         ["Michael","carts"],
    #         ["Bob","Peanut Butter"],
    #         ["Bob","Fragments"],
    #         ["Nibraas","Daniel Caesar"],
    #         ["Arif","smells bad"]]
    #
    # relations = [["has a"],
    #              ["goes to the"],
    #              ["is very"],
    #              ["is a synonym for"],
    #              ["always hits the"],
    #              ["random edge 1"],
    #              ["random edge 2"],
    #              ["random edge 3"],
    #              ["random edge 4"],
    #              ["random edge 5"]]

    kg = KnowledgeGraph(data, plt)
    kg.print_graph()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERR => Provide a filename AND option")
        sys.exit(1)
    main()
