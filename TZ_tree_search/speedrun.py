from tree_search_utils.speedtest import check_graphs
import networkx as nx
import logging

speed_trial_name = 'order_5' # give your trial a quick name for logging purposes
where_to_log = 'E:/speedrunresults' # where to save logging info (to view results)

graphs = nx.read_graph6('C:/users/emily/dissertation/code/data/mckay/graph5.g6') # read in a list of graphs
order_limit = 20
max_children = 100
time_limit = 60 # seconds allowed


################################################################################
################################################################################
################################################################################
##################### leave this stuff alone :) ################################
################################################################################
################################################################################
################################################################################

logging.basicConfig(filename=f'{where_to_log}/speedrun_{speed_trial_name}_{time_limit}seconds_max{order_limit}.log',
filemode = 'a',
format = '',
datefmt='',
level=logging.INFO)

check_graphs(graphs, order_limit, time_limit, max_children = max_children)