import numpy as np
import pandas as pd
"""
Tool Class
"""
class Util:
    @staticmethod
    def list_in_list(list1, list2):
        for x in list1:
            if x not in list2:
                return False
        return True

    @staticmethod
    def list_solved_list(list1, list2):
        for x in list2:
            if x in list1:
                return True
        return False
    @staticmethod
    def transferAttrPos(attributes):
        pos=[]
        for idx,attr in enumerate(attributes):
            if attr==1: pos.append(idx)
        return pos

    @staticmethod
    def prune_affinity_matrix(affinity_matrix):
        affinity_matrix_copy = affinity_matrix.copy()
        accessedAttr = []
        for i, row in enumerate(affinity_matrix):
            if sum(row) != 0:
                accessedAttr.append(i)
        return affinity_matrix_copy[accessedAttr, :][:, accessedAttr], np.array(accessedAttr)

    @staticmethod
    def partition_ordering(schema):
        res=[]
        for par in schema:
            res.append(sorted(par))
        return sorted(res)
    @staticmethod
    def wirteResultToFile(result,path):
        data = list()
        for wload in result.keys():
            formatted_row = list()
            for metric in result[wload]: formatted_row += metric
            data.append(formatted_row)
        df = pd.DataFrame(index=result.keys(), data=data)
        # df.to_csv("experiment/result/metric_record.csv")
        df.to_csv(path)