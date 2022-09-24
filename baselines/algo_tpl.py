import time
from partitioner.scvp import Scvp
from db.disk_io import DiskIo

"""
    A template class for dynamic partitioning algorithm.
    Implement two methods: 
        1. partition -> a public method is used to call scvp partitioner to get new partitions and return cost reduction
        2. repartition -> run whole workload and generate a list of repartitioning actions, and finally return the result.
"""
class AlgorithmTemplate:
    scvp_time=0
    def partition(self, windowsql, wLoad, cur_par_schema):
        if not isinstance(windowsql,list):
            windowsql = windowsql.tolist()
        min_schema=cur_par_schema
        time0=time.time()
        schema=Scvp.partitioner(wLoad.compute_affinity_matrix_by_sqls(windowsql),windowsql,wLoad.attrs_length)
        self.scvp_time+=time.time()-time0
        init_cost = DiskIo.compute_cost(windowsql, cur_par_schema, wLoad.attrs_length)
        cost = DiskIo.compute_cost(windowsql, schema, wLoad.attrs_length)
        if cost<init_cost:
            min_schema=schema
        return min_schema,init_cost-cost

    def repartition(self,initial_par,wLoad):
        pass
    # def repartition(self, initial_par, wLoad):
    #     total_blocks = 0
    #     total_rep_blocks = 0
    #     collector=np.array([])
    #     self.action_list = dict()
    #     cur_par_schema = initial_par
    #     self.optimize_time=0
    #     total_actions=0
    #     true_actions=0
    #     isFirst=True
    #     begin_time=wLoad.sql_list[0]['time']
    #     for idx,sql in enumerate(wLoad.sql_list):
    #         if collector.shape[0]>=2:
    #             # 数据库处于低功耗状态时
    #             # print(f"time0:{wLoad.sql_list[idx-1]['time']} time1:{sql['time']}")
    #             if sql['time']-wLoad.sql_list[idx-1]['time']>=3 or (sql['time']>=begin_time+2 and isFirst):
    #                 isFirst=False
    #                 time0=time.time()
    #                 min_schema, cost_increment = self.partition(collector, wLoad, cur_par_schema)
    #                 operator_cost=DiskIo.compute_repartitioning_cost(cur_par_schema,min_schema,wLoad.attrs_length)
    #                 self.optimize_time+=time.time()-time0
    #                 total_actions+=1
    #                 total_blocks += DiskIo.compute_cost(collector, cur_par_schema, wLoad.attrs_length)
    #                 if min_schema!=cur_par_schema and cost_increment>operator_cost:
    #                     true_actions+=1
    #                     self.action_list[sql['time']] = min_schema
    #                     total_rep_blocks+=operator_cost
    #                     print("时刻",wLoad.sql_list[idx-1]['time'],",更新分区方案为:",min_schema,",预计成本收益为:",cost_increment)
    #                     cur_par_schema=min_schema
    #                 collector=np.array([])
    #         collector=np.append(collector,sql['feature'])
    #     if collector.shape[0]>0:
    #         total_blocks += DiskIo.compute_cost(collector, cur_par_schema, wLoad.attrs_length)
    #     self.action_ratio=[true_actions,round(true_actions/total_actions,3)]
    #     total_freq=(sum([sql['feature'].frequency for sql in wLoad.sql_list]))
    #     return total_blocks/total_freq,total_rep_blocks/total_freq
