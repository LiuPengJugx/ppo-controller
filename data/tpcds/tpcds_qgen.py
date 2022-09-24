import pandas as pd
import numpy as np
import random
def gen_ques_by_qgen(tpl_path,total_time,query_num):
    query_templates=pd.read_csv('template/'+tpl_path,header=None)
    data=[]
    for i in range(query_num):
        # query_templates.iloc[0]
        new_query=np.copy(query_templates.iloc[[np.random.randint(0,len(query_templates))-1]])
        new_query[0][3]=round(0.4*random.random(),3)
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
    pd.DataFrame(data).to_csv('queries/'+tpl_path,index=False,header=False)


# 该工具只对负载特征较丰富、数量较多的的标准测试有用
# eg.tpch- lineitem
# eg.tpcds- catalog_sales store_sales web_sales
if __name__ == '__main__':
    # gen_ques_by_qgen('catalog_sales.csv',400,2000)
    # gen_ques_by_qgen('store_sales.csv',400,1000)
    gen_ques_by_qgen('web_sales.csv',400,1000)
