import matplotlib.pyplot as plt
from db.workload import Workload
from db.conf import Conf
plt.rcParams['figure.figsize']=(12.0,8.0)
def show_workload_flow(wLoad:Workload):
    # time_list=[time for time in  range(wLoad.sql_list[0]['time'],wLoad.sql_list[-1]['time'])]
    start_time=0
    # end_time=wLoad.sql_list[-1]['time']
    end_time=20
    last_time=0
    cnt=0
    # plt.subplot(i,j,k)
    for sql in wLoad.sql_list:
        cur_time=sql['time']
        if start_time <= cur_time <= end_time:
            query=sql['feature']
            if cur_time!=last_time:
                last_time=cur_time
                cnt=0
            else:
                cnt+=0.1
                cnt+=0
            solved_attrs = [i for i, x in enumerate(query.attributes) if x == 1]
            plt.plot([cur_time*1+cnt]*len(solved_attrs),solved_attrs,'-o',linewidth='0.12')
    plt.show()
    # save synthetic datasets
    # plt.savefig(f'{len(wLoad.sql_list)}/{start_time}-{end_time}.svg',bbox_inches='tight',pad_inches=0)

    # save tpc benchmark
    # plt.savefig(f'{len(wLoad.sql_list)}/{start_time}-{end_time}.svg',bbox_inches='tight',pad_inches=0)



if __name__=='__main__':
    workload_dict = {
        # 'tpch':['lineitem','orders','supplier'],
        # 'tpcds':['catalog_sales','store_sales','web_sales'],
        'tpch':['lineitem'],
        'tpcds':['catalog_sales'],
    }
    # b=sum([len(workload_dict[key]) for key in workload_dict.keys()])
    for path in workload_dict.keys():
        for table in workload_dict[path]:
            wLoad = Workload(Conf.WORDTYPE[path][table], f'../data/{path}/queries/{table}.csv')
            show_workload_flow(wLoad)
    # for query_num in [1600]:
    #     wLoad=Workload(Conf.WORDTYPE['synthetic']['test'],f'../data/data3/{query_num}query-steam.csv')
    #     show_workload_flow(wLoad)

    # plt.show()