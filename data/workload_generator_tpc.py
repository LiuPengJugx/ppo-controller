# two types of workload distribution
# a uniform distribution with 30, 000 distinct transactions 
# a Zipf distribution with 23, 457 distinct transactions (parameter s=1.16 , obey the 8-2 rule.)
# Poisson distribution =>how many transactions are submitted to the system during each interval
# vary the percentage of tuples α we need to repartition, which varies from 100% to 20%.

import random
import math
import pandas as pd
from pandas.core.frame import DataFrame
import numpy as np
import os

# def generate_random_query(attr_num_complete,total_time,query_num,maximum_sigma_percentage,cut_num,sel_range):
def generate_random_query(attr_num_complete,total_time,query_num,maximum_sigma_percentage,cut_num):
    # choose access attributes
    # 每个查询所有属性的方差波动范围都是一样的
    # 将属性范围随机切分成5份,随机选中某一份   [[0,10],[20,40],[5,35],[40,50],[30,49]]
    # cut_num=5
    attr_split_list=[]
    min_length=round(attr_num_complete/cut_num)
    start_list=[random.randint(i*cut_num,(i+1)*cut_num-1) for i in range(min_length)]
    # start_list = [random.randint(i * min_length, (i + 1) * min_length - 1) for i in range(cut_num)]
    while(len(attr_split_list)<=cut_num):
        # 随机确定长度
        split_length = random.randint(min_length, 2 * min_length)
        # split_length = random.randint(2, min_length)

        # 随机确定起始属性
        # start_index = start_list[random.randint(0,min_length-1)]
        start_index = start_list[random.randint(0,cut_num)]
        end_index=start_index+split_length-1
        # if end_index<attr_num_complete and [start_index,end_index] not in attr_split_list:
        #     attr_split_list.append([start_index,end_index])
        # elif [start_index,attr_num_complete-1] not in attr_split_list:
        #     attr_split_list.append([start_index, attr_num_complete-1])
        if end_index<attr_num_complete:
            attr_split_list.append([start_index,end_index])

    querys=[]
    is_generate_perform=0
    access_attr_temp_list=[list() for _ in range(len(attr_split_list))]
    uniform_num=int(query_num)
    cnt=0
    while cnt<uniform_num:
        access_attr = list()
        range_integer = random.randint(0, len(attr_split_list) - 1)
        # 0~99
        range_lower, range_upper = attr_split_list[range_integer][0], attr_split_list[range_integer][1]
        # 分成三个点
        point_list=[range_lower+round(range_upper-range_lower)*th/4 for th in range(1,4)]
        selected_point = point_list[random.randint(0,2)]
        # 控制sql访问属性的数量
        access_attr_sum = random.randint(1, range_upper-range_lower+1)
        if access_attr_sum>6:access_attr_sum=6  #访问属性数量不超过6个
        for i in range(range_lower, range_upper + 1):
            sigma = random.uniform(0, (range_upper - selected_point) * maximum_sigma_percentage)
            attr_value = math.ceil(random.gauss(selected_point, sigma))
            if attr_value > range_upper:
                attr_value = range_upper
            elif attr_value < range_lower:
                attr_value = range_lower
            if attr_value in access_attr:
                continue
            else:
                access_attr.append(attr_value)
            if len(access_attr) == access_attr_sum: break
        rep_times=random.randint(1,1)
        if cnt+rep_times>uniform_num: rep_times=uniform_num-cnt
        [access_attr_temp_list[range_integer].append(access_attr) for _ in range(rep_times)]
        cnt+=rep_times
    access_attr_list=list()
    for item in access_attr_temp_list:access_attr_list+=item
    phase=10
    steps=int(total_time / (2 * phase))
    poisson_data=np.array([])
    base_index=0
    query_num_rest=query_num
    for i in range(steps):
        item_size=query_num_rest if i==steps-1 else int(query_num/steps)
        poisson_item=np.random.poisson(lam=phase, size=item_size)+base_index
        poisson_data=np.concatenate([poisson_data,poisson_item])
        base_index+=2*phase
        query_num_rest-=int(query_num/steps)
    poisson_data=poisson_data.astype(int)
    poisson_data=sorted(poisson_data)
    # 为access_attr_list 生成其他的特征
    for iter,access_attr in enumerate(access_attr_list):
        # choose frequency
        if is_generate_perform<=5:
            freq=random.randint(round(query_num/10),round(query_num/8))
            is_generate_perform+=1
        else:
            # 干扰query ：1~20之间的整数
            freq=random.randint(1,20)

        # choose access keys
        # access_attr范围内之间的a个整数,其中0<=a<=2
        scan_key_num=min(random.randint(0,2),len(access_attr))
        scan_attr=[]
        for i in random.sample(access_attr,scan_key_num):
            scan_attr.append(str(i))
        scan_attr=",".join(scan_attr)

        # choose selectivity
        selectivity=round(0.2*random.random(),3)
        # selectivity=round(sel_range[0]+random.random()*(sel_range[1]-sel_range[0]),3)
        time=poisson_data[iter]
        attr_list_str = [str(attr) for attr in access_attr]
        querys.append([",".join(attr_list_str), freq, scan_attr, selectivity, time])
    return querys


