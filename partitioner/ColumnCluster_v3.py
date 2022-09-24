import numpy as np
import copy
from sklearn.cluster import SpectralClustering
from partitioner.fp_growth_plus import load_data,Fp_growth_plus
from util import Util
from db.disk_io import DiskIo
import multiprocessing as mul
import threading
lock = threading.Lock()
L_GLOBAL = []
QUERYS=[]
ATTRS_LENGTH=[]
import warnings
def get_freq_set_by_range(complete_column):
    global L_GLOBAL
    part_L = []
    for item in reversed(L_GLOBAL):
        for key in item:
            if Util.list_in_list([x for x in key], complete_column):
                part_L.append({key: item[key]})
    return part_L


def normalizePartition(candidate_paritions, accessed_attributes):
    new_candidate_paritions = []
    accessed_attributes = accessed_attributes.tolist()
    unaccessed_un_par = [[]]
    unaccessed_complete_par = []
    for i in range(len(ATTRS_LENGTH)):
        if (i not in accessed_attributes):
            unaccessed_un_par[0].append(i)
            unaccessed_complete_par.append([i])
    for par in candidate_paritions:
        new_par = []
        for attr in par:
            if attr in accessed_attributes: new_par.append(attr)
        if (len(new_par) > 0): new_candidate_paritions.append(new_par)
    cost1 = DiskIo.compute_cost(QUERYS, new_candidate_paritions + unaccessed_un_par, ATTRS_LENGTH)
    cost2 = DiskIo.compute_cost(QUERYS, new_candidate_paritions + unaccessed_complete_par, ATTRS_LENGTH)
    if cost1 < cost2:
        return new_candidate_paritions + unaccessed_un_par
    else:
        return new_candidate_paritions + unaccessed_complete_par

def compute_cost_by_spectal_cluster(affinity_matrix,querys,attrs_length):
    warnings.filterwarnings('ignore')
    global L_GLOBAL
    global QUERYS
    global ATTRS_LENGTH
    QUERYS = querys
    ATTRS_LENGTH = attrs_length
    X, accessedAttr = Util.prune_affinity_matrix(affinity_matrix)
    min_cost = float('inf')
    min_cluster = []
    for k in range(1, len(X) + 1):
        y_pred = SpectralClustering(n_clusters=k, affinity='precomputed',
                                    assign_labels="discretize",
                                    random_state=0).fit_predict(X)
        # print(y_pred)
        candidate_paritions = []
        for i in range(k):
            class_label = np.where(y_pred == i)[0]
            candidate_paritions.append(accessedAttr[class_label.tolist()].tolist())
        candidate_paritions_normalization = candidate_paritions
        cost = DiskIo.compute_cost(QUERYS, candidate_paritions_normalization, ATTRS_LENGTH)
        # cost=cal_total_memory_cost(querys,candidate_paritions,attrs_length)
        if cost < min_cost:
            min_cost = cost
            min_cluster = candidate_paritions_normalization
    data_set, _ = load_data(accessedAttr,QUERYS)
    min_support = 0
    L_GLOBAL, _ = Fp_growth_plus().generate_L(data_set, min_support)

    optimal_candidate_paritions = get_best_partition_res(min_cluster)
    return optimal_candidate_paritions

# @ray.remote
# def processNumberFreqset(itemset, complete_column_range, temp_candidates):
#     freq_item_dict = []
#     for key in itemset:
#         temp_complete_column_range = complete_column_range.copy()
#         [temp_complete_column_range.remove(x) for x in key]
#         if len(temp_complete_column_range) == 0: continue
#         reward_res = cut_reward_fun_update([[x for x in key], temp_complete_column_range],temp_candidates)
#         if (reward_res['val'] >= 0):
#             freq_item_dict.append(reward_res)
#     return freq_item_dict

