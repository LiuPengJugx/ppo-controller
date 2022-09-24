import math
from partitioner.pid import PID
from db.disk_io import DiskIo
import numpy as np
from baselines.algo_tpl import AlgorithmTemplate
from scipy import optimize
from sympy import *
from autograd import grad

class Feedback(AlgorithmTemplate):

    def ziegler_nichols(self):
        # G(x)=Ke^(-tx)/(Tx+1) #Where k is the scale coefficient; T is the inertial time constant; τ Is a pure delay time constant
        K, T, t = 2, 30, 10
        t=np.arange(0,300,0.02)
        def fun(x):
            y = K * (math.e ** (-t * x)) / (T * x + 1)
            return y
        def my_grad():
            x=symbols('x')
            y=K*x/(T*x+1)
            return diff(y,x)
        fun_grad=my_grad()
        def fun2(x):
            y = -K / (x**2+0.4 * x + 1)
            return y
        fun_grad2=grad(fun2)

        # print(fun_grad.evalf(subs={'x':3}))
        # step(fun)
        # t1,c1=step2(system=lti([K],[T,1]),T=t)
        # plt.plot(t,[fun_grad2(x) for x in t],'r',label='s1 Step Response',linewidth=0.5)
        # plt.show()
        # maximum=optimize.fminbound(lambda x:-fun_grad.evalf(subs={'x':x}),0,300)
        maxpoint=optimize.fminbound(lambda x:-fun_grad2(x),0,300) #Horizontal coordinate of the tangent point
        maxy=fun2(maxpoint)# Vertical coordinate of the tangent point
        maxr=fun_grad2(maxpoint) # slope
        # Intersection of tangent line and y-axis (i.e. constant term)
        tangent_b=maxy-maxr*maxpoint
        # Intersection of tangent line and x-axis
        tt=(0-tangent_b)/maxr
        TT=maxpoint-tt
        # update the key parameters of PID
        kp=1.2*TT/tt
        ki=2*tt
        kd=0.5*tt
        return kp,ki,kd

    def repartition(self, initial_par, wLoad, **kwargs):
        # SP:the desired output value / PV:the actual measured value
        # repartition_threshold=-30
        repartition_threshold=0
        isFirst = True
        start_time=wLoad.sql_list[0]['time']
        collector = {'content':[],
                     'start':start_time}
        pid = PID(1, 0.001, 0)
        # pid = PID(1, 0, 0)
        # pid.SetPoint=SP  #Evaluate the execution cost (per query).
        pid.setSampleTime(0)
        pid.setLastTime(start_time)
        cur_par_schema = initial_par
        self.action_list =dict()
        total_blocks=[]
        total_rep_blocks = 0
        total_sql_num=0
        total_actions = 0
        true_actions = 0
        last_time=0
        cost_time_map={"cost":list(),"cdf":list()}
        for cur_time in range(wLoad.sql_list[0]['time'],wLoad.sql_list[-1]['time']+1):
        # for sql in wLoad.sql_list:
            collector['content'] += wLoad.load_sql_by_time_range(cur_time,cur_time+1)
            PV=(DiskIo.compute_cost(collector['content'], cur_par_schema, wLoad.attrs_length)+sum(total_blocks))\
               /((total_sql_num+sum([item.frequency for item in collector['content']])))
            if pid.SetPoint==0:
                pid.SetPoint = PV-10
            pid.update(PV,cur_time)
            print('PV:', PV, '  output:', pid.output)
            if pid.output>=100:
                pid.SetPoint = PV - 10
            if pid.output>=5:
                pid.SetPoint-=10
            """
            Heuristic parameter adjustment method: if the error of PID is always lower than the threshold, and the adjustment effect is not good in the last 10 times, and the output is always maintained near a certain value, it indicates that the environment has reached a stable state and is not suitable for adjustment. 
            The threshold is too high. Therefore, it is necessary to reset the threshold to output mean value - 5. PID stops adjustment. With the change of environment, the current state is not suitable, The output value decreases below the threshold. At this time, the PID needs to be readjusted, so the threshold can be updated to the average value of output + 10.
            """
            # if len(latest_output_set) >= 10:
            #     latest_output_set.pop(0)
            # latest_output_set.append(pid.output)
            # print('Standard deviation:', np.std(latest_output_set, ddof=1))

            # if len(latest_output_set) >= 10 and np.std(latest_output_set, ddof=1) < 0.5 and is_add:
            #     repartition_threshold = np.mean(latest_output_set) - 5
            #     latest_output_set.clear()
            #     is_add=False
            if pid.output<=repartition_threshold or isFirst:
                isFirst=False
                # if len(latest_output_set) >= 10 and np.std(latest_output_set, ddof=1) < 0.5 and not is_add:
                #     repartition_threshold = np.mean(latest_output_set) + 10
                #     latest_output_set.clear()
                #     is_add = True

                min_schema, cost_increment = self.partition(collector['content'], wLoad, cur_par_schema)
                # temp_cur_par_schema = cur_par_schema.copy()
                # if len(temp_cur_par_schema) == 1 and len(temp_cur_par_schema[0]) == 50:
                #     temp_cur_par_schema = [[num] for num in range(50)]
                # for par in temp_cur_par_schema:
                #     temp_par = par.copy()
                #     for par_new in min_schema:
                #         if Util.list_solved_list(par_new, temp_par):
                #             [temp_par.remove(attr) for attr in par_new if attr in temp_par]
                #     if temp_par: min_schema.append(temp_par)
                operator_cost = DiskIo.compute_repartitioning_cost(cur_par_schema, min_schema, wLoad.attrs_length)
                total_actions+=1
                multiple_factor=1 # tune for Syntic test dataset
                # multiple_factor=5 # tune for TPCH test dataset
                # multiple_factor=5 # tune for TPC-DS test dataset
                if min_schema!=cur_par_schema and cost_increment>multiple_factor*operator_cost:
                    true_actions+=1
                    self.action_list[cur_time]=min_schema
                    cost_blocks=DiskIo.compute_cost(collector['content'], cur_par_schema, wLoad.attrs_length)
                    total_blocks.append(cost_blocks)
                    cost_time_map['cost'].append(f"({last_time+1} {cur_time})->{cost_blocks}")
                    cost_time_map['cdf'].append(f"{cur_time}->{sum(total_blocks)}")
                    last_time=cur_time
                    total_rep_blocks +=operator_cost
                    total_sql_num+=sum([item.frequency for item in collector['content']])
                    print("Time:",cur_time,", the workload cost in the interval with the previous repartition point is:",cost_blocks,", update the partition scheme as:",min_schema)
                    cur_par_schema=min_schema
                    collector['content']=[]
        if len(collector['content']) > 0:
            total_blocks.append(DiskIo.compute_cost(collector['content'], cur_par_schema, wLoad.attrs_length))
        self.action_ratio = [true_actions, round(true_actions / total_actions, 3)]
        total_freq=(sum([sql['feature'].frequency for sql in wLoad.sql_list]))
        return sum(total_blocks)/total_freq , total_rep_blocks/total_freq