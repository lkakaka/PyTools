#!/usr/bin/env python

import sqlite3


def import_spider_script():
    cx = sqlite3.connect('./data/project.db')  # 创建数据库，如果数据库已经存在，则链接数据库；如果数据库不存在，则先创建数据库，再链接该数据库。
    cu = cx.cursor()  # 定义一个游标，以便获得查询对象。
    script = None
    with open('./src/main.py', mode='r', encoding="utf8") as f:
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


if __name__ == "__main__":
    import_spider_script()
