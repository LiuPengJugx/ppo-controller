from baselines.algo_tpl import AlgorithmTemplate
from db.disk_io import DiskIo
import time
class AutoStore(AlgorithmTemplate):
    # adjust the parameter N depend on the kind of test data
    # synthetic: N=8
    # tpch (N=15): N=8->979.62; N=9->971 ; 10->971 ; 15->962 ;  20->948;  25->949; 30->968
    # tpcds (N=20)

    def repartition(self, initial_par, wLoad):
        total_blocks=0
        N=8
        total_rep_blocks=0
        collector=[]
        self.action_list = dict()
        cur_par_schema = initial_par
        self.optimize_time=0
        total_actions = 0
        true_actions = 0
        isFirst=True
        for cur_time in range(wLoad.sql_list[0]['time'], wLoad.sql_list[-1]['time'] + 1):
            collector+=wLoad.load_sql_by_time_range(cur_time,cur_time+1)
            if len(collector)>=N or isFirst:
                isFirst=False
                time0 = time.time()
                min_schema, cost_increment = self.partition(collector, wLoad, cur_par_schema)
                operator_cost = DiskIo.compute_repartitioning_cost(cur_par_schema, min_schema, wLoad.attrs_length)
                self.optimize_time+=time.time()-time0
                total_actions+=1
                if min_schema!=cur_par_schema and cost_increment>operator_cost:
                    true_actions+=1
                    self.action_list[cur_time] = min_schema
                    total_blocks+=DiskIo.compute_cost(collector,cur_par_schema,wLoad.attrs_length)
                    total_rep_blocks+=operator_cost
                    print("Time:",cur_time,", update the partition scheme as:",min_schema,", expected cost reduction:",cost_increment)
                    cur_par_schema=min_schema
                    collector.clear()
        if len(collector)>0:
            total_blocks += DiskIo.compute_cost(collector, cur_par_schema, wLoad.attrs_length)
        self.action_ratio = [true_actions, round(true_actions / total_actions, 3)]
        total_freq=(sum([sql['feature'].frequency for sql in wLoad.sql_list]))
        return total_blocks/total_freq,total_rep_blocks/total_freq
