### Self-Adapting Vertical Partitioning for Dynamic Workload

This is the project code of dynamic partitioning algorithm PPO controller. The structure and function of each directory are listed below.

#### Project structure description:
- **baselines:** Some classic dynamic partitioning algorithms, including AutoStore, Smopdc, Feedback, PPO Controller etc. It also includes a template class, AlgorithmTemplate, which all algorithms need to implement its defined methods.
- **data:** This directory includes workload generator and generated workload files (i.e. tpc-h/ tpc-ds/ synthetic). 
- **db:** Database related module. Provide driver class, transaction class, data types related to table structure and load structure, cost model, etc.
- **environment:** Environment module of RL. Where env.py and env5.py respectively is the initial and final version of PPO-Controller's environment file.
- **experiment:** Drawing related files and is responsible for the visualization of experimental results.
- **log:** Log files.
- **partitioner:** Partitioner module. Some files related to SCVP algorithm.
- **pretrained:** Save temporarily generated model and data files.
- **selector:** Workload selector module. A query selection algorithm for repartitioning. 
- **visualization:** It also includes some code files related to workload data visualization.
- **other single files:**
  - util.py: A tool class.
  - tianshou_ppo.py: Use tianshou RL library to implement ppo controller (temporary version).
  - adapter_controller_pg.py: Partition generator module and conducting experiments on postgresql database.
  - tpc-main.py/ syn-main.py: The main program entry file, which is used to conduct the comparative experiment. The dataset and dynamic partition algorithms can be flexibly specified.

#### Project dependency package:

Some modules required by the project can be seen in the requirement.txt file.  It is recommended to run the following commands on the console:

`cd ppo-controller`

`conda create -n dyppo python==3.6`

`source activate dyppo`

`pip install -r requirements.txt`

#### DB Configuration (Non-required)

When conducting experiments about latency, users need to configure the PG database environment in advance and modify the user connection information in _db\pg.py_. 
All table structures can be imported through _db\ppoc.sql_. Call _adapter_controller_pg.py_ to deploy partitions and get experimental results.

#### Run partitioning algorithms on HDD cost model:
- **syn-main.py:** Test the performance of baselines over synthetic datasets
- **tpc-main.py:** Test the performance of baselines over TPC-H / TPC-DS datasets and conduct sensitivity analysis experiments.