# recursion function
def split_candidate_parition_by_cut_reward(complete_column_range, temp_candidates2):
    # If the cluster to be split has only one element, you can return it directly
    if (len(complete_column_range) == 1): return [complete_column_range]
    temp_candidates = temp_candidates2.copy()
    L = get_freq_set_by_range(complete_column_range)
    freq_item_dict=[]
    # chunk_freq_set = [processNumberFreqset.remote(itemset, complete_column_range, temp_candidates)
    #                   for itemset in reversed(L)]
    for itemset in reversed(L):
        for key in itemset:
            temp_complete_column_range=complete_column_range.copy()
            [temp_complete_column_range.remove(x) for x in key]
            if len(temp_complete_column_range)==0:continue
            reward_res=cut_reward_fun_update([[x for x in key],temp_complete_column_range],temp_candidates)
            if(reward_res['val']>=0):
                freq_item_dict.append(reward_res)
    # res = ray.get(chunk_freq_set)
    # freq_item_dict = [item for list in res for item in list if len(list) != 0]
    splited_paritions = []
    left_unsplited_par = copy.deepcopy(complete_column_range)
    while (True):
        # If the frequent itemset list is empty, it indicates that the candidates have been arranged
        if len(freq_item_dict) == 0:
            if len(left_unsplited_par) > 0: splited_paritions.append(left_unsplited_par)
            break
        # Select the first frequent item with the largest reward
        freq_item_dict.sort(key=lambda x: (x["val"]), reverse=True)
        current_cut_item = freq_item_dict[0]
        freq_item_dict.remove(current_cut_item)
        left_unsplited_par = list(set(left_unsplited_par) - set(current_cut_item['fre_item'][0]))
        # The splits partitions may also be re-cut
        if (len(left_unsplited_par) == 0):
            other_temp_candidates = temp_candidates.copy()
        else:
            other_temp_candidates = [left_unsplited_par] + temp_candidates.copy()
        splited_paritions += split_candidate_parition_by_cut_reward( current_cut_item['fre_item'][0],
                                                                     other_temp_candidates)

        temp_candidates.append(current_cut_item['fre_item'][0])
        if (len(left_unsplited_par) == 0):
            break
        elif (len(left_unsplited_par) == 1):
            splited_paritions.append(left_unsplited_par)
            break
        # i=0
        for i in range(len(freq_item_dict) - 1, -1, -1):
            freq_item = freq_item_dict[i]
            if Util.list_in_list(freq_item['fre_item'][0], left_unsplited_par):
                n_avg_sel = 0
                update_freq_item = update_reward_fun_update(current_cut_item, freq_item,
                                                             temp_candidates)
                if len(freq_item['fre_item'][0]) == len(left_unsplited_par):
                    update_freq_item['val'] = 0
                if (update_freq_item['val'] >= 0):
                    freq_item_dict[i] = update_freq_item
                else:
                    freq_item_dict.remove(freq_item)
            else:
                freq_item_dict.remove(freq_item)

    return splited_paritions

# @ray.remote
def get_atom_partition(split_cluster,candidate_clusters,queue):
    temp_clusters = candidate_clusters.copy()
    temp_clusters.remove(split_cluster)
    init_cost = DiskIo.compute_cost(QUERYS,[split_cluster], ATTRS_LENGTH)
    new_split_clusters = split_candidate_parition_by_cut_reward(split_cluster,temp_clusters)
    splited_update_cost = DiskIo.compute_cost(QUERYS, new_split_clusters, ATTRS_LENGTH)
    if splited_update_cost < init_cost:
       queue.put({'o_clusters': split_cluster,
                'u_clusters': new_split_clusters})
    else:
        queue.put({})


