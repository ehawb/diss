import importlib

class TricolorEncoder:
    def name(self):
        raise NotImplementedError
    
    def encode(self, game_state):
        raise NotImplementedError()
    
    def encode_edge(self, edge):
        raise NotImplementedError()
        
    def decode_edge_index(self, index):
        raise NotImplementedError()
    
    def num_points(self):
        raise NotImplementedError()
        
    def shape(self):
        raise NotImplementedError()
    
    def get_encoder_by_name(name, host_graph_order):
        module = name
        module = importlib.import_module(f'tricolor.encoders.{name}')
        constructor = getattr(module, 'create')
        return constructor(host_graph_order)
