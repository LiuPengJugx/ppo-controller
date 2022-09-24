from partitioner.ColumnCluster_v2 import ColumnCluster_V2
from partitioner.ColumnCluster_v3 import compute_cost_by_spectal_cluster


class Scvp:
    @staticmethod
    def partitioner(affinity_matrix,temp_workload,attrs_length):
        schema=ColumnCluster_V2().compute_cost_by_spectal_cluster(affinity_matrix,temp_workload,attrs_length)
        return schema

    def partitioner2(affinity_matrix,temp_workload,attrs_length):
        schema=ColumnCluster_V2().compute_cost_by_spectal_cluster2(affinity_matrix,temp_workload,attrs_length)
        return schema

    def partitioner3(affinity_matrix,temp_workload,attrs_length):
        schema=compute_cost_by_spectal_cluster(affinity_matrix,temp_workload,attrs_length)
        return schema