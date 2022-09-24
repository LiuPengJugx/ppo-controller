from db.workload import Workload
from baselines.feedback import Feedback
from baselines.ppo_controller import PpoController
from db.conf import Conf
import os
import time
basePath=os.getcwd()
workload_dict={
    'tpch':['lineitem','orders','supplier'],
    'tpcds':['catalog_sales','store_sales','web_sales'],
    # 'synthetic':['test']
}
"""
Test the performance of baselines over tpc-h and tpc-ds datasets
"""
def main():
    res_per_workload=dict()
    for path in workload_dict.keys():
        for table in workload_dict[path]:
            wLoad=Workload(Conf.WORDTYPE[path][table],f'data/{path}/queries/{table}.csv')
            initial_par=[[i for i in range(wLoad.attr_num)]]
            # algorithms=[Applyall(),Smopdc(),Feedback(),PpoController(),OptimalController()]
            algorithms=[Feedback()]
            result=[]
            for algo in algorithms:
                start_time=time.time()
                avg_accessed_cost,avg_operate_cost=algo.repartition(initial_par, wLoad)
                total_time_cost=time.time()-start_time
                # print(algo.scvp_time)
                result.append([round(avg_accessed_cost,2),round(avg_operate_cost,2),algo.action_ratio[0],algo.action_ratio[1]*(total_time_cost)])
            print(result)
            res_per_workload[table]=result
    print(res_per_workload)
    # Util.wirteResultToFile(res_per_workload,"experiment/result/metric_record_partitioner2.csv")
    return res_per_workload

def sensitivity_main():
    # Testing the effect of slow to fast query rates on the repartitioning quality of algorithms
    # Test the effect of the number of queries on the repartitioning quality of algorithms when the query arrival rate is constant
    # Test the effect of query's selectivity on algorithms
    res_per_workload = dict()
    saved_path='queries/vary_que_vol'
    # saved_path='queries/vary_que_size'
    # saved_path='queries/vary_selectivity'
    # saved_path='queries/vary_selectivity2'
    for path in workload_dict.keys():
        for table in workload_dict[path]:
            for no in range(1,9):
                wLoad = Workload(Conf.WORDTYPE[path][table], f'data/{path}/{saved_path}/{table}_{no}.csv')
                initial_par = [[i for i in range(wLoad.attr_num)]]
                # algorithms = [Applyall(), Smopdc(), Feedback(), PpoController(), OptimalController()]
                algorithms=[Feedback(),PpoController()]
                result = []
                for algo in algorithms:
                    start_time = time.time()
                    avg_accessed_cost, avg_operate_cost = algo.repartition(initial_par, wLoad)
                    total_time_cost = time.time() - start_time
                    result.append(
                        [round(avg_accessed_cost, 2), round(avg_operate_cost, 2), algo.action_ratio[0],total_time_cost*algo.action_ratio[1]])
                print(result)
                res_per_workload[table+'_'+str(no)] = result
    print(res_per_workload)
    # Util.wirteResultToFile(res_per_workload, "experiment/result/metric_record_size.csv")

# Test the effect of page_size(block_size) of block on the repartitioning quality of algorithms
# Test the effect of cardinality of table on the repartitioning quality of algorithms
def block_size_or_cardinality_main(key='block'):
    size_list=[1024*2*x for x in range(1,5)]
    cardinality_list=[1e5,1e6,1e7,1e8]
    result=dict()
    if key=='block':
        for page_size in size_list:
            Conf.PAGE_SIZE=page_size
            result[page_size]=main()
    elif key=='cardinality':
        for cardinality in cardinality_list:
            Conf.CARDINALITY=cardinality
            result[cardinality]=main()
    print(result)

if __name__ == '__main__':
    # sensitivity_main()
    main()
    # block_size_main()