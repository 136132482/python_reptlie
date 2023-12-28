import time

from dynamic_database import test1
import importlib
import sys
importlib.reload(sys)
import os
from reptliie_picture import taotu_reptile
from  dynamic_database import mysql_DBUtils
import threading
from reptliie_picture import url_picture
mysql = mysql_DBUtils.MyPymysqlPool("dbMysql1")
config=mysql_DBUtils.Config

columns=[]
def createtabl():
  column = {}
  column['column_name']='taotu_type_name'
  column['column_definition']='varchar(50)'
  column['column_isornot'] = 1
  column1 = {}
  column1['column_name'] = 'taotu_name'
  column1['column_definition'] = 'varchar(50)'
  column1['column_isornot'] = 1
  column2 = {}
  column2['column_name'] = 'taotu_url'
  column2['column_definition'] = 'varchar(255)'
  column2['column_isornot'] = 1
  column3={}
  column3['column_name'] = 'taotu_index'
  column3['column_definition'] = 'int'
  column3['column_isornot'] = 0

  columns.append(column.copy())
  columns.append(column1.copy())
  columns.append(column2.copy())
  columns.append(column3.copy())
  test1.createTable('reptlie_taotu',columns)
  return  columns

field_list=[]
field_value_list=[]

insert_datas = []
#批量插入值自定义  自定义的插入值要和对应字段数相同
def  downurl():
  taotu_dict=url_picture.taotu_dict
  for name,values in  taotu_dict.items():
      index=0;
      for  key,value in values.items():
           field=(name,key,value,index)
           insert_datas.append(field)
           index+=1
  return insert_datas
#组装
def packageList(tableName,insert_datas):
  if len(field_value_list)!=len(field_list):
      raise IndexError("参数字段数量与值的数量不相等")
  field_string = " ( "+','.join([elem for elem in field_list])+" ) "
  value_string =" ( "+ ','.join([elem for elem in field_value_list])+" ) "
  insert_sql = f"INSERT INTO `{tableName}` {field_string} VALUES {value_string}"
  # sql=packageSql(insert_datas)
  # print(insert_datas)
  # print(insert_sql)
  threadDownnload(insert_sql,insert_datas)


def packageList(tableName,columns,insert_datas,*args):
  if len(field_value_list)!=len(field_list):
      raise IndexError("参数字段数量与值的数量不相等")
  field_string = " ( " + ','.join([elem['column_name'] for elem in columns])+")"
  # field_string = " ( "+','.join([elem for elem in field_list])+" ) "
  # value_string =" ( "+ ','.join([elem for elem in field_value_list])+" ) "
  # insert_sql = f"INSERT INTO `{tableName}` {field_string} VALUES {value_string}"
  sql=packageSql(tableName,field_string,insert_datas,*args)
  print(sql)
  # print(insert_datas)
  # print(insert_sql)
  mysql.insertMany(sql)
  mysql.dispose()






def packageSql(tableName,field_string,insert_datas,*args):
    sql = f"INSERT INTO `{tableName}` {field_string} VALUES "
    update_clause = f"ON DUPLICATE KEY UPDATE "

    values = []
    for item in insert_datas:
        values.append(f"{item}")

    value_name =[]
    for item in args:
        value_name.append(f"{item} = VALUES({item})")


    sql += ",".join(values)
    sql += " " + update_clause
    sql += ",".join(value_name)

    return sql
def  beansFieldtoPackage(tableName):
     res=insertsql(tableName)
     for  column in res:
         if column.get('Extra')=='auto_increment':
               continue
         field=column.get('Field')
         field_list.append(field)
         field_value_list.append('%s')


def insertsql(tableName):
    # insert_sql = f"INSERT INTO `{tableName}`(`user_name`, `pazzword`, `sex`, `age`, `birthday`) VALUES (%s, %s, %s, %s, %s)"
    #
    # insert_datas = [
    #   ("赵子龙1", "123456", "男", 18, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    #   ("赵子龙2", "123456", "男", 19, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    #   ("赵子龙3", "123456", "男", 20, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
    #第一步 先判断表是否存在

    db_name = mysql.conf.get('db_name')
    sql="SHOW DATABASES LIKE  '%s' " % db_name
    res=mysql.getOne(sql)
    if res is not None:
      # 第二步查询是否有 该表
      sql2 = "show tables  LIKE  '%s' " % tableName
      res2 = mysql.getOne(sql2)
      if res2 is not None:
          # s第三部查询该表所有字段
          sql3 = f"show full columns from {tableName} from {db_name}"
          res3 = mysql.getAll(sql3)
          if res3 is not None:
              return res3
          else:
              raise ValueError(tableName + '字段查询不存在')
      else:
          raise ValueError(tableName + '查询不存在')
    else:
      raise  ValueError(db_name +'查询不存在')


          # return insert_sql,insert_datas


thread_count=2000

def threadDownnload(insert_sql,insert_datas):
    sub_lists = [insert_datas[i:i + thread_count] for i in range(0, len(insert_datas), thread_count)]
    print(sub_lists)
    threads = []
    for sub_list in sub_lists:
        t = threading.Thread(target=mysql.insertMany, args=(insert_sql,sub_list,))
        threads.append(t)
        t.start()

    # 等待所有线程执行完毕】=
    for t in threads:
        t.join()

if __name__ == '__main__':
    columns=createtabl()
    tableName='reptlie_taotu'
    beansFieldtoPackage(tableName)
    insert_datas=downurl()
    packageList(tableName,columns,insert_datas,'taotu_name')

    # insert_datas = [
    #   ("赵子龙1", "123456", "男", 18, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    #   ("赵子龙2", "123456", "男", 19, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
    #   ("赵子龙3", "123456", "男", 20, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
    #
    # sql=packageSql(insert_datas,'作者','书名')
    #
    # print(sql)



