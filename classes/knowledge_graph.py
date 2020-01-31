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

                self.kg = pd.DataFrame({'source': df['subj'], 'target': df['obj'], 'edge': df['relations']})
                self.G = nx.from_pandas_edgelist(self.kg, "source", "target",
                                                 edge_attr=True, create_using=nx.MultiDiGraph())
        except:
            print("ERR => Problem loading entities or relations")
            sys.exit(1)

    def print_graph(self):
        node_coords = []
        fig = self.plt.figure(figsize=(8, 8))
        pos = nx.spring_layout(self.G, k=[len(max(str(i), key=len)) for i in self.relations][0] + .4)
        node_coords += [list((round(pos[i][0], 1), round(pos[i][1], 1))) for i in pos.keys()]
        print('NEW =>', node_coords)

        ann = self.plt.annotate("", xy=(-1,1), xytext=(-20, 20), textcoords='offset points', bbox=dict(boxstyle="round", fc="w"))
        ann.set_visible(False)

        nx.draw(self.G, with_labels=True, node_size=1000, node_color='skyblue', edge_cmap=self.plt.cm, pos=pos)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_edge_labels(self.G, pos)

        def build_table(coords):
            tmp = (coords[0], coords[1])
            text = str(i for i in pos.keys() if all(j in pos[i] for j in tmp))
            ann.set_text(text)

        def hover(event):
            if event.inaxes is not None:
                vis = ann.get_visible()
                tmp = [round(event.xdata, 1), round(event.ydata,1)]
                print(tmp)
                if tmp in node_coords:
                    build_table(tmp)
                    ann.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        ann.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
        self.plt.show()

    def bolster_node_data(self):

        pass
