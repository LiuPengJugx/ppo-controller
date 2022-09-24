import time
from db.jta import JTA
"""
Test the difference between the HDD cost model and the actual PG database environment
"""
my_jta=JTA()
test_times=10

# time0=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab WHERE a2='1' and a3='5' and a4='1020'")
# print('Example 1:',(time.time()-time0)/10)
#
#
# time1=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab WHERE a2<>'1' and a3<>'5' and a4<>'1020'")
# print('Example 2:',(time.time()-time1)/10)
#
# time2=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab WHERE a2<>'1'")
# print('Example 3:',(time.time()-time2)/10)
#
#
# time3=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab")
# print('Example 4:',(time.time()-time3)/10)
#
#
# time4=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT a1,a2 FROM tt_tab")
# print('Example 5:',(time.time()-time4)/10)

# Example 1: 0.016120219230651857
# Example 2: 0.3979427576065063
# Example 3: 0.40204148292541503
# Example 4: 0.396588659286499
# Example 5: 0.03543694019317627

# Split into multiple tables for testing
# my_jta.query("DROP TABLE IF EXISTS tt_tab_sub;\n CREATE TABLE tt_tab_sub (a0 SERIAL,a2 CHAR(4),a3 CHAR(4))")
# my_jta.query("INSERT INTO tt_tab_sub (SELECT a0,a2,a3 FROM tt_tab)")
# my_jta.commit()
# time5=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT a0,a2,a3 FROM tt_tab WHERE a2<>'1' and a3<>'5'")
# print('Example 6:',(time.time()-time5)/10)
#
#
# time6=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT a2,a3 FROM tt_tab_sub")
# print('Example 7:',(time.time()-time6)/10)
#
# time7=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab_sub WHERE a2<>'1' and a3<>'5'")
# print('Example 8:',(time.time()-time7)/10)
#
# time8=time.time()
# for _ in range(test_times):
#     my_jta.query("SELECT * FROM tt_tab_sub WHERE a0='1' and a2='1' and a3='5'")
# print('Example 9:',(time.time()-time8)/10)


# Example 6: 0.04241459369659424
# Example 7: 0.024752044677734376
# Example 8: 0.033130741119384764
# Example 9: 0.006550335884094238

"""
Conclusion:
1: In the same case, the small table relative to the large table, when the query data volume remains the same, the time is basically the same, the large table time is slightly longer. For example, Example 5 and Example 7 (0.035 slightly greater than 0.024), Example 6 and Example 8 (0.042 slightly greater than 0.033), Example 6 and Example 8 (0.042 slightly greater than 0.033). 
Example 6 and Example 8 (0.042 slightly greater than 0.033), Example 1 and Example 9 (0.0139 slightly greater than 0.0077)
"""

time9=time.time()
for _ in range(test_times):
    my_jta.query("SELECT * FROM tt_tab_sub limit 10000")
print('Example 10:',(time.time()-time9)/10)

time10=time.time()
for _ in range(test_times):
    my_jta.query("SELECT * FROM tt_tab_sub limit 10")
print('Example 11:',(time.time()-time10)/10)

time11=time.time()
for _ in range(test_times):
    my_jta.query("SELECT * FROM tt_tab_sub")
print('Example 12:',(time.time()-time11)/10)

# Example 10: 0.01700148582458496
# Example 11: 0.0014611482620239258
# Example 12: 0.07124898433685303

"""
Conclusion:
1.Under the same conditions, the fewer the number of tuples involved in the limit clause, the shorter the query time
"""
