#coding=utf-8
import MySQLdb
class MysqlClass(object):
    """Args:
        server:服务器ip
        username:mysql 登录用户名，比如root
        psw:密码
        dbname:数据库
        port：端口号,默认:3306
        charset:编码，默认utf-8
    """
    def __init__(self, server, username, pwd, dbName,port=3306,charset='utf-8'):
        self.db = MySQLdb.connect(server, username, pwd, dbName, port, charset)
        self.dbName = dbName
        cursor = self.db.cursor()
        cursor.execute("set names 'UTF8'")

    # 提取所有的表
    def getTables(self):
        sql = "SELECT TABLE_NAME,TABLE_COMMENT FROM  information_schema.TABLES WHERE table_schema = '%s' AND TABLE_TYPE = 'base table'" % self.dbName
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        tables = list()
        for table in data:
            tables.append([table[0], self.getComment(table[1])])
        return tables

    # 提取表格的备注信息
    def getComment(self,comment):
        if comment == None:
            return ""
        try:
            data = json.loads(comment)
            return data[0]['value']
        except:
            return comment

    # 提取列信息
    def getColumn(self,tableName):
        sql = "SELECT COLUMN_NAME,DATA_TYPE,COLUMN_COMMENT FROM " \
              " information_schema.`COLUMNS` " \
              "WHERE TABLE_SCHEMA = '%s' AND TABLE_name = '%s'" % (self.dbName, tableName)
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return list(data)

    # 销毁资源
    def __del__(self):
        self.db.close()



