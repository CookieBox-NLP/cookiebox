class GraphNode:
    def __init__(self, df, entities):
        self.relations = {}
        self.df = df
        self.entities = entities

    def get_entitiy_relation(self):
        pass

    def get_tag(self):
        return self.pos_tag

    def get_id(self):
        return self.node_id
