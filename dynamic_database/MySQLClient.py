import MySQLdb
import operator

db = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='python-test', charset='utf8')
db1 = MySQLdb.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='py_db', charset='utf8')

db.autocommit(1)
db1.autocommit(1)

cursor = db.cursor()
cursor1 = db1.cursor()



def createTable(tableName,columns):
    create_table_sql = f"CREATE TABLE  if NOT EXISTS `{tableName}` ( \
      `id` bigint NOT NULL AUTO_INCREMENT,\
      PRIMARY KEY (`id`)\
    ) ENGINE=InnoDB"

    # # 使用 execute()  方法执行 SQL
    # res = cursor1.execute(create_table_sql)
    # print(res)  # 0`
    execute1(create_table_sql)
    addCloums(columns,tableName)



#
# # #使用 fetchall() 方法获取s所有数据.
# data = cursor.fetchall()
# print(data)

def addCloums(columns,tableName):
    for column in columns:
        addsql =f'ALTER TABLE  {tableName} ADD COLUMN  '
        column_name=column.get('column_name')
        column_definition=column.get('column_definition')
        column_isornot=column.get('column_isornot')
        column_utf=' CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci '
        column_end =' DEFAULT NULL '
        if column_name is None:
            raise ValueError("参数不能为空")
        else:
            if column_isornot == 0:
                if operator.contains('int',column_definition):
                    column_end= ' DEFAULT 0 '
                if operator.contains('varchar',column_definition):
                    column_end=' DEFAULT NULL '
                if operator.contains('timestamp',column_definition):
                    column_end =' DEFAULT "0000-00-00 00:00:00" '
                else:
                    column_end=' DEFAULT NULL '
            else:
                column_end =' NOT NULL '
        addsql =f'ALTER TABLE  {tableName} ADD COLUMN  {column_name}  {column_definition} {column_utf} {column_end} '
        execute1(addsql)
        print("新增字段"+column_name+"成功")  # 1


#   `user_name` varchar(145) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,\
#   `pazzword` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
#   `sex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,\
#   `age` int DEFAULT NULL,\
#   `birthday` date DEFAULT NULL,\


def execute1(sql,parm=None):
    # 使用 cursor() 方法创建一个游标对象 cursor
    try:
        # 执行 SQL语句
        if parm is None:
         res = cursor1.execute(sql)
        else:
         res = cursor1.execute(sql,parm)
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


if __name__ == '__main__':
   # insert1()
   # test1()
   # createtabl()
   sql = "select * from t_user where id = %s"
   parm = '1'
   execute1(sql, parm)

#
# cursor.close()
# db.close()



#
# # # 获取数据库连接
# # dbConn = pymysql.connect(host='localhost',
# #                          port=3306,
# #                          user='root',
# #                          password='123456',
# #                          database='py_db',
# #                          # charset='utf8',
# #                          cursorclass=pymysql.cursors.DictCursor)
#
# # 使用 cursor() 方法创建一个游标对象 cursor
# # cursor = dbConn.cursor()