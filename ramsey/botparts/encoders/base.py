# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:42:43 2020

@author: Emily Smith
"""

import importlib

class Encoder:
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
    
    def get_encoder_by_name(name, graph_order):
        module = name
        module = importlib.import_module(f'botparts.encoders.{name}')
        constructor = getattr(module, 'create')
        return constructor(graph_order)
