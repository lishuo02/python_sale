#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql as MySQLdb
import pandas as pd

import matplotlib.pyplot as plt
import datetime

host = 
user = 
passwd = 
port = 3306
db = "trade_stats"


def connect_sql():
    conn = MySQLdb.connect(host=host,port=port,user=user,passwd=passwd,db=db, charset='utf8')
    cur = conn.cursor()
    return conn,cur

def close_connect(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

def select_sql(cur,sql):
    try:
        cur.execute(sql)
        alldata = cur.fetchall()
        frame = pd.DataFrame(list(alldata))
    except:
        frame = pd.DataFrame()
    return frame

#将日期转换为星期
def data_to_week(arrLike):
    create_time = arrLike["count_day"]
    create_time = str(create_time)
    create_time = pd.to_datetime(create_time)
    # #获取第几周
    # week = str(create_time.strftime("%W"))
    #获取周几
    week_day = str(create_time.strftime("%w"))
    return week_day


if __name__ == "__main__":
    #打开连接
    conn,cur = connect_sql()
    result = pd.DataFrame()
    months = ["201801", "201802", "201803", "201804", "201805", "201806", "201807", "201808", "201809", "2018010",
              "201811", "201812"]
    for month in months:
        sql = "SELECT goods_name,sale_amount,count_day FROM `svm_goods_stats_" + month + "` where svm_id=23833;"
        # print(sql)
        result1 = select_sql(cur,sql)
        # print(result1)
        result = result.append(result1)

    #关闭连接
    close_connect(conn,cur)

    #修改列名
    result.columns = ["goods_name","sale_amount","count_day"]

    # 添加周几
    result["week_day"] = result.apply(data_to_week, axis=1)

    print(result)
    #雀巢罐装(180ml/罐)
    quechao=result[result["goods_name"].isin(["卫龙大面筋(106g袋)"])]
    print(quechao)

    week = quechao["week_day"]
    sale = quechao["sale_amount"]
    plt.bar(week,sale)

    plt.title("雀巢每周销量散点图")
    plt.xlabel("week")
    plt.ylabel("sale")

    # plt.show()

