import os
import pandas as pd
TPCDS={
    'catalog_sales':{
        'columns':['cs_sold_date_sk','cs_sold_time_sk','cs_ship_date_sk','cs_bill_customer_sk','cs_bill_cdemo_sk','cs_bill_hdemo_sk','cs_bill_addr_sk','cs_ship_customer_sk','cs_ship_cdemo_sk','cs_ship_hdemo_sk',
                   'cs_ship_addr_sk','cs_call_center_sk','cs_catalog_page_sk','cs_ship_mode_sk','cs_warehouse_sk','cs_item_sk','cs_promo_sk','cs_order_number','cs_quantity','cs_wholesale_cost',
                   'cs_list_price','cs_sales_price','cs_ext_discount_amt','cs_ext_sales_price','cs_ext_wholesale_cost','cs_ext_list_price','cs_ext_tax','cs_coupon_amt','cs_ext_ship_cost',
                   'cs_net_paid','cs_net_paid_inc_tax','cs_net_paid_inc_ship','cs_net_paid_inc_ship_tax','cs_net_profit'
                   ],
        'length':[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
    },
    'store_sales':{
        'columns':['ss_sold_date_sk','ss_sold_time_sk','ss_item_sk','ss_customer_sk','ss_cdemo_sk','ss_hdemo_sk','ss_addr_sk','ss_store_sk','ss_promo_sk',
                   'ss_ticket_number','ss_quantity','ss_wholesale_cost','ss_list_price','ss_sales_price','ss_ext_discount_amt','ss_ext_sales_price','ss_ext_wholesale_cost','ss_ext_list_price',
                   'ss_ext_tax','ss_coupon_amt','ss_net_paid','ss_net_paid_inc_tax','ss_net_profit'
                   ],
        'length':[4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7]
    },
    'web_sales':{
        'columns':['ws_sold_date_sk','ws_sold_time_sk','ws_ship_date_sk','ws_item_sk','ws_bill_customer_sk','ws_bill_cdemo_sk','ws_bill_hdemo_sk','ws_bill_addr_sk','ws_ship_customer_sk','ws_ship_cdemo_sk',
                   'ws_ship_hdemo_sk','ws_ship_addr_sk','ws_web_page_sk','ws_web_site_sk','ws_ship_mode_sk','ws_warehouse_sk','ws_promo_sk','ws_order_number','ws_quantity','ws_wholesale_cost',
                   'ws_list_price','ws_sales_price','ws_ext_discount_amt','ws_ext_sales_price','ws_ext_wholesale_cost','ws_ext_list_price','ws_ext_tax','ws_coupon_amt','ws_ext_ship_cost','ws_net_paid',
                   'ws_net_paid_inc_tax','ws_net_paid_inc_ship','ws_net_paid_inc_ship_tax','ws_net_profit'
                   ],
        'length':[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,4,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]
    }

}

def gen_csv_from_txt(txt_path):
    sql_template_list=[]
    with open(f'{os.getcwd()}/schema/{txt_path}.txt') as f:
        while True:
            line=f.readline()
            if not line:
                break
            column_names=line.replace("  "," ").replace('\n', '').split(" ")
            while "" in column_names:column_names.remove("")
            access_attrs=[]
            selectivity=1
            freq=1
            scan_keys=[]
            for column_name in column_names:
                flag=False
                if column_name.find('*')>=0:
                    flag=True
                    column_name=column_name.replace("*","")
                col_idx=TPCDS[txt_path]['columns'].index(column_name)
                access_attrs.append(str(col_idx))
                if flag:scan_keys.append(str(col_idx))
            sql_template_list.append([','.join(access_attrs),freq,','.join(scan_keys),selectivity])

    print(sql_template_list)
    pd.DataFrame(sql_template_list).to_csv(f"template/{txt_path}.csv",index=False,header=False)
if __name__ == '__main__':
    gen_csv_from_txt('catalog_sales')
    # gen_csv_from_txt('store_sales')
    # gen_csv_from_txt('web_sales')