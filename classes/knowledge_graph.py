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
                self.master_repository = self.build_master_repository(df)
                self.plt = plt

                '''                
                 :Initalizing the source, target, and relation values that will be contained in a dataframe under respective named columns.
                 :NetworkX constructor will take care of our DiGraph.
                 :***ORDERING MATTERS HERE!***
                '''

                # self.source = [i for i in df['subj']]
                # self.source_ques = [i for i in df['subj_ques']]
                # self.target = [i for i in df['obj']]
                # self.target_ques = [i for i in df['obj_ques']]
                # self.relations = [i for i in df['relations']]

                self.kg = pd.DataFrame({'source': df['subj'], 'target': df['obj'], 'edge': df['relations']})
                self.G = nx.from_pandas_edgelist(self.kg, "source", "target",
                                                 edge_attr=True, create_using=nx.MultiDiGraph())
                print(self.G.edges(data=True))
        except:
            print("ERR => Problem loading entities or relations")
            sys.exit(1)

    @staticmethod
    def build_master_repository(df):
        tmp = {}
        for row in df.itertuples(index=True, name='Pandas'):
            tmp[getattr(row, 'subj')] = [getattr(row, 'subj_ques'),
                                         getattr(row, 'obj'),
                                         getattr(row, 'obj_ques'),
                                         getattr(row, 'relations')]

            tmp[getattr(row,  'obj')] = [getattr(row, 'obj_ques'),
                                         getattr(row, 'subj'),
                                         getattr(row, 'subj_ques'),
                                         getattr(row, 'relations')]
        return tmp

    def print_graph(self):

        '''
         :The repository is an inversion of our Position dictionary. The repository key-value pair is: '(x,y): label'
         :This is useful for our annotation process
         :return: void
        '''

        repository = {}
        fig = self.plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(self.G, k=[len(max(str(i), key=len)) for i in self.kg['edge']][0] + .4)

        for i, e in pos.items():
            repository[str(list((round(e[0], 1), round(e[1], 1))))] = i

        ann = self.plt.annotate("",
                                xy=(-1, 1),
                                xytext=(-30, 30),
                                textcoords='offset points',
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->"))
        ann.set_visible(False)

        nx.draw(self.G, with_labels=True, node_size=1000, node_color='skyblue', edge_cmap=self.plt.cm, pos=pos)
        nx.draw_networkx_edge_labels(self.G, pos)
        def build_table(coord):
            '''
            Stub. I will need to convert key values in pos to a custom object that contains
            real values for Id, Ques, and Neighbors
            :param coord: Coordinate of the matching
            :return:
            '''
            label = repository[str(coord)]
            label_list = self.master_repository[label]

            ann.set_text('AUXILIARY NODE INFORMATION' + '\n\n' +
                         'Node_Nam: ' + label + '\n' +
                         'Subj/Obj: ' + label_list[1] + '\n' +
                         'Subj/Obj_Ques_1: ' + label_list[0] + '\n' +
                         'Subj/Obj_ques_2: ' + label_list[2] + '\n' +
                         'Relation: ' + label_list[3])
            ann.xy = (coord[0], coord[1])

        def hover(event):
            if event.inaxes is not None:
                vis = ann.get_visible()
                tmp = [round(event.xdata, 1), round(event.ydata, 1)]
                if str(tmp) in list(repository.keys()):
                    build_table(tmp)
                    ann.set_visible(True)
                    fig.canvas.draw_idle()
                else:
                    if vis:
                        ann.set_visible(False)
                        fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover)
        self.plt.show()
