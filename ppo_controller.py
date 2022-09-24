import torch
from stable_baselines3 import PPO
import numpy as np
from db.workload import Workload
from environment.env_v5 import Env5
import multiprocessing as mul
from partitioner.MyThread import MyThread
from db.conf import Conf
class PpoController:
    action_list=dict()

    @staticmethod
    def train_ppo_model(env,reward_threshold,saved_model_path,queue):
        env.reward_threshold = reward_threshold
        # model = PPO("MlpPolicy", env, verbose=1,device='cuda:4',tensorboard_log="./ppo_controller_tensorboard_env2/env4/")
        # # Run Command: tensorboard --logdir ./ppo_controller_tensorboard_env2/env4/  --bind
        # model.learn(total_timesteps=2e5)
        # model.save(saved_model_path)
        # del model
        results = dict()
        model = PPO.load(saved_model_path,device='cuda:4')
        obs = env.reset()
        epoch = 0
        total_reward = []
        # 记录奖励为正的比例
        total_actions = 0
        good_actions = 0
        reward_list = []
        for i in range(5000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            reward_list.append(reward)
            if reward != 0: total_actions += 1
            if reward > 0: good_actions += 1
            total_reward.append(reward)
            if done:
                result = {
                          'reward': sum(total_reward),
                          'avg_cost': sum(env.io_cost) / sum([sql['feature'].frequency for sql in env.w.sql_list]),
                          'action_ratio': [len(env.action_list.keys()), round(good_actions / total_actions, 3)],
                          'rep_cost': sum(env.rep_cost) / sum([sql['feature'].frequency for sql in env.w.sql_list])}
                results[reward_threshold]=result
                print(f"The total reward : {result['reward']}")
                print(env.cost_time_map['cost'])
                print(env.cost_time_map['cdf'])
                print('action list : ', env.action_list.keys())
                print(f"Average query cost: {result['avg_cost']}")
                print(f"Average repartition cost: {result['rep_cost']}")
                print(reward_list)
                epoch += 1
                obs = env.reset()
                if epoch == 1: break
        print(results)
        env.close()
        queue.put(results)

    @staticmethod
    def train_model_diff_reward_threshold(wLoad):
        reward_threshold_list=np.linspace(0.05,0.2,7)
        queue = mul.Queue()
        jobs = []
        # torch.multiprocessing.set_start_method('spawn')
        # ctx = mul.get_context("spawn")
        chunk_result=list()
        for reward_threshold in reward_threshold_list:
            reward_threshold=round(reward_threshold,3)
            env = Env5(wLoad)
            process = mul.Process(target=PpoController.train_ppo_model, args=(env,reward_threshold,"stable_pretrained_model/ppo_controller_v4_2800_"+str(reward_threshold),queue))
            process.start()
            jobs.append(process)
        for idx,_ in enumerate(jobs):
            chunk_result.append(queue.get())
        # for process in jobs: process.join()
        print(chunk_result)
    # ENV-MASK 5e4
    # {0: [{'reward': 19.3995236345659, 'avg_cost': 352.90716189553115}],   0.05
    #  1: [{'reward': 20.14576704070486, 'avg_cost': 357.55844785212366}],
    #  2: [{'reward': 16.243991450266673, 'avg_cost': 356.3261102841912}],
    #  3: [{'reward': 17.375958753271036, 'avg_cost': 367.72155491709646}],
    #  4: [{'reward': 12.902817836046264, 'avg_cost': 366.117380317768}],
    #  5: [{'reward': 15.955132572416616, 'avg_cost': 369.739554847866}],
    #  6: [{'reward': 16.710481931576798, 'avg_cost': 379.1565647824431}],
    #  7: [{'reward': 19.78887987204151, 'avg_cost': 374.60074768943196}]}

    # ENV-MASK 7e4
    # {0.05: [{'reward': 23.14980539662517, 'avg_cost': 357.5984976980858}],
    #  0.07500000000000001: [{'reward': 21.98387226196716, 'avg_cost': 357.0407767662432}],
    #  0.1: [{'reward': 18.670401458223147, 'avg_cost': 359.28249506732664}],
    #  0.125: [{'reward': 17.292929704634687, 'avg_cost': 353.7374087022742}],
    #  0.15000000000000002: [{'reward': 16.058873474634538, 'avg_cost': 349.06383052372877}],
    #  0.17500000000000004: [{'reward': 15.10050512230219, 'avg_cost': 358.08522274914327}],
    #  0.2: [{'reward': 16.367051455992307, 'avg_cost': 355.10716881858144}]}

    # 1300
    # {0.05: [{'reward': 17.203203206088713, 'avg_cost': 424.1025513467415}],
    #  0.07500000000000001: [{'reward': 4.303690942785271, 'avg_cost': 424.34432520787436}],
    #  0.1: [{'reward': 1.0860642793946864, 'avg_cost': 421.8261672944354}],
    #  0.125: [{'reward': -2.472714895188576, 'avg_cost': 423.4357188543814}],
    #  0.15000000000000002: [{'reward': 7.603659372300443, 'avg_cost': 418.071849904058}],
    #  0.17500000000000004: [{'reward': -4.390639229559201, 'avg_cost': 426.2825669817355}],
    #  0.2: [{'reward': 10.763970635840122, 'avg_cost': 429.0972923033189}]}

    # ENV-MASK-CURVE
    # {0.05: [{'reward': 24.380812571998987, 'avg_cost': 356.7552355567863}],
    #  0.1: [{'reward': 22.791591658146565, 'avg_cost': 352.6265706670359}],  0.1
    #  0.15: [{'reward': 20.17534079661996, 'avg_cost': 355.7318010315345}],
    #  0.2: [{'reward': 16.439277887468336, 'avg_cost': 346.26387206203054}],  0.2
    #  0.25: [{'reward': 20.436372596666764, 'avg_cost': 369.24947211741494}],
    #  0.3: [{'reward': 21.497969893865577, 'avg_cost': 385.71743570217035}],
    #  0.35: [{'reward': 27.014314143791466, 'avg_cost': 376.49814808404585}],
    #  0.4: [{'reward': 28.29824078231645, 'avg_cost': 374.45342517913394}]}

    def repartition(self,initial_par, wLoad, **kwargs):
        # env = EnvSkew4000(wLoad)
        # env = EnvWithClassifier(wLoad)
        # env.reward_threshold = 0.1
        # pretrained = PPO("MlpPolicy", env, verbose=1,tensorboard_log="./ppo_controller_tensorboard_env2/")
        # pretrained.learn(total_timesteps=5e4)
        # pretrained.save("stable_pretrained_model/ppo_controller_v2_4000_copy")
        # Run Command: tensorboard --logdir ./ppo_controller_tensorboard_env2/ --bind_all
        # del pretrained
        # env = Env2600(wLoad)
        # env = EnvMaskCurve(wLoad)
        # env = EnvMask(wLoad)
        # env = EnvMaskNew(wLoad)
        env = Env5(wLoad)
        # env = EnvParMask(wLoad)
        # env = EnvState(wLoad)
        # env = Env2600Speedup(wLoad)
        env.reward_threshold = 0.1
        # pretrained = PPO("MlpPolicy", env, verbose=1,tensorboard_log="./ppo_controller_tensorboard_env2/env_mask_new")
        # pretrained.learn(total_timesteps=1e4)
        # # Run Command: tensorboard --logdir ./ppo_controller_tensorboard_env2/
        # # pretrained.save("stable_pretrained_model/ppo_controller_v2_2600")
        # # pretrained.save("stable_pretrained_model/ppo_controller_v2_2600_state")
        # pretrained.save("stable_pretrained_model/ppo_controller_v2_2600_speedup")
        # pretrained.save("stable_pretrained_model/ppo_controller_v2_2600_mask")
        # pretrained.save("stable_pretrained_model/ppo_controller_v2_2600_par_mask")
        # del pretrained
        # model = PPO.load("stable_pretrained_model/ppo_controller_v4_2800_0.05",device='cuda:4')
        model = PPO.load("stable_pretrained_model/ppo_controller_v4_2800_best", device='cuda:4')
        # model = PPO.load("stable_pretrained_model/ppo_controller_v2_2600_0.05",device='cuda:4')
        # model = PPO.load("stable_pretrained_model/ppo_controller_v2_2600_state")
        # model = PPO.load("stable_pretrained_model/ppo_controller_v2_2600_mask",device='cuda:4')
        # model = PPO.load("stable_pretrained_model/ppo_controller_v2_2600_par_mask_0.05")
        # model = PPO.load("stable_pretrained_model/ppo_controller_v2_2600_curve_0.05")
        # model=pretrained
        obs = env.reset()
        epoch = 0
        total_reward = []
        # 记录奖励为正的比例
        total_actions=0
        good_actions=0
        reward_list=[]
        result=dict()
        for i in range(5000):
            action, _states = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            reward_list.append(reward)
            if reward!=0:total_actions+=1
            if reward>0:good_actions+=1
            total_reward.append(reward)
            if done:
                result = {'reward': sum(total_reward),
                          'avg_cost': sum(env.io_cost) / sum([sql['feature'].frequency for sql in env.w.sql_list]),
                          'action_ratio':[len(env.action_list.keys()),round(good_actions/total_actions,3),total_actions],
                          'rep_cost':sum(env.rep_cost)/sum([sql['feature'].frequency for sql in env.w.sql_list])}
                          # 'optimize_time':env.optimize_time}
                print(f"The total reward : {result['reward']}")
                print(env.cost_time_map['cost'])
                print(env.cost_time_map['cdf'])
                print('action list : ', env.action_list.keys())
                self.action_list = env.action_list
                print(f"Average query cost: {result['avg_cost']}")
                print(f"Average repartition cost: {result['rep_cost']}")
                # print(f"Optimize Time : {env.optimize_time}")
                print(reward_list)
                epoch += 1
                if epoch == 1: break
        env.close()
        return result


if __name__=="__main__":
    torch.multiprocessing.set_start_method('spawn')
    ppo=PpoController()
    test_result=dict()
    task_list=[]
    workload_dict = {
        'data1': [1500],
        # 'data1': [1500, 3000, 1300, 4000],
        # 'data2': [1200, 1350],
        # 'data3': [1600, 2600]
    }
    for w_path in workload_dict.keys():
        for query_num in workload_dict[w_path]:
            wLoad = Workload(Conf.WORDTYPE['synthetic']['test'], f'data/{w_path}/{query_num}query-steam.csv')
            # ppo.train_model_diff_reward_threshold(wLoad)
            task=MyThread(ppo.repartition,(None, wLoad))
            task.start()
            task_list.append(task)
    for i,task in enumerate(task_list):
        test_result[i]=task.get_result()
    print(test_result)