def get_best_partition_res(candidate_clusters_orgin):
    candidate_clusters = candidate_clusters_orgin.copy()
    to_split_clusters = []
    for item in candidate_clusters_orgin:
        if len(item) > 1:
            to_split_clusters.append(item)
    queue=mul.Queue()
    jobs=[]
    for split_cluster in to_split_clusters:
        process=mul.Process(target=get_atom_partition,args=(split_cluster, candidate_clusters,queue))
        process.start()
        jobs.append(process)
    # for job in jobs:job.join()
    chunk_splited_cluster=[queue.get() for _ in jobs]
    for idx,item in enumerate(chunk_splited_cluster):
        if item:
            candidate_clusters.remove(item['o_clusters'])
            candidate_clusters+=item['u_clusters']
    # Looking for a combining scheme
    combine_schema = combine_candidate_parition_by_combine_reward(candidate_clusters)
    for item in combine_schema:
        for par in item['o_clusters']:
            candidate_clusters.remove(par)
        candidate_clusters += item['u_clusters']
    return candidate_clusters

def get_best_partition_res2(candidate_clusters_orgin):
    candidate_clusters = candidate_clusters_orgin.copy()
    to_split_clusters = []
    split_schema = []
    for item in candidate_clusters_orgin:
        if len(item) > 1:
            to_split_clusters.append(item)
    for split_cluster in to_split_clusters:
        init_cost = DiskIo.compute_cost(QUERYS, [split_cluster], ATTRS_LENGTH)
        temp_clusters = candidate_clusters.copy()
        temp_clusters.remove(split_cluster)
        new_split_clusters = split_candidate_parition_by_cut_reward( split_cluster,
                                                                    temp_clusters)
        splited_update_cost = DiskIo.compute_cost(QUERYS, new_split_clusters, ATTRS_LENGTH)
        if splited_update_cost < init_cost:
            split_schema.append({
                'o_clusters': [split_cluster],
                'u_clusters': new_split_clusters,
                'reward': init_cost - splited_update_cost
            })
            candidate_clusters.remove(split_cluster)
            for new_cluster in new_split_clusters:
                candidate_clusters.append(new_cluster)
    # Looking for a combining scheme
    combine_schema = combine_candidate_parition_by_combine_reward(candidate_clusters)
    for item in combine_schema:
        for par in item['o_clusters']:
            candidate_clusters.remove(par)
        candidate_clusters += item['u_clusters']

    return candidate_clusters

def rayProcessNumberFreqset(itemset, to_combined_clusters, temp_combined_cluster, init_cost):
    freq_item_dict = []
    for key in itemset:
        if len(key) < 2: continue
        # Judge whether the original cluster scheme can form the frequent itemset
        temp_key = []
        for item_cluster in to_combined_clusters:
            if Util.list_solved_list(item_cluster, key):
                temp_key.append(item_cluster)
        if set(key) <= set([y for x in temp_key for y in x]):
            if temp_key in temp_combined_cluster: continue
            lock.acquire()
            temp_combined_cluster.append(temp_key)
            lock.release()
            # calculate combing reward
            temp_combined_clusters = to_combined_clusters.copy()
            [temp_combined_clusters.remove(cluster) for cluster in temp_key]
            temp_combined_clusters.append([x for item in temp_key for x in item])
            combined_cost = DiskIo.compute_cost(QUERYS, temp_combined_clusters, ATTRS_LENGTH)
            if init_cost - combined_cost > 0:
                freq_item_dict.append({'item': temp_key, 'val': init_cost - combined_cost})
    return freq_item_dict


from partitioner.MyThread import MyThread


