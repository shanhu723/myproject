#coding=utf-8
'''
@author: zhangdongmei
'''
from common_lib.linkModel import linkDbModel
from shangji.shangji_conf.shangji_other_enum import *
from common_lib.common_config import EnvConfig

class ShangjiDbModel(linkDbModel):

    def __init__(self, env="test-shangji.home.lianjia.com"):
        self.dbhost= EnvConfig(env).get_config_by_env()['db_host']
        self.dbport = EnvConfig(env).get_config_by_env()['db_port']
        self.dbname = EnvConfig(env).get_config_by_env()['db_name']
        self.dbpwd = EnvConfig(env).get_config_by_env()['db_pwd']
        super(ShangjiDbModel, self).__init__(dbHost=self.dbhost,dbPort=self.dbport,dbName=self.dbname,dbPwd=self.dbpwd)

    def get_seek_buy_count(self):
        res = self.query_sql("SELECT COUNT(*) FROM shangji_seek_rent")
        return res[0]["COUNT(*)"]

    def get_shangji_id(self, shangjiType=3):
        table = shangji_type_enum.shangji_type_config[shangjiType]
        res = self.query_sql("SELECT count(*) FROM %s" % table)
        print 'shangjiId is %s' % res[0]['count(*)']
        return res[0]['count(*)']

    def get_new_shangjiId(self,shangjiType):
        table = shangji_type_enum.shangji_type_config[shangjiType]
        res = self.query_sql("SELECT * FROM %s ORDER BY id DESC limit 1" % table)
        print 'shangjiId is %s' % res[0]['id']
        return res[0]['id']

    def up_shangji_status(self,shangjiType,shangjiId,status):
        table = shangji_type_enum.shangji_type_config[shangjiType]
        return self.update('%s' % table, {"id": shangjiId}, status=status)

    #更新商机用户行为0浏览，1联系，2转录
    def up_shangji_user_type(self,shangjiId,user_type):
        table = "shangji_user_record"
        return self.update('%s' % table, {"shangji_id": shangjiId}, user_type=user_type)

    def get_shangjiinfo_by_status(self,status):
        try:
            res = self.get("shangji_sell", status=status)[0]
            return res['id']
        except Exception, e:
            print e
            print "res = None"
            return None

    #查询某个字段不为空的shangjiId
    def get_post_info(self,shangjiType=3,key='post_title'):
        table = shangji_type_enum.post_type_config[shangjiType]
        res = self.query_sql("SELECT * FROM %s WHERE house_source=0 AND %s IS NOT NULL ORDER BY release_time DESC" % (table,key))
        postId = res[0]['id']
        keyResult = res[0][key]
        print 'postId is', postId
        print '%s result is %s' % (key,keyResult)
        #根据post_id 查询商机Id
        table2= shangji_type_enum.shangji_type_config[shangjiType]
        res2= self.query_sql("SELECT * FROM %s WHERE post_id=%s" % (table2,postId))
        print 'shangjiId is',res2[0]['id']
        return res2[0]['id'],keyResult

    #统计浏览次数
    def get_contact_count(self, shangjiId, shangjiType):
        res = self.query_sql('SELECT COUNT(*) FROM shangji_user_record WHERE shangji_id = %s AND shangji_type = %s AND user_type = 1' % (shangjiId,shangjiType))
        return res[0]["COUNT(*)"]

class apiDbModel(linkDbModel):
    DBNAME = "bc_api_info"
    DBHOST = "m6667.zeus.test.mysql.ljnode.com"
    DBPORT = 6667

    def __init__(self, table="api_config"):
        self.table = table

    def add_table(self,tablename):
        self.query_sql("create table self.table(`id` int(100) NOT NULL AUTO_INCREMENT,`interface` varchar(100) NOT NULL,`method` varchar(50) DEFAULT NULL,`parameter` varchar(50) DEFAULT NULL,`description` varchar(300) DEFAULT NULL,`parameter_value` varchar(50) DEFAULT '',`required` tinyint(50) DEFAULT NULL COMMENT '1是true,0是false',`update_time` tinyint(4) DEFAULT NULL,PRIMARY KEY (`id`))") % tablename

    def add_interface(self,interface,method,parameter,description,required):
        self.add(tableName=self.table, interface=interface, method=method,parameter=parameter,description=description,required=required)
        print '接口添加成功'

    def get_interface(self,interface,method,parameter):
        res = self.get(tableName=self.table, interface=interface, method=method,parameter=parameter)
        try:
            ret = res[0]
            return ret
        except Exception, e:
            print "interface is null"

    def get_interface2(self,interface,method):
        res = self.get(tableName=self.table, interface=interface, method=method)
        try:
            ret = res[0]
            return ret
        except Exception, e:
            print "interface is null"

    def up_interface(self,interface,method,parameter,description,required):
        self.update(self.table, {"interface":interface,"method":method,"parameter":parameter},description=description,required=required)
        print '接口更新成功'

    def get_api_info(self,interfaceName):
        res=self.get(self.table,interface=interfaceName)
        method = res[0]['method']
        parameters={}
        for i in range(len(res)):
            if res[i]["parameter_value"] != None:
                parameters[res[i]["parameter"]] = res[i]["parameter_value"]
        return method,parameters

if __name__ == '__main__':
    shangji = ShangjiDbModel()
    # print shangji.get_api_info("/shangji/listCards")
    #print shangji.get_interface("/shangji/listCards",'post','snapshotTime')
    print shangji.get_shangji_id(1)
    #print shangji.up_shangji_user_type('4678',2)
    #shangji = ShangjiDbModel()
    # print shangji.get_seek_buy_count()