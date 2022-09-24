# -*- coding: utf-8 -*-
from tqdm import tqdm
def load_data(column_range, querys):  # Load dataset according to path
    ans = []  # Save data to this array
    item_num = 0
    for query in querys:
        item = []
        for i, v in enumerate(query.attributes):
            if v == 1 and i in column_range:
                item.append(i)
        if len(item) == 0: continue
        ans.append({"value": item, "freq": query.frequency})
        item_num += query.frequency
    return ans, item_num


def save_rule(rule, path):  # save result to .txt file
    with open(path, "w") as f:
        f.write("index  confidence" + "   rules\n")
        index = 1
        for item in rule:
            s = " {:<4d}  {:.3f}        {}=>{}\n".format(index, item[2], str(list(item[0])), str(list(item[1])))
            index += 1
            f.write(s)
        f.close()
    print("result saved,path is:{}".format(path))


class Node:
    def __init__(self, node_name, count, parentNode):
        self.name = node_name
        self.count = count
        self.nodeLink = None  # According to nodeLink, you can find all nodes with the same node name in the whole tree
        self.parent = parentNode  # parent node
        self.children = {}  # child node {name: pointer}


class Fp_growth_plus():

    def data_compress(self, data_set):
        data_dic = {}
        for data in data_set:
            if frozenset(data['value']) not in data_dic:
                data_dic[frozenset(data['value'])] = 1 * data['freq']
            else:
                data_dic[frozenset(data['value'])] += 1 * data['freq']
        return data_dic

    def update_header(self, node, targetNode):  # Update the linked list formed by node nodes in header table
        while node.nodeLink != None:
            node = node.nodeLink
        node.nodeLink = targetNode

    def update_fptree(self, items, count, node, headerTable):  # used to update fp-tree
        if items[0] in node.children:
            # Determine if the first node of items has been used as a child node
            node.children[items[0]].count += count
        else:
            # create new branches
            node.children[items[0]] = Node(items[0], count, node)
            # Update the linked list corresponding to the frequent itemset, adding backwards
            if headerTable[items[0]][1] == None:
                headerTable[items[0]][1] = node.children[items[0]]
            else:
                self.update_header(headerTable[items[0]][1], node.children[items[0]])
            # 递归
        if len(items) > 1:
            self.update_fptree(items[1:], count, node.children[items[0]], headerTable)

    def create_fptree(self, data_dic, min_support, flag=False):  # the main function for constructing tree
        '''
        create fp-tree based on data_dic
        the structure of header_table is
        {"nodename":[num,node],..}
        '''
        item_count = {}  # Count the number of occurrences of each item
        for t in data_dic:  # First traversal, get frequent 1st item set
            for item in t:
                if item not in item_count:
                    item_count[item] = data_dic[t]
                else:
                    item_count[item] += data_dic[t]
        headerTable = {}
        for k in item_count:  # Delete items that do not meet the minimum support
            if item_count[k] >= min_support:
                headerTable[k] = item_count[k]

        freqItemSet = set(headerTable.keys())  # The frequent item set that satisfy the minimum support
        if len(freqItemSet) == 0:
            return None, None
        for k in headerTable:
            headerTable[k] = [headerTable[k], None]  # element: [count, node]
        tree_header = Node('head node', 1, None)
        if flag:
            ite = tqdm(data_dic)
        else:
            ite = data_dic
        for t in ite:  # Second traversal, constructing tree
            localD = {}
            for item in t:
                if item in freqItemSet:  # Filtering to take only the frequent items that satisfy the minimum support in this sample
                    localD[item] = headerTable[item][0]  # element : count
            if len(localD) > 0:
                # Sorting single samples according to global frequencies from largest to smallest
                order_item = [v[0] for v in sorted(localD.items(), key=lambda x: x[1], reverse=True)]
                # Update the tree with filtered and sorted samples
                self.update_fptree(order_item, data_dic[t], tree_header, headerTable)
        return tree_header, headerTable

    def find_path(self, node, nodepath):
        '''
        Recursively add the node's parent node to the path
        '''
        if node.parent != None:
            nodepath.append(node.parent.name)
            self.find_path(node.parent, nodepath)

    def find_cond_pattern_base(self, node_name, headerTable):
        '''
        Find all conditional pattern bases based on node names
        '''
        treeNode = headerTable[node_name][1]
        cond_pat_base = {}  # save all conditional pattern bases
        while treeNode != None:
            nodepath = []
            self.find_path(treeNode, nodepath)
            if len(nodepath) > 1:
                cond_pat_base[frozenset(nodepath[:-1])] = treeNode.count
            treeNode = treeNode.nodeLink
        return cond_pat_base

    def create_cond_fptree(self, headerTable, min_support, temp, freq_items, support_data):
        # The initial frequent sets are elements of header table.
        freqs = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]  # Sorted by the total frequency of frequent item
        for freq in freqs:
            freq_set = temp.copy()
            freq_set.add(freq)
            freq_items.add(frozenset(freq_set))
            if frozenset(freq_set) not in support_data:  # Check whether the frequent items in support_data.
                support_data[frozenset(freq_set)] = headerTable[freq][0]
            else:
                support_data[frozenset(freq_set)] += headerTable[freq][0]

            cond_pat_base = self.find_cond_pattern_base(freq, headerTable)  # Seek all conditional pattern bases
            # Creating a conditional pattern tree
            cond_tree, cur_headtable = self.create_fptree(cond_pat_base, min_support)
            if cur_headtable != None:
                self.create_cond_fptree(cur_headtable, min_support, freq_set, freq_items, support_data)  # Recursive mines conditional FP trees

    def generate_L(self, data_set, min_support):
        data_dic = self.data_compress(data_set)
        freqItemSet = set()
        support_data = {}
        tree_header, headerTable = self.create_fptree(data_dic, min_support, flag=True)  # create fp-tree for dataset
        if (headerTable is None): return [], {}
        # Create a fptree of each 1st frequent item, and mine the frequent items and save the support count
        self.create_cond_fptree(headerTable, min_support, set(), freqItemSet, support_data)
        # cond_pat_base=self.find_cond_pattern_base(14,headerTable)
        max_l = 0
        for i in freqItemSet:  # Save frequent items to the specified container L according to size
            if len(i) > max_l: max_l = len(i)
        # L=[set() for _ in range(max_l)]
        # for i in freqItemSet:
        #     L[len(i)-1].add(i)
        # for i in range(len(L)):
        #     print("frequent item {}:{}".format(i+1,len(L[i])))
        L = [{} for _ in range(max_l)]
        for i in support_data:
            # L[len(i)-1].add({i:support_data[i]})
            L[len(i) - 1][i] = support_data[i]
        # for i in range(len(L)):
        #     print("frequent item {}:{}".format(i+1,len(L[i])))

        return L, support_data

    def generate_R(self, data_set, min_support, min_conf):
        L, support_data = self.generate_L(data_set, min_support)
        rule_list = []
        sub_set_list = []
        for i in range(0, len(L)):
            for freq_set in L[i]:
                for sub_set in sub_set_list:
                    if sub_set.issubset(
                            freq_set) and freq_set - sub_set in support_data:  # and freq_set-sub_set in support_data
                        conf = support_data[freq_set] / support_data[freq_set - sub_set]
                        big_rule = (freq_set - sub_set, sub_set, conf)
                        if conf >= min_conf and big_rule not in rule_list:
                            # print freq_set-sub_set, " => ", sub_set, "conf: ", conf
                            rule_list.append(big_rule)
                sub_set_list.append(freq_set)
        rule_list = sorted(rule_list, key=lambda x: (x[2]), reverse=True)
        return rule_list