def combine_candidate_parition_by_combine_reward(candidate_clusters_orgin):
    # combine the splitted clusters
    to_combined_clusters = candidate_clusters_orgin.copy()
    init_cost = DiskIo.compute_cost(QUERYS, to_combined_clusters, ATTRS_LENGTH)
    L = L_GLOBAL
    freq_item_dict = []
    temp_combined_cluster = []
    res = []
    for itemset in reversed(L):
        task = MyThread(rayProcessNumberFreqset,
                        (itemset, to_combined_clusters, temp_combined_cluster, init_cost))
        task.start()
        res.append(task.get_result())

    # chunk_freq_set=[rayProcessNumberFreqset(itemset,to_combined_clusters,temp_combined_cluster,init_cost,querys,attrs_length) for itemset in reversed(L)]
    # res=ray.get(chunk_freq_set)
    freq_item_dict = [item for list in res for item in list if len(list) != 0]
    # for itemset in reversed(L):
    #     for key in itemset:
    #         if len(key) < 2: continue
    #         # 判断原簇方案是否可以组成该频繁项集
    #         temp_key = []
    #         for item_cluster in to_combined_clusters:
    #             if list_solved_list(item_cluster, key):
    #                 temp_key.append(item_cluster)
    #         if set(key) <= set([y for x in temp_key for y in x]):
    #             if temp_key in temp_combined_cluster:continue
    #             temp_combined_cluster.append(temp_key)
    #             # 计算合并收益
    #             temp_combined_clusters = to_combined_clusters.copy()
    #             [temp_combined_clusters.remove(cluster) for cluster in temp_key]
    #             temp_combined_clusters.append([x for item in temp_key for x in item])
    #             combined_cost = DiskIo.compute_cost(querys, temp_combined_clusters, attrs_length)
    #             if init_cost - combined_cost > 0:
    #                 freq_item_dict.append({'item': temp_key, 'val': init_cost - combined_cost})
    combine_schema = []
    left_uncombined_par = to_combined_clusters.copy()
    freq_item_dict.sort(key=lambda x: (x["val"]), reverse=True)
    while (True):
        if len(freq_item_dict) == 0: break
        # Select the top frequent item with the largest reward
        freq_item_dict.sort(key=lambda x: (x["val"]), reverse=True)
        current_combined_item = freq_item_dict[0]['item']
        combine_schema.append({
            'o_clusters': current_combined_item,
            'u_clusters': [[x for item in current_combined_item for x in item]],
            'reward': freq_item_dict[0]['val']
        })
        del freq_item_dict[0]
        [left_uncombined_par.remove(x) for x in current_combined_item]
        if (len(left_uncombined_par) == 1):
            break
        for i in range(len(freq_item_dict) - 1, -1, -1):
            freq_item = freq_item_dict[i]
            # temp_left_uncombined_par = left_uncombined_par.copy()
            flag = True
            for par in freq_item['item']:
                if par in current_combined_item:
                    flag = False
                    freq_item_dict.remove(freq_item)
                    break
    return combine_schema


def cut_reward_fun_update(splited_column, temp_candidates2):
    temp_candidates = temp_candidates2.copy()
    # The number of queries that only access segment B attributes is n1. The number of queries that only access segment C attributes is n2. The number of queries accessing both segment B and segment C attributes is n3
    b_parition = splited_column[0]
    c_parition = splited_column[1]
    res = {
        'fre_item': [b_parition, c_parition],
        # Consider the overall partition scheme, rather than the sub partitions in the original cluster
        'val': DiskIo.compute_cost(QUERYS, temp_candidates + [b_parition + c_parition],
                                     ATTRS_LENGTH) - DiskIo.compute_cost(QUERYS, splited_column + temp_candidates,
                                                                           ATTRS_LENGTH),
    }
    return res


# Since the frequent items of cutting have been determined, avg_sel,n3_matrix_ind can be calculated in advance without affecting the update
def update_reward_fun_update(last_cut_info, my_cut_info,temp_candidates2):
    temp_candidates = temp_candidates2.copy()
    before_change_par = [last_cut_info['fre_item'][1]]
    after_change_par = [my_cut_info['fre_item'][0],
                        list(set(my_cut_info['fre_item'][1]) - set(last_cut_info['fre_item'][0]))]
    res = {
        'fre_item': [my_cut_info['fre_item'][0],
                     list(set(my_cut_info['fre_item'][1]) - set(last_cut_info['fre_item'][0]))],
        'val': DiskIo.compute_cost(QUERYS, temp_candidates + before_change_par, ATTRS_LENGTH) - DiskIo.compute_cost(
            QUERYS, temp_candidates + after_change_par, ATTRS_LENGTH)
    }
    return res