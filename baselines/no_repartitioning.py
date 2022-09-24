from baselines.algo_tpl import AlgorithmTemplate
import numpy as np
from db.disk_io import DiskIo
class NoController(AlgorithmTemplate):
    def repartition(self, initial_par, wLoad, **kwargs):
        print("Consider the case that no repartitioning actions are executed!")
        self.action_list=dict()
        collector = np.array([])
        for idx, sql in enumerate(wLoad.sql_list):
            collector = np.append(collector, sql['feature'])
        return DiskIo.compute_cost(collector, initial_par, wLoad.attrs_length)/sum([sql['feature'].frequency for sql in wLoad.sql_list])

if __name__=="__main__":
    nc=NoController()
    nc.repartition(None,None)
    print(nc.action_list)