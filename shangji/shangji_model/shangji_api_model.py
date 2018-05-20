#coding=utf-8
'''
created by zhangdongmei
'''

from shangji.shangji_conf.shangji_api_enum import *
from common_lib.linkModel import linkApiModel
from shangji_db_model import apiDbModel
from common_lib.common_config import EnvConfig
import time
import sys
sys.setdefaultencoding('utf8')

class ShangjiApiModel(linkApiModel):

    def __init__(self, env="test-shangji.home.lianjia.com",ucid=2210000000000016):
        self.ihost= EnvConfig(env).get_config_by_env()['ihost']
        self.iport = EnvConfig(env).get_config_by_env()['iport']
        super(ShangjiApiModel, self).__init__(iHost=self.ihost,iPort=self.iport)
        self.ucid = ucid
        self.apiDbModel = apiDbModel()

    #或者当前时间的13位时间戳
    def get_current_time(self):
        millis = int(round(time.time() * 1000))
        return millis

    #发送post请求
    def shangji_post(self, path, data):
        return self.post(path=path, data=data,headers={"Lianjia-Ucid": self.ucid, "bc_citycode": 8737,"bc_orgcode":"ZZ0000050002","bc_compcode":"0000050"})

    #获取接口method
    def shangji_method(self,method, path, data):
        if method=='get':
            return self.get(path=path, data=data, headers={"Lianjia-Ucid": self.ucid, "bc_citycode": 8737,"bc_orgcode":"ZZ0000050002","bc_compcode":"0000050"})
        elif method=='post':
            return self.post(path=path, data=data, headers={"Lianjia-Ucid": self.ucid, "bc_citycode": 8737,"bc_orgcode":"ZZ0000050002","bc_compcode":"0000050"})

    def shangji_get(self,path, data):
        return self.get(path=path, data=data,headers={"Lianjia-Ucid": self.ucid, "bc_citycode": 8737,"bc_orgcode":"ZZ0000050002","bc_compcode":"0000050"})

    # 商机列表   shangjiTypeCode 0求租 1求购 2出租 3出售
    def shangji_list(self,typeCode):
        path = shangji_url_enum.shangji_list_url
        data = {
            "snapshotTime":self.get_current_time(),
            "shangjiTypeCode":typeCode
            }
        res = self.shangji_post(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res["data"]['list']

    # 商机列表   shangjiTypeCode 0求租 1求购 2出租 3出售
    def shangji_list_new(self, typeCode):
        path="/shangji/listCards"
        method,data = self.apiDbModel.get_api_info(path)
        res=self.shangji_method(method,path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res["data"]['list']

    def get_list_by_id(self,typeCode,shangjiId):
        time.sleep(10)
        listA = self.shangji_list(typeCode)
        for i in range(len(listA)):
            if shangjiId == listA[i]['shangjiId']:
                return listA[i]

    # 商机小红点
    def shangji_reddot(self,freshtime):
        path = shangji_url_enum.shangji_reddot_url
        data = {
            "lastRefreshTime":freshtime
        }
        res = self.shangji_get(path = path, data = data)
        self.verify(res, errno =0, error="操作成功")
        return res['data']

    # 商机筛选配置
    def shangji_select(self,shangjiType=1):
        path = shangji_url_enum.shangji_selection_url
        data = {
            "shangjiTypeCode": shangjiType
        }
        res = self.shangji_get(path = path, data = data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机筛选配置——更多
    def shangji_select_more(self, shangjiType=1):
        path = shangji_url_enum.shangji_selection_more_url
        data = {
            "shangjiTypeCode": shangjiType
        }
        res = self.shangji_get(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机详情页
    def shangji_detail(self,shangjiId, typeCode):
        path = shangji_url_enum.shangji_detail_url
        data = {
            "shangjiId": shangjiId,
            "shangjiTypeCode": typeCode,
        }
        res = self.shangji_get(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机一键联系
    def shangji_contact(self, shangjiId, typeCode):
        path = shangji_url_enum.shangji_contact_url
        data = {
            "shangjiId": shangjiId,
            "shangjiTypeCode": typeCode,
        }
        res = self.shangji_post(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机联系反馈
    def shangji_feedback(self, shangjiId, typeCode):
        path = shangji_url_enum.shangji_feedback_url
        data = {
            "shangjiId": shangjiId,
            "shangjiTypeCode": typeCode,
            "feedbackId":0,
            "feedbackContent":"feed back test"
        }
        res = self.shangji_post(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机联系反馈选项
    def shangji_feedback_selections(self):
        path = shangji_url_enum.shangji_feedback_selections_url
        data = {}
        res = self.shangji_get(path=path,data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机添加关键词
    def shangji_add_keyword(self):
        path = shangji_url_enum.shangji_add_keyword_url
        data = {
            "keywords":"关键字1,关键字2"
        }
        res = self.shangji_post(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res

    # 商机获取关键词
    def shangji_keyword(self):
        path = shangji_url_enum.shangji_keyword_url
        data = {}
        res = self.shangji_get(path=path, data=data)
        self.verify(res, errno=0, error="操作成功")
        return res


if __name__ == '__main__':
    con = ShangjiApiModel()
    #print con.shangji_detail(1,1)
    #print con.shangji_list(0)
    #print con.shangji_feedback_selections(61,3)
    print con.shangji_contact(1,1)
