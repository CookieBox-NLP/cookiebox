'''
 :CookieBox - Fake News Classifier
 :Author(s) - Ruj Haan, George Boktor, Arif Bashar
 :Middle Tennessee State University
'''

import pandas as pd
import sys
import networkx as nx


class KnowledgeGraph:
    def __init__(self, df, plt):
        try:
            if df is None:
                print("ERR => Please provide non-empty entities and relations")
                sys.exit(1)
            else:
                self.plt = plt

                '''
                 :Initalizing the source, target, and relation values that will be contained in a dataframe under respective named columns.
                 :NetworkX constructor will take care of our DiGraph.
                 :***ORDERING MATTERS HERE!***
                '''

                self.source = [i for i in df['subj']]
                self.source_ques = [i for i in df['subj_ques']]
                self.target = [i for i in df['obj']]
                self.target_ques = [i for i in df['obj_ques']]
                self.relations = [i for i in df['relations']]

                self.kg = pd.DataFrame({'source': df['subj'], 'target': df['obj'], 'ques': df['subj_ques'], 'edge': df['relations']})
                self.G = nx.from_pandas_edgelist(self.kg, "source", "target",
                                                 edge_attr=True, create_using=nx.MultiDiGraph())
        except:
            print("ERR => Problem loading entities or relations")
            sys.exit(1)

    def print_graph(self):
        self.plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(self.G, k=[len(max(str(i), key=len)) for i in self.relations][0] + .4)

        '''
         :ann = self.plt.annotate("", xy=(0, 0), xytext=(-20, 20), textcoords='offset points')
        '''

        nx.draw(self.G, with_labels=True, node_size=1000, node_color='skyblue', edge_cmap=self.plt.cm, pos=pos)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_edge_labels(self.G, pos)
        self.plt.show()

    def bolster_node_data(self, source):
        pass
