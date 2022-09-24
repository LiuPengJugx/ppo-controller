from db.workload import Workload
from db.conf import Conf
workload_dict = {
        # 'tpch':['lineitem','orders','supplier'],
        # 'tpcds':['catalog_sales','store_sales','web_sales'],
        'synthetic':['test_'+str(x) for x in range(1,9)]
    }
cul_queries_per_sec=[]
for path in workload_dict.keys():
    for table in workload_dict[path]:
        # wLoad=Workload(Conf.WORDTYPE[path][table], f'{path}/template/{table}.csv')
        wLoad=Workload(Conf.WORDTYPE[path]['test'], f'{path}/queries/vary_que_vol/{table}.csv')
        time_units=wLoad.sql_list[-1]['time']
        total_freq=0
        total_query_type=0
        # print(time_units)
        total_que_num=0
        # for time in range(wLoad.sql_list[0]['time'],time_units+1):
        #     if len(wLoad.load_sql_by_time_range(time,time+1))==0:continue
        #     for sql in wLoad.load_sql_by_time_range(time,time+1):
        #         total_que_num+=sql.frequency
        #     # wLoad.load_sql_by_time_range(0, time + 1)
        #     cul_queries_per_sec.append(total_que_num)
        for sql in wLoad.sql_list:
            total_query_type+=1
            total_freq += sql['feature'].frequency
        # print(f'{table}:time:{time_units}, types:{total_query_type}, queries:{total_freq}')
        print(total_freq)
        # print(len(cul_queries_per_sec))
        # print(cul_queries_per_sec)
        # que_size
        # 3056
        # 6643
        # 10112
        # 13114
        # 16337
        # 20010
        # 23339
        # 26491