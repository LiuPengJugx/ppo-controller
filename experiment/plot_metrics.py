import numpy as np
from scipy import interpolate
import xlrd
import matplotlib.pyplot as plt
"""
Visualize experiment result by multiple charts
"""
def read_csv(file_name,sheet_name):
    BASE_PATH= "result/"
    # data=pd.read_csv(BASE_PATH+file_name)
    table=xlrd.open_workbook(BASE_PATH+file_name).sheet_by_name(sheet_name)
    data=list()
    for row in range(table.nrows):
        data_row=list()
        for col in range(table.ncols):
            data_row.append(table.cell(row,col).value)
        data.append(data_row)
    data=np.array(data)
    chart_dict={
        'column_names':data[0,1:],
        'row_names':data[1:,0],
        'data':data[1:,1:].astype('float')
    }
    return chart_dict

def draw_estimated_query_cost():
    sheets = ['sheet1']
    for sid, sheet_name in enumerate(sheets):
        plt.figure(figsize=(10, 5))
        # 包括分区收益和重分区成本
        chart_dict = read_csv('PG数据库实验.xlsx', sheet_name)
        datasets = chart_dict['row_names']
        workload_names = ['Synthetic', 'TPC-H', 'TPC-DS', ]
        methods = chart_dict['column_names']
        data = chart_dict['data']
        colors = ['#00CD66', '#000000', '#007BFF', '#FF7F50', '#6C757D']
        markers=['2','*','4','+','.']
        for i in range(0, len(datasets)):
            plt.subplot(2,5,i + 1)
            for x in range(len(methods)):
                plt.plot(x,data[i][x],color=colors[x],marker=markers[x],markersize='12')
            plt.plot([x for x in range(len(methods))],data[i],color='#d3d7d4',linewidth='0.15')
            plt.xticks(ticks=[x for x in range(len(methods))], labels=['' for _ in range(len(methods))], ha='left')
            plt.xlabel(datasets[i])
            if i==0:
                plt.ylabel('Average access cost per query')
                plt.legend(methods, bbox_to_anchor=[3.4, 1], loc='lower center', frameon=False, ncol=len(methods))
            # plt.grid()
        plt.subplots_adjust(hspace=0.4, wspace=0.4)
        # plt.show()
        plt.savefig(f'chart/estimate_query_cost2.pdf', bbox_inches='tight')



def draw_estimated_rep_cost():
    # sheets=['sheet1','sheet2']
    sheets=['sheet2']
    for sid,sheet_name in enumerate(sheets):
        plt.figure(figsize=(10, 5))
        # 包括分区收益和重分区成本
        chart_dict = read_csv('PG数据库实验.xlsx', sheet_name)
        datasets = chart_dict['row_names']
        workload_names=['Synthetic','TPC-H','TPC-DS',]
        methods= chart_dict['column_names']
        data= chart_dict['data']
        phases=[[0,4],[4,7],[7,10]]
        colors=['#00CD66','#000000','#007BFF', '#FF7F50', '#6C757D']
        markers = ['2', '*', '4', '+', '.']
        # markers = ['2', '*', 'v', '+', '.']
        # for i in range(0,3):
        #     plt.subplot(int(f'{1}{3}{i+1}'))
        #     phase=phases[i]
        #     for rid,row in enumerate(data[phase[0]:phase[1]].T):
        #         plt.plot(row,marker=markers[rid],color=colors[rid])
        #     ref_datasets=datasets[phase[0]:phase[1]]
        #     plt.xticks(ticks=[x for x in range(len(ref_datasets))], labels=ref_datasets, ha='left')
        #     plt.xlabel(workload_names[i])
        #     if i==0:
        #         plt.ylabel('Repartition cost')
        #         plt.legend(methods,bbox_to_anchor=[1.7, 1], loc='lower center',frameon=False, ncol=len(methods))
        #     plt.grid()
        # plt.show()

        for i in range(len(datasets)):
            plt.subplot(2, 5, i + 1)
            for x in range(len(methods)):
                plt.plot(x, data[i][x], color=colors[x], marker=markers[x], markersize='12')
            plt.plot([x for x in range(len(methods))], data[i], color='#d3d7d4', linewidth='0.12')
            plt.xticks(ticks=[x for x in range(len(methods))], labels=['' for _ in range(len(methods))], ha='left')
            plt.xlabel(datasets[i])
            max_val=max(data[i])
            if max_val>=10: plt.ylim(bottom=0,top=max_val+5)
            else: plt.ylim(bottom=0,top=max_val+1)
            if i == 0:
                plt.ylabel('Repartition cost')
                plt.legend(methods,bbox_to_anchor=[3.3, 1], loc='lower center',frameon=False, ncol=len(methods))
        plt.subplots_adjust(hspace=0.4, wspace=0.4)
        # plt.show()
        plt.savefig(f'chart/estimate_rep2.pdf', bbox_inches='tight')
def draw_workload_size_scalability():
    cul_que_num=[682, 1424, 1443, 1504, 1583, 1661, 1699, 1779, 1862, 1936, 1979, 1985, 2009, 2035, 2092, 2115, 2155, 2209, 2225, 2323, 2370, 2385, 2427, 2466, 2498, 2506, 2517, 2522, 2560, 2600, 2691, 2739, 2823, 2889, 2930, 3013, 3040, 3067, 3079, 3085, 3122, 3138, 3152, 3236, 3272, 3333, 3377, 3492, 3602, 3636, 3686, 3708, 3757, 3763, 3771, 3809, 3810, 3874, 3965, 4041, 4135, 4196, 4225, 4276, 4307, 4346, 4382, 4394, 4399, 4422, 4496, 4543, 4635, 4693, 4807, 4854, 4903, 4960, 4980, 5023, 5053, 5083, 5101, 5119, 5133, 5200, 5221, 5250, 5353, 5403, 5496, 5530, 5560, 5619, 5675, 5699, 5708, 5715, 5738, 5767, 5834, 5895, 5938, 6043, 6095, 6137, 6175, 6189, 6224, 6294, 6300, 6320, 6331, 6335, 6387, 6450, 6522, 6600, 6660, 6714, 6746, 6842, 6864, 6920, 6964, 6980, 6992, 7051, 7116, 7199, 7261, 7354, 7431, 7537, 7601, 7619, 7620, 7651, 7716, 7762, 7842, 7993, 8054, 8164, 8193, 8194, 8224, 8232, 8248, 8281, 8318, 8359, 8435, 8512, 8652, 8713, 8750, 8868, 8870, 8888, 8894, 8908, 8909, 8910, 8951, 8985, 9067, 9123, 9192, 9319, 9393, 9482, 9532, 9536, 9548, 9558, 9575, 9618, 9658, 9729, 9771, 9855, 9945, 10058, 10115, 10139, 10181, 10198, 10210, 10257, 10283, 10316, 10408, 10496, 10557, 10607, 10648, 10679, 10754, 10769, 10784, 10792, 10804, 10821, 10829, 10870, 10900, 10959, 11038, 11106, 11199, 11251, 11329, 11389, 11414, 11438, 11474, 11479, 11492, 11504, 11505, 11521, 11562, 11614, 11686, 11714, 11855, 11927, 11997, 12028, 12072, 12098, 12107, 12122, 12133, 12143, 12208, 12240, 12289, 12396, 12457, 12507, 12624, 12660, 12707, 12731, 12770, 12784, 12798, 12845, 12862, 12967, 13069, 13122, 13164, 13183, 13315, 13384, 13394, 13420, 13430, 13454, 13500, 13551, 13631, 13666, 13743, 13833, 13869, 13928, 13939, 13977, 14005, 14016, 14018, 14033, 14054, 14061, 14149, 14220, 14285, 14333, 14447, 14485, 14544, 14596, 14615, 14620, 14636, 14673, 14687, 14689, 14726, 14791, 14847, 14868, 14970, 15035, 15096, 15120, 15165, 15213, 15250, 15260, 15276, 15286, 15336, 15435, 15514, 15536, 15600, 15678, 15763, 15801, 15841, 15846, 15852, 15867, 15872, 15897, 15913, 15974, 16055, 16096, 16188, 16246, 16329, 16375, 16434, 16439, 16465, 16478, 16490, 16508, 16535, 16597, 16694, 16743, 16868, 16891, 16998, 17027, 17053, 17067, 17111, 17145, 17149, 17156, 17221, 17248, 17314, 17367, 17472, 17597, 17690, 17705, 17737, 17753, 17768, 17787, 17835, 17891, 17970, 18093, 18149, 18176, 18243, 18314, 18328, 18352, 18443, 18487, 18568, 18663, 18752, 18788, 18816, 18896, 18908, 18946, 18966, 18985, 18996, 19020, 19042, 19064, 19119, 19182, 19269, 19331, 19421, 19479, 19505, 19575, 19593, 19612, 19624, 19711, 19728, 19788, 19814, 19903, 19987, 20105, 20153, 20192, 20202, 20216, 20223, 20237, 20298, 20327, 20374, 20460, 20552, 20649, 20714, 20763, 20806, 20842, 20860, 20870, 20895, 20957, 21012, 21096, 21176, 21279, 21332, 21369, 21393, 21404, 21413, 21421, 21436, 21454, 21461, 21466, 21505, 21577, 21596, 21705, 21814, 21858, 21892, 21954, 21962, 22007, 22013, 22014, 22047, 22067, 22079, 22095, 22178, 22230, 22309, 22354, 22472, 22492, 22535, 22592, 22616, 22632, 22642, 22695, 22752, 22822, 22864, 22994, 23106, 23256, 23295, 23297, 23305, 23328, 23339]
    data_original=[
        [2455.426, 589.234, 21.009, 42.656, 75.692, 71.131, 34.23, 114.07, 86.188, 70.147, 20.861, 5.325, 31.003, 20.859, 48.305, 23.579, 36.007, 36.293, 23.005, 76.208, 31.985, 11.936, 22.056, 33.172, 28.913, 1.623, 6.785, 8.232, 28.139, 14.597, 65.217, 62.819, 92.508, 50.784, 36.298, 66.544, 29.491, 20.63, 4.731, 5.788, 28.697, 19.801, 9.678, 90.629, 30.253, 51.905, 49.018, 85.402, 60.329, 44.649, 50.458, 22.192, 47.145, 3.292, 12.122, 45.014, 1.023, 62.725, 80.965, 61.72, 64.339, 46.026, 13.151, 35.037, 32.832, 32.773, 34.856, 7.159, 5.285, 32.9, 76.601, 36.086, 49.597, 32.454, 149.216, 48.419, 49.446, 50.846, 27.468, 45.814, 44.786, 33.838, 18.638, 13.49, 18.882, 61.364, 14.94, 25.672, 114.916, 71.44, 100.318, 49.963, 15.691, 56.952, 70.449, 18.035, 11.401, 3.362, 20.379, 30.576, 65.751, 46.592, 33.473, 96.014, 55.643, 38.541, 26.24, 11.16, 43.174, 90.799, 10.778, 13.497, 12.355, 2.587, 57.824, 72.863, 60.074, 87.844, 50.888, 56.875, 31.442, 87.062, 32.8, 64.916, 44.383, 13.187, 8.735, 73.108, 70.157, 88.273, 58.546, 106.652, 88.958, 108.077, 50.567, 20.116, 1.167, 21.08, 66.613, 36.83, 77.984, 131.866, 72.02, 96.951, 39.355, 1.095, 42.817, 8.765, 17.65, 20.428, 37.01, 22.085, 49.883, 100.289, 134.956, 26.802, 20.67, 66.834, 3.302, 3.644, 3.716, 5.777, 0.203, 0.274, 10.87, 24.766, 35.525, 32.171, 34.869, 92.272, 48.849, 57.814, 33.347, 4.379, 9.867, 6.701, 7.423, 32.365, 23.962, 30.767, 21.793, 34.565, 46.266, 86.33, 35.783, 16.753, 36.48, 8.265, 4.885, 34.632, 17.772, 21.995, 79.227, 76.141, 21.629, 18.646, 38.053, 14.469, 44.388, 17.706, 11.504, 7.285, 3.285, 7.564, 5.323, 25.15, 12.507, 35.8, 44.208, 54.993, 46.711, 37.693, 66.903, 28.339, 18.96, 16.491, 34.518, 4.808, 6.235, 2.44, 1.374, 8.43, 21.861, 29.118, 41.664, 16.692, 81.866, 56.944, 37.084, 22.722, 29.434, 27.734, 12.314, 20.637, 6.578, 10.933, 49.669, 10.081, 28.68, 59.978, 35.37, 23.937, 87.669, 38.574, 31.964, 21.992, 22.072, 7.294, 8.831, 36.249, 8.832, 76.824, 54.767, 43.492, 37.293, 11.272, 97.556, 45.899, 9.609, 14.648, 3.439, 14.926, 39.076, 38.403, 43.612, 14.699, 30.234, 58.605, 25.664, 32.215, 4.977, 27.96, 30.75, 9.875, 1.511, 8.979, 9.003, 4.995, 63.608, 50.251, 53.606, 25.138, 81.454, 21.913, 46.187, 29.679, 8.242, 1.677, 6.852, 19.671, 10.396, 1.082, 24.25, 40.253, 35.797, 23.757, 68.859, 31.018, 43.605, 25.288, 31.766, 24.439, 25.279, 7.332, 14.223, 4.061, 39.084, 86.188, 35.796, 14.037, 50.22, 54.246, 56.803, 25.912, 22.071, 3.898, 0.798, 10.028, 3.278, 22.282, 11.401, 41.461, 66.131, 32.241, 82.762, 52.154, 71.913, 40.911, 62.592, 5.79, 27.009, 17.885, 17.27, 21.155, 36.774, 41.34, 65.764, 24.862, 93.396, 19.337, 75.473, 37.899, 19.486, 13.409, 24.992, 19.409, 2.435, 4.277, 35.246, 20.279, 44.595, 37.215, 82.284, 92.151, 51.679, 11.577, 25.733, 12.959, 21.621, 12.29, 48.837, 42.057, 64.704, 82.99, 43.449, 19.649, 56.517, 65.238, 15.432, 24.714, 83.469, 48.7, 63.398, 73.293, 68.483, 12.302, 28.413, 61.521, 15.677, 39.983, 6.841, 23.417, 4.471, 16.832, 7.827, 14.127, 54.124, 53.521, 72.763, 58.478, 74.217, 32.031, 19.88, 45.116, 6.107, 7.973, 6.503, 52.744, 10.272, 43.556, 16.93, 43.537, 59.571, 114.958, 31.715, 40.558, 4.034, 5.097, 6.335, 12.425, 39.413, 19.014, 47.694, 57.107, 54.919, 91.134, 58.879, 39.501, 39.78, 13.746, 4.899, 2.729, 9.828, 48.461, 28.834, 54.397, 87.486, 44.87, 68.629, 18.15, 9.4, 3.785, 2.447, 2.185, 9.899, 7.319, 2.822, 1.364, 25.567, 59.907, 15.027, 75.762, 65.747, 40.825, 33.172, 43.686, 2.455, 43.054, 4.846, 0.593, 12.872, 16.436, 4.543, 13.081, 78.118, 25.625, 69.746, 39.41, 73.18, 9.316, 30.164, 41.587, 14.702, 23.054, 7.121, 40.84, 42.765, 48.059, 27.389, 96.87, 78.726, 89.739, 10.443, 0.546, 3.316, 11.515, 10.252],
        [2447.353, 585.857, 20.907, 50.601, 77.951, 61.963, 28.536, 100.831, 72.002, 69.056, 18.431, 4.944, 23.525, 19.743, 46.634, 26.616, 42.105, 35.528, 20.629, 87.175, 33.801, 12.622, 32.955, 35.605, 29.587, 2.182, 4.474, 8.603, 18.028, 16.007, 65.842, 51.224, 98.79, 44.531, 40.521, 67.261, 23.412, 24.719, 3.761, 5.771, 28.602, 25.267, 9.645, 92.502, 33.966, 55.558, 47.798, 85.163, 74.97, 37.808, 52.185, 22.246, 50.357, 3.291, 9.961, 53.653, 1.19, 56.355, 81.44, 62.701, 74.178, 52.858, 13.108, 43.42, 31.761, 34.212, 41.044, 9.078, 4.922, 30.501, 77.193, 47.946, 50.13, 32.044, 130.998, 55.741, 46.011, 45.084, 24.86, 38.503, 39.045, 34.876, 9.871, 12.267, 20.825, 75.349, 15.099, 33.066, 91.711, 56.769, 66.725, 41.838, 22.501, 52.168, 59.417, 13.356, 10.234, 2.434, 17.759, 28.273, 72.687, 43.675, 31.205, 82.892, 49.445, 45.755, 29.329, 12.403, 43.703, 79.964, 6.626, 11.867, 9.993, 1.913, 62.486, 71.422, 59.676, 96.314, 48.036, 47.877, 30.667, 92.548, 27.562, 64.592, 36.568, 14.477, 8.455, 57.322, 70.199, 80.342, 46.644, 105.763, 81.831, 99.658, 53.697, 17.884, 1.165, 18.823, 70.232, 34.861, 83.876, 109.527, 64.723, 90.536, 46.468, 1.404, 36.619, 11.049, 11.021, 17.353, 39.083, 33.258, 55.575, 102.734, 86.749, 30.682, 22.259, 64.882, 2.892, 3.665, 4.538, 5.777, 0.204, 0.273, 10.903, 22.636, 46.458, 37.1, 40.028, 119.507, 48.888, 43.2, 30.413, 4.394, 10.623, 6.804, 6.9, 36.023, 22.7, 32.113, 24.794, 42.403, 48.074, 87.18, 34.468, 15.533, 37.819, 8.319, 4.862, 39.375, 12.345, 25.102, 83.187, 61.95, 19.401, 16.109, 28.783, 12.529, 48.168, 17.431, 10.36, 6.912, 2.432, 6.522, 4.508, 24.266, 10.839, 33.396, 43.312, 48.834, 46.686, 32.399, 65.248, 23.641, 13.751, 18.088, 41.969, 3.086, 6.144, 2.679, 0.963, 7.299, 31.084, 29.6, 42.763, 17.227, 70.514, 46.516, 34.072, 20.462, 30.546, 28.187, 5.552, 18.653, 5.314, 11.005, 37.268, 10.997, 27.662, 64.855, 27.684, 29.06, 79.799, 30.115, 31.968, 22.747, 25.598, 3.822, 10.294, 19.419, 9.515, 77.622, 54.805, 45.965, 40.257, 16.031, 81.352, 50.591, 11.796, 12.206, 4.749, 11.844, 40.933, 30.277, 34.945, 23.254, 31.09, 55.186, 23.291, 32.271, 4.754, 21.529, 18.307, 12.105, 1.373, 6.352, 6.212, 3.284, 53.733, 47.565, 35.016, 28.937, 75.308, 22.164, 33.589, 24.066, 7.76, 2.384, 3.255, 19.379, 7.666, 0.545, 25.985, 37.446, 43.956, 17.977, 75.167, 31.785, 41.156, 25.192, 31.188, 26.59, 22.265, 8.699, 11.992, 2.043, 30.465, 68.028, 32.137, 13.572, 46.995, 38.921, 58.952, 23.295, 23.517, 2.908, 1.218, 8.719, 2.397, 20.52, 8.02, 40.756, 66.231, 30.586, 75.019, 49.023, 63.793, 34.666, 55.353, 5.117, 22.823, 18.461, 14.868, 12.212, 22.705, 48.636, 64.395, 26.006, 95.683, 18.87, 70.864, 37.847, 20.127, 16.918, 23.201, 17.289, 2.999, 5.245, 37.107, 25.151, 53.061, 34.257, 96.419, 104.609, 55.283, 10.909, 30.319, 17.396, 21.659, 14.032, 44.381, 48.972, 73.048, 96.606, 45.54, 18.934, 57.391, 62.662, 19.222, 34.67, 82.746, 48.748, 68.183, 66.749, 67.112, 21.467, 24.807, 54.744, 15.131, 38.46, 5.442, 13.04, 3.002, 10.375, 7.219, 14.138, 38.582, 47.532, 72.229, 58.411, 59.448, 31.713, 13.56, 47.802, 7.497, 5.229, 8.272, 55.606, 10.271, 34.017, 12.788, 42.137, 64.479, 86.802, 33.426, 34.988, 5.56, 6.4, 5.622, 13.457, 29.47, 19.573, 30.172, 74.931, 51.357, 82.123, 62.403, 32.677, 32.977, 20.433, 7.326, 2.738, 9.482, 45.858, 36.903, 57.182, 73.263, 34.885, 55.702, 19.773, 5.796, 5.839, 4.276, 1.62, 7.835, 13.135, 3.606, 1.015, 29.558, 60.27, 23.692, 80.789, 58.839, 39.938, 23.582, 50.211, 3.276, 29.985, 4.618, 0.461, 10.936, 17.86, 2.701, 9.853, 77.829, 22.158, 61.344, 33.792, 70.814, 9.307, 27.569, 41.057, 12.345, 21.959, 8.651, 40.9, 49.044, 49.093, 24.566, 77.623, 74.106, 86.908, 9.197, 0.671, 4.947, 7.045, 9.226],
        # [2446.886, 463.654, 7.851, 47.171, 49.002, 49.611, 22.632, 73.43, 60.623, 47.378, 9.131, 5.178, 32.819, 23.745, 41.163, 20.274, 25.131, 32.332, 11.174, 66.358, 26.536, 8.603, 26.145, 21.76, 13.808, 1.068, 6.657, 3.116, 17.255, 11.887, 60.657, 32.639, 79.354, 31.16, 22.121, 53.342, 15.909, 14.33, 2.623, 3.321, 15.152, 18.703, 9.629, 87.611, 21.214, 40.759, 36.157, 73.091, 67.337, 30.9, 35.39, 14.039, 31.593, 4.12, 12.149, 56.82, 1.051, 55.707, 69.355, 54.754, 47.765, 41.406, 9.523, 28.299, 18.584, 26.33, 15.973, 10.17, 4.422, 26.239, 61.169, 29.147, 35.299, 20.668, 108.221, 35.281, 35.816, 29.359, 12.46, 30.05, 24.766, 20.447, 3.646, 8.601, 18.865, 75.938, 7.423, 10.613, 77.661, 39.388, 61.892, 28.409, 8.849, 39.888, 33.71, 7.721, 3.54, 3.345, 18.75, 28.331, 54.87, 34.006, 27.386, 65.674, 40.288, 20.625, 24.552, 8.658, 28.963, 60.01, 4.133, 9.048, 12.365, 2.877, 55.925, 45.713, 50.503, 52.848, 37.275, 39.189, 18.981, 72.439, 19.029, 48.287, 23.471, 15.294, 10.111, 41.473, 42.126, 63.447, 35.255, 77.645, 64.551, 70.63, 30.777, 20.165, 0.957, 18.862, 67.997, 30.748, 63.31, 106.437, 39.252, 82.037, 29.534, 1.209, 19.172, 10.984, 14.236, 16.725, 32.796, 16.216, 31.857, 77.806, 79.655, 18.741, 13.723, 51.516, 3.309, 3.671, 3.712, 5.791, 0.205, 0.273, 10.888, 20.238, 35.158, 27.654, 31.726, 76.945, 36.157, 35.094, 21.969, 3.852, 6.035, 4.352, 6.99, 37.159, 23.333, 46.143, 18.403, 33.589, 47.933, 70.316, 21.707, 11.231, 25.329, 3.034, 2.435, 32.638, 16.162, 14.341, 67.734, 42.248, 18.963, 15.81, 21.817, 9.884, 35.31, 8.509, 7.844, 4.198, 2.443, 15.424, 6.403, 19.26, 9.064, 29.781, 36.104, 39.43, 49.225, 24.458, 66.945, 19.139, 11.143, 9.898, 19.794, 3.087, 4.054, 3.198, 0.965, 7.139, 17.44, 21.708, 38.761, 13.398, 65.529, 42.637, 19.825, 15.492, 25.415, 16.022, 12.304, 15.456, 4.756, 10.298, 33.214, 5.721, 19.185, 53.958, 25.11, 20.097, 49.258, 24.603, 30.59, 14.313, 16.023, 2.855, 8.809, 33.922, 9.556, 75.213, 55.517, 34.145, 30.009, 8.305, 74.884, 34.379, 9.904, 14.836, 3.364, 12.006, 45.059, 32.252, 30.759, 17.636, 30.273, 48.422, 18.725, 25.788, 2.551, 18.174, 20.063, 9.865, 0.963, 6.737, 8.675, 2.803, 52.106, 39.993, 32.788, 20.07, 62.025, 16.843, 39.465, 21.073, 4.106, 1.015, 4.781, 28.508, 14.451, 1.488, 18.315, 34.919, 26.491, 13.043, 62.392, 21.865, 27.092, 13.916, 20.996, 22.831, 25.102, 11.371, 8.751, 3.419, 34.933, 62.619, 29.899, 10.051, 27.171, 36.139, 48.13, 16.964, 10.926, 1.92, 0.792, 9.972, 2.591, 15.302, 11.323, 25.62, 66.208, 25.419, 59.627, 29.546, 59.826, 25.985, 41.363, 3.084, 18.227, 8.932, 19.808, 22.142, 23.727, 36.321, 54.663, 18.635, 95.58, 12.239, 66.263, 23.069, 13.639, 8.83, 20.264, 16.934, 1.625, 2.857, 37.9, 15.688, 38.42, 22.884, 83.293, 85.6, 44.36, 7.109, 19.791, 9.254, 24.791, 20.049, 31.577, 35.664, 59.717, 78.112, 33.781, 11.512, 33.5, 49.237, 15.48, 21.041, 83.359, 44.413, 49.369, 57.122, 53.475, 12.362, 18.162, 36.531, 12.098, 17.883, 6.858, 11.748, 4.461, 16.916, 12.978, 10.051, 30.18, 41.385, 69.97, 47.0, 59.916, 29.683, 12.957, 35.03, 4.956, 5.316, 6.479, 53.956, 8.435, 27.201, 16.941, 39.398, 40.889, 75.338, 29.61, 18.87, 4.214, 5.428, 6.187, 13.584, 29.958, 14.962, 26.955, 53.755, 45.508, 71.259, 42.261, 20.942, 17.94, 16.212, 7.32, 2.029, 7.586, 32.011, 28.776, 48.942, 60.68, 33.504, 54.035, 16.303, 5.028, 3.218, 4.319, 2.373, 9.811, 10.663, 3.15, 1.01, 19.875, 47.916, 12.881, 61.922, 55.38, 34.823, 20.158, 43.735, 1.35, 24.265, 4.853, 0.647, 6.47, 16.409, 4.39, 6.866, 57.349, 15.983, 58.414, 23.697, 64.521, 9.347, 20.652, 32.993, 11.39, 11.02, 7.114, 44.373, 39.172, 43.504, 15.087, 75.476, 60.78, 84.901, 5.79, 0.935, 3.333, 8.287, 11.306],
    ]
    data=[]
    begin=0
    [data.append(row[begin:]) for row in data_original]
    gap=10
    xlabel=[]
    new_data=[]
    markers = ['v', 'o']
    # colors = ['#5cb3cc', '#c04851']
    colors = ['#007BFF', '#c04851']#5390fe
    methods=['Feedback','PPOController']
    plt.figure(figsize=(10, 3))
    for rid,row in enumerate(data):
        new_row=[]
        cnt=0
        cnt+=gap
        while(cnt<len(row)-1):
            new_row.append(sum(row[0:cnt]))
            if rid==0:xlabel.append(cul_que_num[cnt-1])
            cnt+=gap
        new_row.append(sum(row))
        if rid==0:xlabel.append(cul_que_num[-1])
        new_data.append(new_row)
    plt.subplot(1, 2, 1)
    plt.yticks(fontproperties='DejaVu Sans', size=7)
    plt.xticks(fontproperties='DejaVu Sans', size=7)
    # sample_x = [x * 3 for x in range(int(len(new_data[0]) / 3))]
    sample_x=[10000+15000*x/10 for x in range(0,10)]
    new_y=[]
    for rid,row in enumerate(new_data):
        arr_x_list = np.array(xlabel)
        # arr_x = np.linspace(min(arr_x_list), max(arr_x_list), 25)
        arr_y = np.array(row)
        f = interpolate.interp1d(arr_x_list, arr_y, kind='cubic', fill_value="extrapolate")
        # plt.plot(row,color=colors[rid])
        # for sx in sample_x:
        #     plt.plot(sx,row[sx],marker=markers[rid],ls='--', color=colors[rid],markerfacecolor='none')
        new_y.append(f(sample_x)/sample_x)
        plt.plot(sample_x, f(sample_x)/sample_x, marker=markers[rid], ls='-', color=colors[rid], markerfacecolor='none')
    plt.fill_between(sample_x, new_y[0], new_y[1], interpolate=False, facecolor='cornflowerblue', alpha=0.2)
    # sample_points=[10,20,30,40,47]
    sample_points=[5*(x+1)-1 for x in range(9)]
    # plt.xticks(ticks=sample_points, labels=[str(xlabel[x]) for x in sample_points], ha='left')
    plt.legend(methods, ncol=len(methods), frameon=False)
    plt.ylabel('Latency Per Query(s)')
    plt.xlabel('Workload Size')
    # plt.ylim(bottom=10000)
    plt.xlim(left=10000,right=25000)
    plt.grid()
    # plt.legend(methods, ncol=len(methods), frameon=False)
    plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
    plt.subplot(1,2,2)
    plt.yticks(fontproperties='DejaVu Sans', size=7)
    plt.xticks(fontproperties='DejaVu Sans', size=7)
    rep_data=[
        [28.25,89.4,90.87,85.19,133.09,176.52,358.7],
        [32,61.28,52.39,52.058,49.8,94.43,145.21]
    ]
    x_list= [3056, 6643,10112, 13114, 16337, 23339,26491]
    sample_y = [10000+15000*x/10 for x in range(0,11)]
    for rid,row in enumerate(rep_data):
        arr_x_list = np.array(x_list)
        arr_x = np.linspace(min(arr_x_list), max(arr_x_list), 25)
        arr_y = np.array(row)
        f = interpolate.interp1d(arr_x_list, arr_y, kind='cubic',fill_value="extrapolate")
        smooth_y = f(arr_x)
        # plt.plot(arr_x,smooth_y,color=colors[rid])
        for sid,sy in enumerate(sample_y):
            # plt.plot(sy,f(sy), color=colors[rid],marker=markers[rid],markerfacecolor='none')
            if rid==0:
                plt.bar(sy-250, f(sy), color=colors[rid], width=500)
            else:
                plt.bar(sy+250, f(sy), color=colors[rid], width=500)
    # plt.xlim(left=10000,right=25000)
    plt.ylabel('Total Repartition Time(s)')
    plt.xlabel('Workload Size')
    plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
    # plt.subplots_adjust(wspace=0.2)
    plt.grid()
    # plt.show()
    plt.savefig(f'chart/scaling_workload_size3.pdf', bbox_inches='tight')

