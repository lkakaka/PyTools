#!/usr/bin/env python

import sqlite3
import os

cur_path = os.path.dirname(__file__)


def import_script():
    cx = sqlite3.connect(cur_path + '/../data/project.db')  # 创建数据库，如果数据库已经存在，则链接数据库；如果数据库不存在，则先创建数据库，再链接该数据库。
    cu = cx.cursor()  # 定义一个游标，以便获得查询对象。
    script = None
    with open(cur_path + '/main.py', mode='r', encoding="utf8") as f:
        script = f.read()
    if not script:
        print("cannot open script file!!!")
        return
    script = script.replace("'", "''")
    sql = "update projectdb set script = '{0}' where name = 'StockMarket'".format(script)
    # print(sql)
    cu.execute(sql)

    cu.close()  # 关闭游标
    cx.commit()  # 事务提交
    cx.close()
    print("import script file success!!!")


def clear_task():
    cx = sqlite3.connect(cur_path + '/../data/task.db')
    cu = cx.cursor()
    sql = "delete from taskdb_StockMarket"
    cu.execute(sql)
    cu.close()  # 关闭游标
    cx.commit()  # 事务提交
    cx.close()
    print("clear task success!!!")


def clear_result():
    cx = sqlite3.connect(cur_path + '/../data/result.db')
    cu = cx.cursor()
    sql = "delete from resultdb_StockMarket"
    cu.execute(sql)
    cu.close()  # 关闭游标
    cx.commit()  # 事务提交
    cx.close()
    print("clear result success!!!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        parm = sys.argv[1]
        if parm == "is":
            import_script()
        if parm == "ct":
            clear_task()
        if parm == "cr":
            clear_result()
    else:
        import_script()
