from .resultset import Resultset
from .par_management import ParManagement as PM
from util import Util
from db.disk_io import DiskIo
import time
"""
Transaction API Class: deploy new partitions and replace old partitions on postgresql
"""
class Transaction:
    def __init__(self,queries,jta,time_point,benchmark):
        self.queries=queries
        self.jta=jta
        self.time_point=time_point
        self.benchmark=benchmark

    def repartition(self,partitions)->Resultset:
        tb_name=PM.test_tables[self.benchmark]['name']
        create_tb_sql ,insert_tb_sql,drop_tb_sql= "","",""
        structured_partitions = Util.partition_ordering(partitions)
        pre_allow_no=[]
        for tb_no in PM.cur_partitions.keys():
            if PM.cur_partitions[tb_no] in structured_partitions:
                structured_partitions.remove(PM.cur_partitions[tb_no])
            else:
                pre_allow_no.append(tb_no)
        if len(structured_partitions)>len(pre_allow_no):
            step_length=len(structured_partitions)-len(pre_allow_no)
            cur_par_keys=sorted(PM.cur_partitions.keys())
            if cur_par_keys:
                counter=1
                for i in cur_par_keys:
                    while i!=counter:
                        if step_length>0:
                            pre_allow_no.append(counter)
                            step_length-=1
                        else: break
                        counter += 1
                    counter+=1
            if step_length>0:
                if cur_par_keys: start_no = cur_par_keys[-1] + 1
                else: start_no = 1
                [pre_allow_no.append(i) for i in range(start_no,start_no+step_length)]
        new_tab_list=[]
        for index in pre_allow_no:
            sub_tab_name = tb_name + "sub" + str(index)
            # delete replaced raw sub-table
            if index in PM.cur_partitions.keys():
                drop_tb_sql += "DROP TABLE %s;\n" % (sub_tab_name)
                PM.cur_partitions.pop(index)
            if(len(structured_partitions)>0):
                new_tab_list.append(sub_tab_name)
                partition=structured_partitions.pop(0)
                create_tb_sql+="DROP TABLE IF EXISTS %s;\n"%(sub_tab_name)
                create_tb_sql += "CREATE TABLE %s ( %s %s" % (
                    sub_tab_name, PM.test_tables[self.benchmark]['attrs'][0], PM.test_tables[self.benchmark]['types'][0])
                # No more duplicate primary keys for each sub-table
                # create_tb_sql += "CREATE TABLE %s ( " % (sub_tab_name)
                for idx, attr_id in enumerate(partition):
                    if attr_id == 0:
                        continue
                    create_tb_sql += ",\n%s %s" % (
                        PM.test_tables[self.benchmark]['attrs'][attr_id], PM.test_tables[self.benchmark]['types'][attr_id])
                create_tb_sql += ");\n"
                # Insert data statement
                if partition.count(0) == 0:
                    tmp_par = [0]+partition
                else: tmp_par = partition
                attr_list = ",".join([PM.test_tables[self.benchmark]["attrs"][x] for x in tmp_par])
                # attr_list = ",".join([PM.test_tables[self.benchmark]["attrs"][x] for x in partition])
                insert_tb_sql += "INSERT INTO %s (SELECT %s from %s);\n" % (sub_tab_name, attr_list, tb_name)
                # Update partition dicts.
                PM.cur_partitions[index] = partition
        result = Resultset()
        result.startTime = time.time()
        # If the sub-table exists, delete the sut-table and recreate it
        for line in drop_tb_sql.split("\n")[:-1]:
            self.jta.query(line)
        self.jta.commit()
        # create table
        for line in create_tb_sql.split(";\n")[:-1]:
            self.jta.query(line + ";")
        # insert data
        for line in insert_tb_sql.split("\n")[:-1]:
            self.jta.query(line)
        self.jta.commit()
        result.finishTime = time.time()
        result.succeed = True
        print(f"Time：{self.time_point} , the number of updated partitions:{len(pre_allow_no)}")
        print(sorted(PM.cur_partitions.values()))
        # To prevent the first access to the newly generated table from affecting the query speed, scan the whole table beforehand
        for sub_tab_name in new_tab_list:
            prepared_query="SELECT * FROM %s;"%(sub_tab_name)
            self.jta.query(prepared_query)
        return result

    def call(self)->Resultset:
        cardinality = DiskIo.cardinality
        tb_name=PM.test_tables[self.benchmark]['name']
        converted_query=""
        query_weight=[]
        result = Resultset()
        for sql_dict in self.queries:
            result.txn_count+=sql_dict.frequency
            # Splitting SQL statements based on partition results
            attr_indxs = [attr_idx for attr_idx, attr_val in enumerate(sql_dict.attributes) if attr_val == 1]
            for idx in PM.cur_partitions.keys():
                partition=PM.cur_partitions[idx]
                if Util.list_solved_list(attr_indxs, partition):
                    sub_tb_name = PM.test_tables[self.benchmark]['name'] + "sub" + str(idx)
                    # attr_list2=[attr for attr in attr_indxs if attr in partition]
                    attr_list=partition
                    attr_list_str = ",".join([PM.test_tables[self.benchmark]["attrs"][attr] for attr in attr_list])
                    if not Util.list_solved_list(sql_dict.scan_key,attr_list):
                        # converted_query += ("SELECT %s FROM %s;\n" % (attr_list_str, sub_tb_name))
                        converted_query += ("SELECT %s FROM %s LIMIT %d;\n" % (attr_list_str, sub_tb_name, cardinality*sql_dict.selectivity))
                        converted_query += ("SELECT %s FROM %s;\n" % (PM.test_tables[self.benchmark]["attrs"][0], sub_tb_name))
                        query_weight.append(sql_dict.frequency)
                    else:
                        cur_scan_key=[attr for attr in attr_list if attr in sql_dict.scan_key]
                        # converted_query += ("SELECT %s FROM %s LIMIT %d;\n" % (
                        #     attr_list, tb_name, cardinality * sql_dict.selectivity))
                        predicate_conds = " and ".join(['a' + str(i) + "<>'1'" for i in cur_scan_key])
                        converted_query += ("SELECT %s FROM %s WHERE %s;\n" % (attr_list_str, sub_tb_name, predicate_conds))
                    query_weight.append(sql_dict.frequency)

            if len(PM.cur_partitions.keys())==0:
                # attr_list=",".join(['a'+str(i) for i in attr_indxs])
                if not sql_dict.scan_key:
                    # converted_query += ("SELECT %s FROM %s;\n" % (attr_list,tb_name))
                    converted_query += ("SELECT * FROM %s;\n" % (tb_name))
                else:
                    # converted_query += ("SELECT %s FROM %s LIMIT %d;\n" % (
                    #     attr_list, tb_name, cardinality * sql_dict.selectivity))
                    predicate_conds=" and ".join(['a' + str(i)+"<>'1'" for i in sql_dict.scan_key])
                    # converted_query += ("SELECT %s FROM %s WHERE %s;\n" % (attr_list, tb_name, predicate_conds))
                    converted_query += ("SELECT * FROM %s WHERE %s;\n" % (tb_name, predicate_conds))
                query_weight.append(sql_dict.frequency)
        result.startTime = time.time()
        assert len(query_weight)==len(converted_query.split(";\n")[:-1])
        # Execute the converted statement
        for idx,line in enumerate(converted_query.split(";\n")[:-1]):
            init_time=time.time()
            # To avoid randomness, the query is run 3 times and the average is taken
            [self.jta.query(line + ";") for _ in range(3)]
            result.costTime+=(time.time()-init_time)*query_weight[idx]/3
        result.succeed=True
        return result