"""
Profile Class: table | workload | db parameters
"""
class Conf:
    TIME_LINE=10**8
    CARDINALITY=1000000
    PAGE_SIZE=5000
    # TABLE_ATTRIBUTE_NUM=50
    WORDTYPE={
        'tpch': {
            'customer': [4, 25, 40, 4, 15, 4, 10, 117],
            'lineitem': [4, 8, 8, 4, 15, 15, 15, 15, 1, 1, 10, 10, 10, 25, 10, 44],
            'nation': [4, 25, 4, 152],
            'orders': [4, 4, 1, 4, 10, 15, 15, 4, 79],
            'part': [4, 55, 25, 10, 25, 4, 10, 4, 23],
            'partsupp': [4, 4, 4, 4, 199],
            'region': [4, 25, 152],
            'supplier': [4, 25, 40, 4, 15, 4, 101]
        },
        'tpcds': {
            'catalog_sales': [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales0': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales1': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales2': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales3': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'store_sales4': [4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7],
            'web_sales': [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
        },
        'synthetic':{
            'test':[4 for _ in range(50)]
        }

    }
