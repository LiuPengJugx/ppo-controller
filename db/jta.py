import random

from db.pg import Pg
from db.par_management import ParManagement as PM
from db.conf import Conf
class JTA:
    def __init__(self):
        self.conn=Pg().get_conn()
        self.cur = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def cancel(self):
        self.conn.cancel()

    def query(self, sql):
        self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()

# create table data
if __name__=='__main__':
    # table_dict=[('tpch','lineitem'),('tpch','orders'),('tpch','supplier'),('tpcds','catalog_sales'),('tpcds','store_sales'),('tpcds','web_sales'),]
    table_dict=[('tpcds','store_sales')]
    for cid,cardinality in enumerate([1e5,2e5,4e5,6e5,8e5]):
        for item in table_dict:
            jta=JTA()
            benchmark=item[1]
            directory=item[0]
            TABLE_INFO=PM.test_tables[benchmark+str(cid)]
            attrs=TABLE_INFO['attrs']
            attrs_length_arr=Conf.WORDTYPE[directory][benchmark]
            create_statement=f"DROP TABLE IF EXISTS {TABLE_INFO['name']};\nCREATE TABLE {TABLE_INFO['name']} ({attrs[0]} {TABLE_INFO['types'][0]} PRIMARY KEY"
            for idx in range(1,len(attrs)):
                create_statement+=f",\n{attrs[idx]} {TABLE_INFO['types'][idx]} NOT NULL"
            create_statement += ");\n"
            print(create_statement)
            jta.query(create_statement)
            jta.commit()
            # cardinality = 100000
            for cnt in range(1,int(cardinality)+1):
                # insert_statement=f"INSERT INTO {TABLE_INFO['name']}({','.join([attrs[i] for i in range(1,len(attrs))])}) VALUES ({','.join([str(random.randint(1000,9999)) for _ in range(len(attrs)-1)])})"
                insert_statement=f"INSERT INTO {TABLE_INFO['name']}({','.join([attrs[i] for i in range(1,len(attrs))])}) VALUES ({','.join([str(random.randint(0,9))*attrs_length_arr[ith+1] for ith in range(len(attrs)-1)])})"
                jta.query(insert_statement)
            jta.commit()
            jta.close()