import math
from db.conf import Conf
from util import Util
"""
HDD Cost model: compute the I/O cost of given partition scheme 

Input parameters: 1. workload 2. partition scheme 3. the length of table attributes. 
"""
class DiskIo:
    tid_length = 4
    cardinality = 1000000
    page_size=5000
    block_factor = 10

    @staticmethod
    def compute_cost(querys,candidate_partitions,attrs_length):
        DiskIo.cardinality = Conf.CARDINALITY
        DiskIo.page_size = Conf.PAGE_SIZE
        if len(candidate_partitions) == 0: return 0
        total_cost = 0
        for query in querys:
            primary_fragments = []
            secondary_fragments = []
            solved_attrs = [i for i, x in enumerate(query.attributes) if x == 1]
            # Determine primary_fragments and secondary_fragments
            for partition in candidate_partitions:
                if Util.list_solved_list(partition, query.scan_key):
                    primary_fragments.append({
                        'key': [key for key in query.scan_key if key in partition],
                        'val': partition
                    })
                elif Util.list_solved_list(partition, solved_attrs):
                    secondary_fragments.append(partition)
            # Calculate the length of tuple in the primary partition
            primary_cost = 0
            for primary_fragment in primary_fragments:
                tuple_length_primary_fragment = sum([attrs_length[x] for x in primary_fragment['val']]) + DiskIo.tid_length
                # compute Sequential
                sequential_cost = math.ceil((DiskIo.cardinality * tuple_length_primary_fragment) / (DiskIo.page_size * DiskIo.block_factor))
                primary_cost += sequential_cost
            # Calculate the tuple length of the secondary partition
            secondary_cost = 0
            index_key_num = math.ceil(DiskIo.cardinality * query.selectivity)
            for secondary_fragment in secondary_fragments:
                # If the index file is put into the main memory buffer, finding the key value K only involves the main memory access without performing IO operation. This situation will not be considered
                tuple_length_secondary_fragments = sum([attrs_length[x] for x in secondary_fragment]) + DiskIo.tid_length
                # At this time, the hash table has been established for the key values of the main partition. When traversing the hash table, you only need to find the whole index block
                join_cost = DiskIo.cardinality * DiskIo.tid_length / (DiskIo.page_size * DiskIo.block_factor)
                secondary_cost += join_cost + math.ceil(
                    (DiskIo.cardinality * query.selectivity * tuple_length_secondary_fragments) / (
                                DiskIo.page_size * DiskIo.block_factor))
            total_cost += (primary_cost + secondary_cost) * query.frequency
        return total_cost

    @staticmethod
    def compute_cost_detail(query, candidate_partitions, attrs_length):
        if len(candidate_partitions) == 0: return 0
        primary_fragments = []
        secondary_fragments = []
        solved_attrs = [i for i, x in enumerate(query.attributes) if x == 1]
        for partition in candidate_partitions:
            if Util.list_solved_list(partition, query.scan_key):
                primary_fragments.append({
                    'key': [key for key in query.scan_key if key in partition],
                    'val': partition
                })
            elif Util.list_solved_list(partition, solved_attrs):
                secondary_fragments.append(partition)
        # 计算主分区内元组长度
        primary_cost = 0
        for primary_fragment in primary_fragments:
            tuple_length_primary_fragment = sum(
                [attrs_length[x] for x in primary_fragment['val']]) + DiskIo.tid_length
            # compute Sequential
            sequential_cost = math.ceil(
                (DiskIo.cardinality * tuple_length_primary_fragment) / (DiskIo.page_size * DiskIo.block_factor))
            primary_cost += sequential_cost
        secondary_cost = 0
        for secondary_fragment in secondary_fragments:
            tuple_length_secondary_fragments = sum(
                [attrs_length[x] for x in secondary_fragment]) + DiskIo.tid_length
            join_cost = DiskIo.cardinality * DiskIo.tid_length / (DiskIo.page_size * DiskIo.block_factor)
            secondary_cost += join_cost + math.ceil(
                (DiskIo.cardinality * query.selectivity * tuple_length_secondary_fragments) / (
                        DiskIo.page_size * DiskIo.block_factor))
        total_cost=(primary_cost+secondary_cost)*query.frequency
        par_nums=len(primary_fragments)+len(secondary_fragments)
        return total_cost,par_nums


    # Try to optimize the calculation of primary partition so that the cost difference between no vertical partitioning and vertical partitioning is not so large
    @staticmethod
    def compute_cost_revised(querys, candidate_partitions, attrs_length):
        if len(candidate_partitions) == 0: return 0
        total_cost = 0
        for query in querys:
            primary_fragments = []
            secondary_fragments = []
            solved_attrs = [i for i, x in enumerate(query.attributes) if x == 1]
            for partition in candidate_partitions:
                if Util.list_solved_list(partition, query.scan_key):
                    primary_fragments.append({
                        'key': [key for key in query.scan_key if key in partition],
                        'val': partition
                    })
                elif Util.list_solved_list(partition, solved_attrs):
                    secondary_fragments.append(partition)
            primary_cost = 0
            for primary_fragment in primary_fragments:
                tuple_length_primary_fragment_key = sum(
                    [attrs_length[x] for x in primary_fragment['key']]) + DiskIo.tid_length
                tuple_length_primary_fragment_no_key = sum([attrs_length[x] for x in primary_fragment['val'] if x not in primary_fragment['key']])
                read_key_sequential_cost = math.ceil((DiskIo.cardinality * tuple_length_primary_fragment_key) / (DiskIo.page_size * DiskIo.block_factor))
                no_key_sequential_cost=math.ceil((DiskIo.cardinality * tuple_length_primary_fragment_key) / (DiskIo.page_size * DiskIo.block_factor))
                primary_cost += read_key_sequential_cost+no_key_sequential_cost
            secondary_cost = 0
            index_key_num = math.ceil(DiskIo.cardinality * query.selectivity)
            for secondary_fragment in secondary_fragments:
                tuple_length_secondary_fragments = sum(
                    [attrs_length[x] for x in secondary_fragment]) + DiskIo.tid_length
                join_cost = DiskIo.cardinality * DiskIo.tid_length / (DiskIo.page_size * DiskIo.block_factor)
                secondary_cost += join_cost + math.ceil(
                    (DiskIo.cardinality * query.selectivity * tuple_length_secondary_fragments) / (
                            DiskIo.page_size * DiskIo.block_factor))
            total_cost += (primary_cost + secondary_cost) * query.frequency
        return total_cost


    @staticmethod
    def compute_repartitioning_cost(old_schema,new_schema,attrs_length):
        write_multiplier=1.2  #how expensive writes are compared to a read
        # Unit: page_size * block_factor
        # Step 1: partitions normalization
        structured_old_schema=Util.partition_ordering(old_schema)
        structured_new_schema=Util.partition_ordering(new_schema)
        # Step 2: find these changed partitions and compute their transfer cost
        total_cost=0
        for par in structured_new_schema:
            if par not in structured_old_schema:
                total_cost+=sum([attrs_length[attr] for attr in par])*DiskIo.cardinality

        total_cost=math.ceil(write_multiplier*total_cost/(DiskIo.page_size * DiskIo.block_factor))
        return total_cost