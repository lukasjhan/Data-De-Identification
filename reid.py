import pandas as pd
import numpy as np
import time

sex_mapping_table = {
    'M': 'END',
    'F': 'END'
}

age_mapping_table = {
    '20': '[20, 29[',
    '21': '[20, 29[',
    '22': '[20, 29[',
    '23': '[20, 29[',
    '24': '[20, 29[',
    '25': '[20, 29[',
    '26': '[20, 29[',
    '27': '[20, 29[',
    '28': '[20, 29[',
    '29': '[29, 38[',
    '30': '[29, 38[',
    '31': '[29, 38[',
    '32': '[29, 38[',
    '33': '[29, 38[',
    '34': '[29, 38[',
    '35': '[29, 38[',
    '36': '[29, 38[',
    '37': '[29, 38[',
    '38': '[38, 47[',
    '39': '[38, 47[',
    '40': '[38, 47[',
    '41': '[38, 47[',
    '42': '[38, 47[',
    '43': '[38, 47[',
    '44': '[38, 47[',
    '45': '[38, 47[',
    '46': '[38, 47[',
    '47': '[47, 56[',
    '48': '[47, 56[',
    '49': '[47, 56[',
    '50': '[47, 56[',
    '51': '[47, 56[',
    '52': '[47, 56[',
    '53': '[47, 56[',
    '54': '[47, 56[',
    '55': '[47, 56[',

    '[20, 29[': 'A',
    '[29, 38[': 'B',
    '[38, 47[': 'C',
    '[47, 56[': 'D',

    'A': 'END',
    'B': 'END',
    'C': 'END',
    'D': 'END'
}

loc_mapping_table = {
    '{서울, 인천, 경기}': '0',
    '{강원, 충청}': '1',
    '{경상, 전라, 제주}': '2',

    '서울': '{서울, 인천, 경기}',
    '인천': '{서울, 인천, 경기}',
    '경기': '{서울, 인천, 경기}',

    '강원': '{강원, 충청}',
    '충청': '{강원, 충청}',

    '경상': '{경상, 전라, 제주}',
    '전라': '{경상, 전라, 제주}',
    '제주': '{경상, 전라, 제주}',

    '0': 'END',
    '1': 'END',
    '2': 'END'
}

def main():
    # open data
    ori_df = pd.read_csv('ori.csv')
    pri_df = pd.read_csv('pri.csv')

    # set meaning tree table.
    table_list = [sex_mapping_table, age_mapping_table, loc_mapping_table]

    # column setting
    name_id = ['name']
    q_id = ['sex', 'age', 'loc']
    s_info = ['salary']
    s_weight = [1]

    # calculate avg & std
    s_info_avg = []
    s_info_std = []
    for i in s_info:
        d = ori_df[i].values.tolist()
        s_info_avg.append(np.mean(d))
        s_info_std.append(np.std(d))

    # THE RESULT!!
    ret = []

    # making data dict
    data_dict = {}
    index_dict = {}

    for i in ori_df.index:
        q_tmp_list = ori_df.loc[i, q_id].values.tolist()
        s_tmp_list = ori_df.loc[i, s_info].values.tolist()

        # s data -> standardize
        s_tmp_list = trans_to_std_value(s_tmp_list, s_info_avg, s_info_std)

        key = qlist_to_hashstring(q_tmp_list, table_list)

        append_on_dataset_dict(data_dict, key, s_tmp_list)
        append_on_dataset_dict(index_dict, key, i + 1) # start from 1
    
    #print(data_dict)
    #print(index_dict)

    # re sick star!
    for i in pri_df.index:
        q_tmp_list = pri_df.loc[i, q_id].values.tolist()
        s_tmp_list = pri_df.loc[i, s_info].values.tolist()

        # s data -> standardize
        s_tmp_list = trans_to_std_value(s_tmp_list, s_info_avg, s_info_std)

        key = qlist_to_hashstring(q_tmp_list, table_list)
        s_data_set = data_dict[key]
        index_list = index_dict[key]

        # get "standard distance" for every data in list 
        index = index_list[get_min_distance_index(s_data_set, s_tmp_list, s_weight)]
        ret.append(index)
            
    #print(ret)
    print_ret(ret)


def qlist_to_hashstring(qlist: list, tablelist: list) -> str:
    ret_list = []
    for data, table in zip(qlist, tablelist):
        ret_list.append(get_representative(str(data), table))

    return ''.join(ret_list)

def get_representative(data: str, mapping_table: dict) -> str:
    while data != 'END':
        next_data = mapping_table[data]
        if next_data == 'END':
            return data
        else:
            data = next_data
    return data
    
def append_on_dataset_dict(table: dict, key: str, value: list):
    if key in table.keys():
        table[key].append(value)
    else:
        tmp_list = []
        tmp_list.append(value)
        table[key] = tmp_list

def print_ret(ret: list):
    with open('result.txt', 'w') as f:
        i = 1
        for r in ret:
            s = '({0}, {1})\n'.format(i, r)
            f.write(s)
            i += 1

# **** REMEMBER!! lesser value means close value!! ****
def get_dis(ori: list, pri: list, wei: list): 
    sum = 0
    for a, b, w in zip(ori, pri, wei):
        sum += abs(a - b) * w
    return sum

def trans_to_std_value(ori_l: list, avg_l: list, std_l: list) -> list:
    ret = []
    for ori, avg, std in zip(ori_l, avg_l, std_l):
        ret.append((ori - avg) / std)
    return ret

def get_min_distance_index(ori_datasets: list, pri_dataset: list, weight: list) -> int:
    min_index = 0
    min_distance = 999 # init with big value
   
    for idx, data in enumerate(ori_datasets):
        dis = get_dis(data, pri_dataset, weight)
        
        if dis < min_distance:
            min_distance = dis
            min_index = idx

    return min_index


if __name__ == "__main__":
    start = time.time()
    main()
    elapsed = round(time.time() - start, 2)
    print('done in ' + str(elapsed) + ' seconds.')