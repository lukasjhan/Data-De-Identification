from scipy.spatial import distance
import pandas as pd
import numpy as np

def get_representative(data: str, mapping_table: dict) -> str:
    while data != 'END':
        next_data = mapping_table[data]
        if next_data == 'END':
            return data
        else:
            data = next_data
    return data

def qlist_to_hashstring(qlist: list, tablelist: list) -> str:
    ret_list = []
    for data, table in zip(qlist, tablelist):
        ret_list.append(get_representative(data, table))

    return ''.join(ret_list)

def append_on_dataset_dict(table: dict, key: str, value: list):
    if key in table.keys():
        table[key].append(value)
    else:
        tmp_list = []
        tmp_list.append(value)
        table[key] = tmp_list
    
test_map = {
    '1': '2',
    '2': '3',
    '3': 'END'
}

ret = get_representative('1', test_map)
print(ret)

ret = qlist_to_hashstring(['1','1','1'], [test_map, test_map, test_map])
print(ret)

new_dict = {'1': [[1], [2]]}
append_on_dataset_dict(new_dict, '2', [2])
append_on_dataset_dict(new_dict, '2', [3])
append_on_dataset_dict(new_dict, '2', [4])
append_on_dataset_dict(new_dict, '1', [3])
print(new_dict)

a= [1]
b= [4]
dst = distance.euclidean(a, b)
print(dst)

f_df = pd.read_csv('ori.csv')
f_name = f_df['salary'].values.tolist()
print(f_name)
print(np.mean(f_name))
print(np.std(f_name))

# 1. sperate data into q_id & rest of data
#    it means categorical & non-categorical
# 2. make categorical values to representative string
# 3. sort the representative string
