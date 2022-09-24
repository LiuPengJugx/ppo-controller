from db.conf import Conf
class ParManagement:
    # test_tables = {
    #     'name':"tt_tab",
    #     'attrs': ["a" + str(i) for i in range(50)],
    #     'types': ["SERIAL"]+["CHAR(4)" for _ in range(49)]
    # }

    test_tables = {
        'synthetic':{
            'name': "tt_tab",
            'attrs': ["a" + str(i) for i in range(50)],
            'types': ["SERIAL"] + ["CHAR(4)" for _ in range(49)]
        },
        'lineitem':{
            'name': "lineitem",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpch']['lineitem']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpch']['lineitem'][1:]]
        },
        'orders':{
            'name': "orders",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpch']['orders']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpch']['orders'][1:]]
        },
        'supplier':{
            'name': "supplier",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpch']['supplier']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpch']['supplier'][1:]]
        }
        ,
        'catalog_sales': {
            'name': "catalog_sales",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['catalog_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['catalog_sales'][1:]]
        },
        'store_sales': {
            'name': "store_sales",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },
        'web_sales': {
            'name': "web_sales",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['web_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['web_sales'][1:]]
        },
        'store_sales0': {
            'name': "store_sales0",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },
        'store_sales1': {
            'name': "store_sales1",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },
        'store_sales2': {
            'name': "store_sales2",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },
        'store_sales3': {
            'name': "store_sales3",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },'store_sales4': {
            'name': "store_sales4",
            'attrs': ["a" + str(i) for i in range(len(Conf.WORDTYPE['tpcds']['store_sales']))],
            'types': ["SERIAL"] + [f"CHAR({width})" for width in Conf.WORDTYPE['tpcds']['store_sales'][1:]]
        },

    }
    # cur_partitions=[[i+1 for i in range(50)]]
    cur_partitions=dict()