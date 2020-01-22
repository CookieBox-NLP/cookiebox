import sys
sys.path.append("..")
from classes.parsing import Parsing
from classes.knowledge_graph import KnowledgeGraph
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

    test = [["Bob", "car"],
            ["Ricky", "store"],
            ["Ruj", "petite"],
            ["Gay people", "Ruj's family"]]

    relations = [["has a"],
                 ["goes to the"],
                 ["is very"],
                 ["is a synonym for"]]

    kg = KnowledgeGraph(test, relations, plt)
    kg.print_graph()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("ERR => Provide a filename AND option")
        sys.exit(1)
    main()
