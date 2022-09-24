from db.conf import Conf
import pandas as pd
from data.workload_generator_tpc import generate_random_query
# from controller.data.workload_generator_v2 import generate_random_query


def gen_ques_by_gaussian(attrs_length,total_time,query_num,maximum_sigma_percentage,cut_num,save_path):
    # maximum_sigma_percentage=0.5
    querys=generate_random_query(len(attrs_length),total_time,query_num,maximum_sigma_percentage,cut_num)
    pd.DataFrame(querys).to_csv(save_path, index=False, header=False)

if __name__ == '__main__':
    # 控制查询速率
    T=200
    avg_volume=[x for x in range(1,9)]
    for vol in avg_volume:
        que_num=T*vol
        gen_ques_by_gaussian(Conf.WORDTYPE['synthetic']['test'], T, que_num,0.4,5,f'queries/vary_que_vol/test_{vol}.csv')


    # 控制负载尺寸，保证速率不变
    # vol=3
    # T_list=[100*x for x in range(1,9)]
    # for idx,T in enumerate(T_list):
    #     que_num=T*vol
    #     # produce dataset for test table
    #     gen_ques_by_gaussian(Conf.WORDTYPE['synthetic']['test'], T, que_num, 0.4, 5,f'queries/vary_que_size/test_{idx + 1}.csv')

    # 控制selectivity阈值
    # thresholds=[0.1*i for i in range(11)]
    # for tid,_ in enumerate(thresholds):
    #     # if tid!=4:continue
    #     if tid==len(thresholds)-1:break
    #     sel_range=[thresholds[tid],thresholds[tid+1]]
    #     gen_ques_by_gaussian(Conf.WORDTYPE['synthetic']['test'], 400, 3000, 0.4, 5,f'queries/vary_selectivity/test_{tid + 1}.csv',sel_range)
