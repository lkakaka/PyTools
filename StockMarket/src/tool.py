#!/usr/bin/env python

import sqlite3
import os

cur_path = os.path.dirname(__file__)


class Tool(object):

    @staticmethod
    def import_script(project_name):
        cx = sqlite3.connect(cur_path + '/../data/project.db')  # 创建数据库，如果数据库已经存在，则链接数据库；如果数据库不存在，则先创建数据库，再链接该数据库。
        cu = cx.cursor()  # 定义一个游标，以便获得查询对象。
        with open(cur_path + '/main.py', mode='r', encoding="utf8") as f:
            script = f.read()
        if not script:
            print("cannot open script file!!!")
            return
        script = script.replace("'", "''")
        sql = "update projectdb set script = '{0}' where name = '{1}'".format(script, project_name)
        # print(sql)
        cu.execute(sql)

        cu.close()  # 关闭游标
        cx.commit()  # 事务提交
        cx.close()
        print("[{0}]import script file success!!!".format(project_name))

    @staticmethod
    def clear_task(project_name):
        cx = sqlite3.connect(cur_path + '/../data/task.db')
        cu = cx.cursor()
        sql = "delete from taskdb_{0}".format(project_name)
        cu.execute(sql)
        cu.close()  # 关闭游标
        cx.commit()  # 事务提交
        cx.close()
        print("[{0}]clear task success!!!".format(project_name))

    @staticmethod
    def clear_result(project_name):
        cx = sqlite3.connect(cur_path + '/../data/result.db')
        cu = cx.cursor()
        sql = "delete from resultdb_{0}".format(project_name)
        cu.execute(sql)
        cu.close()  # 关闭游标
        cx.commit()  # 事务提交
        cx.close()
        print("[{0}]clear result success!!!".format(project_name))

    @staticmethod
    def help():
        help_tips = '''
    Usage: tool command project
    command:
        is -import project's script
        ct -clear the spider task of project
        cr -clear the spider result of project
    project: 
        project name
        '''
        print(help_tips)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        parm = sys.argv[1]
        proj_name = sys.argv[2]
        if parm == "is":
            Tool.import_script(proj_name)
        if parm == "ct":
            Tool.clear_task(proj_name)
        if parm == "cr":
            Tool.clear_result(proj_name)
    else:
        Tool.help()
