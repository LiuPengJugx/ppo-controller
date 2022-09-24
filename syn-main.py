from db.workload import Workload
from baselines.smopdc import Smopdc
from baselines.auto_store import AutoStore
from baselines.feedback import Feedback
from baselines.ppo_controller import PpoController
from db.conf import Conf
import os
import time
basePath=os.getcwd()
# Specify datasets
workload_dict={
    'data1':[1500,4000],
    # 'data3':[1600],
    # 'data2':[1200],
}
res_per_workload=dict()
# Test the performance of baselines over synthetic datasets
for path in workload_dict.keys():
    for query_num in workload_dict[path]:
        wLoad=Workload(Conf.WORDTYPE['synthetic']['test'],f'data/{path}/{query_num}query-steam.csv')
        initial_par=[[i for i in range(50)]]
        # algorithms=[NoController(),RandomDynamic(),AutoStore(),Smopdc(),Feedback(),PpoController(),OptimalController()]
        # algorithms=[AutoStore(),Smopdc(),Feedback(),PpoController(),OptimalController()]
        algorithms=[AutoStore(),Smopdc(),Feedback(),PpoController()]
        result=[]
        for algo in algorithms:
            start_time=time.time()
            avg_accessed_cost,avg_operate_cost=algo.repartition(initial_par, wLoad)
            result.append([round(avg_accessed_cost,2),round(avg_operate_cost,2),algo.action_ratio[0],algo.action_ratio[1]*(time.time()-start_time)])
        print(result)
        res_per_workload[query_num]=result
print(res_per_workload)