def draw_scalability():
    plt.figure(figsize=(10, 3))
    # sheet_names=['sheet4','sheet8','sheet7']
    sheet_names=['sheet8']
    for sheet in sheet_names:
        chart_dict = read_csv('PG数据库实验.xlsx', sheet)
        datasets = chart_dict['row_names']
        methods = chart_dict['column_names']
        colors1 = ['#007BFF', '#FF7F50']
        # colors = ['#5cb3cc', '#c04851']
        colors = ['#007BFF', '#c04851']#5390fe
        data = chart_dict['data']
        if sheet=='sheet4':
            phases = [[0, 8], [8, 17]]
            x_labels = [3056, 6643, 10112, 13114, 16337, 20010, 23339, 26491]
        if sheet=='sheet8':
            phases = [[0, 8], [8, 17]]
            # query_size=[200*x for x in range(1,9)]
            query_size=[2302,4492,6763,8840,11255,12862,15385,17733]
            x_labels =np.array([x+1 for x in range(8)])
        elif sheet=='sheet7':
            phases = [[0, 5], [5, 10]]
            x_labels=[float(x) for x in datasets[0:5]]
        # markers=['4','+']
        markers=['v','o']
        markers1=['v','+']
        for i in range(2):
            plt.subplot(1,2,i+1)
            plt.xticks(fontproperties='DejaVu Sans', size=7)
            plt.yticks(fontproperties='DejaVu Sans', size=7)
            phase=phases[i]
            ref_data=data[phase[0]:phase[1]].T
            if sheet == 'sheet7':
                new_y1=ref_data[0]-ref_data[1]
                arr_x=np.linspace(min(x_labels),max(x_labels),8)
                new_y2=[0 for _ in range(len(arr_x))]
                f = interpolate.interp1d(np.array(x_labels), new_y1, kind='cubic')
                smooth_y = f(arr_x)
                plt.plot(arr_x, smooth_y , marker=markers1[0], color=colors1[0],ls='-.',markerfacecolor='none')
                plt.plot(arr_x, new_y2, marker=markers1[1], color=colors[1])
                plt.fill_between(arr_x, smooth_y, new_y2, interpolate=False, facecolor='cornflowerblue', alpha=0.7)
                #cornflowerblue
            elif sheet=='sheet8':
                if i==0:
                    avg_y_list=[]
                    for rid, row in enumerate(ref_data):
                        avg_y=row/query_size
                        avg_y_list.append(avg_y)
                        # avg_y_list.append([cell/query_size[cell_id] for cell_id,cell in enumerate(row)])
                        plt.plot(x_labels,avg_y, marker=markers[rid], color=colors[rid],markerfacecolor='none')
                    new_average_diff=[cell/query_size[cell_id] for cell_id,cell in enumerate(ref_data[1]-ref_data[0])]
                    plt.fill_between(x_labels, avg_y_list[0], avg_y_list[1], interpolate=False, facecolor='cornflowerblue',
                                     alpha=0.2)

                    plt.ylim(bottom=0.55,top=1.1)
                    # print()
                    # ax2 = plt.twinx()
                    # ax2.plot(x_labels,new_average_diff)
                    # ax2.set_ylabel("difference", color='b')
                else:
                    plt.bar(x_labels*2-0.25,ref_data[0],color=colors[0],width=0.5)
                    plt.bar(x_labels*2+0.25,ref_data[1],color=colors[1],width=0.5)
                    plt.legend(methods, ncol=len(methods), frameon=False)
            elif sheet=='sheet4':
                for rid, row in enumerate(ref_data):
                    plt.plot(x_labels,row, marker=markers[rid], color=colors[rid],markerfacecolor='none')

            if i==0:
                if sheet == 'sheet8':
                    plt.ylabel('Latency Per Query(s)')
                elif sheet == 'sheet7':
                    plt.ylabel('Query Latency Difference(s)')
                else:
                    plt.ylabel('Total Query Latency(s)')
            else:
                if sheet == 'sheet4':
                    plt.ylim(top=600)
                # if sheet == 'sheet7':
                #     # plt.fill_between(x_labels, ref_data[0], ref_data[1], where=ref_data[1] <= ref_data[0], interpolate=False, facecolor='cornflowerblue', alpha=0.7)
                #     new_y1=ref_data[0] - ref_data[1]
                #     new_y2=
                #     plt.plot(x_labels, new_y1, marker=markers1[0], color=colors[0], ls='--', markerfacecolor='none')
                #     plt.plot(x_labels, new_y1, marker=markers1[0], color=colors[0], ls='--', markerfacecolor='none')
                #     plt.fill_between(x_labels, new_y1,[0 for _ in range(len(ref_data[0]))], where=ref_data[1] <= ref_data[0], interpolate=False, facecolor='cornflowerblue', alpha=0.7)
                #     plt.ylabel('Repartition Time Difference')
                if sheet!='sheet7':
                    plt.ylabel('Total Repartition Time(s)')
                else:
                    plt.ylabel('Repartition Time Difference')
                # plt.ylim(bottom=0)
            if sheet=='sheet7':
                plt.legend(['Diff.(Feedback,PPO)'], ncol=1,frameon=False)
            else:
                plt.legend(methods, ncol=len(methods),frameon=False)
            plt.grid()
            if sheet == 'sheet4':
                plt.xlabel('Workload Size')
            if sheet == 'sheet8':
                plt.xlabel('Workload Arrival Rate')
                if i==1:
                    plt.xticks(ticks=[x*2 for x in range(1,len(ref_data[0])+1)], labels=x_labels, ha='left')
            elif sheet == 'sheet7':
                plt.xlabel('Data Size (tuples)')
                plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')
            # plt.xticks(ticks=[x for x in range(8)], labels=[(x+1)*300 for x in range(8)])

        # plt.show()
        # plt.savefig(f'chart/scaling_workload_size2.png', bbox_inches='tight')
        plt.savefig(f'chart/scaling_workload_arrival_rate3.pdf', bbox_inches='tight')
        # plt.savefig(f'chart/scaling_data_size.pdf', bbox_inches='tight')

def draw_selectivity_scalability():
    plt.figure(figsize=(10, 3))
    chart_dict = read_csv('PG数据库实验.xlsx', 'sheet6')
    datasets = chart_dict['row_names']
    methods = chart_dict['column_names']
    # colors = ['#5cb3cc', '#c04851']
    colors = ['#007BFF', '#c04851']#5390fe
    data = chart_dict['data']
    sel_list=[round(0.1*x,1) for x in range(1,11)]
    phases = [[0, 10], [10, 20]]
    # markers = ['s', '*']
    markers = ['v', 'o']
    arr_sel=np.array(sel_list)
    arr_x=np.linspace(min(arr_sel),max(arr_sel),300)
    sample_idx=[x*int(len(arr_x)/15) for x in range(1,16)]
    lines=[]
    for i in range(2):
        plt.subplot(1, 2, i + 1)
        plt.xticks(fontproperties='DejaVu Sans', size=7)
        plt.yticks(fontproperties='DejaVu Sans', size=7)
        phase = phases[i]
        for rid, row in enumerate(data[phase[0]:phase[1]].T):
            if i == 0:
                arr_y=np.array(row)
                f=interpolate.interp1d(arr_sel, arr_y, kind='cubic')
                smooth_y=f(arr_x)
                handle,=plt.plot(arr_x, smooth_y, color=colors[rid])
                lines.append(handle)
                for sam_idx in sample_idx:
                    plt.plot(arr_x[sam_idx-1], smooth_y[sam_idx-1], color=colors[rid],marker=markers[rid], markerfacecolor='none')
                # plt.plot(sel_list, row, marker=markers[rid], color=colors[rid])
            else:
                plt.bar([str(sel) for sel in sel_list], row, color=colors[rid], width=0.35)
            # if i==0:
            #     plt.plot(sel_list, row, marker=markers[rid], color=colors[rid])
            # else:
            #     if rid==1:
            #         plt.bar([x*2 for x in range(len(sel_list))], row, color=colors[rid],width=0.4)
            #     else:
            #         plt.bar([x*2+1 for x in range(len(sel_list))], row, color=colors[rid],width=0.4)
        plt.xlabel('Workload Selectivity')
        if i == 0:
            # plt.title('(a) Total Repartition Latency(s)')
            plt.ylabel('Total Repartition Latency(s)')
            plt.legend(handles=lines,labels=methods.tolist(),ncol=len(methods),frameon=False)
            # plt.legend(methods, ncol=len(methods))
        else:
            # plt.ylim(top=600)
            # plt.title('(b) Optimization Time(s)')
            plt.ylabel('Optimization Time(s)')
            plt.legend(methods,ncol=len(methods),frameon=False)
        # plt.title('Scaling workload selectivity')
        plt.grid()
    # plt.show()
    plt.savefig(f'chart/scaling_sel3.pdf', bbox_inches='tight')

