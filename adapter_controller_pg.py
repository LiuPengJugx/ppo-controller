from db.workload import Workload
from baselines.ppo_controller import PpoController
from db.conf import Conf
from db.transaction import Transaction
from db.par_management import ParManagement as PM
from baselines.feedback import Feedback
from db.jta import JTA
from util import Util
import numpy as np
np.set_printoptions(threshold=np.inf)

# This is a middleware that connecting dynamic partition algorithms, postgresql and queries.
class AdapterController:
    # algorithms = [Afterall(),Smopdc(),Feedback(),PpoController(),OptimalController()]
    benchmark='synthetic'
    algorithms = [Feedback(),PpoController()]
    def experiment(self,wLoad):
        res_map=[]
        self.wLoad = wLoad
        initial_par = [[i for i in range(self.wLoad.attr_num)]]
        for algo in self.algorithms:
            algo.repartition(initial_par,self.wLoad)
            res_map.append(self.get_schema_metrics(algo.action_list))
        return res_map
        # #检查负载矩阵变化
        # for algo in self.algorithms:
        #     algo.repartition(initial_par,self.wLoad)
        #     self.compute_affinity_matrix_change(algo.action_list)

    def compute_affinity_matrix_change(self,action_list:dict):
        start_time=0
        last_aff_mat=self.wLoad.compute_affinity_matrix_consider_selectivity(0,0)
        last_par=[[i for i in range(50)]]
        # aff_mat_change=dict()
        for time in action_list.keys():
            if len(action_list[time])>0:
                print('-'*100)
                print(f"Time Range:[{start_time},{time}]")
            cur_aff_mat=self.wLoad.compute_affinity_matrix_consider_selectivity(start_time,time+1)
            aff_mat_change,accessed_att=Util.prune_affinity_matrix(last_aff_mat - cur_aff_mat)
            if len(action_list[time]) > 0:
                print(last_par)
                print(f"Partition Schema: {[par for par in last_par if Util.list_solved_list(accessed_att,par)]};\n Time: {time} ;\n Matrix Change: \n{aff_mat_change,accessed_att}")
            last_aff_mat=cur_aff_mat.copy()
            if len(action_list[time]) > 0:
                last_par = action_list[time]
                print(last_par)
                print(f"After Partition: {[par for par in last_par if Util.list_solved_list(accessed_att, par)]}")
            start_time=time+1


    def get_schema_metrics(self,action_list):
        txn_list=self.process_workload()
        metrics=dict()
        txn_count=0
        exec_scale,latency,rep_latency=0.0,0.0,0.0
        jta=JTA()
        latency_list=list()
        throughput_list=list()
        # comparison: estimated accessed blocks vs actual latency
        for key in txn_list.keys():
            print("Time:"+str(key))
            queries=txn_list[key]
            t=Transaction(queries,jta,key,self.benchmark)
            result=t.call()
            txn_count+=result.txn_count
            latency+=result.costTime
            latency_list.append(round(result.costTime,3))
            # executed repartitioning
            if key in action_list.keys():
                if action_list[key]:
                    result2=t.repartition(action_list[key])
                    rep_latency+=result2.finishTime-result2.startTime
                    throughput_list.append([txn_count,round(result.costTime,3),round(rep_latency,3)])
            else:
                throughput_list.append([txn_count, round(result.costTime,3), 0])
        metrics['Latency']=latency
        metrics['Rep_latency']=rep_latency
        metrics['Throughput']=txn_count/latency
        self.clear_table_data(jta)
        print(f'Action Length:{len(action_list)} , Content:{action_list.keys()}', )
        print(latency_list)
        return metrics

    def clear_table_data(self,jta):
        drop_tb_sql=""
        for index in PM.cur_partitions.keys():
            sub_tab_name = PM.test_tables[self.benchmark]['name'] + "sub" + str(index)
            drop_tb_sql += "DROP TABLE %s;\n"%(sub_tab_name)
        for line in drop_tb_sql.split("\n")[:-1]:
            jta.query(line)
        jta.commit()
        jta.close()
        PM.cur_partitions=dict()

    def process_workload(self)->dict:
        txn_list=dict()
        cur_time=0
        queries=[]
        for idx,item in enumerate(self.wLoad.sql_list):
            if item['time']!=cur_time:
                if len(queries)>0: txn_list[self.wLoad.sql_list[idx-1]['time']]=queries.copy()
                cur_time=item['time']
                queries.clear()
            queries.append(item['feature'])
        txn_list[self.wLoad.sql_list[-1]['time']] = queries.copy()
        return txn_list

if __name__=='__main__':
    ac=AdapterController()
    result=dict()
    cardinality_list=[1e5, 2e5, 4e5, 6e5, 8e5]
    workload_dict = {
        # 'data1': [3000, 1300, 4000],
        # 'data1': [1500, 3000, 1300, 4000],
        # 'data2': [1200, 1350],
        # 'data3': [1600, 2600],
        # 'tpch':['orders','supplier'],
        # 'tpch':['lineitem','orders','supplier'],
        # 'tpcds':['catalog_sales','store_sales','web_sales'],
        # 'tpcds': ['store_sales0','store_sales1','store_sales2','store_sales3','store_sales4'],
        'synthetic':['vary_que_size/test_'+str(x) for x in range(1,9)]
        # 'synthetic':['vary_que_vol/test_'+str(x) for x in range(7,8)]
    }
    for path in workload_dict.keys():
        for tid,table in enumerate(workload_dict[path]):
            # Conf.CARDINALITY=cardinality_list[tid]
            if path!='synthetic':
                ac.benchmark=table
                wLoad=Conf.WORDTYPE[path][table]
            else:
                wLoad=Conf.WORDTYPE[path]['test']
            result[table] = ac.experiment(Workload(wLoad, f'data/{path}/queries/{table}.csv'))
    print(result)