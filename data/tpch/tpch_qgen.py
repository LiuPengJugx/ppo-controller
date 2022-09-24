import pandas as pd
import numpy as np
import random
from db.conf import Conf
from data.workload_generator_tpc import generate_random_query
def gen_ques_by_qgen(tpl_path,total_time,query_num,save_path):
    query_templates=pd.read_csv('template/'+tpl_path,header=None)
    data=[]
    for i in range(query_num):
        # query_templates.iloc[0]
        new_query=np.copy(query_templates.iloc[[np.random.randint(0,len(query_templates))-1]])
        new_query[0][3]=round(0.8*random.random(),3)
        # produce freq
        new_query[0][1]=random.randint(1,25)
        data.append(new_query[0].tolist())
    data=np.array(data)
    # 泊松分布：为查询分配到达时间
    phase = 10  #每次分配20s
    steps = int(total_time / (2 * phase))
    queries_per_step=int(query_num / steps)
    poisson_time = np.array([])
    base_index=0  #起始时间
    unallocated_query_num=query_num
    for i in range(steps):
        item_size = unallocated_query_num if i == steps - 1 else queries_per_step
        poisson_item = np.random.poisson(lam=phase, size=item_size) + base_index
        poisson_time = np.concatenate([poisson_time, poisson_item])
        base_index+=2*phase
        unallocated_query_num-=queries_per_step
    poisson_time = np.array(sorted(poisson_time.astype(int)))
    data=np.concatenate([data,poisson_time.reshape(query_num,1)],axis=1)
    pd.DataFrame(data).to_csv(save_path,index=False,header=False)


def gen_ques_by_gaussian(tpl_path,attrs_length,total_time,query_num,maximum_sigma_percentage,cut_num):
    # maximum_sigma_percentage=0.5
    querys=generate_random_query(len(attrs_length),total_time,query_num,maximum_sigma_percentage,cut_num)
    pd.DataFrame(querys).to_csv('queries/' + tpl_path, index=False, header=False)

# 该工具只对负载特征较丰富、数量较多的的标准测试有用
# eg.tpch- lineitem
# eg.tpcds-
if __name__ == '__main__':
    # gen_ques_by_qgen('lineitem.csv',400,2000,'queries/lineitem.csv')
    # gen_ques_by_gaussian('orders.csv',Conf.WORDTYPE['tpch']['orders'],80,400,0.5,2)
    gen_ques_by_gaussian('supplier.csv',Conf.WORDTYPE['tpch']['supplier'],50,400,0.6,1)

    # 控制查询速率
    # T=200
    # avg_volume=[x for x in range(1,9)]
    # for vol in avg_volume:
    #     que_num=T*vol
    #     gen_ques_by_qgen('lineitem.csv', T, que_num,f'queries/vary_que_vol2/lineitem_{vol}.csv')

    # 控制负载尺寸，保证速率不变
    # vol=3
    # T_list=[100*x for x in range(1,9)]
    # for idx,T in enumerate(T_list):
    #     que_num=T*vol
    #     # produce dataset for lineitem/orders table.
    #     # gen_ques_by_qgen('lineitem.csv', T, que_num,f'queries/vary_que_size/lineitem_{idx+1}.csv')
    #     gen_ques_by_qgen('orders_1.csv', T, que_num,f'queries/vary_que_size/orders_{idx+1}.csv')

