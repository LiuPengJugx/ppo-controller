from environment.env_v5 import Env5
from baselines.algo_tpl import AlgorithmTemplate
from stable_baselines3 import PPO
import time
class PpoController(AlgorithmTemplate):
    def repartition(self,initial_par, wLoad, **kwargs):
        env = Env5(wLoad)
        env.reward_threshold = 0.1
        self.load_time=0
        time0=time.time()
        model = PPO.load("stable_pretrained_model/ppo_controller_v4_2800_best",device='cuda:4')
        self.load_time+=time.time()-time0
        obs = env.reset()
        epoch = 0
        total_reward = []
        # 记录奖励为正的比例
        total_actions=0
        good_actions=0
        actual_actions=0
        reward_list=[]
        result=dict()
        for i in range(5000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            reward_list.append(reward)
            if reward!=0:
                total_actions+=1
                if reward+env.reward_threshold*3/5>0:good_actions+=1
                if reward>0:actual_actions+=1
            total_reward.append(reward)
            if done:
                result = {'reward': sum(total_reward),
                          'avg_cost': sum(env.io_cost) / sum([sql['feature'].frequency for sql in env.w.sql_list]),
                          'action_ratio':[actual_actions,round(actual_actions/total_actions,3)],
                          'rep_cost':sum(env.rep_cost)/sum([sql['feature'].frequency for sql in env.w.sql_list])}
                          # 'optimize_time':env.optimize_time}
                self.action_list = env.action_list
                epoch += 1
                if epoch == 1: break
        env.close()
        self.action_ratio=result['action_ratio']
        # self.scvp_time+=env.scvp_time
        print(f"cluster_time:{env.cluster_time}")
        # print(f"partition_update_time:{env.partition_update_time}")
        # print(f"reward_compute_time:{env.reward_compute_time}")
        # print(f"judge_next_time:{env.judge_next_time}")
        return result['avg_cost'],result['rep_cost']