import random
import time
from db.workload import Workload
from util import Util
from partitioner.scvp import Scvp
from db.conf import Conf
def partition_by_wide_workload(workload,wLoad):
    # Trigger repartitioning
    attr_clusters = []
    # Find attribute clusters according to the nearest time point
    time_sequence = sorted(workload.keys(), reverse=True)
    cur_time=time_sequence[0]
    complete_attr_clusters = []
    cnt = 0
    while True:
        queries = workload[time_sequence[cnt]].copy()
        not_complete_attr_clusters = []
        #Note: The order of the queries affects the allocation of the cluster.
        QUERIES=[]
        while len(queries)>0:
            item=queries.pop(0)
            QUERY={'Q': [item], 'A': [i for i, x in enumerate(item.attributes) if x == 1]}
            have_flag=True
            while have_flag:
                have_flag=False
                for query in queries.copy():
                    solved_attrs = [i for i, x in enumerate(query.attributes) if x == 1]
                    if Util.list_solved_list(solved_attrs,QUERY['A']):
                        QUERY['Q'].append(query)
                        [QUERY['A'].append(attr) for attr in solved_attrs if attr not in QUERY['A']]
                        queries.remove(query)
                        have_flag=True
            QUERIES.append(QUERY)
        for QUERY in QUERIES:
            solved_attrs =QUERY['A']
            is_exist = False
            will_combined_cluster = []
            for attr_cluster in attr_clusters:
                if Util.list_solved_list(attr_cluster['range'], solved_attrs):
                    # The first relevant cluster encountered by this query
                    if not is_exist:
                        is_exist = True
                        attr_cluster['queries']+=QUERY['Q']
                        [attr_cluster['range'].append(attr) for attr in solved_attrs if attr not in attr_cluster['range']]
                    # Add the cluster to the combine_cluster queue whenever it is related to query
                    will_combined_cluster.append(attr_cluster)
            # Merge all elements in the combine cluster queue
            if will_combined_cluster:
                new_cluster = will_combined_cluster[0]
                if len(will_combined_cluster) > 1:
                    for item in will_combined_cluster[1:]:
                        new_cluster['queries'] += item['queries']
                        [new_cluster['range'].append(attr) for attr in item['range'] if
                         attr not in new_cluster['range']]
                    #  Clear all elements in the combine cluster queue from attr_clusters
                    [attr_clusters.remove(item) for item in will_combined_cluster[1:]]
                # Merge attribute clusters with overlapping attribute ranges
                if new_cluster not in not_complete_attr_clusters:
                    not_complete_attr_clusters.append(new_cluster)
            # If no cluster related to the query is found in the first and second round of workload, it needs to be assigned a new cluster
            if not is_exist and cnt <= 1:
                cluster = {'queries': QUERY['Q'], 'range': solved_attrs}
                attr_clusters.append(cluster)
                not_complete_attr_clusters.append(cluster)
        # Clear completed attribute clusters
        for attr_cluster in attr_clusters.copy():
            if attr_cluster not in not_complete_attr_clusters:
                # As long as it is added to the complete_attr_clusters list, it is necessary to judge whether there are coincident clusters
                flag_combined = False
                for complete_cluster in complete_attr_clusters:
                    if Util.list_solved_list(complete_cluster['range'], attr_cluster['range']):
                        # Merge
                        complete_cluster['queries'] += attr_cluster['queries']
                        [complete_cluster['range'].append(attr) for attr in attr_cluster['range'] if
                         attr not in complete_cluster['range']]
                        flag_combined = True
                        break
                if not flag_combined: complete_attr_clusters.append(attr_cluster)
                attr_clusters.remove(attr_cluster)
        # All attribute clusters do not add new elements in this round of workload
        if not attr_clusters:
            break
        # The number of queries within an attribute cluster should not exceed the limit
        total_queries_num = [len(cluster['queries']) for cluster in complete_attr_clusters]
        total_queries_num += [len(cluster['queries']) for cluster in attr_clusters]
        if sum(total_queries_num)>=70:
            break
        if cnt >= len(time_sequence)-1:
            # Time comes to an end, if attr_clusters has elements, which should be added to complete_attr_clusters
            # However, before adding, you must first judge whether there are clusters with coincident attributes, which need to be merged
            for attr_cluster in attr_clusters:
                flag_combined = False
                for complete_cluster in complete_attr_clusters:
                    if Util.list_solved_list(complete_cluster['range'], attr_cluster['range']):
                        # Merge
                        complete_cluster['queries'] += attr_cluster['queries']
                        [complete_cluster['range'].append(attr) for attr in attr_cluster['range'] if
                         attr not in complete_cluster['range']]
                        flag_combined = True
                        break
                if not flag_combined: complete_attr_clusters.append(attr_cluster)
            break
        cnt += 1
    # call partitioning algorithm to get scheme of selected attribute clusters
    new_par_schema = []
    # Eliminate clusters that do not meet the number of query types
    [complete_attr_clusters.remove(cluster) for cluster in complete_attr_clusters.copy() if len(cluster['queries'])<=2]
    query_of_cluster=[]
    time0=time.time()
    for cluster in complete_attr_clusters:
        affinity_matrix = wLoad.compute_affinity_matrix_by_sqls(cluster['queries'])
        query_of_cluster.append(len(cluster['queries']))
        new_par_schema += Scvp.partitioner2(affinity_matrix, cluster['queries'], wLoad.attrs_length)
    time1=time.time()
    print(f"Back in time:{cur_time}--->{time_sequence[cnt]}, query count:{sum(query_of_cluster)}, time-consuming:{time1-time0}, partition scheme:{new_par_schema}")
    return new_par_schema,time_sequence[cnt],time1-time0

def partitioner_simulation(wLoad):
    time_range=[wLoad.sql_list[0]['time'], wLoad.sql_list[-1]['time']]
    max_split=10
    collect_time = []
    # collect_time=[9,15,19,27,33,50,120,170,188,200,230]
    start_time = time_range[0]
    while(True):
        start_time +=random.randint(2,max_split)
        if start_time>time_range[1]:break
        collect_time.append(start_time)
    workload=dict()
    for cur_time in range(wLoad.sql_list[0]['time'],wLoad.sql_list[-1]['time']+1):
        workload[cur_time]=wLoad.load_sql_by_time_range(cur_time,cur_time+1)
        # if cur_time in collect_time:
        #     partition_by_wide_workload(workload,wLoad)
        partition_by_wide_workload(workload,wLoad)

if __name__=='__main__':
    for query_num in [1600]:

        wLoad=Workload(Conf.WORDTYPE['synthetic']['test'],f'../data/data3/{query_num}query-steam.csv')
        start_time=time.time()
        partitioner_simulation(wLoad)
        print(f"load:{query_num}, time:{time.time()-start_time}")