def draw_time_overhead():
    plt.figure(figsize=(10, 4))
    # 包括分区收益和重分区成本
    chart_dict = read_csv('PG数据库实验.xlsx', 'sheet3-1')
    datasets = chart_dict['row_names']
    workload_names = ['Synthetic', 'TPC-H', 'TPC-DS']
    methods = chart_dict['column_names']
    data = chart_dict['data']
    colors = ['#00CD66', '#464547', '#007BFF', '#FF7F50', '#6C757D']

    for i in range(10):
        plt.subplot(2,5,i+1)
        sorted_data_row = sorted(data[i].copy())
        for cid,cell in enumerate(data[i]):
            rects=plt.bar(cid,cell,color=colors[cid],edgecolor='black',width=0.9,hatch='//')
            rect=rects[0]
            plt.annotate('{}'.format(sorted_data_row.index(cell)+1),
                        xy=(rect.get_x() + rect.get_width() / 2, rect.get_height()),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
        if max(data[i])<100:
            if i==5:
                plt.ylim(top=max(data[i])+2)
            elif i==6:
                plt.ylim(top=max(data[i])+1.5)
            else: plt.ylim(top=max(data[i])+35)
        # plt.xticks(ticks=range(len(data[i])),labels=['%d' % (sorted_data_row.index(e)+1) for e in data[i]])
        plt.xlabel(datasets[i])
        plt.xticks(ticks=[x for x in range(len(methods))], labels=['' for _ in range(len(methods))])
        if i==0:
            plt.legend(methods,bbox_to_anchor=[3.5, 1], loc='lower center',frameon=False,ncol=len(methods))
        if i==0:
            plt.ylabel('Optimization Time(s)')
        # plt.legend(methods)
        # plt.grid()

    plt.subplots_adjust(hspace=0.3, wspace=0.4)
    # plt.show()
    plt.savefig(f'chart/time_overhead2.pdf', bbox_inches='tight')


def accumulate_val(data,interval):
    new_data=[]
    temp_data=[]
    for idx,x in enumerate(data):
        temp_data.append(x)
        if (idx+1)%interval==0:
            new_data.append(sum(temp_data))
            temp_data.clear()
    new_data.append(sum(temp_data))
    return new_data

def draw_rep_latency():
    a=[177.16,170.93,179.71,706.81,266.91,228.16,125.64,180.87]
    b=[9.64,10.89,65.3,213.16,104.26,88.42,104.31,114.8]
    titles=[1500,3000,1300,4000,1200,1350,1600,2600]
    labels = ['pid', 'ppo-controller']
    plt.figure(figsize=(10, 5))

    for i in range(len(titles)):
        plt.subplot(int(f'{2}{4}{i + 1}'))
        plt.bar(labels, [a[i],b[i]],color=['#007BFF','#FF7F50'],width=0.4)
        plt.text(labels[0],a[i]+0.05,str(a[i]),ha='center',va='bottom')
        plt.text(labels[1],b[i]+0.05,str(b[i]),ha='center',va='bottom')
        plt.title(f'TPC-{titles[i]}',fontdict={'fontsize':10})
        plt.ylim(0,max(a[i],b[i])+70)
        if i==0 or i==4:
            plt.ylabel('Repartition Latency(s)', loc='center')
    plt.subplots_adjust(hspace=0.4,wspace=0.4)
    # plt.show()
    plt.savefig('chart/rep_latency.svg')

def draw_latency_throughput():
    latency_data={
        'SY1500':(
            [33.1, 15.652, 160.078, 138.552, 30.618, 154.41, 21.821, 195.442, 25.842, 28.277, 2.38, 2.781, 1.456, 14.311, 3.876, 6.433, 0.556, 34.842, 32.919, 24.842, 6.785, 36.702, 38.23, 31.873, 26.357, 11.858, 6.249, 11.462, 1.747, 6.619, 16.983, 21.529, 12.397, 96.474, 19.252, 25.703, 27.953, 13.77, 9.938, 2.207, 3.567, 3.899, 2.748, 6.789, 30.963, 21.332, 17.101, 35.975, 47.976, 17.724, 27.769, 18.231, 11.105, 17.432, 12.658, 13.939, 22.643, 14.059, 4.34, 2.769, 4.203, 10.337, 31.751, 61.494, 20.941, 31.686, 21.364, 24.122, 27.695, 6.96, 8.774, 6.803, 5.031, 4.207, 2.756, 29.914, 16.375, 47.827, 48.848, 29.13, 11.633, 42.58, 25.307, 12.62, 4.458, 1.09, 0.511, 4.811, 1.109, 7.744, 0.917, 23.816, 18.475, 16.117, 32.637, 31.164, 13.271, 33.061, 9.043, 34.984, 0.414, 19.439, 5.448, 2.524, 29.015, 5.521, 17.527, 20.81, 29.143, 24.047, 37.223, 10.98, 36.945, 7.268, 4.606, 8.559, 2.903, 4.179, 6.529, 31.457, 5.38, 52.085, 13.968, 31.111, 19.552, 11.598, 19.576, 5.251, 7.949, 5.477, 15.488, 5.984, 8.019, 21.768, 14.921, 13.77, 51.22, 71.538, 4.166, 46.316, 14.432, 4.647, 4.352, 1.328, 11.5, 22.269, 15.439, 50.114, 21.811, 21.521, 40.368, 29.045, 34.377, 13.189, 17.221, 25.602, 2.233, 5.508, 7.121, 33.593, 16.812, 11.187, 40.655, 24.377, 47.837, 28.9, 23.963, 20.946, 29.292, 23.062, 13.928, 20.725, 36.431, 29.34, 19.443, 57.294, 13.407, 28.642, 9.395, 39.816, 4.667, 2.894, 2.239, 8.879, 4.078, 9.029, 14.322, 4.255, 28.769, 12.592, 8.654, 42.843, 47.33, 43.351, 31.135, 25.887, 12.011, 19.449, 15.63, 10.049, 2.702, 10.077, 6.719, 5.111, 40.269, 13.097, 25.216, 30.844, 26.834, 31.896, 31.349, 27.433, 19.252, 16.924, 17.307, 12.318, 11.813, 9.518, 19.649, 0.861, 15.042, 8.355, 1.222, 25.898, 7.273, 7.142, 3.232, 2.275, 10.626, 5.854, 22.157, 14.946, 9.483, 12.734, 16.106, 14.436, 14.213, 1.273, 4.073, 1.678, 9.248, 12.361, 4.534, 4.797, 4.41, 18.518, 33.175, 13.542, 9.865, 10.736, 2.697, 0.543, 2.301, 0.837, 2.439, 6.903, 10.954, 6.049, 20.074, 1.929, 9.506, 35.095, 3.768, 21.382, 9.04, 14.235, 5.206, 2.875, 1.36, 0.269, 0.546, 2.464, 2.579, 21.366, 5.91, 24.403, 30.284, 28.378, 8.586, 9.807, 3.253, 8.344, 0.842, 3.726, 17.573, 32.541, 4.777, 22.19, 23.627, 19.856, 13.203, 5.662, 7.13, 2.295, 0.644, 5.375, 6.659, 31.524, 4.683, 12.292, 28.496, 20.964, 13.895, 10.654, 9.267, 0.545, 1.226, 0.27, 1.871, 5.468, 0.675, 35.351, 16.788, 15.329, 5.325, 12.736, 18.693, 17.652, 17.407, 5.595, 14.808, 2.139, 11.265, 14.742, 15.477, 10.989, 10.378, 16.967, 9.888, 13.207, 17.195, 0.929, 3.071, 0.824, 15.688, 8.971, 6.869, 20.504, 18.756, 26.208, 10.811, 23.344, 14.535, 6.81, 1.627, 2.037],
            [32.795, 15.616, 158.184, 136.904, 29.483, 190.191, 16.337, 168.864, 28.11, 50.733, 1.92, 2.762, 1.477, 10.802, 3.922, 3.677, 0.351, 28.797, 28.765, 21.759, 7.386, 28.736, 33.882, 27.173, 26.939, 9.45, 5.231, 9.133, 1.038, 4.271, 13.419, 16.391, 9.314, 70.346, 18.078, 20.701, 30.183, 12.705, 8.274, 1.332, 4.125, 2.909, 2.059, 5.528, 29.721, 21.237, 18.999, 31.424, 41.096, 15.209, 25.498, 13.716, 8.179, 16.538, 13.773, 9.619, 16.925, 13.154, 3.066, 2.057, 3.145, 9.883, 23.64, 40.177, 20.975, 31.715, 21.348, 24.206, 27.832, 7.02, 8.757, 6.908, 4.986, 4.157, 2.724, 29.95, 16.305, 47.726, 47.82, 20.825, 9.884, 40.344, 22.598, 9.521, 3.72, 1.658, 0.449, 4.182, 0.764, 3.916, 0.611, 19.697, 17.793, 16.579, 22.278, 27.788, 11.391, 29.486, 7.48, 25.522, 0.413, 15.997, 3.952, 1.901, 21.23, 4.369, 14.753, 18.957, 24.506, 24.8, 29.78, 6.7, 28.655, 11.451, 2.28, 11.332, 3.193, 4.924, 7.249, 25.45, 4.821, 51.132, 12.473, 24.724, 16.585, 12.194, 15.164, 6.561, 6.299, 4.821, 14.269, 5.305, 6.718, 15.309, 12.02, 11.823, 32.074, 59.275, 3.091, 47.365, 14.427, 3.499, 4.856, 0.604, 9.921, 19.168, 14.309, 43.567, 14.167, 19.048, 28.66, 24.943, 29.102, 11.897, 14.952, 23.039, 2.758, 4.613, 8.473, 28.213, 13.238, 8.013, 25.265, 24.395, 39.111, 24.097, 22.567, 15.468, 19.848, 16.221, 11.063, 26.467, 27.519, 25.576, 14.239, 51.038, 11.423, 25.923, 9.401, 27.111, 4.007, 3.876, 2.031, 5.389, 2.195, 6.292, 9.698, 4.195, 23.956, 10.181, 6.295, 27.272, 45.239, 31.218, 27.56, 21.109, 9.487, 14.402, 12.001, 6.167, 2.066, 8.364, 4.201, 3.605, 32.695, 10.781, 23.389, 25.41, 23.321, 23.416, 26.54, 16.843, 21.539, 13.934, 17.282, 11.672, 11.764, 8.695, 19.68, 0.857, 15.058, 8.499, 1.21, 25.924, 7.286, 7.117, 3.167, 2.313, 10.563, 5.869, 22.061, 14.995, 9.55, 12.79, 16.059, 14.406, 13.62, 1.273, 4.074, 1.69, 9.254, 12.365, 4.545, 4.754, 4.427, 18.543, 31.975, 13.471, 9.907, 10.757, 2.751, 0.534, 2.294, 0.815, 2.443, 6.939, 9.959, 6.057, 20.159, 1.864, 9.46, 34.802, 3.798, 21.247, 9.72, 12.971, 5.252, 2.851, 1.344, 0.273, 0.539, 2.408, 2.573, 21.361, 5.806, 24.494, 28.91, 27.507, 8.416, 9.941, 3.276, 8.356, 0.831, 3.747, 20.511, 33.637, 4.651, 20.89, 21.662, 18.709, 12.504, 6.399, 7.141, 2.287, 0.64, 5.374, 6.678, 30.665, 3.538, 12.212, 25.73, 23.666, 13.785, 10.765, 9.237, 0.542, 1.201, 0.267, 1.901, 5.449, 0.684, 35.342, 15.538, 15.259, 5.286, 11.262, 18.542, 14.985, 19.684, 4.591, 14.712, 2.138, 11.231, 10.457, 16.336, 12.41, 10.394, 16.873, 9.828, 13.328, 17.141, 0.939, 3.125, 0.823, 16.853, 8.942, 6.81, 20.862, 18.821, 26.037, 10.81, 23.294, 14.589, 6.639, 1.611, 1.987]
        ) ,
        # 'SY3000':(
        #     [25.568, 12.071, 10.437, 30.699, 192.666, 174.784, 96.082, 56.291, 190.298, 71.402, 212.629, 13.359, 180.792, 202.128, 9.081, 0.551, 24.291, 37.859, 50.173, 63.407, 72.232, 20.085, 64.057, 53.881, 90.168, 7.882, 13.748, 10.137, 12.517, 9.688, 1.671, 12.57, 2.504, 13.914, 29.575, 60.726, 45.378, 81.976, 92.399, 45.431, 47.874, 42.875, 22.742, 12.863, 3.335, 11.114, 6.181, 3.259, 1.078, 5.301, 7.532, 17.534, 21.138, 54.207, 104.658, 46.321, 105.562, 79.276, 25.706, 48.661, 30.817, 5.7, 7.305, 17.252, 15.549, 6.017, 4.637, 15.333, 39.467, 49.294, 60.802, 31.045, 85.101, 37.446, 48.14, 69.2, 36.571, 35.837, 8.858, 5.217, 3.782, 26.014, 4.377, 18.042, 40.899, 68.143, 109.158, 53.3, 77.016, 54.025, 20.693, 36.472, 51.092, 1.841, 9.095, 4.864, 4.081, 1.885, 6.846, 16.248, 26.065, 47.953, 46.861, 29.429, 137.379, 115.293, 67.787, 30.844, 36.059, 7.594, 3.601, 10.161, 16.255, 3.835, 11.952, 1.878, 2.081, 4.783, 11.037, 70.381, 42.779, 35.945, 55.619, 45.724, 30.427, 53.914, 26.058, 26.434, 1.181, 25.736, 5.879, 5.516, 7.667, 4.728, 28.241, 42.503, 50.969, 77.147, 54.65, 47.93, 71.408, 92.33, 53.571, 12.377, 18.697, 2.819, 15.071, 7.523, 2.243, 29.09, 20.79, 73.567, 60.823, 90.959, 45.289, 71.059, 39.756, 36.095, 14.394, 10.724, 17.321, 32.677, 15.856, 6.09, 4.539, 52.175, 31.963, 82.956, 68.518, 62.422, 67.109, 43.882, 42.232, 27.264, 30.755, 7.713, 2.435, 6.276, 7.066, 15.182, 36.729, 61.613, 22.977, 49.758, 71.083, 63.688, 40.072, 23.561, 13.558, 8.115, 5.332, 7.701, 17.144, 34.317, 24.915, 57.457, 45.558, 44.635, 39.553, 40.478, 39.472, 36.216, 33.67, 23.851, 7.504, 2.523, 4.554, 13.244, 15.091, 57.821, 52.226, 66.631, 71.753, 46.635, 81.301, 48.158, 41.296, 37.052, 9.178, 21.224, 36.32, 4.916, 4.086, 5.038, 2.481, 20.734, 49.739, 55.967, 62.239, 41.359, 47.058, 54.964, 63.8, 47.134, 24.744, 25.525, 2.753, 4.915, 1.857, 11.26, 14.995, 18.336, 48.694, 36.727, 35.637, 27.324, 25.208, 15.737, 18.19, 11.887, 7.78, 6.79, 8.488, 2.855, 1.619, 6.025, 13.612, 10.249, 14.856, 34.684, 60.57, 38.122, 27.414, 17.914, 16.008, 15.246, 4.7, 9.812, 2.453, 0.931, 2.356, 1.601, 26.668, 20.154, 33.199, 37.918, 30.338, 23.743, 17.212, 26.754, 15.459, 13.3, 0.404, 2.831, 1.77, 5.968, 6.79, 19.949, 11.08, 35.485, 17.657, 44.362, 54.199, 38.332, 32.574, 21.317, 8.47, 1.677, 3.025, 2.155, 4.491, 0.136, 2.525, 5.214, 3.839, 16.809, 32.083, 52.995, 46.112, 36.497, 33.04, 10.969, 4.094, 10.239, 3.394, 5.865, 1.785, 10.989, 3.983, 7.328, 19.802, 26.096, 58.408, 21.398, 29.987, 25.893, 12.934, 38.964, 14.381, 4.089, 13.718, 1.635, 2.007, 2.904, 2.436, 5.387, 13.129, 15.686, 49.7, 46.016, 17.99, 33.632, 33.582, 29.171, 15.512, 10.944, 3.412, 2.438, 2.289, 0.819, 6.306, 13.025, 24.859, 29.617, 24.922, 17.254, 17.459, 35.726, 40.685, 29.16, 4.004, 4.474, 1.146, 2.522, 2.696, 13.98, 12.265, 29.634, 30.396, 12.99, 46.009, 17.741, 19.435, 43.894, 11.945, 4.204, 9.213, 0.813, 1.758, 1.435, 4.798, 3.805, 16.144, 31.167, 10.246, 20.178, 37.791, 61.963, 33.065, 10.454, 10.479, 0.981, 8.223, 1.64],
        #     [25.729, 14.08, 10.499, 31.373, 133.603, 205.766, 83.195, 42.479, 146.851, 52.645, 165.33, 15.538, 181.539, 262.75, 9.179, 0.415, 25.421, 35.96, 48.891, 60.468, 59.92, 19.992, 54.066, 47.377, 91.805, 8.197, 14.262, 7.207, 10.759, 6.855, 1.651, 9.39, 1.656, 10.016, 22.365, 56.275, 45.155, 75.855, 92.324, 42.17, 44.782, 36.352, 22.293, 12.846, 2.78, 7.788, 3.086, 3.344, 0.833, 8.113, 7.557, 9.055, 17.502, 41.433, 88.609, 40.801, 84.359, 62.768, 26.298, 50.924, 31.54, 5.794, 4.319, 11.959, 9.426, 4.661, 4.678, 11.139, 32.429, 40.354, 51.593, 30.76, 84.104, 33.966, 46.164, 60.502, 33.251, 20.068, 6.744, 2.799, 2.879, 19.57, 3.335, 13.774, 36.036, 59.285, 117.871, 48.977, 63.876, 54.174, 18.303, 24.719, 37.989, 1.886, 8.203, 6.203, 3.112, 1.44, 4.99, 9.565, 24.026, 34.513, 45.278, 24.205, 110.182, 81.252, 64.726, 29.605, 39.729, 6.955, 2.722, 9.402, 15.438, 3.697, 12.013, 1.858, 2.074, 4.778, 13.316, 64.575, 43.107, 38.441, 55.694, 48.691, 30.623, 53.363, 27.484, 18.32, 1.08, 25.701, 5.544, 4.103, 5.346, 3.881, 17.469, 50.094, 45.003, 66.581, 49.82, 43.554, 70.404, 66.867, 50.069, 9.005, 15.669, 4.687, 9.414, 5.704, 1.509, 21.356, 17.38, 58.102, 51.9, 78.036, 42.888, 56.498, 46.091, 34.302, 12.432, 9.865, 13.795, 28.192, 12.711, 3.306, 6.808, 43.404, 29.957, 65.495, 68.449, 55.41, 67.225, 43.815, 42.136, 27.13, 31.266, 7.652, 2.416, 6.289, 7.089, 15.113, 36.62, 61.562, 22.968, 49.592, 70.38, 63.02, 38.462, 20.594, 13.638, 8.14, 5.345, 7.587, 17.177, 40.542, 24.832, 56.854, 47.748, 44.692, 41.154, 42.543, 37.048, 33.307, 29.422, 29.215, 5.026, 2.101, 3.961, 9.629, 10.079, 46.169, 43.083, 64.96, 67.184, 40.202, 79.211, 41.132, 34.019, 38.339, 9.99, 19.318, 28.332, 4.436, 3.104, 3.342, 1.695, 13.459, 47.148, 56.647, 69.742, 33.707, 46.932, 49.872, 53.174, 48.409, 20.802, 21.598, 2.054, 3.349, 1.884, 11.204, 15.05, 18.519, 48.614, 30.92, 39.076, 27.36, 25.018, 15.025, 16.54, 11.652, 7.845, 4.501, 8.609, 2.783, 1.629, 5.786, 13.133, 9.723, 14.934, 29.761, 60.694, 35.127, 27.5, 17.872, 16.095, 15.29, 4.596, 9.798, 2.472, 0.947, 2.359, 1.606, 26.82, 20.257, 22.665, 37.664, 30.432, 23.533, 16.774, 26.38, 14.712, 13.19, 0.411, 2.853, 1.74, 6.019, 6.794, 19.834, 11.16, 34.353, 17.632, 43.611, 52.45, 36.684, 32.642, 17.347, 8.406, 1.97, 2.935, 2.195, 4.507, 0.137, 2.518, 5.204, 3.836, 16.91, 32.917, 53.769, 42.994, 36.306, 30.383, 10.946, 4.1, 10.271, 3.397, 5.883, 1.769, 10.821, 3.832, 7.585, 19.919, 25.966, 58.096, 21.437, 29.943, 25.955, 11.757, 38.645, 14.447, 4.196, 16.718, 1.64, 2.008, 2.945, 2.46, 5.488, 13.196, 15.822, 48.563, 44.966, 18.007, 33.332, 36.136, 28.13, 16.361, 10.904, 3.396, 2.43, 2.269, 0.817, 6.237, 13.063, 24.888, 29.424, 24.901, 17.242, 17.495, 35.395, 38.842, 29.111, 4.096, 4.434, 1.151, 2.512, 2.713, 13.948, 13.646, 30.143, 31.929, 13.044, 46.758, 17.66, 19.383, 44.537, 12.001, 4.242, 9.379, 0.805, 1.755, 1.431, 4.816, 3.893, 16.277, 31.076, 10.187, 20.094, 37.968, 62.173, 33.008, 10.505, 10.457, 0.979, 8.333, 1.646]
        # ),
        # 'SY1300':(
        #     [106.377, 8.386, 30.448, 59.217, 75.081, 86.58, 151.929, 104.143, 43.956, 113.331, 50.826, 77.989, 44.228, 15.532, 24.909, 11.005, 13.96, 9.278, 22.5, 64.595, 120.619, 136.911, 71.457, 101.429, 93.416, 61.87, 51.336, 25.509, 52.14, 11.302, 2.777, 0.822, 26.541, 24.425, 38.743, 65.267, 55.599, 157.325, 97.182, 67.99, 66.781, 53.695, 22.515, 28.131, 9.1, 6.799, 6.623, 66.394, 39.073, 140.966, 125.1, 313.404, 377.849, 569.318, 402.427, 424.468, 313.517, 362.193, 156.263, 109.892, 156.013, 55.438, 12.907, 10.193, 26.667, 7.922, 18.749, 91.211, 201.409, 132.849, 133.329, 241.073, 162.892, 179.572, 29.369, 47.236, 27.502, 20.141, 48.499, 12.86, 22.319, 26.474, 7.715, 48.213, 68.089, 128.626, 36.134, 131.62, 135.65, 125.407, 152.698, 108.426, 42.749, 82.098, 22.107, 37.787, 29.993, 13.313, 13.662, 4.42, 14.286, 27.056, 69.794, 89.278, 104.162, 106.545, 164.219, 151.257, 111.894, 101.033, 88.274, 48.231, 75.408, 0.738, 30.124, 12.052],
        #     [106.177, 8.541, 30.803, 59.108, 79.577, 69.805, 165.573, 105.166, 49.0, 102.753, 35.047, 67.981, 30.127, 10.745, 29.82, 9.688, 10.481, 10.104, 15.878, 64.745, 105.914, 105.189, 68.396, 107.209, 102.368, 52.176, 52.938, 29.092, 50.622, 8.576, 3.299, 0.938, 22.173, 15.073, 27.591, 56.279, 54.672, 155.247, 107.385, 78.507, 73.172, 52.759, 22.297, 24.716, 7.066, 4.405, 5.031, 54.425, 40.216, 113.217, 126.524, 328.681, 352.911, 538.609, 416.91, 421.214, 325.446, 368.559, 149.66, 117.016, 134.764, 56.774, 14.371, 7.16, 26.046, 8.702, 22.299, 71.426, 188.047, 138.563, 124.742, 227.452, 157.367, 173.256, 29.421, 46.781, 29.127, 26.281, 26.965, 11.532, 24.167, 20.724, 5.454, 33.764, 71.928, 143.697, 40.959, 112.645, 132.267, 115.904, 157.758, 91.256, 51.588, 67.863, 25.086, 29.788, 26.028, 11.337, 11.003, 2.237, 9.245, 24.293, 69.066, 85.198, 110.626, 113.497, 154.784, 139.83, 120.375, 102.417, 90.776, 42.703, 73.811, 0.688, 17.894, 7.761]
        # ),
        'SY4000':(
            [47.818, 44.248, 551.639, 84.614, 67.59, 180.734, 106.025, 468.59, 428.369, 426.043, 84.81, 43.817, 94.021, 493.991, 41.475, 17.685, 33.056, 15.13, 46.732, 138.075, 135.059, 171.578, 158.394, 86.059, 146.97, 68.472, 66.377, 39.257, 18.09, 5.443, 13.445, 7.001, 18.07, 37.182, 117.19, 120.898, 98.519, 157.007, 176.658, 122.744, 89.012, 44.183, 69.655, 91.288, 8.098, 6.771, 13.662, 10.724, 5.161, 36.212, 98.366, 129.888, 189.135, 133.809, 124.9, 103.596, 133.989, 108.274, 39.083, 76.183, 46.568, 8.753, 2.919, 2.464, 1.766, 25.521, 60.778, 121.426, 83.104, 124.971, 126.188, 168.745, 59.972, 103.441, 134.607, 13.803, 8.29, 14.458, 11.146, 9.717, 79.243, 73.884, 86.623, 129.295, 158.582, 136.973, 86.402, 164.303, 55.206, 7.857, 2.312, 43.5, 19.677, 15.885, 6.532, 22.819, 37.503, 55.309, 49.461, 113.68, 140.142, 115.92, 64.499, 137.679, 59.771, 171.91, 57.242, 38.43, 40.831, 0.828, 33.845, 8.236, 8.659, 107.184, 118.335, 169.728, 125.636, 83.217, 133.598, 180.198, 38.428, 69.707, 54.392, 70.677, 9.097, 2.496, 13.32, 27.601, 24.063, 122.578, 108.038, 133.0, 217.712, 86.552, 100.774, 140.531, 48.32, 89.93, 57.711, 65.834, 9.217, 5.853, 9.345, 56.557, 46.052, 79.802, 137.913, 184.91, 185.855, 133.299, 90.131, 106.822, 45.952, 66.871, 80.552, 26.242, 1.477, 8.431, 8.666, 70.458, 47.913, 167.335, 215.227, 141.998, 68.085, 150.526, 133.943, 92.959, 66.523, 20.86, 3.91, 14.935, 0.676, 2.489, 14.517, 48.524, 69.647, 31.984, 151.999, 181.819, 150.726, 163.732, 66.384, 78.445, 73.934, 59.147, 28.843, 4.043, 2.418, 33.485, 20.236, 23.039, 50.497, 105.833, 85.323, 201.898, 85.646, 178.435, 127.955, 137.196, 52.337, 58.347, 17.538, 17.501, 13.77, 13.863, 44.09, 122.93, 26.9, 87.32, 135.393, 147.44, 95.816, 154.242, 159.071, 82.57, 57.814, 15.832, 29.612, 15.185, 2.956, 25.179, 84.696, 89.795, 120.516, 107.685, 86.136, 158.501, 132.516, 98.253, 59.314, 30.705, 65.712, 9.443, 34.518, 14.382, 6.523, 10.319, 51.295, 53.341, 179.334, 155.384, 149.353, 187.322, 123.635, 183.663, 103.146, 37.029, 12.4, 7.303, 5.528, 5.06, 6.636, 32.47, 6.719, 13.645, 67.753, 125.54, 109.496, 196.004, 122.988, 197.899, 88.82, 90.54, 44.736, 22.045, 16.146, 63.306, 4.022, 7.003, 39.998, 47.904, 148.731, 58.797, 162.445, 111.032, 116.118, 191.507, 99.288, 37.574, 74.687, 34.69, 11.745, 17.152, 5.566, 29.306, 6.726, 20.116, 63.163, 107.405, 145.01, 67.188, 244.289, 124.08, 152.989, 164.591, 64.059, 62.945, 29.961, 21.79, 51.109, 1.22, 4.321, 1.888, 1.703, 20.017, 65.363, 118.416, 76.128, 174.838, 141.754, 123.218, 177.943, 124.726, 63.096, 20.875, 68.099, 38.307, 55.217, 57.468, 96.233, 99.422, 139.822, 153.093, 215.473, 137.747, 110.923, 79.542, 54.324, 54.381, 21.316, 9.864, 5.6, 6.64, 20.164, 11.238, 113.791, 91.512, 183.44, 91.192, 167.85, 90.679, 179.591, 67.563, 40.438, 25.966, 17.862, 4.963, 2.207, 2.095, 13.284, 61.545, 55.686, 83.793, 130.492, 66.356, 136.542, 196.316, 99.353, 144.663, 102.856, 65.512, 10.236, 8.079, 45.774, 2.184, 5.403, 4.432, 74.087, 22.836, 126.839, 185.57, 99.098, 153.424, 145.837, 140.643, 69.379, 62.858, 30.194, 68.639, 30.587, 26.522, 3.545, 37.956, 92.092, 56.968, 113.95, 94.977, 105.597, 194.346, 118.625, 69.084, 145.747, 159.159, 75.684, 29.834, 14.151, 17.213, 0.948, 2.242],
            [47.442, 47.883, 557.052, 73.426, 78.292, 147.73, 100.155, 488.589, 419.163, 430.128, 92.987, 44.318, 82.349, 562.091, 39.32, 16.6, 35.999, 17.246, 49.198, 152.206, 133.725, 177.492, 146.945, 93.268, 149.766, 71.57, 67.49, 34.204, 13.766, 2.727, 12.904, 3.885, 12.685, 31.01, 92.704, 114.094, 94.948, 134.992, 156.823, 126.024, 83.139, 39.386, 67.232, 79.683, 9.844, 6.101, 9.798, 9.583, 4.956, 34.786, 82.901, 133.614, 194.315, 116.294, 111.64, 103.134, 105.317, 106.674, 40.941, 63.381, 41.424, 11.596, 3.204, 3.488, 1.382, 27.107, 57.321, 126.46, 84.449, 109.474, 158.046, 154.482, 64.861, 111.857, 132.411, 17.428, 6.013, 10.743, 7.166, 9.09, 73.5, 80.562, 100.838, 136.779, 173.957, 156.597, 95.582, 189.659, 71.248, 10.044, 2.904, 45.127, 17.938, 14.502, 11.341, 30.1, 33.056, 61.724, 45.615, 122.014, 136.031, 97.72, 67.211, 133.004, 58.358, 143.202, 48.683, 31.598, 39.149, 0.63, 26.066, 5.024, 7.441, 82.902, 96.734, 172.428, 119.613, 75.765, 127.216, 169.466, 43.511, 68.719, 48.407, 55.091, 9.037, 2.097, 9.446, 17.974, 22.796, 106.749, 107.689, 141.289, 201.938, 93.632, 115.336, 110.79, 55.628, 71.898, 54.981, 58.753, 5.531, 3.786, 4.738, 45.992, 34.751, 65.894, 107.057, 162.42, 174.727, 117.219, 82.149, 96.905, 46.82, 66.465, 82.404, 25.745, 1.501, 11.184, 4.687, 58.861, 44.905, 138.156, 203.416, 122.29, 70.234, 144.463, 130.0, 92.566, 63.733, 28.011, 4.939, 11.216, 1.044, 1.819, 14.548, 35.643, 71.627, 28.482, 135.907, 170.097, 146.992, 146.784, 59.264, 62.281, 77.569, 55.701, 24.8, 3.351, 2.411, 22.577, 16.751, 20.267, 50.121, 111.078, 86.723, 207.904, 73.182, 165.753, 122.143, 137.176, 55.02, 52.051, 19.523, 18.453, 14.966, 15.155, 31.812, 129.504, 27.141, 75.874, 132.672, 154.066, 85.159, 144.147, 153.825, 86.928, 62.26, 12.291, 19.9, 15.84, 3.058, 16.656, 66.632, 86.778, 128.801, 93.681, 79.674, 148.77, 160.017, 96.849, 53.504, 34.235, 54.741, 10.761, 21.317, 15.047, 9.28, 14.66, 45.393, 44.405, 170.815, 154.759, 160.792, 196.926, 111.372, 173.556, 101.762, 36.015, 8.203, 7.348, 2.428, 5.022, 8.727, 24.471, 8.303, 12.008, 65.744, 125.114, 93.988, 188.749, 111.224, 192.587, 94.996, 77.953, 42.795, 24.708, 19.71, 56.24, 4.19, 2.72, 30.688, 40.818, 132.588, 58.285, 157.871, 107.444, 111.638, 165.417, 105.324, 32.029, 73.094, 37.553, 10.492, 9.02, 5.642, 29.59, 6.728, 17.573, 50.05, 100.564, 146.859, 73.429, 191.181, 105.886, 154.268, 158.496, 56.082, 52.145, 29.661, 19.073, 42.18, 3.143, 3.05, 2.429, 1.103, 17.156, 51.528, 110.503, 78.42, 165.66, 150.993, 117.439, 172.915, 118.711, 49.884, 27.111, 70.101, 29.291, 37.25, 52.315, 97.465, 111.772, 155.628, 144.745, 205.991, 117.148, 84.329, 89.373, 60.574, 37.307, 12.85, 4.947, 9.624, 3.303, 14.052, 10.268, 89.714, 94.64, 179.237, 97.006, 176.932, 79.709, 153.157, 65.281, 42.163, 30.478, 15.07, 3.715, 2.494, 2.921, 13.02, 49.49, 46.751, 84.259, 107.503, 71.408, 106.813, 183.64, 83.343, 136.754, 101.211, 67.938, 13.423, 7.845, 37.789, 2.218, 5.895, 4.867, 79.585, 22.52, 98.574, 174.873, 107.957, 139.087, 122.188, 150.898, 68.416, 58.705, 31.407, 62.176, 25.423, 31.278, 6.006, 39.308, 77.215, 50.68, 119.597, 87.195, 101.394, 174.847, 115.83, 64.778, 136.182, 144.017, 64.872, 23.916, 15.098, 17.101, 1.441, 2.228]
        ),
        'SY1200':(
            [1449.356, 141.929, 126.194, 65.157, 40.083, 124.842, 60.243, 66.516, 57.784, 32.708, 47.564, 12.199, 4.465, 25.182, 33.702, 42.072, 78.817, 129.527, 93.167, 42.847, 43.458, 36.665, 54.176, 35.835, 14.789, 15.26, 11.597, 16.983, 1.874, 36.374, 35.076, 187.122, 73.896, 84.138, 49.899, 27.757, 68.528, 17.649, 13.453, 34.35, 4.875, 18.202, 24.224, 27.685, 45.312, 70.875, 95.903, 88.799, 93.129, 46.449, 43.254, 7.807, 6.758, 1.972, 8.297, 6.499, 1.452, 14.89, 93.59, 81.598, 32.872, 33.941, 47.018, 48.299, 118.622, 39.562, 26.341, 20.885, 63.047, 36.925, 68.726, 57.985, 50.318, 115.345, 71.0, 92.331, 26.159, 9.633, 3.296, 2.692, 40.324, 8.8, 66.275, 39.367, 35.723, 26.952, 116.845, 123.68, 74.225, 76.293, 102.685, 9.172, 34.835, 6.239, 13.63, 80.28, 75.93, 89.033, 53.441, 96.716, 135.869, 44.896, 73.644, 90.657, 10.402, 28.795, 22.946, 17.593, 41.645, 73.516, 24.243, 72.207, 87.385, 80.193, 54.423, 118.175, 30.744, 14.777, 63.497, 18.039, 2.043, 1.885, 52.853, 91.348, 101.214, 43.263, 84.887, 137.024, 87.572, 50.921, 30.205, 11.31, 16.609, 50.623, 13.315, 0.889, 33.491, 32.976, 126.035, 151.946, 218.925, 81.46, 53.35, 39.003, 0.974, 3.958, 1.539, 23.019, 11.136, 41.741, 58.522, 46.894, 40.761, 68.141, 41.683, 4.497, 19.62, 1.428, 2.196, 3.211, 5.303, 26.427, 8.361, 63.386, 39.649, 83.964, 71.953, 31.786, 15.372, 35.03, 24.958, 38.694, 17.792, 1.603, 4.345, 28.331, 21.665, 23.134, 60.919, 38.956, 36.18, 24.339, 72.97, 26.114, 20.444, 57.884, 21.625, 23.391, 6.123, 6.499, 0.497, 5.83, 58.537, 76.876, 35.646, 66.513, 97.442, 52.16, 85.278, 32.061, 45.806, 17.159, 31.886, 53.548, 50.116, 95.774, 126.989, 122.997, 48.564, 70.797, 21.659, 44.166, 32.262, 16.682, 17.327, 24.41, 55.433, 18.07, 16.721, 32.082, 75.902, 121.595, 82.827, 47.883, 82.687, 27.748, 50.11, 13.646, 3.614, 16.452, 9.299, 2.754, 27.572, 47.885, 146.409, 47.66, 44.314, 81.861, 49.35, 43.486, 52.538, 23.389, 40.523, 34.321, 23.626, 96.789, 104.021, 59.691, 20.601, 152.007, 57.479, 43.498, 51.649, 55.771, 2.689, 9.235, 5.257, 3.685, 23.034, 20.997, 65.97, 60.013, 109.347, 125.884, 49.441, 57.702, 141.593, 39.52, 19.683, 4.805],
            [1448.634, 143.159, 126.616, 65.794, 45.26, 137.74, 69.363, 76.142, 56.377, 37.946, 46.332, 16.905, 5.905, 29.712, 32.676, 52.408, 89.292, 117.923, 83.723, 37.579, 41.336, 42.41, 64.051, 36.031, 14.988, 15.265, 12.603, 19.727, 4.298, 46.87, 40.884, 204.966, 73.497, 73.248, 44.369, 21.932, 43.151, 11.724, 7.306, 26.893, 8.33, 23.705, 32.304, 19.863, 47.82, 60.218, 96.266, 89.316, 90.542, 37.256, 36.771, 5.697, 6.694, 3.432, 10.038, 7.427, 2.905, 25.243, 86.376, 83.36, 47.412, 29.639, 49.277, 50.826, 115.976, 41.803, 15.542, 12.617, 62.866, 21.844, 65.941, 45.123, 30.018, 82.696, 62.304, 78.713, 33.655, 8.349, 7.895, 5.372, 38.176, 8.557, 54.58, 32.519, 29.687, 18.113, 96.75, 99.583, 71.275, 82.505, 92.335, 19.803, 34.634, 3.928, 6.206, 70.391, 62.821, 79.017, 53.011, 102.386, 117.586, 40.902, 59.24, 80.12, 10.387, 26.602, 19.541, 10.936, 23.091, 63.489, 17.629, 59.968, 58.24, 76.907, 45.929, 103.881, 40.013, 17.27, 57.218, 15.348, 2.858, 2.465, 52.143, 55.719, 96.557, 42.897, 92.486, 133.985, 87.493, 40.49, 19.273, 6.079, 9.32, 31.221, 7.788, 0.624, 24.039, 35.461, 91.192, 105.204, 188.407, 74.646, 36.551, 41.225, 0.959, 3.873, 1.49, 22.388, 22.9, 45.415, 58.385, 39.623, 46.033, 68.354, 42.814, 3.554, 16.246, 1.384, 2.104, 3.162, 5.143, 26.306, 10.751, 58.904, 42.115, 78.792, 45.742, 23.078, 9.02, 22.954, 22.955, 24.029, 9.769, 1.579, 4.328, 19.909, 32.202, 23.31, 52.236, 44.733, 43.421, 24.537, 61.541, 37.272, 26.006, 62.109, 22.378, 26.737, 7.682, 8.513, 0.49, 5.794, 60.019, 77.175, 34.982, 68.772, 78.53, 44.44, 89.02, 24.936, 38.092, 15.375, 33.136, 44.473, 40.007, 80.529, 122.397, 102.895, 54.467, 81.68, 25.146, 50.205, 34.751, 14.239, 11.325, 18.947, 42.426, 18.962, 22.312, 37.697, 80.1, 101.448, 91.898, 53.433, 79.145, 24.905, 54.637, 11.754, 9.564, 10.687, 13.036, 2.903, 28.597, 47.136, 154.706, 44.847, 52.261, 67.359, 93.685, 43.79, 61.345, 27.625, 39.271, 33.359, 22.796, 83.447, 96.377, 59.49, 26.13, 123.384, 39.998, 43.566, 36.287, 52.819, 5.615, 8.838, 9.585, 6.503, 29.126, 20.967, 54.619, 61.689, 97.078, 148.23, 40.158, 60.92, 139.333, 34.532, 17.597, 1.662]
        ),
        # 'SY1350':(
        #     [525.438, 647.343, 5.344, 25.102, 45.206, 123.991, 49.279, 26.229, 19.944, 52.906, 35.763, 36.428, 48.49, 3.75, 15.186, 32.707, 41.903, 72.29, 54.44, 95.807, 85.191, 94.292, 112.438, 106.506, 77.606, 6.927, 44.379, 27.95, 31.683, 40.743, 19.748, 76.073, 53.032, 60.52, 75.158, 68.924, 96.538, 22.836, 62.389, 85.297, 1.115, 6.07, 19.484, 62.944, 27.954, 22.529, 70.912, 49.806, 66.567, 39.35, 58.649, 58.022, 27.647, 14.258, 14.65, 11.36, 10.001, 20.429, 69.159, 30.152, 83.389, 24.198, 52.986, 71.186, 13.789, 66.401, 35.772, 13.526, 6.808, 2.106, 13.514, 28.987, 33.229, 58.17, 40.078, 50.781, 32.642, 10.282, 66.707, 31.395, 38.196, 18.646, 3.732, 9.141, 7.397, 5.635, 37.465, 31.98, 103.378, 66.422, 43.245, 61.463, 30.085, 27.162, 24.057, 13.313, 13.937, 1.382, 4.444, 4.958, 5.486, 11.698, 37.433, 4.539, 167.783, 86.931, 168.94, 60.734, 36.688, 83.235, 7.212, 6.552, 2.308, 8.108, 16.589, 32.009, 51.151, 14.256, 181.942, 126.711, 52.229, 98.732, 18.546, 39.255, 61.75, 32.322, 11.238, 18.208, 16.121, 59.391, 126.319, 128.432, 150.757, 108.811, 23.675, 97.44, 20.527, 38.143, 18.531, 22.909, 16.296, 112.357, 23.407, 119.688, 42.893, 114.655, 105.93, 84.355, 49.874, 36.464, 15.481, 2.654, 4.297, 2.032, 5.151, 42.195, 25.531, 36.769, 15.313, 42.552, 35.131, 89.417, 59.822, 81.742, 105.268, 17.401, 1.109, 0.269, 2.723, 12.746, 8.865, 56.486, 29.305, 53.528, 59.914, 46.625, 54.58, 42.649, 42.931, 111.222, 29.271, 36.755, 18.223, 18.046, 19.355, 3.556, 20.91, 25.858, 46.174, 6.713, 113.275, 85.877, 67.133, 28.243, 79.455, 54.946, 46.556, 5.008, 13.247, 17.466, 13.897, 14.488, 4.248, 69.853, 32.787, 58.245, 83.437, 155.495, 110.922, 111.376, 72.972, 22.964, 5.575, 12.635, 36.948, 6.413, 0.676, 21.117, 26.733, 84.005, 160.425, 70.398, 100.873, 112.736, 78.636, 9.656, 17.726, 35.212, 9.438, 6.228, 5.565, 3.828, 13.935, 9.39, 4.46, 56.001, 70.462, 44.897, 81.134, 55.579, 141.298, 40.88, 50.406, 22.984, 50.248, 6.654, 14.364, 9.444, 7.79, 1.402, 5.264, 2.126, 56.439, 92.44, 59.557, 190.28, 114.261, 95.854, 61.659, 67.212, 7.102, 11.818, 2.307, 51.421, 71.387, 70.091, 113.611, 73.934, 143.274, 188.543, 75.318, 17.451, 6.096, 1.112, 25.435, 14.436, 78.163, 115.572, 151.498, 71.282, 61.904, 113.831, 37.88, 3.322, 63.678],
        #     [509.832, 721.787, 8.083, 25.875, 46.859, 92.547, 52.733, 24.278, 16.11, 42.531, 33.996, 33.527, 41.084, 2.711, 11.145, 25.169, 31.7, 54.529, 42.572, 97.717, 91.085, 90.447, 86.391, 89.259, 54.331, 4.222, 29.533, 20.613, 27.967, 35.023, 14.434, 70.446, 48.935, 53.859, 74.275, 61.871, 80.336, 29.152, 76.851, 66.276, 0.982, 7.178, 20.991, 37.857, 20.475, 8.952, 77.226, 50.581, 66.439, 31.755, 54.515, 57.918, 20.248, 7.01, 23.488, 11.369, 10.007, 15.712, 58.943, 31.473, 83.851, 26.561, 46.424, 81.403, 13.674, 64.872, 31.625, 14.912, 5.262, 1.587, 9.941, 30.529, 38.479, 53.156, 33.505, 41.76, 33.925, 10.702, 72.661, 20.405, 21.046, 11.629, 5.017, 7.987, 10.023, 5.694, 41.054, 36.192, 95.302, 58.955, 51.898, 56.056, 30.094, 27.245, 24.532, 17.846, 22.382, 1.046, 3.323, 3.695, 4.566, 9.777, 33.661, 3.696, 168.245, 87.259, 199.95, 65.961, 50.165, 95.744, 9.91, 5.893, 3.058, 10.083, 15.855, 37.786, 43.903, 20.641, 196.173, 101.982, 70.058, 101.16, 22.019, 45.461, 75.457, 39.004, 11.291, 26.425, 16.898, 53.307, 150.373, 141.068, 140.183, 78.142, 24.189, 89.098, 33.691, 53.55, 26.957, 21.677, 37.188, 92.33, 25.924, 82.358, 46.61, 127.043, 102.866, 78.354, 49.587, 62.256, 16.373, 5.618, 8.595, 1.574, 4.676, 34.281, 26.24, 39.471, 20.765, 47.003, 42.707, 81.779, 48.309, 77.774, 112.414, 30.725, 2.545, 0.841, 2.71, 12.173, 13.362, 39.596, 27.081, 83.55, 58.001, 58.468, 63.061, 50.506, 70.269, 105.913, 32.204, 23.47, 10.655, 12.918, 15.11, 2.932, 18.175, 29.212, 46.769, 7.634, 139.787, 84.171, 61.056, 25.002, 75.335, 65.288, 62.78, 6.841, 30.437, 33.482, 16.267, 38.031, 4.188, 70.966, 31.048, 55.859, 88.37, 141.988, 116.516, 104.628, 60.826, 22.775, 7.78, 18.925, 21.556, 6.151, 1.648, 28.594, 29.499, 82.081, 139.821, 77.945, 124.892, 116.472, 58.358, 15.661, 26.32, 48.796, 19.906, 8.489, 6.951, 5.8, 14.62, 31.966, 11.33, 66.852, 78.292, 41.493, 70.118, 62.701, 158.441, 40.007, 54.322, 33.426, 62.348, 15.002, 27.36, 8.042, 20.572, 2.639, 6.093, 1.854, 61.886, 91.458, 58.816, 132.281, 128.592, 101.296, 50.419, 60.825, 7.408, 31.514, 3.363, 56.379, 60.864, 87.959, 113.885, 75.982, 95.61, 146.273, 64.742, 16.626, 13.866, 2.371, 32.685, 18.96, 81.477, 120.848, 166.536, 78.243, 81.59, 108.002, 34.565, 8.919, 59.003]
        # ),
        'SY1600':(
            [32.834, 18.253, 16.584, 134.108, 120.274, 93.112, 111.517, 29.593, 30.761, 66.301, 23.163, 4.019, 37.099, 3.344, 10.636, 28.909, 32.202, 12.163, 69.271, 95.099, 183.102, 37.31, 33.814, 119.682, 77.814, 57.923, 31.155, 16.145, 25.797, 100.761, 90.903, 106.078, 117.184, 69.78, 44.434, 42.192, 116.654, 113.394, 26.704, 3.634, 13.795, 7.159, 23.443, 27.421, 76.875, 115.408, 208.8, 292.452, 609.553, 553.144, 426.235, 345.918, 476.905, 460.522, 269.367, 176.661, 157.498, 73.642, 17.948, 8.14, 82.861, 83.595, 100.475, 102.587, 179.198, 171.014, 150.607, 92.782, 163.298, 51.476, 27.609, 1.052, 4.537, 5.495, 5.426, 17.52, 14.796, 19.912, 28.551, 84.092, 82.447, 242.648, 85.352, 153.18, 77.708, 102.199, 109.031, 51.22, 19.963, 20.066, 0.912, 13.386, 18.143, 7.23, 60.364, 64.389, 225.405, 178.382, 134.137, 83.678, 192.154, 100.05, 47.9, 36.831, 40.313, 51.267, 33.494, 20.429, 70.972, 91.14, 123.759, 35.229, 126.16, 73.64, 32.141, 77.551, 17.829, 2.709, 29.047, 7.869, 46.236, 23.694, 20.438, 56.355, 53.23, 114.242, 100.237, 39.686, 37.584, 18.038, 61.779, 10.763, 69.959, 11.024, 15.018, 5.327, 16.148, 43.78, 26.769, 105.891, 38.278, 47.564, 95.388, 31.242, 60.2, 73.468, 11.11, 23.32, 9.305, 18.731, 22.408, 114.311, 174.83, 130.174, 341.658, 345.753, 318.287, 331.916, 213.579, 180.172, 69.803, 56.511, 70.933, 11.25, 10.052, 9.423, 57.4, 23.577, 36.672, 212.963, 94.373, 100.095, 60.095, 100.329, 47.194, 44.726, 10.391, 2.414, 13.217, 27.524, 106.739, 60.71, 100.161, 184.404, 79.663, 127.195, 49.815, 179.452, 43.481, 18.186, 1.863, 2.732, 35.688, 55.819, 49.258, 39.515, 71.733, 122.057, 93.538, 81.467, 26.111, 32.918, 19.245, 16.919, 17.357, 7.116],
            [32.88, 17.879, 16.39, 134.947, 114.558, 90.973, 104.052, 32.582, 32.514, 77.9, 24.845, 4.887, 38.373, 3.213, 10.619, 29.118, 31.656, 13.208, 77.596, 94.737, 187.01, 29.22, 33.74, 110.519, 80.085, 58.294, 33.001, 17.734, 40.582, 95.177, 73.144, 103.501, 123.096, 68.237, 44.534, 30.053, 112.566, 84.669, 24.584, 3.631, 15.219, 10.971, 27.842, 27.515, 75.025, 124.916, 229.414, 280.443, 597.253, 511.302, 401.289, 340.584, 405.34, 420.691, 255.536, 155.923, 133.484, 49.719, 16.665, 7.444, 71.962, 85.321, 100.01, 118.721, 170.651, 154.334, 113.742, 82.877, 133.031, 40.868, 20.958, 0.984, 4.472, 6.71, 3.321, 17.669, 14.592, 12.807, 25.197, 73.096, 71.874, 213.066, 84.993, 153.969, 54.567, 113.048, 79.025, 40.653, 14.511, 14.412, 0.906, 13.434, 23.865, 7.963, 59.79, 57.102, 240.538, 179.914, 135.743, 91.485, 192.148, 88.607, 43.798, 35.114, 27.505, 40.782, 31.368, 20.543, 58.42, 88.765, 107.344, 29.578, 118.131, 77.333, 33.402, 60.707, 15.636, 2.106, 25.419, 7.4, 43.979, 24.452, 17.716, 53.209, 45.702, 93.601, 75.499, 45.397, 25.454, 16.743, 45.913, 10.74, 56.651, 4.856, 13.465, 4.856, 11.852, 34.466, 25.546, 92.685, 34.428, 38.421, 60.318, 35.131, 49.854, 68.61, 9.1, 20.506, 12.568, 15.378, 18.581, 104.422, 188.587, 120.486, 312.423, 335.234, 284.511, 326.101, 197.904, 154.523, 65.419, 59.138, 78.862, 11.377, 9.908, 11.208, 64.766, 24.116, 34.009, 232.284, 92.134, 95.803, 59.736, 102.853, 47.483, 42.132, 9.77, 1.976, 13.329, 27.451, 70.042, 61.49, 72.864, 128.837, 64.572, 87.305, 46.21, 163.545, 39.574, 17.575, 2.026, 5.589, 23.462, 47.773, 58.611, 28.964, 72.397, 142.483, 84.453, 85.504, 30.867, 32.913, 14.378, 22.591, 21.79, 10.663]
        ),
        # 'SY2600':(
        #     [14.689, 54.743, 114.537, 136.734, 160.266, 319.67, 132.555, 397.405, 94.846, 171.122, 96.048, 52.404, 37.074, 5.376, 9.313, 19.792, 150.531, 214.018, 206.131, 264.988, 190.716, 151.427, 96.621, 110.71, 30.412, 30.246, 23.864, 10.272, 4.28, 28.193, 21.268, 20.742, 71.186, 34.293, 122.4, 236.232, 201.39, 150.531, 113.713, 59.536, 93.934, 141.771, 44.726, 51.539, 52.063, 23.656, 28.291, 59.718, 111.93, 199.285, 579.125, 884.329, 587.499, 1042.874, 938.61, 553.219, 752.928, 301.505, 507.685, 214.504, 93.366, 51.89, 38.875, 35.801, 28.416, 28.973, 59.387, 26.605, 34.643, 71.621, 270.394, 220.259, 382.419, 205.029, 330.551, 108.311, 288.859, 207.135, 138.103, 37.304, 81.172, 18.301, 22.496, 16.428, 71.878, 117.5, 101.939, 152.828, 120.934, 172.137, 158.518, 197.498, 63.846, 87.226, 72.306, 13.772, 3.386, 6.131, 35.153, 88.514, 89.076, 238.389, 296.667, 415.232, 272.941, 431.824, 300.827, 184.746, 207.913, 41.141, 42.575, 3.756, 14.273, 7.681, 43.622, 66.537, 74.9, 139.83, 114.396, 109.327, 91.431, 50.013, 91.523, 23.501, 30.675, 21.034, 2.218, 28.26, 17.174, 125.553, 179.966, 136.04, 114.712, 68.997, 175.208, 44.963, 20.55, 30.96, 4.969, 27.309, 26.753, 2.376, 21.48, 149.42, 82.128, 87.966, 72.134, 86.218, 138.717, 135.834, 33.507, 8.64, 19.856, 28.712, 4.876, 3.357, 24.657, 74.958, 119.072, 346.632, 417.362, 453.037, 476.912, 652.338, 663.099, 406.721, 236.024, 231.995, 82.246, 93.755, 94.482, 23.742, 26.176, 1.927, 3.03, 34.754, 63.103, 130.059, 136.795, 90.13, 161.138, 194.518, 158.582, 76.764, 55.669, 57.173, 8.333, 18.631, 29.025, 5.346, 10.632, 7.172, 55.1, 136.74, 92.824, 170.665, 263.832, 193.871, 160.27, 101.972, 124.994, 29.851, 47.152, 38.06, 18.503, 10.012, 27.966, 20.58, 58.838, 31.744, 78.65, 171.267, 111.665, 88.815, 94.515, 89.574, 157.757, 49.771, 46.97, 23.04],
        #     [14.529, 64.851, 108.267, 139.074, 143.52, 280.267, 133.34, 330.844, 62.809, 162.607, 81.237, 51.648, 37.129, 7.645, 8.72, 22.59, 162.638, 214.754, 189.376, 270.618, 170.991, 147.988, 103.038, 84.702, 32.561, 14.25, 17.833, 5.612, 3.565, 34.612, 31.939, 27.89, 77.903, 42.027, 127.96, 225.037, 191.322, 130.901, 108.574, 43.953, 95.564, 131.298, 34.361, 36.235, 39.203, 27.561, 26.613, 64.316, 97.141, 195.872, 533.876, 830.804, 557.641, 1036.074, 842.853, 491.625, 685.064, 303.862, 452.928, 210.662, 93.208, 55.038, 34.342, 33.544, 14.662, 34.718, 82.163, 30.729, 39.046, 72.414, 246.654, 220.083, 363.839, 273.453, 361.199, 111.231, 277.366, 196.729, 137.84, 40.996, 66.82, 14.132, 21.634, 9.591, 68.331, 129.734, 105.519, 155.488, 113.985, 165.214, 157.778, 182.677, 61.943, 77.787, 54.482, 11.216, 2.525, 6.206, 41.69, 117.447, 81.409, 250.081, 250.227, 411.429, 261.112, 418.219, 250.135, 162.73, 172.656, 45.831, 49.235, 3.622, 10.939, 6.989, 37.131, 58.671, 82.573, 127.245, 95.366, 94.506, 105.629, 57.254, 87.05, 27.705, 18.886, 22.055, 1.646, 37.167, 20.453, 127.487, 168.818, 148.302, 106.126, 70.271, 151.727, 41.26, 18.127, 31.294, 8.219, 18.797, 18.084, 2.453, 19.988, 120.551, 86.707, 91.143, 72.038, 81.1, 137.298, 151.386, 35.381, 8.241, 20.024, 25.114, 3.906, 3.628, 20.057, 78.41, 126.246, 342.621, 382.426, 450.319, 441.201, 533.795, 513.532, 347.578, 205.144, 200.719, 72.128, 93.51, 80.385, 13.233, 21.754, 1.598, 2.654, 42.683, 60.88, 145.242, 144.809, 85.727, 156.211, 215.456, 150.434, 87.373, 53.532, 53.387, 7.854, 15.736, 27.325, 4.355, 10.557, 7.054, 59.432, 134.438, 92.231, 141.98, 224.724, 154.038, 128.489, 96.301, 121.797, 27.576, 35.282, 33.268, 16.221, 5.765, 22.472, 12.343, 77.23, 28.985, 74.841, 190.844, 102.092, 79.353, 89.21, 84.493, 154.19, 49.07, 43.208, 15.184]
        # )
        'lineitem':(
            [58.47, 46.75, 4.926, 39.597, 166.877, 69.385, 101.068, 199.631, 177.73, 251.161, 119.831, 55.244, 143.279,
             91.655, 41.765, 20.772, 7.111, 16.923, 110.775, 64.468, 118.376, 154.375, 308.258, 154.4, 178.041, 153.001,
             59.898, 42.953, 6.33, 87.764, 12.373, 11.992, 42.664, 86.74, 112.068, 204.307, 196.333, 133.697, 166.579,
             95.598, 152.95, 79.935, 119.401, 34.956, 14.807, 24.443, 1.822, 8.893, 25.435, 62.977, 86.977, 238.292,
             120.637, 298.792, 81.435, 213.822, 145.314, 62.901, 77.696, 19.49, 13.342, 60.652, 9.03, 9.389, 146.352,
             80.47, 107.841, 147.091, 145.402, 115.106, 213.714, 172.12, 123.129, 41.973, 25.444, 3.588, 18.807, 32.933,
             29.79, 10.599, 24.745, 65.928, 104.828, 174.615, 201.749, 282.569, 221.527, 37.848, 135.57, 84.393, 44.908,
             26.5, 10.378, 54.896, 12.182, 46.471, 27.982, 89.903, 154.999, 197.935, 229.499, 151.588, 186.914, 75.659,
             94.335, 23.492, 28.276, 13.576, 58.098, 27.386, 9.325, 21.469, 36.082, 120.578, 77.668, 116.139, 125.551,
             58.303, 227.165, 180.944, 260.314, 103.863, 140.827, 56.957, 14.499, 21.788, 47.818, 64.905, 308.341,
             155.255, 257.456, 141.589, 116.639, 165.866, 116.643, 64.935, 54.813, 11.295, 43.733, 20.082, 7.267,
             82.985, 88.906, 106.785, 126.479, 244.774, 89.304, 138.885, 163.112, 141.349, 106.558, 44.415, 19.962,
             22.958, 12.902, 34.347, 74.902, 79.229, 143.764, 179.6, 169.29, 145.734, 192.268, 115.104, 71.107, 110.17,
             72.11, 23.455, 25.387, 19.729, 40.426, 54.365, 63.066, 130.158, 158.713, 145.956, 199.43, 156.592, 213.329,
             135.746, 147.963, 26.066, 32.425, 8.703, 38.533, 44.961, 87.087, 93.954, 162.236, 142.793, 208.51, 135.6,
             180.481, 156.97, 56.432, 45.105, 15.098, 14.627, 30.21, 145.667, 185.861, 90.166, 105.827, 156.159,
             240.088, 165.997, 103.954, 50.57, 18.301, 34.018, 19.016, 30.888, 94.292, 90.08, 105.116, 103.41, 289.447,
             125.838, 217.63, 216.017, 47.354, 92.509, 59.698, 29.6, 6.762, 49.389, 18.932, 16.292, 100.877, 127.632,
             163.763, 198.045, 221.17, 157.914, 126.782, 146.637, 66.284, 54.461, 69.058, 53.308, 25.675, 7.48, 50.218,
             118.852, 129.924, 91.626, 102.587, 95.383, 264.419, 153.637, 117.451, 75.272, 132.409, 63.973, 4.43,
             13.479, 16.574, 49.524, 42.876, 115.046, 158.846, 203.289, 218.201, 160.314, 247.838, 122.941, 101.772,
             36.694, 66.229, 34.662, 23.276, 2.428, 6.525, 17.569, 57.016, 46.396, 134.314, 127.593, 42.994, 226.315,
             283.635, 228.861, 152.193, 151.651, 98.446, 34.842, 24.55, 4.373, 81.166, 129.735, 108.871, 119.521,
             324.125, 74.056, 130.889, 128.88, 136.659, 80.072, 19.09, 83.311, 21.176, 11.717, 25.903, 4.025],
            [58.648, 49.661, 3.75, 35.38, 136.793, 82.58, 102.962, 206.716, 193.853, 216.426, 118.005, 60.154, 121.169,
             83.93, 47.238, 21.389, 7.152, 18.284, 100.196, 55.692, 121.637, 155.014, 323.685, 148.571, 191.557,
             159.185, 67.721, 41.474, 5.347, 69.1, 18.649, 19.781, 43.411, 93.898, 120.438, 184.112, 175.505, 134.057,
             133.279, 84.782, 142.382, 64.121, 96.411, 31.272, 11.96, 27.085, 1.621, 8.652, 23.368, 62.342, 91.827,
             214.329, 118.825, 267.225, 79.864, 187.331, 129.09, 44.47, 81.173, 28.11, 11.934, 57.346, 10.162, 10.773,
             126.094, 80.526, 99.363, 133.735, 153.145, 107.098, 231.249, 184.427, 119.156, 42.527, 25.522, 4.613,
             17.406, 32.168, 23.356, 9.65, 22.552, 60.972, 95.369, 154.959, 198.645, 279.294, 208.187, 43.613, 120.74,
             77.097, 42.086, 25.755, 6.402, 30.772, 11.277, 41.058, 29.906, 74.665, 142.455, 195.278, 231.2, 159.699,
             167.424, 67.098, 94.53, 25.234, 38.966, 9.493, 43.208, 16.732, 6.654, 17.266, 29.983, 112.807, 69.395,
             127.201, 133.126, 44.998, 207.18, 175.069, 244.34, 112.8, 143.658, 51.115, 13.331, 19.94, 50.532, 57.369,
             291.847, 141.244, 231.289, 137.839, 117.025, 153.137, 98.72, 69.201, 52.333, 6.955, 39.901, 19.53, 8.411,
             74.333, 77.692, 104.368, 130.949, 221.609, 91.31, 133.371, 131.2, 140.306, 118.315, 35.238, 28.257, 21.495,
             11.895, 34.404, 80.304, 69.887, 110.416, 153.871, 161.451, 137.408, 190.018, 118.623, 65.826, 99.626,
             79.038, 24.668, 26.27, 25.199, 45.87, 52.845, 64.054, 125.026, 181.994, 146.15, 222.147, 140.598, 185.615,
             120.156, 144.061, 26.507, 32.499, 5.834, 31.797, 44.944, 92.874, 102.154, 150.845, 151.615, 222.663,
             128.971, 153.622, 119.041, 56.532, 47.037, 14.663, 11.135, 22.815, 137.392, 203.213, 87.517, 84.662,
             146.752, 223.817, 168.034, 96.239, 51.53, 15.823, 25.618, 18.995, 24.159, 66.377, 82.246, 107.467, 95.422,
             263.908, 120.915, 199.029, 194.836, 54.124, 82.054, 48.89, 27.079, 5.515, 41.082, 17.368, 17.395, 77.825,
             102.827, 147.083, 190.979, 219.734, 121.732, 122.392, 129.498, 73.281, 70.673, 54.754, 46.563, 16.686,
             7.913, 46.825, 117.261, 133.62, 101.226, 89.181, 95.514, 246.648, 167.01, 113.345, 64.424, 128.679, 55.757,
             3.99, 18.311, 16.656, 27.698, 32.515, 94.057, 160.111, 208.083, 211.321, 154.126, 241.647, 103.885,
             103.129, 29.03, 53.895, 17.546, 28.525, 2.063, 5.611, 15.758, 40.52, 49.16, 108.088, 93.762, 36.52,
             209.719, 270.452, 223.754, 157.226, 155.951, 88.757, 31.312, 14.859, 4.416, 58.64, 120.864, 112.087,
             143.771, 302.569, 69.344, 141.983, 124.918, 136.899, 75.862, 16.351, 88.488, 21.633, 14.18, 30.993, 4.109],

        ),
        'orders':(
            [66.537, 143.924, 39.539, 53.577, 114.748, 140.19, 39.525, 92.992, 45.695, 6.4, 83.935, 86.419, 25.188,
             1.295, 10.638, 1.449, 4.611, 58.999, 33.311, 43.708, 41.93, 52.409, 83.178, 35.527, 116.699, 43.509,
             54.681, 32.78, 22.517, 19.018, 15.78, 2.773, 4.664, 31.275, 29.144, 73.584, 123.655, 83.724, 45.773,
             71.655, 64.221, 62.803, 58.64, 22.803, 3.317, 11.241, 6.257, 26.835, 11.384, 24.588, 19.47, 45.914, 69.711,
             65.199, 87.049, 43.187, 67.634, 94.875, 51.509, 9.258, 21.484, 7.854, 23.675],
            [66.64, 134.315, 6.113, 53.577, 114.762, 140.254, 39.427, 93.061, 45.669, 6.394, 83.895, 86.175, 25.159,
             1.288, 10.675, 1.459, 4.625, 59.0, 33.275, 43.778, 41.8, 52.407, 83.197, 35.459, 116.392, 43.614, 54.626,
             32.819, 22.556, 19.061, 15.79, 2.773, 4.656, 31.28, 29.146, 73.481, 123.693, 83.879, 45.834, 71.788,
             71.589, 67.388, 65.78, 25.122, 5.766, 10.437, 7.052, 23.23, 10.36, 23.433, 21.021, 49.509, 69.066, 74.257,
             95.635, 45.415, 69.405, 102.113, 54.739, 8.707, 20.422, 7.847, 23.18],

        ),
        'supplier':(
            [86.538, 60.909, 36.479, 15.26, 53.124, 63.636, 92.644, 103.331, 102.184, 125.162, 117.258, 17.766, 43.533,
             40.567, 12.296, 14.548, 8.725, 1.601, 45.174, 32.962, 138.719, 112.805, 149.944, 199.403, 101.5, 112.045,
             136.96, 106.794, 63.17, 37.983, 22.746, 13.379, 0.504, 2.25, 8.263],
            [86.307, 60.866, 36.432, 15.278, 52.944, 63.6, 92.325, 103.014, 101.919, 124.704, 116.975, 17.715, 43.359,
             40.484, 12.243, 14.561, 8.716, 1.606, 44.957, 32.244, 139.16, 113.693, 149.844, 198.909, 101.238, 111.854,
             136.531, 106.467, 63.148, 38.014, 22.717, 13.406, 0.503, 2.245, 8.232],
        ),
        'catalog_sales':(
            [34.776, 55.835, 86.367, 124.473, 110.398, 97.798, 130.972, 172.791, 96.678, 112.867, 91.223, 49.725,
             60.962, 5.188, 16.824, 57.844, 87.962, 106.994, 159.679, 81.483, 127.895, 88.915, 50.454, 17.263, 28.451,
             15.851, 44.754, 4.958, 31.306, 2.783, 9.829, 15.026, 25.68, 66.276, 36.68, 103.296, 121.441, 234.548,
             155.174, 80.935, 128.911, 161.939, 0.829, 25.248, 3.036, 30.112, 20.024, 45.411, 39.014, 168.997, 204.455,
             88.319, 131.496, 114.536, 157.509, 87.561, 50.966, 8.72, 23.828, 1.754, 29.447, 57.45, 19.921, 91.045,
             121.299, 122.517, 197.763, 219.512, 147.714, 43.503, 65.961, 69.348, 14.707, 15.032, 27.127, 35.122,
             81.575, 108.482, 106.672, 238.668, 175.928, 107.687, 74.699, 82.447, 63.37, 44.393, 48.298, 8.605, 86.283,
             21.66, 42.65, 62.005, 153.821, 245.156, 135.141, 94.236, 95.955, 73.178, 87.259, 44.719, 23.571, 3.221,
             15.167, 31.029, 1.216, 62.647, 29.923, 110.852, 97.144, 210.09, 68.48, 86.593, 179.467, 68.351, 83.265,
             73.031, 8.787, 32.349, 6.217, 71.533, 27.585, 65.629, 44.333, 97.906, 221.872, 102.791, 134.995, 27.419,
             133.849, 12.148, 2.905, 19.732, 5.278, 43.579, 47.742, 142.678, 104.5, 101.011, 179.134, 154.14, 177.873,
             101.846, 57.656, 66.404, 74.04, 11.103, 24.245, 22.171, 78.281, 96.169, 177.776, 130.034, 32.321, 189.48,
             87.344, 77.819, 31.854, 58.044, 76.018, 11.278, 15.319, 44.861, 18.711, 84.812, 52.697, 98.007, 137.898,
             65.936, 99.023, 128.392, 122.86, 59.862, 36.839, 61.87, 25.215, 0.744, 16.179, 24.87, 15.298, 31.533,
             25.279, 62.835, 154.541, 80.655, 122.567, 218.43, 144.275, 49.894, 33.522, 20.129, 51.798, 7.952, 6.539,
             24.674, 71.945, 104.525, 124.865, 65.618, 79.101, 121.688, 186.074, 106.633, 84.615, 39.912, 40.395, 6.897,
             4.325, 4.832, 14.974, 0.571, 39.371, 22.615, 37.711, 2.18, 136.986, 74.157, 140.813, 96.379, 135.796,
             71.115, 127.672, 40.764, 48.762, 5.826, 10.366, 9.466, 39.333, 3.668, 25.668, 76.945, 84.49, 127.186,
             174.858, 134.189, 110.795, 163.806, 94.963, 96.194, 13.309, 38.341, 0.74, 29.412, 6.334, 6.035, 22.655,
             32.172, 145.881, 262.051, 152.805, 84.5, 201.572, 66.036, 53.494, 143.992, 53.546, 28.341, 18.805, 40.762,
             43.983, 40.267, 162.198, 215.292, 101.36, 91.44, 163.512, 103.087, 39.728, 10.939, 16.374, 15.03, 53.588,
             19.999, 57.481, 72.403, 193.89, 120.799, 220.618, 137.081, 87.727, 59.92, 106.152, 32.407, 55.68, 5.063,
             10.341, 40.872, 26.259, 84.48, 191.418, 111.537, 120.967, 136.321, 70.674, 76.524, 47.355, 12.514, 19.061,
             17.509, 32.551, 23.677, 2.148],
            [34.724, 44.366, 73.157, 82.623, 78.699, 67.31, 128.605, 170.576, 94.786, 133.882, 95.601, 49.641, 60.938,
             7.878, 18.125, 56.417, 88.9, 99.762, 172.476, 80.404, 114.932, 101.821, 53.281, 17.898, 27.658, 16.272,
             47.212, 5.355, 34.81, 2.589, 9.831, 16.819, 27.146, 68.428, 37.434, 107.78, 112.535, 218.438, 165.197,
             67.224, 116.142, 175.91, 1.428, 19.112, 3.763, 30.081, 26.938, 41.838, 39.794, 172.64, 210.132, 80.379,
             122.304, 109.204, 164.946, 84.986, 49.244, 11.226, 24.413, 2.032, 33.579, 62.911, 20.481, 91.931, 128.46,
             155.92, 177.041, 215.316, 122.441, 47.125, 55.304, 87.855, 11.469, 15.987, 30.734, 28.21, 85.388, 112.16,
             122.259, 208.486, 190.945, 101.324, 67.682, 75.922, 56.652, 43.449, 34.299, 6.986, 77.393, 23.195, 41.23,
             48.367, 134.961, 275.393, 131.434, 95.813, 111.129, 60.156, 76.391, 43.653, 21.239, 3.697, 18.002, 28.778,
             0.893, 57.099, 35.025, 118.496, 94.147, 224.359, 78.257, 81.674, 154.603, 64.14, 70.867, 57.993, 10.64,
             32.842, 3.798, 65.06, 28.783, 56.248, 42.567, 92.481, 212.451, 88.157, 117.784, 31.056, 105.613, 15.854,
             1.845, 12.412, 2.539, 45.25, 48.9, 145.765, 95.308, 100.786, 152.914, 145.66, 156.849, 90.852, 56.493,
             61.6, 64.185, 9.678, 24.484, 21.575, 71.522, 79.879, 180.032, 124.352, 31.673, 174.568, 69.301, 73.033,
             39.335, 48.885, 63.381, 14.083, 10.575, 44.155, 18.593, 100.584, 49.699, 89.438, 132.748, 60.123, 93.08,
             113.511, 93.702, 57.892, 34.346, 40.369, 23.622, 0.742, 20.373, 24.173, 12.877, 24.553, 23.361, 62.686,
             132.42, 82.981, 125.365, 220.204, 148.467, 46.499, 24.343, 17.821, 53.268, 7.916, 8.446, 26.208, 77.868,
             111.951, 138.259, 70.583, 79.902, 118.846, 186.095, 108.915, 88.002, 33.399, 50.383, 5.663, 4.292, 5.96,
             9.394, 0.713, 33.564, 27.888, 41.391, 2.381, 135.139, 74.087, 127.968, 98.219, 141.872, 71.464, 124.868,
             33.838, 47.112, 5.799, 10.392, 5.819, 31.942, 2.323, 18.195, 75.06, 82.821, 106.693, 163.931, 130.265,
             88.399, 149.692, 88.457, 75.91, 8.318, 35.234, 0.689, 26.075, 6.305, 4.106, 19.334, 27.564, 118.478,
             207.423, 127.859, 78.492, 214.059, 69.992, 43.438, 98.979, 47.067, 28.916, 16.694, 40.604, 41.738, 38.405,
             159.433, 223.657, 121.224, 98.077, 149.057, 89.905, 33.334, 9.321, 17.614, 11.45, 51.967, 19.175, 64.958,
             86.071, 194.4, 114.698, 230.341, 113.727, 84.039, 55.796, 95.461, 36.438, 50.672, 6.206, 7.959, 37.001,
             26.201, 89.611, 214.255, 111.573, 109.611, 119.382, 77.397, 71.049, 38.541, 10.612, 20.324, 12.856, 32.405,
             20.143, 1.482],
        ),
        'store_sales':(
            [24.467, 29.004, 64.17, 78.335, 65.74, 53.878, 57.897, 27.034, 55.586, 37.623, 21.076, 6.777, 7.268, 11.029,
             27.223, 91.037, 8.373, 67.745, 94.103, 25.731, 58.47, 14.988, 51.526, 8.323, 17.051, 16.802, 10.666,
             34.453, 29.944, 20.956, 42.113, 54.216, 75.065, 27.017, 50.96, 48.947, 21.78, 4.816, 43.37, 5.064, 6.211,
             9.008, 21.819, 33.428, 25.55, 81.381, 73.319, 64.512, 75.119, 48.066, 53.448, 44.555, 30.938, 9.897,
             17.713, 12.621, 13.584, 21.474, 0.818, 38.587, 81.224, 56.297, 54.363, 41.215, 32.707, 33.673, 7.384,
             4.181, 32.72, 0.546, 14.58, 11.065, 46.421, 40.025, 102.968, 43.64, 45.659, 88.674, 23.818, 180.698,
             15.241, 19.707, 32.549, 17.741, 3.04, 6.542, 41.281, 42.953, 87.452, 71.505, 88.814, 28.817, 52.882,
             47.678, 21.787, 30.75, 4.076, 40.999, 60.475, 17.882, 24.665, 81.095, 42.124, 58.753, 105.222, 25.864,
             14.832, 27.497, 22.512, 3.244, 3.586, 3.547, 8.124, 15.334, 6.826, 0.632, 103.644, 58.758, 28.165, 155.012,
             71.101, 19.639, 1.057, 1.483, 8.655, 11.982, 6.092, 17.214, 53.957, 105.534, 14.966, 152.034, 29.957,
             27.463, 32.067, 33.452, 8.318, 38.77, 0.573, 12.04, 11.591, 5.797, 5.366, 8.313, 14.842, 62.127, 28.07,
             41.925, 71.36, 90.549, 61.728, 34.151, 35.443, 5.503, 18.637, 2.274, 12.891, 21.024, 54.596, 69.843,
             47.841, 33.396, 61.877, 41.849, 20.963, 24.032, 2.277, 16.128, 5.919, 18.149, 12.774, 5.539, 16.413, 4.427,
             10.809, 24.66, 74.197, 83.43, 61.577, 87.741, 17.905, 58.965, 36.469, 34.429, 25.799, 10.051, 10.925,
             15.726, 9.839, 70.148, 39.594, 86.264, 114.838, 16.981, 38.643, 17.354, 16.041, 35.698, 13.825, 69.352,
             65.193, 12.312, 20.162, 43.131, 71.852, 117.274, 116.964, 25.307, 0.42, 5.175, 25.302, 3.708, 7.21, 15.718,
             39.275, 36.803, 72.043, 106.441, 44.672, 62.139, 102.745, 4.213, 78.949, 20.135, 27.228, 37.425, 34.766,
             6.729, 22.276, 82.757, 96.779, 21.482, 74.29, 37.448, 50.1, 19.372, 26.536, 4.285, 48.869, 29.236, 10.206,
             19.664, 68.284, 62.254, 51.005, 67.797, 25.27, 51.581, 45.546, 14.605, 34.108, 7.493, 16.712, 22.592,
             28.727, 37.136, 86.391, 56.982, 42.101, 68.094, 28.939, 75.683, 32.672, 4.204, 28.228, 7.751, 29.188,
             7.326, 67.277, 67.83, 46.958, 85.248, 45.574, 34.027, 47.55, 31.452],
            [24.422, 27.55, 56.006, 78.031, 71.405, 51.978, 57.673, 21.855, 55.761, 30.847, 17.713, 6.777, 6.945,
             16.589, 27.39, 95.072, 8.337, 69.036, 84.471, 27.996, 58.25, 11.92, 54.778, 8.322, 13.764, 15.593, 12.711,
             28.154, 42.133, 21.597, 38.547, 55.63, 62.691, 17.57, 49.405, 30.983, 21.505, 4.309, 36.301, 5.8, 3.594,
             10.368, 19.684, 33.261, 27.77, 71.898, 69.912, 58.392, 58.656, 49.065, 49.151, 51.689, 29.418, 11.982,
             16.171, 12.028, 8.462, 23.675, 1.245, 35.902, 84.412, 61.606, 50.405, 32.027, 28.313, 36.719, 5.207, 3.575,
             42.115, 0.565, 7.782, 11.021, 47.339, 37.198, 91.875, 43.975, 29.071, 78.554, 26.006, 162.487, 16.301,
             10.184, 34.296, 18.769, 2.859, 4.75, 45.041, 43.029, 93.817, 66.943, 79.287, 28.022, 64.746, 38.445,
             21.814, 22.892, 1.688, 34.016, 37.747, 20.023, 22.014, 79.794, 37.666, 44.867, 103.848, 26.745, 12.847,
             31.02, 23.089, 2.904, 1.76, 3.538, 5.929, 18.138, 4.957, 0.636, 112.896, 51.832, 27.518, 131.877, 78.77,
             16.7, 1.06, 1.486, 8.052, 8.334, 4.612, 14.03, 46.032, 102.302, 16.117, 127.131, 32.023, 26.808, 33.497,
             38.586, 10.286, 50.553, 0.907, 8.476, 11.016, 4.769, 6.459, 7.09, 16.453, 70.205, 28.03, 41.969, 78.802,
             76.406, 59.862, 36.945, 30.339, 4.404, 18.582, 2.467, 8.508, 22.478, 62.722, 71.806, 46.19, 32.858, 56.802,
             42.905, 18.159, 25.709, 1.455, 13.947, 6.517, 11.698, 12.877, 6.774, 13.252, 5.414, 12.066, 24.025, 59.792,
             87.827, 61.788, 70.9, 16.086, 41.038, 28.683, 23.098, 25.831, 7.108, 5.082, 15.607, 14.294, 68.963, 35.704,
             67.111, 108.126, 14.218, 34.721, 15.582, 11.127, 43.957, 15.854, 55.742, 49.24, 10.845, 20.197, 36.957,
             70.199, 129.357, 116.581, 18.064, 0.42, 5.172, 28.436, 2.91, 4.33, 16.143, 38.187, 32.922, 67.242, 77.236,
             36.049, 59.762, 92.42, 5.687, 83.339, 20.801, 22.582, 45.199, 30.354, 6.743, 27.965, 84.663, 88.407,
             21.142, 75.258, 36.641, 54.966, 16.695, 30.587, 4.38, 55.341, 28.837, 4.479, 16.838, 67.753, 68.111,
             48.195, 67.42, 27.25, 43.106, 43.679, 18.379, 36.162, 10.887, 8.811, 22.233, 24.952, 38.729, 100.863,
             69.219, 43.081, 55.423, 30.546, 73.719, 42.281, 3.221, 26.08, 6.447, 29.75, 5.811, 63.014, 55.016, 52.601,
             79.764, 42.392, 31.964, 39.028, 41.289],
        ),
        'web_sales':(
            [37.506, 21.486, 37.476, 35.042, 98.104, 54.281, 44.226, 15.183, 17.173, 31.248, 2.405, 16.004, 11.833, 9.574, 8.372, 46.586, 69.813, 63.307, 54.34, 119.742, 75.867, 54.664, 4.423, 32.591, 21.053, 7.011, 20.707, 26.399, 52.5, 25.009, 50.203, 57.782, 76.318, 7.053, 57.314, 90.478, 5.29, 20.463, 23.122, 7.594, 20.632, 11.377, 19.201, 57.451, 63.12, 58.448, 24.514, 57.436, 17.424, 21.288, 19.212, 4.991, 1.154, 34.333, 8.306, 48.281, 28.945, 72.214, 42.365, 39.539, 62.729, 25.818, 22.857, 4.063, 30.354, 7.696, 2.888, 39.407, 40.626, 33.162, 55.271, 41.826, 35.088, 86.19, 42.756, 64.877, 19.742, 20.558, 30.388, 3.322, 10.476, 45.782, 58.093, 146.522, 63.666, 19.505, 23.384, 60.886, 25.491, 26.741, 12.028, 7.98, 30.177, 65.444, 47.136, 91.411, 15.783, 90.166, 53.546, 22.251, 34.205, 12.183, 42.694, 12.842, 29.075, 24.31, 28.349, 15.347, 22.31, 79.84, 75.337, 7.538, 81.638, 70.428, 26.481, 8.034, 1.884, 3.06, 11.362, 25.316, 12.364, 60.065, 10.072, 36.363, 60.837, 45.803, 32.727, 27.98, 118.404, 11.388, 3.971, 25.397, 10.332, 12.208, 15.56, 5.757, 9.995, 9.757, 33.661, 29.875, 71.031, 16.241, 47.412, 12.207, 61.949, 19.772, 21.195, 8.908, 11.978, 18.608, 37.633, 31.147, 9.366, 85.394, 51.836, 74.336, 111.89, 41.63, 10.362, 11.824, 31.805, 14.865, 14.553, 6.397, 9.473, 46.628, 28.43, 45.764, 76.425, 86.887, 42.892, 37.619, 4.668, 7.205, 7.197, 10.954, 15.761, 26.536, 56.44, 51.706, 76.124, 85.912, 52.149, 50.219, 34.471, 8.532, 13.392, 7.642, 23.458, 4.105, 13.036, 10.464, 14.588, 12.561, 17.548, 46.522, 9.683, 36.93, 98.585, 27.699, 26.396, 14.747, 11.401, 19.301, 7.825, 4.516, 11.931, 15.589, 6.591, 0.601, 13.626, 43.009, 60.961, 53.315, 37.852, 60.241, 85.576, 58.901, 0.715, 54.799, 6.887, 12.645, 21.296, 5.172, 11.211, 64.916, 104.53, 110.881, 55.904, 24.112, 48.037, 23.494, 1.13, 6.077, 17.694, 9.783, 31.799, 48.007, 61.406, 47.285, 95.996, 15.207, 29.661, 19.103, 12.57, 14.895, 9.825, 17.551, 30.851, 41.913, 60.211, 55.265, 49.857, 58.276, 89.388, 78.453, 21.667, 12.871, 13.989, 4.512, 1.375, 0.687, 20.546, 2.087, 66.887, 34.702, 6.663, 85.291, 55.759, 34.992, 5.87, 17.409, 7.96],
            [37.712, 17.897, 29.806, 30.72, 73.297, 51.874, 34.479, 16.412, 13.752, 29.939, 1.926, 13.097, 11.695,
             7.807, 7.477, 48.417, 68.931, 66.153, 48.721, 97.47, 72.034, 44.777, 6.104, 33.18, 21.455, 2.472, 23.875,
             28.928, 54.454, 26.439, 49.281, 57.077, 88.88, 8.878, 57.149, 89.559, 6.55, 15.979, 29.622, 12.066, 21.352,
             13.29, 18.486, 40.788, 61.943, 63.325, 25.491, 63.912, 15.14, 21.489, 11.571, 4.683, 0.562, 31.818, 9.025,
             51.85, 31.029, 75.34, 51.135, 42.645, 52.014, 27.91, 25.473, 3.396, 32.353, 8.299, 2.603, 35.865, 40.74,
             34.65, 50.367, 50.455, 36.057, 83.949, 34.879, 56.862, 17.624, 19.445, 38.085, 5.293, 10.769, 43.15,
             66.088, 143.611, 68.76, 19.255, 21.423, 56.264, 33.256, 25.54, 13.719, 12.242, 34.051, 51.525, 54.956,
             77.382, 18.386, 95.518, 56.174, 35.803, 48.396, 9.67, 30.077, 14.315, 40.919, 15.796, 32.462, 19.701,
             21.278, 76.066, 80.551, 7.523, 75.578, 60.638, 26.178, 10.37, 4.022, 6.46, 10.883, 22.318, 6.316, 61.634,
             11.111, 32.833, 76.578, 46.959, 28.19, 26.687, 128.86, 14.05, 3.999, 29.151, 3.362, 13.009, 17.835, 4.472,
             8.403, 10.308, 39.691, 30.947, 58.982, 15.273, 44.39, 13.107, 46.045, 21.771, 20.178, 5.927, 8.555, 17.046,
             29.731, 35.724, 10.255, 94.838, 48.844, 62.668, 99.212, 47.398, 7.141, 10.442, 29.748, 13.435, 13.579, 7.9,
             11.669, 44.768, 28.445, 42.468, 73.507, 78.393, 34.304, 34.051, 6.473, 7.504, 8.644, 11.629, 12.465,
             17.314, 49.712, 49.856, 74.731, 75.073, 52.768, 60.148, 33.25, 6.405, 11.953, 6.626, 23.727, 7.029, 13.072,
             10.015, 14.948, 13.183, 15.658, 42.668, 10.586, 40.515, 96.221, 27.405, 25.265, 14.725, 7.502, 19.382,
             7.806, 4.508, 16.474, 13.808, 6.586, 0.601, 12.8, 38.39, 63.027, 40.435, 35.187, 61.942, 64.144, 46.768,
             0.903, 46.187, 5.474, 9.512, 10.885, 5.137, 11.688, 65.582, 81.775, 108.986, 50.772, 19.292, 39.277,
             20.413, 1.747, 5.796, 12.726, 8.081, 25.096, 45.391, 61.101, 51.596, 105.202, 14.741, 24.38, 17.285,
             12.871, 9.696, 9.463, 23.271, 35.544, 36.422, 29.462, 55.091, 36.64, 58.276, 66.355, 80.762, 23.618,
             14.585, 14.957, 4.018, 1.099, 0.549, 15.435, 2.081, 65.325, 34.671, 6.654, 92.986, 55.55, 31.936, 5.915,
             12.185, 9.154],
        )
    }
    # 1500
    # a=[33.1, 15.652, 160.078, 138.552, 30.618, 154.41, 21.821, 195.442, 25.842, 28.277, 2.38, 2.781, 1.456, 14.311, 3.876, 6.433, 0.556, 34.842, 32.919, 24.842, 6.785, 36.702, 38.23, 31.873, 26.357, 11.858, 6.249, 11.462, 1.747, 6.619, 16.983, 21.529, 12.397, 96.474, 19.252, 25.703, 27.953, 13.77, 9.938, 2.207, 3.567, 3.899, 2.748, 6.789, 30.963, 21.332, 17.101, 35.975, 47.976, 17.724, 27.769, 18.231, 11.105, 17.432, 12.658, 13.939, 22.643, 14.059, 4.34, 2.769, 4.203, 10.337, 31.751, 61.494, 20.941, 31.686, 21.364, 24.122, 27.695, 6.96, 8.774, 6.803, 5.031, 4.207, 2.756, 29.914, 16.375, 47.827, 48.848, 29.13, 11.633, 42.58, 25.307, 12.62, 4.458, 1.09, 0.511, 4.811, 1.109, 7.744, 0.917, 23.816, 18.475, 16.117, 32.637, 31.164, 13.271, 33.061, 9.043, 34.984, 0.414, 19.439, 5.448, 2.524, 29.015, 5.521, 17.527, 20.81, 29.143, 24.047, 37.223, 10.98, 36.945, 7.268, 4.606, 8.559, 2.903, 4.179, 6.529, 31.457, 5.38, 52.085, 13.968, 31.111, 19.552, 11.598, 19.576, 5.251, 7.949, 5.477, 15.488, 5.984, 8.019, 21.768, 14.921, 13.77, 51.22, 71.538, 4.166, 46.316, 14.432, 4.647, 4.352, 1.328, 11.5, 22.269, 15.439, 50.114, 21.811, 21.521, 40.368, 29.045, 34.377, 13.189, 17.221, 25.602, 2.233, 5.508, 7.121, 33.593, 16.812, 11.187, 40.655, 24.377, 47.837, 28.9, 23.963, 20.946, 29.292, 23.062, 13.928, 20.725, 36.431, 29.34, 19.443, 57.294, 13.407, 28.642, 9.395, 39.816, 4.667, 2.894, 2.239, 8.879, 4.078, 9.029, 14.322, 4.255, 28.769, 12.592, 8.654, 42.843, 47.33, 43.351, 31.135, 25.887, 12.011, 19.449, 15.63, 10.049, 2.702, 10.077, 6.719, 5.111, 40.269, 13.097, 25.216, 30.844, 26.834, 31.896, 31.349, 27.433, 19.252, 16.924, 17.307, 12.318, 11.813, 9.518, 19.649, 0.861, 15.042, 8.355, 1.222, 25.898, 7.273, 7.142, 3.232, 2.275, 10.626, 5.854, 22.157, 14.946, 9.483, 12.734, 16.106, 14.436, 14.213, 1.273, 4.073, 1.678, 9.248, 12.361, 4.534, 4.797, 4.41, 18.518, 33.175, 13.542, 9.865, 10.736, 2.697, 0.543, 2.301, 0.837, 2.439, 6.903, 10.954, 6.049, 20.074, 1.929, 9.506, 35.095, 3.768, 21.382, 9.04, 14.235, 5.206, 2.875, 1.36, 0.269, 0.546, 2.464, 2.579, 21.366, 5.91, 24.403, 30.284, 28.378, 8.586, 9.807, 3.253, 8.344, 0.842, 3.726, 17.573, 32.541, 4.777, 22.19, 23.627, 19.856, 13.203, 5.662, 7.13, 2.295, 0.644, 5.375, 6.659, 31.524, 4.683, 12.292, 28.496, 20.964, 13.895, 10.654, 9.267, 0.545, 1.226, 0.27, 1.871, 5.468, 0.675, 35.351, 16.788, 15.329, 5.325, 12.736, 18.693, 17.652, 17.407, 5.595, 14.808, 2.139, 11.265, 14.742, 15.477, 10.989, 10.378, 16.967, 9.888, 13.207, 17.195, 0.929, 3.071, 0.824, 15.688, 8.971, 6.869, 20.504, 18.756, 26.208, 10.811, 23.344, 14.535, 6.81, 1.627, 2.037]
    # b=[32.795, 15.616, 158.184, 136.904, 29.483, 190.191, 16.337, 168.864, 28.11, 50.733, 1.92, 2.762, 1.477, 10.802, 3.922, 3.677, 0.351, 28.797, 28.765, 21.759, 7.386, 28.736, 33.882, 27.173, 26.939, 9.45, 5.231, 9.133, 1.038, 4.271, 13.419, 16.391, 9.314, 70.346, 18.078, 20.701, 30.183, 12.705, 8.274, 1.332, 4.125, 2.909, 2.059, 5.528, 29.721, 21.237, 18.999, 31.424, 41.096, 15.209, 25.498, 13.716, 8.179, 16.538, 13.773, 9.619, 16.925, 13.154, 3.066, 2.057, 3.145, 9.883, 23.64, 40.177, 20.975, 31.715, 21.348, 24.206, 27.832, 7.02, 8.757, 6.908, 4.986, 4.157, 2.724, 29.95, 16.305, 47.726, 47.82, 20.825, 9.884, 40.344, 22.598, 9.521, 3.72, 1.658, 0.449, 4.182, 0.764, 3.916, 0.611, 19.697, 17.793, 16.579, 22.278, 27.788, 11.391, 29.486, 7.48, 25.522, 0.413, 15.997, 3.952, 1.901, 21.23, 4.369, 14.753, 18.957, 24.506, 24.8, 29.78, 6.7, 28.655, 11.451, 2.28, 11.332, 3.193, 4.924, 7.249, 25.45, 4.821, 51.132, 12.473, 24.724, 16.585, 12.194, 15.164, 6.561, 6.299, 4.821, 14.269, 5.305, 6.718, 15.309, 12.02, 11.823, 32.074, 59.275, 3.091, 47.365, 14.427, 3.499, 4.856, 0.604, 9.921, 19.168, 14.309, 43.567, 14.167, 19.048, 28.66, 24.943, 29.102, 11.897, 14.952, 23.039, 2.758, 4.613, 8.473, 28.213, 13.238, 8.013, 25.265, 24.395, 39.111, 24.097, 22.567, 15.468, 19.848, 16.221, 11.063, 26.467, 27.519, 25.576, 14.239, 51.038, 11.423, 25.923, 9.401, 27.111, 4.007, 3.876, 2.031, 5.389, 2.195, 6.292, 9.698, 4.195, 23.956, 10.181, 6.295, 27.272, 45.239, 31.218, 27.56, 21.109, 9.487, 14.402, 12.001, 6.167, 2.066, 8.364, 4.201, 3.605, 32.695, 10.781, 23.389, 25.41, 23.321, 23.416, 26.54, 16.843, 21.539, 13.934, 17.282, 11.672, 11.764, 8.695, 19.68, 0.857, 15.058, 8.499, 1.21, 25.924, 7.286, 7.117, 3.167, 2.313, 10.563, 5.869, 22.061, 14.995, 9.55, 12.79, 16.059, 14.406, 13.62, 1.273, 4.074, 1.69, 9.254, 12.365, 4.545, 4.754, 4.427, 18.543, 31.975, 13.471, 9.907, 10.757, 2.751, 0.534, 2.294, 0.815, 2.443, 6.939, 9.959, 6.057, 20.159, 1.864, 9.46, 34.802, 3.798, 21.247, 9.72, 12.971, 5.252, 2.851, 1.344, 0.273, 0.539, 2.408, 2.573, 21.361, 5.806, 24.494, 28.91, 27.507, 8.416, 9.941, 3.276, 8.356, 0.831, 3.747, 20.511, 33.637, 4.651, 20.89, 21.662, 18.709, 12.504, 6.399, 7.141, 2.287, 0.64, 5.374, 6.678, 30.665, 3.538, 12.212, 25.73, 23.666, 13.785, 10.765, 9.237, 0.542, 1.201, 0.267, 1.901, 5.449, 0.684, 35.342, 15.538, 15.259, 5.286, 11.262, 18.542, 14.985, 19.684, 4.591, 14.712, 2.138, 11.231, 10.457, 16.336, 12.41, 10.394, 16.873, 9.828, 13.328, 17.141, 0.939, 3.125, 0.823, 16.853, 8.942, 6.81, 20.862, 18.821, 26.037, 10.81, 23.294, 14.589, 6.639, 1.611, 1.987]

    # 3000
    # a=[25.568, 12.071, 10.437, 30.699, 192.666, 174.784, 96.082, 56.291, 190.298, 71.402, 212.629, 13.359, 180.792, 202.128, 9.081, 0.551, 24.291, 37.859, 50.173, 63.407, 72.232, 20.085, 64.057, 53.881, 90.168, 7.882, 13.748, 10.137, 12.517, 9.688, 1.671, 12.57, 2.504, 13.914, 29.575, 60.726, 45.378, 81.976, 92.399, 45.431, 47.874, 42.875, 22.742, 12.863, 3.335, 11.114, 6.181, 3.259, 1.078, 5.301, 7.532, 17.534, 21.138, 54.207, 104.658, 46.321, 105.562, 79.276, 25.706, 48.661, 30.817, 5.7, 7.305, 17.252, 15.549, 6.017, 4.637, 15.333, 39.467, 49.294, 60.802, 31.045, 85.101, 37.446, 48.14, 69.2, 36.571, 35.837, 8.858, 5.217, 3.782, 26.014, 4.377, 18.042, 40.899, 68.143, 109.158, 53.3, 77.016, 54.025, 20.693, 36.472, 51.092, 1.841, 9.095, 4.864, 4.081, 1.885, 6.846, 16.248, 26.065, 47.953, 46.861, 29.429, 137.379, 115.293, 67.787, 30.844, 36.059, 7.594, 3.601, 10.161, 16.255, 3.835, 11.952, 1.878, 2.081, 4.783, 11.037, 70.381, 42.779, 35.945, 55.619, 45.724, 30.427, 53.914, 26.058, 26.434, 1.181, 25.736, 5.879, 5.516, 7.667, 4.728, 28.241, 42.503, 50.969, 77.147, 54.65, 47.93, 71.408, 92.33, 53.571, 12.377, 18.697, 2.819, 15.071, 7.523, 2.243, 29.09, 20.79, 73.567, 60.823, 90.959, 45.289, 71.059, 39.756, 36.095, 14.394, 10.724, 17.321, 32.677, 15.856, 6.09, 4.539, 52.175, 31.963, 82.956, 68.518, 62.422, 67.109, 43.882, 42.232, 27.264, 30.755, 7.713, 2.435, 6.276, 7.066, 15.182, 36.729, 61.613, 22.977, 49.758, 71.083, 63.688, 40.072, 23.561, 13.558, 8.115, 5.332, 7.701, 17.144, 34.317, 24.915, 57.457, 45.558, 44.635, 39.553, 40.478, 39.472, 36.216, 33.67, 23.851, 7.504, 2.523, 4.554, 13.244, 15.091, 57.821, 52.226, 66.631, 71.753, 46.635, 81.301, 48.158, 41.296, 37.052, 9.178, 21.224, 36.32, 4.916, 4.086, 5.038, 2.481, 20.734, 49.739, 55.967, 62.239, 41.359, 47.058, 54.964, 63.8, 47.134, 24.744, 25.525, 2.753, 4.915, 1.857, 11.26, 14.995, 18.336, 48.694, 36.727, 35.637, 27.324, 25.208, 15.737, 18.19, 11.887, 7.78, 6.79, 8.488, 2.855, 1.619, 6.025, 13.612, 10.249, 14.856, 34.684, 60.57, 38.122, 27.414, 17.914, 16.008, 15.246, 4.7, 9.812, 2.453, 0.931, 2.356, 1.601, 26.668, 20.154, 33.199, 37.918, 30.338, 23.743, 17.212, 26.754, 15.459, 13.3, 0.404, 2.831, 1.77, 5.968, 6.79, 19.949, 11.08, 35.485, 17.657, 44.362, 54.199, 38.332, 32.574, 21.317, 8.47, 1.677, 3.025, 2.155, 4.491, 0.136, 2.525, 5.214, 3.839, 16.809, 32.083, 52.995, 46.112, 36.497, 33.04, 10.969, 4.094, 10.239, 3.394, 5.865, 1.785, 10.989, 3.983, 7.328, 19.802, 26.096, 58.408, 21.398, 29.987, 25.893, 12.934, 38.964, 14.381, 4.089, 13.718, 1.635, 2.007, 2.904, 2.436, 5.387, 13.129, 15.686, 49.7, 46.016, 17.99, 33.632, 33.582, 29.171, 15.512, 10.944, 3.412, 2.438, 2.289, 0.819, 6.306, 13.025, 24.859, 29.617, 24.922, 17.254, 17.459, 35.726, 40.685, 29.16, 4.004, 4.474, 1.146, 2.522, 2.696, 13.98, 12.265, 29.634, 30.396, 12.99, 46.009, 17.741, 19.435, 43.894, 11.945, 4.204, 9.213, 0.813, 1.758, 1.435, 4.798, 3.805, 16.144, 31.167, 10.246, 20.178, 37.791, 61.963, 33.065, 10.454, 10.479, 0.981, 8.223, 1.64]
    # b=[25.729, 14.08, 10.499, 31.373, 133.603, 205.766, 83.195, 42.479, 146.851, 52.645, 165.33, 15.538, 181.539, 262.75, 9.179, 0.415, 25.421, 35.96, 48.891, 60.468, 59.92, 19.992, 54.066, 47.377, 91.805, 8.197, 14.262, 7.207, 10.759, 6.855, 1.651, 9.39, 1.656, 10.016, 22.365, 56.275, 45.155, 75.855, 92.324, 42.17, 44.782, 36.352, 22.293, 12.846, 2.78, 7.788, 3.086, 3.344, 0.833, 8.113, 7.557, 9.055, 17.502, 41.433, 88.609, 40.801, 84.359, 62.768, 26.298, 50.924, 31.54, 5.794, 4.319, 11.959, 9.426, 4.661, 4.678, 11.139, 32.429, 40.354, 51.593, 30.76, 84.104, 33.966, 46.164, 60.502, 33.251, 20.068, 6.744, 2.799, 2.879, 19.57, 3.335, 13.774, 36.036, 59.285, 117.871, 48.977, 63.876, 54.174, 18.303, 24.719, 37.989, 1.886, 8.203, 6.203, 3.112, 1.44, 4.99, 9.565, 24.026, 34.513, 45.278, 24.205, 110.182, 81.252, 64.726, 29.605, 39.729, 6.955, 2.722, 9.402, 15.438, 3.697, 12.013, 1.858, 2.074, 4.778, 13.316, 64.575, 43.107, 38.441, 55.694, 48.691, 30.623, 53.363, 27.484, 18.32, 1.08, 25.701, 5.544, 4.103, 5.346, 3.881, 17.469, 50.094, 45.003, 66.581, 49.82, 43.554, 70.404, 66.867, 50.069, 9.005, 15.669, 4.687, 9.414, 5.704, 1.509, 21.356, 17.38, 58.102, 51.9, 78.036, 42.888, 56.498, 46.091, 34.302, 12.432, 9.865, 13.795, 28.192, 12.711, 3.306, 6.808, 43.404, 29.957, 65.495, 68.449, 55.41, 67.225, 43.815, 42.136, 27.13, 31.266, 7.652, 2.416, 6.289, 7.089, 15.113, 36.62, 61.562, 22.968, 49.592, 70.38, 63.02, 38.462, 20.594, 13.638, 8.14, 5.345, 7.587, 17.177, 40.542, 24.832, 56.854, 47.748, 44.692, 41.154, 42.543, 37.048, 33.307, 29.422, 29.215, 5.026, 2.101, 3.961, 9.629, 10.079, 46.169, 43.083, 64.96, 67.184, 40.202, 79.211, 41.132, 34.019, 38.339, 9.99, 19.318, 28.332, 4.436, 3.104, 3.342, 1.695, 13.459, 47.148, 56.647, 69.742, 33.707, 46.932, 49.872, 53.174, 48.409, 20.802, 21.598, 2.054, 3.349, 1.884, 11.204, 15.05, 18.519, 48.614, 30.92, 39.076, 27.36, 25.018, 15.025, 16.54, 11.652, 7.845, 4.501, 8.609, 2.783, 1.629, 5.786, 13.133, 9.723, 14.934, 29.761, 60.694, 35.127, 27.5, 17.872, 16.095, 15.29, 4.596, 9.798, 2.472, 0.947, 2.359, 1.606, 26.82, 20.257, 22.665, 37.664, 30.432, 23.533, 16.774, 26.38, 14.712, 13.19, 0.411, 2.853, 1.74, 6.019, 6.794, 19.834, 11.16, 34.353, 17.632, 43.611, 52.45, 36.684, 32.642, 17.347, 8.406, 1.97, 2.935, 2.195, 4.507, 0.137, 2.518, 5.204, 3.836, 16.91, 32.917, 53.769, 42.994, 36.306, 30.383, 10.946, 4.1, 10.271, 3.397, 5.883, 1.769, 10.821, 3.832, 7.585, 19.919, 25.966, 58.096, 21.437, 29.943, 25.955, 11.757, 38.645, 14.447, 4.196, 16.718, 1.64, 2.008, 2.945, 2.46, 5.488, 13.196, 15.822, 48.563, 44.966, 18.007, 33.332, 36.136, 28.13, 16.361, 10.904, 3.396, 2.43, 2.269, 0.817, 6.237, 13.063, 24.888, 29.424, 24.901, 17.242, 17.495, 35.395, 38.842, 29.111, 4.096, 4.434, 1.151, 2.512, 2.713, 13.948, 13.646, 30.143, 31.929, 13.044, 46.758, 17.66, 19.383, 44.537, 12.001, 4.242, 9.379, 0.805, 1.755, 1.431, 4.816, 3.893, 16.277, 31.076, 10.187, 20.094, 37.968, 62.173, 33.008, 10.505, 10.457, 0.979, 8.333, 1.646]

    # 1200
    # a=[1449.356, 141.929, 126.194, 65.157, 40.083, 124.842, 60.243, 66.516, 57.784, 32.708, 47.564, 12.199, 4.465, 25.182, 33.702, 42.072, 78.817, 129.527, 93.167, 42.847, 43.458, 36.665, 54.176, 35.835, 14.789, 15.26, 11.597, 16.983, 1.874, 36.374, 35.076, 187.122, 73.896, 84.138, 49.899, 27.757, 68.528, 17.649, 13.453, 34.35, 4.875, 18.202, 24.224, 27.685, 45.312, 70.875, 95.903, 88.799, 93.129, 46.449, 43.254, 7.807, 6.758, 1.972, 8.297, 6.499, 1.452, 14.89, 93.59, 81.598, 32.872, 33.941, 47.018, 48.299, 118.622, 39.562, 26.341, 20.885, 63.047, 36.925, 68.726, 57.985, 50.318, 115.345, 71.0, 92.331, 26.159, 9.633, 3.296, 2.692, 40.324, 8.8, 66.275, 39.367, 35.723, 26.952, 116.845, 123.68, 74.225, 76.293, 102.685, 9.172, 34.835, 6.239, 13.63, 80.28, 75.93, 89.033, 53.441, 96.716, 135.869, 44.896, 73.644, 90.657, 10.402, 28.795, 22.946, 17.593, 41.645, 73.516, 24.243, 72.207, 87.385, 80.193, 54.423, 118.175, 30.744, 14.777, 63.497, 18.039, 2.043, 1.885, 52.853, 91.348, 101.214, 43.263, 84.887, 137.024, 87.572, 50.921, 30.205, 11.31, 16.609, 50.623, 13.315, 0.889, 33.491, 32.976, 126.035, 151.946, 218.925, 81.46, 53.35, 39.003, 0.974, 3.958, 1.539, 23.019, 11.136, 41.741, 58.522, 46.894, 40.761, 68.141, 41.683, 4.497, 19.62, 1.428, 2.196, 3.211, 5.303, 26.427, 8.361, 63.386, 39.649, 83.964, 71.953, 31.786, 15.372, 35.03, 24.958, 38.694, 17.792, 1.603, 4.345, 28.331, 21.665, 23.134, 60.919, 38.956, 36.18, 24.339, 72.97, 26.114, 20.444, 57.884, 21.625, 23.391, 6.123, 6.499, 0.497, 5.83, 58.537, 76.876, 35.646, 66.513, 97.442, 52.16, 85.278, 32.061, 45.806, 17.159, 31.886, 53.548, 50.116, 95.774, 126.989, 122.997, 48.564, 70.797, 21.659, 44.166, 32.262, 16.682, 17.327, 24.41, 55.433, 18.07, 16.721, 32.082, 75.902, 121.595, 82.827, 47.883, 82.687, 27.748, 50.11, 13.646, 3.614, 16.452, 9.299, 2.754, 27.572, 47.885, 146.409, 47.66, 44.314, 81.861, 49.35, 43.486, 52.538, 23.389, 40.523, 34.321, 23.626, 96.789, 104.021, 59.691, 20.601, 152.007, 57.479, 43.498, 51.649, 55.771, 2.689, 9.235, 5.257, 3.685, 23.034, 20.997, 65.97, 60.013, 109.347, 125.884, 49.441, 57.702, 141.593, 39.52, 19.683, 4.805]
    # b=[1448.634, 143.159, 126.616, 65.794, 45.26, 137.74, 69.363, 76.142, 56.377, 37.946, 46.332, 16.905, 5.905, 29.712, 32.676, 52.408, 89.292, 117.923, 83.723, 37.579, 41.336, 42.41, 64.051, 36.031, 14.988, 15.265, 12.603, 19.727, 4.298, 46.87, 40.884, 204.966, 73.497, 73.248, 44.369, 21.932, 43.151, 11.724, 7.306, 26.893, 8.33, 23.705, 32.304, 19.863, 47.82, 60.218, 96.266, 89.316, 90.542, 37.256, 36.771, 5.697, 6.694, 3.432, 10.038, 7.427, 2.905, 25.243, 86.376, 83.36, 47.412, 29.639, 49.277, 50.826, 115.976, 41.803, 15.542, 12.617, 62.866, 21.844, 65.941, 45.123, 30.018, 82.696, 62.304, 78.713, 33.655, 8.349, 7.895, 5.372, 38.176, 8.557, 54.58, 32.519, 29.687, 18.113, 96.75, 99.583, 71.275, 82.505, 92.335, 19.803, 34.634, 3.928, 6.206, 70.391, 62.821, 79.017, 53.011, 102.386, 117.586, 40.902, 59.24, 80.12, 10.387, 26.602, 19.541, 10.936, 23.091, 63.489, 17.629, 59.968, 58.24, 76.907, 45.929, 103.881, 40.013, 17.27, 57.218, 15.348, 2.858, 2.465, 52.143, 55.719, 96.557, 42.897, 92.486, 133.985, 87.493, 40.49, 19.273, 6.079, 9.32, 31.221, 7.788, 0.624, 24.039, 35.461, 91.192, 105.204, 188.407, 74.646, 36.551, 41.225, 0.959, 3.873, 1.49, 22.388, 22.9, 45.415, 58.385, 39.623, 46.033, 68.354, 42.814, 3.554, 16.246, 1.384, 2.104, 3.162, 5.143, 26.306, 10.751, 58.904, 42.115, 78.792, 45.742, 23.078, 9.02, 22.954, 22.955, 24.029, 9.769, 1.579, 4.328, 19.909, 32.202, 23.31, 52.236, 44.733, 43.421, 24.537, 61.541, 37.272, 26.006, 62.109, 22.378, 26.737, 7.682, 8.513, 0.49, 5.794, 60.019, 77.175, 34.982, 68.772, 78.53, 44.44, 89.02, 24.936, 38.092, 15.375, 33.136, 44.473, 40.007, 80.529, 122.397, 102.895, 54.467, 81.68, 25.146, 50.205, 34.751, 14.239, 11.325, 18.947, 42.426, 18.962, 22.312, 37.697, 80.1, 101.448, 91.898, 53.433, 79.145, 24.905, 54.637, 11.754, 9.564, 10.687, 13.036, 2.903, 28.597, 47.136, 154.706, 44.847, 52.261, 67.359, 93.685, 43.79, 61.345, 27.625, 39.271, 33.359, 22.796, 83.447, 96.377, 59.49, 26.13, 123.384, 39.998, 43.566, 36.287, 52.819, 5.615, 8.838, 9.585, 6.503, 29.126, 20.967, 54.619, 61.689, 97.078, 148.23, 40.158, 60.92, 139.333, 34.532, 17.597, 1.662]

    # 1350
    # a=[525.438, 647.343, 5.344, 25.102, 45.206, 123.991, 49.279, 26.229, 19.944, 52.906, 35.763, 36.428, 48.49, 3.75, 15.186, 32.707, 41.903, 72.29, 54.44, 95.807, 85.191, 94.292, 112.438, 106.506, 77.606, 6.927, 44.379, 27.95, 31.683, 40.743, 19.748, 76.073, 53.032, 60.52, 75.158, 68.924, 96.538, 22.836, 62.389, 85.297, 1.115, 6.07, 19.484, 62.944, 27.954, 22.529, 70.912, 49.806, 66.567, 39.35, 58.649, 58.022, 27.647, 14.258, 14.65, 11.36, 10.001, 20.429, 69.159, 30.152, 83.389, 24.198, 52.986, 71.186, 13.789, 66.401, 35.772, 13.526, 6.808, 2.106, 13.514, 28.987, 33.229, 58.17, 40.078, 50.781, 32.642, 10.282, 66.707, 31.395, 38.196, 18.646, 3.732, 9.141, 7.397, 5.635, 37.465, 31.98, 103.378, 66.422, 43.245, 61.463, 30.085, 27.162, 24.057, 13.313, 13.937, 1.382, 4.444, 4.958, 5.486, 11.698, 37.433, 4.539, 167.783, 86.931, 168.94, 60.734, 36.688, 83.235, 7.212, 6.552, 2.308, 8.108, 16.589, 32.009, 51.151, 14.256, 181.942, 126.711, 52.229, 98.732, 18.546, 39.255, 61.75, 32.322, 11.238, 18.208, 16.121, 59.391, 126.319, 128.432, 150.757, 108.811, 23.675, 97.44, 20.527, 38.143, 18.531, 22.909, 16.296, 112.357, 23.407, 119.688, 42.893, 114.655, 105.93, 84.355, 49.874, 36.464, 15.481, 2.654, 4.297, 2.032, 5.151, 42.195, 25.531, 36.769, 15.313, 42.552, 35.131, 89.417, 59.822, 81.742, 105.268, 17.401, 1.109, 0.269, 2.723, 12.746, 8.865, 56.486, 29.305, 53.528, 59.914, 46.625, 54.58, 42.649, 42.931, 111.222, 29.271, 36.755, 18.223, 18.046, 19.355, 3.556, 20.91, 25.858, 46.174, 6.713, 113.275, 85.877, 67.133, 28.243, 79.455, 54.946, 46.556, 5.008, 13.247, 17.466, 13.897, 14.488, 4.248, 69.853, 32.787, 58.245, 83.437, 155.495, 110.922, 111.376, 72.972, 22.964, 5.575, 12.635, 36.948, 6.413, 0.676, 21.117, 26.733, 84.005, 160.425, 70.398, 100.873, 112.736, 78.636, 9.656, 17.726, 35.212, 9.438, 6.228, 5.565, 3.828, 13.935, 9.39, 4.46, 56.001, 70.462, 44.897, 81.134, 55.579, 141.298, 40.88, 50.406, 22.984, 50.248, 6.654, 14.364, 9.444, 7.79, 1.402, 5.264, 2.126, 56.439, 92.44, 59.557, 190.28, 114.261, 95.854, 61.659, 67.212, 7.102, 11.818, 2.307, 51.421, 71.387, 70.091, 113.611, 73.934, 143.274, 188.543, 75.318, 17.451, 6.096, 1.112, 25.435, 14.436, 78.163, 115.572, 151.498, 71.282, 61.904, 113.831, 37.88, 3.322, 63.678]
    # b=[509.832, 721.787, 8.083, 25.875, 46.859, 92.547, 52.733, 24.278, 16.11, 42.531, 33.996, 33.527, 41.084, 2.711, 11.145, 25.169, 31.7, 54.529, 42.572, 97.717, 91.085, 90.447, 86.391, 89.259, 54.331, 4.222, 29.533, 20.613, 27.967, 35.023, 14.434, 70.446, 48.935, 53.859, 74.275, 61.871, 80.336, 29.152, 76.851, 66.276, 0.982, 7.178, 20.991, 37.857, 20.475, 8.952, 77.226, 50.581, 66.439, 31.755, 54.515, 57.918, 20.248, 7.01, 23.488, 11.369, 10.007, 15.712, 58.943, 31.473, 83.851, 26.561, 46.424, 81.403, 13.674, 64.872, 31.625, 14.912, 5.262, 1.587, 9.941, 30.529, 38.479, 53.156, 33.505, 41.76, 33.925, 10.702, 72.661, 20.405, 21.046, 11.629, 5.017, 7.987, 10.023, 5.694, 41.054, 36.192, 95.302, 58.955, 51.898, 56.056, 30.094, 27.245, 24.532, 17.846, 22.382, 1.046, 3.323, 3.695, 4.566, 9.777, 33.661, 3.696, 168.245, 87.259, 199.95, 65.961, 50.165, 95.744, 9.91, 5.893, 3.058, 10.083, 15.855, 37.786, 43.903, 20.641, 196.173, 101.982, 70.058, 101.16, 22.019, 45.461, 75.457, 39.004, 11.291, 26.425, 16.898, 53.307, 150.373, 141.068, 140.183, 78.142, 24.189, 89.098, 33.691, 53.55, 26.957, 21.677, 37.188, 92.33, 25.924, 82.358, 46.61, 127.043, 102.866, 78.354, 49.587, 62.256, 16.373, 5.618, 8.595, 1.574, 4.676, 34.281, 26.24, 39.471, 20.765, 47.003, 42.707, 81.779, 48.309, 77.774, 112.414, 30.725, 2.545, 0.841, 2.71, 12.173, 13.362, 39.596, 27.081, 83.55, 58.001, 58.468, 63.061, 50.506, 70.269, 105.913, 32.204, 23.47, 10.655, 12.918, 15.11, 2.932, 18.175, 29.212, 46.769, 7.634, 139.787, 84.171, 61.056, 25.002, 75.335, 65.288, 62.78, 6.841, 30.437, 33.482, 16.267, 38.031, 4.188, 70.966, 31.048, 55.859, 88.37, 141.988, 116.516, 104.628, 60.826, 22.775, 7.78, 18.925, 21.556, 6.151, 1.648, 28.594, 29.499, 82.081, 139.821, 77.945, 124.892, 116.472, 58.358, 15.661, 26.32, 48.796, 19.906, 8.489, 6.951, 5.8, 14.62, 31.966, 11.33, 66.852, 78.292, 41.493, 70.118, 62.701, 158.441, 40.007, 54.322, 33.426, 62.348, 15.002, 27.36, 8.042, 20.572, 2.639, 6.093, 1.854, 61.886, 91.458, 58.816, 132.281, 128.592, 101.296, 50.419, 60.825, 7.408, 31.514, 3.363, 56.379, 60.864, 87.959, 113.885, 75.982, 95.61, 146.273, 64.742, 16.626, 13.866, 2.371, 32.685, 18.96, 81.477, 120.848, 166.536, 78.243, 81.59, 108.002, 34.565, 8.919, 59.003]

    # # 1600
    # a=[32.834, 18.253, 16.584, 134.108, 120.274, 93.112, 111.517, 29.593, 30.761, 66.301, 23.163, 4.019, 37.099, 3.344, 10.636, 28.909, 32.202, 12.163, 69.271, 95.099, 183.102, 37.31, 33.814, 119.682, 77.814, 57.923, 31.155, 16.145, 25.797, 100.761, 90.903, 106.078, 117.184, 69.78, 44.434, 42.192, 116.654, 113.394, 26.704, 3.634, 13.795, 7.159, 23.443, 27.421, 76.875, 115.408, 208.8, 292.452, 609.553, 553.144, 426.235, 345.918, 476.905, 460.522, 269.367, 176.661, 157.498, 73.642, 17.948, 8.14, 82.861, 83.595, 100.475, 102.587, 179.198, 171.014, 150.607, 92.782, 163.298, 51.476, 27.609, 1.052, 4.537, 5.495, 5.426, 17.52, 14.796, 19.912, 28.551, 84.092, 82.447, 242.648, 85.352, 153.18, 77.708, 102.199, 109.031, 51.22, 19.963, 20.066, 0.912, 13.386, 18.143, 7.23, 60.364, 64.389, 225.405, 178.382, 134.137, 83.678, 192.154, 100.05, 47.9, 36.831, 40.313, 51.267, 33.494, 20.429, 70.972, 91.14, 123.759, 35.229, 126.16, 73.64, 32.141, 77.551, 17.829, 2.709, 29.047, 7.869, 46.236, 23.694, 20.438, 56.355, 53.23, 114.242, 100.237, 39.686, 37.584, 18.038, 61.779, 10.763, 69.959, 11.024, 15.018, 5.327, 16.148, 43.78, 26.769, 105.891, 38.278, 47.564, 95.388, 31.242, 60.2, 73.468, 11.11, 23.32, 9.305, 18.731, 22.408, 114.311, 174.83, 130.174, 341.658, 345.753, 318.287, 331.916, 213.579, 180.172, 69.803, 56.511, 70.933, 11.25, 10.052, 9.423, 57.4, 23.577, 36.672, 212.963, 94.373, 100.095, 60.095, 100.329, 47.194, 44.726, 10.391, 2.414, 13.217, 27.524, 106.739, 60.71, 100.161, 184.404, 79.663, 127.195, 49.815, 179.452, 43.481, 18.186, 1.863, 2.732, 35.688, 55.819, 49.258, 39.515, 71.733, 122.057, 93.538, 81.467, 26.111, 32.918, 19.245, 16.919, 17.357, 7.116]
    # b=[32.88, 17.879, 16.39, 134.947, 114.558, 90.973, 104.052, 32.582, 32.514, 77.9, 24.845, 4.887, 38.373, 3.213, 10.619, 29.118, 31.656, 13.208, 77.596, 94.737, 187.01, 29.22, 33.74, 110.519, 80.085, 58.294, 33.001, 17.734, 40.582, 95.177, 73.144, 103.501, 123.096, 68.237, 44.534, 30.053, 112.566, 84.669, 24.584, 3.631, 15.219, 10.971, 27.842, 27.515, 75.025, 124.916, 229.414, 280.443, 597.253, 511.302, 401.289, 340.584, 405.34, 420.691, 255.536, 155.923, 133.484, 49.719, 16.665, 7.444, 71.962, 85.321, 100.01, 118.721, 170.651, 154.334, 113.742, 82.877, 133.031, 40.868, 20.958, 0.984, 4.472, 6.71, 3.321, 17.669, 14.592, 12.807, 25.197, 73.096, 71.874, 213.066, 84.993, 153.969, 54.567, 113.048, 79.025, 40.653, 14.511, 14.412, 0.906, 13.434, 23.865, 7.963, 59.79, 57.102, 240.538, 179.914, 135.743, 91.485, 192.148, 88.607, 43.798, 35.114, 27.505, 40.782, 31.368, 20.543, 58.42, 88.765, 107.344, 29.578, 118.131, 77.333, 33.402, 60.707, 15.636, 2.106, 25.419, 7.4, 43.979, 24.452, 17.716, 53.209, 45.702, 93.601, 75.499, 45.397, 25.454, 16.743, 45.913, 10.74, 56.651, 4.856, 13.465, 4.856, 11.852, 34.466, 25.546, 92.685, 34.428, 38.421, 60.318, 35.131, 49.854, 68.61, 9.1, 20.506, 12.568, 15.378, 18.581, 104.422, 188.587, 120.486, 312.423, 335.234, 284.511, 326.101, 197.904, 154.523, 65.419, 59.138, 78.862, 11.377, 9.908, 11.208, 64.766, 24.116, 34.009, 232.284, 92.134, 95.803, 59.736, 102.853, 47.483, 42.132, 9.77, 1.976, 13.329, 27.451, 70.042, 61.49, 72.864, 128.837, 64.572, 87.305, 46.21, 163.545, 39.574, 17.575, 2.026, 5.589, 23.462, 47.773, 58.611, 28.964, 72.397, 142.483, 84.453, 85.504, 30.867, 32.913, 14.378, 22.591, 21.79, 10.663]

    # # 2600
    # a=[14.689, 54.743, 114.537, 136.734, 160.266, 319.67, 132.555, 397.405, 94.846, 171.122, 96.048, 52.404, 37.074, 5.376, 9.313, 19.792, 150.531, 214.018, 206.131, 264.988, 190.716, 151.427, 96.621, 110.71, 30.412, 30.246, 23.864, 10.272, 4.28, 28.193, 21.268, 20.742, 71.186, 34.293, 122.4, 236.232, 201.39, 150.531, 113.713, 59.536, 93.934, 141.771, 44.726, 51.539, 52.063, 23.656, 28.291, 59.718, 111.93, 199.285, 579.125, 884.329, 587.499, 1042.874, 938.61, 553.219, 752.928, 301.505, 507.685, 214.504, 93.366, 51.89, 38.875, 35.801, 28.416, 28.973, 59.387, 26.605, 34.643, 71.621, 270.394, 220.259, 382.419, 205.029, 330.551, 108.311, 288.859, 207.135, 138.103, 37.304, 81.172, 18.301, 22.496, 16.428, 71.878, 117.5, 101.939, 152.828, 120.934, 172.137, 158.518, 197.498, 63.846, 87.226, 72.306, 13.772, 3.386, 6.131, 35.153, 88.514, 89.076, 238.389, 296.667, 415.232, 272.941, 431.824, 300.827, 184.746, 207.913, 41.141, 42.575, 3.756, 14.273, 7.681, 43.622, 66.537, 74.9, 139.83, 114.396, 109.327, 91.431, 50.013, 91.523, 23.501, 30.675, 21.034, 2.218, 28.26, 17.174, 125.553, 179.966, 136.04, 114.712, 68.997, 175.208, 44.963, 20.55, 30.96, 4.969, 27.309, 26.753, 2.376, 21.48, 149.42, 82.128, 87.966, 72.134, 86.218, 138.717, 135.834, 33.507, 8.64, 19.856, 28.712, 4.876, 3.357, 24.657, 74.958, 119.072, 346.632, 417.362, 453.037, 476.912, 652.338, 663.099, 406.721, 236.024, 231.995, 82.246, 93.755, 94.482, 23.742, 26.176, 1.927, 3.03, 34.754, 63.103, 130.059, 136.795, 90.13, 161.138, 194.518, 158.582, 76.764, 55.669, 57.173, 8.333, 18.631, 29.025, 5.346, 10.632, 7.172, 55.1, 136.74, 92.824, 170.665, 263.832, 193.871, 160.27, 101.972, 124.994, 29.851, 47.152, 38.06, 18.503, 10.012, 27.966, 20.58, 58.838, 31.744, 78.65, 171.267, 111.665, 88.815, 94.515, 89.574, 157.757, 49.771, 46.97, 23.04]
    # b=[14.529, 64.851, 108.267, 139.074, 143.52, 280.267, 133.34, 330.844, 62.809, 162.607, 81.237, 51.648, 37.129, 7.645, 8.72, 22.59, 162.638, 214.754, 189.376, 270.618, 170.991, 147.988, 103.038, 84.702, 32.561, 14.25, 17.833, 5.612, 3.565, 34.612, 31.939, 27.89, 77.903, 42.027, 127.96, 225.037, 191.322, 130.901, 108.574, 43.953, 95.564, 131.298, 34.361, 36.235, 39.203, 27.561, 26.613, 64.316, 97.141, 195.872, 533.876, 830.804, 557.641, 1036.074, 842.853, 491.625, 685.064, 303.862, 452.928, 210.662, 93.208, 55.038, 34.342, 33.544, 14.662, 34.718, 82.163, 30.729, 39.046, 72.414, 246.654, 220.083, 363.839, 273.453, 361.199, 111.231, 277.366, 196.729, 137.84, 40.996, 66.82, 14.132, 21.634, 9.591, 68.331, 129.734, 105.519, 155.488, 113.985, 165.214, 157.778, 182.677, 61.943, 77.787, 54.482, 11.216, 2.525, 6.206, 41.69, 117.447, 81.409, 250.081, 250.227, 411.429, 261.112, 418.219, 250.135, 162.73, 172.656, 45.831, 49.235, 3.622, 10.939, 6.989, 37.131, 58.671, 82.573, 127.245, 95.366, 94.506, 105.629, 57.254, 87.05, 27.705, 18.886, 22.055, 1.646, 37.167, 20.453, 127.487, 168.818, 148.302, 106.126, 70.271, 151.727, 41.26, 18.127, 31.294, 8.219, 18.797, 18.084, 2.453, 19.988, 120.551, 86.707, 91.143, 72.038, 81.1, 137.298, 151.386, 35.381, 8.241, 20.024, 25.114, 3.906, 3.628, 20.057, 78.41, 126.246, 342.621, 382.426, 450.319, 441.201, 533.795, 513.532, 347.578, 205.144, 200.719, 72.128, 93.51, 80.385, 13.233, 21.754, 1.598, 2.654, 42.683, 60.88, 145.242, 144.809, 85.727, 156.211, 215.456, 150.434, 87.373, 53.532, 53.387, 7.854, 15.736, 27.325, 4.355, 10.557, 7.054, 59.432, 134.438, 92.231, 141.98, 224.724, 154.038, 128.489, 96.301, 121.797, 27.576, 35.282, 33.268, 16.221, 5.765, 22.472, 12.343, 77.23, 28.985, 74.841, 190.844, 102.092, 79.353, 89.21, 84.493, 154.19, 49.07, 43.208, 15.184]

    # collect query latency data
    pid_latency_list=list()
    ppo_latency_list=list()
    opt_latency_list=[5134.15,25645.54,9624.15,12654.55,27149.968,2883.98,2281.69,18775.61,8472.11,7582.669]
    titles=list()
    for idx, key in enumerate(latency_data.keys()):
        pid_latency_list.append(sum(latency_data[key][0]))
        ppo_latency_list.append(sum(latency_data[key][1]))
        titles.append(key)

    # collect rep latency data
    pid_rep_latency_list = [177.16,706.81, 266.91,125.64,56.877,2.902,1.519,195.745,144.158,86.007]
    ppo_rep_latency_list = [9.64,213.16, 104.26, 104.31,15.317,1.3549,1.104,50.97,43.982,51.219]
    opt_rep_latency_list = [128.8, 707.22, 287.51, 212.49, 93.048, 6.546, 1.19, 240.5, 163.01, 149.27]


    # ['query', 'rep']
    for metric in ['rep']:
        if metric=='query':
            data = [pid_latency_list, ppo_latency_list, opt_latency_list]
            labels = ["Feedback", "PPOController", "OPT"]
            colors = ['#007BFF', '#FF7F50', '#6C757D']
        else:
            data=[pid_rep_latency_list,ppo_rep_latency_list,opt_rep_latency_list]
            labels = ["OPT","Feedback","PPOController"]
            colors = ['#007BFF', '#FF7F50', '#6C757D']

        plt.figure(figsize=(10, 4))
        for i in range(len(titles)):
            plt.subplot(2,5,i + 1)
            if metric=='query':
                for j in range(3):
                    rects=plt.bar(j, data[j][i], color=colors[j],width=1)
                    # rects = plt.bar(j, data[j][i], color=colors[j], width=0.7, edgecolor='black', hatch='\\')
                    # height = rects[0].get_height()
                    # print('{:e}'.format(height))
                    # plt.annotate('{}'.format('{:e}'.format(height)[:3]),
                    #              xy=(rects[0].get_x() + rects[0].get_width() / 2, height),
                    #              xytext=(0, 3),  # 3 points vertical offset
                    #              textcoords="offset points",
                    #              ha='center', va='bottom')
            else:
                for j_no,j in enumerate([2,0,1]):
                    rects = plt.bar(j_no, data[j][i], color=colors[j],width=1)
                    # rects=plt.bar(j_no,data[j][i],color=colors[j],width=0.7,edgecolor='black',hatch='\\')
                    # height = rects[0].get_height()
                    # plt.annotate('{}'.format(round(height,1)),
                    #             xy=(rects[0].get_x() + rects[0].get_width() / 2, height),
                    #             xytext=(0, 3),  # 3 points vertical offset
                    #             textcoords="offset points",
                    #             ha='center', va='bottom')
            plt.xticks(ticks=[x for x in range(len(labels))], labels=['' for _ in range(len(labels))])
            plt.xlabel(titles[i])
            if metric=='query':
                plt.ylim(min(pid_latency_list[i], ppo_latency_list[i],opt_latency_list[i])-500,max(pid_latency_list[i], ppo_latency_list[i]) + 500)
            plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
            if i==0:
                plt.legend(labels,bbox_to_anchor=[3.3, 1.1], loc='lower center',frameon=False,ncol=len(labels))
            if i == 0:
                if metric=='query':
                    plt.ylabel('Total Query Latency(s)', loc='center')
                else:
                    plt.ylabel('Total Repartition Time(s)', loc='center')
            if metric=='rep':
                ytop=max([data[j][i] for j in range(3)])
                if ytop<10:
                    plt.ylim(top=ytop+5)
                else:
                    plt.ylim(top=1.4 * ytop)
            # else:
            #     ytop = max([data[j][i] for j in range(3)])
            #     plt.ylim(top=1.1 * ytop)
        plt.subplots_adjust(hspace=0.45, wspace=0.4)
        # plt.show()
        # plt.savefig('chart/query_latency.pdf',bbox_inches='tight')
        plt.savefig('chart/rep_latency.pdf',bbox_inches='tight')

    # plt.figure(figsize=(12, 6))
    # # plt.figure(figsize=(10, 5))
    # colors = ['#5cb3cc', '#c04851']
    # for idx,key in enumerate(latency_data.keys()):
    #     plt.subplot(2,5,idx + 1)
    #     if key in ['TPC-1300']:
    #         interval = 20
    #     elif key in ['TPC-1600']:
    #         interval = 10
    #     elif key in ['TPC-2600']:
    #         interval = 25
    #     elif key in ['orders']:
    #         interval = 8
    #     elif key in ['supplier']:
    #         interval = 2
    #     else:
    #         interval = 20
    #     a=latency_data[key][0]
    #     b=latency_data[key][1]
    #     a=accumulate_val(a,interval)
    #     b=accumulate_val(b,interval)
    #     x=[(time+1)*interval for time in range(len(b))]
    #     l1,=plt.plot(x,a,'-.',color=colors[0])
    #     l2,=plt.plot(x,b,'--.',color=colors[1])
    #     if idx==0:
    #         methods = ['Feedback', 'PPOController']
    #         plt.legend(methods, bbox_to_anchor=[3.3, 1.05], loc='lower center', frameon=False, ncol=len(methods))
    #         # plt.legend(labels=methods, loc=1, frameon=False)
    #     plt.ylim(min(a+b),max(a+b))
    #     plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='y')
    #     if idx == 0 or idx == 5:
    #         plt.ylabel('Query Latency(s)',loc='center')
    #         # plt.xlabel('Time',loc='right')
    #     # plt.title(f'{key}', fontdict={'fontsize': 10})
    #     plt.xlabel(key)
    # plt.subplots_adjust(hspace=0.25, wspace=0.5)
    # # plt.show()
    # plt.savefig(f'chart/latency_per_time.pdf',bbox_inches='tight')

def draw_workload_types():
    fig = plt.figure(figsize=(10, 5))
    # ax = fig.gca(projection='3d')
    ax = fig.add_subplot(projection='3d')

    # Plot scatterplot data (20 2D points per colour) on the x and z axes.
    colors = ('r', 'g', 'k')
    markers=('x','o','^')
    workloads={
        'TPC-H':[(0.6,0.7,0.2,'lineitem'),(-0.7,-0.4,0.5,'orders'),(-1,-0.4,1,'supplier')],
        'TPC-DS':[(0.7,0.6,0.6,'catalog_sales'),(0.4,0.4,0.5,'store_sales'),(0.5,0.6,0.5,'web_sales')],
        'Synthetic':[(-0.6,0.6,0.9,'SY1500'),(0.8,0.2,-0.7,'SY4000'),(1,1,-0.7,'SY1600'),(1,1,-0.6,'SY1200')]
    }

    for cid,env in enumerate(workloads.keys()):
        for workload_dict in workloads[env]:
            ax.scatter(workload_dict[0], workload_dict[1], workload_dict[2], c=colors[cid],marker=markers[cid])
            ax.text(workload_dict[0], workload_dict[1], workload_dict[2],workload_dict[3])
    # Make legend, set axes limits and labels
    # ax.legend()
   
    ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1),
       xlabel='Global Feature', ylabel='Local Feature', zlabel='Periodicity')
    # ax.grid(False)
    ax.set_xticks(np.linspace(-1,1,6))
    ax.set_yticks(np.linspace(-1,1,6))
    ax.set_zticks(np.linspace(-1,1,6))

    # 设置三维图图形区域背景颜色（r,g,b,a）
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

    # ax.(range(-1,1,10))
    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    # ax.view_init(elev=20., azim=-35)
    plt.tight_layout()
    plt.show()
    plt.savefig('workload_type_visualization.png', bbox_inches='tight')

def main():
    # draw_estimated_query_cost()
    # draw_estimated_rep_cost()
    # draw_latency_throughput()
    # draw_rep_latency()
    draw_time_overhead()
    # draw_scalability()
    # draw_selectivity_scalability()
    # draw_workload_size_scalability()
    # draw_workload_types()

if __name__=='__main__':
   main()