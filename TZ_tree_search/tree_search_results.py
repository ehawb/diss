from tree_search_utils.extract_results import present_realizations as realizers
from tree_search_utils.extract_results import present_graphs_with_status as status


#data = 'E:/tree_search/08Oct2022_203009_ramsey34_1_BFS_FINAL.pickle'

data = 'E:/tree_search/14Jun2023_092513_C_5_BFS_FINAL.pickle'
realizers(data)
large = status(data, 'TL')
bad = status(data, 'TB')
