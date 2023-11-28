from threading import Lock
from dynamic_database import mysql_client
import time
from  dynamic_database import mysql_DBUtils
import operator


mysql = mysql_DBUtils.MyPymysqlPool("dbMysql1")
cursor=mysql._cursor
conn=mysql._conn

# db = MySQLClient.db
db1=mysql_client.db1
#
#
# cursor = db.cursor()
cursor1 = db1.cursor()
lock=Lock()
def test1():
  sql="select * from t_user where id = %s"
  parm =1
  result=mysql.getOne(sql,parm)
  print(result)

def test2():
  sql="select * from t_user where id = %s"
  parm =1
  result=cursor1.excute(sql,parm)
  print(result)


def insert():
  insert_sql = "INSERT INTO `t_user`(`user_name`, `pazzword`, `sex`, `age`, `birthday`) VALUES ('赵云', '123456', '男', 20, now())"
  insert_sql1 = "INSERT INTO `t_user`(`user_name`, `pazzword`, `sex`, `age`, `birthday`) VALUES ('%s', '%s', '%s', %s,  '%s')" % \
               ('赵云2', '123456', '男', 18, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
  insert_sql2= "INSERT INTO `t_user`(`user_name`, `pazzword`, `sex`, `age`, `birthday`) VALUES (%s, %s, %s, %s,  %s)"
  values=[('赵云2', '123456', '男', 18, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]
  result=mysql.insert(insert_sql)
  result1=mysql.insertMany(insert_sql2,values)
  print(result)
  print(result1)
  mysql.dispose()


def insert2(insert_sql,insert_datas):
  # insert_sql = "INSERT INTO `t_user`(`user_name`, `pazzword`, `sex`, `age`, `birthday`) VALUES (%s, %s, %s, %s, %s)"
  #
  # insert_datas = [
  #   ("赵子龙1", "123456", "男", 18, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
  #   ("赵子龙2", "123456", "男", 19, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())),
  #   ("赵子龙3", "123456", "男", 20, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))]

  try:
    # 执行 SQL语句
    # res = cursor.execute(insert_sql)
    lock.acquire()
    res = cursor1.executemany(insert_sql, insert_datas)
    print(res)  # 3

    # 提交事务
    db1.commit()
    lock.release()
    time.sleep(1)
  except:
    # 回滚
    db1.rollback()
    raise
  finally:
    # 释放资源
    cursor1.close()
    db1.close()

def update():
  update_sql = 'UPDATE `t_user` SET `user_name` = %s, `pazzword` = %s, `sex` = %s, `age` = %s WHERE `id` = %s'
  update_datas = ("安琪拉", "123456", "女", 18, 2)

  try:
    # 执行 SQL语句
    res = cursor1.execute(update_sql, update_datas)
    print(res)  # 1

    # 提交事务
    db1.commit()
  except:
    # 回滚
    db1.rollback()
    raise
  finally:
    # 释放资源
    cursor1.close()
    db1.close()

def delete():
  delete_sql = 'DELETE FROM `t_user` WHERE `id` = %s'
  delete_datas = [('8'),('9')]

  try:
     # 执行 SQL语句
     res = cursor1.executemany(delete_sql, delete_datas)
     print(res)  # 2

     # 提交事务
     db1.commit()
  except:
    # 回滚
    db1.rollback()
    raise
  finally:
  # 释放资源
    cursor1.close()
    db1.close()


def  insert1():
  insert_sql = "INSERT INTO `t_user`(`user_name`, `pazzword`,`sex`, `age`) VALUES ('貂蝉', '123456','女',28)"
  result=mysql.insert(insert_sql)
  print(result)
  mysql.dispose()

columns=[]
def createtabl():
  column = {}
  column['column_name']='animal_name'
  column['column_definition']='varchar(50)'
  column['column_isornot'] = 1
  column1 = {}
  column1['column_name'] = 'animal_type'
  column1['column_definition'] = 'int(11)'
  column1['column_isornot'] = 1
  column2 = {}
  column2['column_name'] = 'animal_age'
  column2['column_definition'] = 'int(11)'
  column2['column_isornot'] = 0
  columns.append(column.copy())
  columns.append(column1.copy())
  columns.append(column2.copy())
  createTable('animal',columns)

global list
list=[]
def createTable(tableName, columns):
  create_table_sql = f"CREATE TABLE  if NOT EXISTS `{tableName}` ( \
    `id` bigint NOT NULL AUTO_INCREMENT,\
    PRIMARY KEY (`id`)\
  ) ENGINE=InnoDB"

  # # 使用 execute()  方法执行 SQL
  # res = cursor1.execute(create_table_sql)
  # print(res)  # 0`
  try:
    mysql.insert(create_table_sql)
    addCloums(columns, tableName)
    for add in list:
      mysql.insert(add)
    conn.commit()
  except Exception as e:
            #cursor.close()  # 先关游标
            cursor.rollback()
            print(e)
  # finally:
  #   cursor.close()

  #   conn.close()


#
# # #使用 fetchall() 方法获取s所有数据.
# data = cursor.fetchall()
# print(data)

def addCloums(columns, tableName):
  for column in columns:
    column_name = column.get('column_name')
    column_definition = column.get('column_definition')
    column_isornot = column.get('column_isornot')
    column_utf = ' CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci '
    column_exists=' IF NOT EXISTS '
    column_end = ' DEFAULT NULL '
    if column_name is None:
      raise ValueError("参数不能为空")
    else:
      if column_isornot == 0:
        if operator.contains(column_definition,'int'):
          column_end = ' DEFAULT 0 '
        elif operator.contains(column_definition,'varchar'):
          column_end = ' DEFAULT NULL '
        elif operator.contains(column_definition,'timestamp'):
          column_end = ' DEFAULT "0000-00-00 00:00:00" '
        else:
          column_end = ' DEFAULT NULL '
      else:
        column_end = ' NOT NULL '
    if queryColumns(tableName,column_name):
      if operator.contains(column_definition,'int' ):
        addsql = f'ALTER TABLE  {tableName} ADD COLUMN   {column_name}  {column_definition}  {column_end} '
      else:
        addsql = f'ALTER TABLE  {tableName} ADD COLUMN   {column_name}  {column_definition} {column_utf} {column_end} '
      list.append(addsql)

    # mysql.insert(addsql)
    # print("新增字段" + column_name + "成功")  # 1


def queryColumns(tableName,columnName):
   sql= f'select count(*) as num from information_schema.columns where table_name = "{tableName}" and column_name = "{columnName}"'
   res=mysql.getOne(sql)
   count=res.get('num')
   if count>0:
     return False
   else:
     return True

def  queryone(select_sql,select_datas=None):
  # select_sql = "SELECT * FROM `t_user` WHERE id = %s "
  # select_datas = [('11')]
  try:
    # 执行 SQL语句
    if select_datas is None:
      res=cursor1.execute(select_sql)
    else:
      res=cursor1.execute(select_sql, select_datas)
    res = cursor1.fetchone()
    print(res)
    return res# {'id': 5, 'user_name': '赵子龙1', 'pazzword': '123456', 'sex': '男', 'age': 18, 'birthday': datetime.date(2023, 2, 13)}
  except:
    raise
  # finally:
  #   # 释放资源
  #   cursor1.close()
  #   db1.close()

def querymany(select_sql,select_datas=None):
  # select_sql = "SELECT * FROM `t_user` WHERE id >= %s AND sex = %s"
  # select_datas = (5, "男")
  try:
    # 执行 SQL语句
    if select_datas is None:
      cursor1.execute(select_sql)
    else:
      cursor1.execute(select_sql,select_datas)
    res = cursor1.fetchmany()
    return res
  except Exception as e:
     print(e)
  # finally:
  #   # 释放资源
  #   cursor1.close()
  #   db1.close()

if __name__ == '__main__':
   # insert1()
   # test1()
   # createtabl()
   # test2
   # insert2()
   # update()
   # delete()
   # queryone()
   # querymany()
   data = [
     {'id':1,'name':'Alice','age':25},
     {'id':2,'name':'bob','age':30}
   ]
   sql= "INSERT INTO table_name (id, name, age) VALUES "
   update_clause="ON DUPLICATE KEY UPDATE name = VALUES(name), age = VALUES(age)"


   values=[]
   for item in data:
      values.append(f"({item['id']},{item['name']},{item['age']})")

   sql+=",".join(values)
   sql += " "+update_clause

   print(sql)