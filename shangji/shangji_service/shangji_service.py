#coding=utf-8
'''
created by zhangdongmei
'''

import sys
#sys.path.append('/home/work/local/baichuan_api')
#sys.path.append('/home/work/local/xts')
from shangji.shangji_model.shangji_db_model import ShangjiDbModel
from shangji.shangji_model.shangji_api_model import ShangjiApiModel
from shangji.shangji_model.shangji_kafka_model import ShangjiKafkaModel
from frame.lib.lianjia.link.linkService import linkService
import time

class ShangjiService(linkService):
    def __init__(self,env="test-shangji.home.lianjia.com"):
        self.dbModel = ShangjiDbModel(env)
        self.apiModel = ShangjiApiModel(env)
        self.kafkaModel = ShangjiKafkaModel(env)

    # TODO: 数据初始化
    def data_initialize(self):
        pass

    def date_prepare(self,shangjiType=1):
        if shangjiType==0:
            self.kafkaModel.add_seek_rent()
        elif shangjiType==1:
            self.kafkaModel.add_seek_buy()
        elif shangjiType==2:
            self.kafkaModel.add_rent()
        elif shangjiType==3:
            self.kafkaModel.add_sell()
        shangjiId = self.dbModel.get_new_shangjiId(shangjiType)
        return shangjiId

    def wait(self,func):
        count=0
        while(count < 5):
            try:
                func()
                return
            except:
                time.sleep(2)
        return func()
    #------------------------------------------case等级1--------------------------------------

    # 校验商机db数据与检索一致 shangjiTypeCode 0求租 1求购 2出租 3出售
    def verify_list_count(self):
        res1 = self.apiModel.shangji_list(typeCode=0)
        res2 = self.dbModel.get_seek_buy_count()
        self.isEqual(res1,res2)

    #校验小红点接口
    def verify_reddot(self):
        #增加商机数据
        self.kafkaModel.add_seek_buy()
        time.sleep(5)
        freshtime = self.apiModel.get_current_time()
        res=self.apiModel.shangji_reddot(freshtime)
        self.isEqual(res['seekBuyCount'],2)

    #校验列表字段-title
    def verify_title(self,shangjiType=2):
        #查询title不为空的数据
        shangjiId,title = self.dbModel.get_post_info(shangjiType=shangjiType,key="post_title")
        #校验接口返回
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)
        self.verify(res, title=title)

    # 校验列表字段-image
    def verify_img(self, shangjiType=3):
        shangjiId, imgList = self.dbModel.get_post_info(shangjiType=shangjiType, key="img_url_list")
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)
        if res['imgUrl'] ==None:
            self.verify(res, imgList=None)
        else:
            print "image not none"

    # 校验列表字段-室厅卫
    def verify_bedroom(self, shangjiType=3):
        shangjiId, imgList = self.dbModel.get_post_info(shangjiType=shangjiType, key="bedroom_num")
        # 校验接口返回
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)
        if res['imgUrl'] == None:
            self.verify(res, imgList=None)
        else:
            print "image not none"

    # 校验原帖已删除状态
    def verify_post_del(self,shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.dbModel.up_shangji_status(shangjiType,shangjiId,0)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)
        self.verify(res, originPostStatus='原贴已删除')
        res = self.apiModel.shangji_detail(shangjiId, shangjiType)["data"]['isAbleToTransfer']
        self.isEqual(res, 'false')
        res = self.apiModel.shangji_detail(shangjiId, shangjiType)["data"]['isAbleToContact']
        self.isEqual(res, 'false')

    # 校验商机已转录 user_type=2
    def verify_shangji_transfer(self,shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.dbModel.up_shangji_user_type(shangjiId,2)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)['statusInfos']
        self.isEqual(res[2], '已转录')

     # 校验商机先联系1后转录2
    def verify_shangji_contact_transfer(self,shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        #估计应该用insert插入数据库
        self.dbModel.up_shangji_user_type(shangjiId,1)
        self.dbModel.up_shangji_user_type(shangjiId,2)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)['statusInfos']
        self.isEqual(res[2], '已转录')

    # 校验商机先转录2后联系1
    def verify_shangji_transfer_contact(self,shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.dbModel.up_shangji_user_type(shangjiId,2)
        self.dbModel.up_shangji_user_type(shangjiId,1)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)['statusInfos']
        self.isEqual(res[2], '已转录')




    # 校验原帖已更新状态  status=2
    def verify_post_update(self, shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.dbModel.up_shangji_status(shangjiType,shangjiId,2)
        res = self.apiModel.get_list_by_id(shangjiType,shangjiId)
        self.verify(res, originPostStatus='原贴已更新')

    # 校验商机已浏览状态 (以当前经纪人维度)
    def verify_browser_status(self, shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.apiModel.shangji_detail(shangjiId,shangjiType)
        res = self.apiModel.get_list_by_id(shangjiType,shangjiId)
        self.verify(res, isBrowsed=True)

    # 校验商机已联系状态(以当前经纪人维度)
    def verify_contact_status(self, shangjiType=1):
        shangjiId=self.date_prepare(shangjiType)
        self.apiModel.shangji_contact(shangjiId, shangjiType)
        res = self.apiModel.get_list_by_id(shangjiType,shangjiId)['statusInfos']
        self.isEqual(res[2], '已联系')

    # 校验商机已转录房状态(以当前经纪人维度)
    def verify_transfer_house(self, shangjiType=2):
        shangjiId = self.date_prepare(shangjiType)
        self.kafkaModel.add_house(shangjiType, shangjiId)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)['statusInfos']
        self.isEqual(res[2], '已转录')
        res= self.apiModel.shangji_detail(shangjiId,shangjiType)["data"]['isAbleToTransfer']
        self.isEqual(res, 'false')

    # 校验商机已转录客状态(以当前经纪人维度)
    def verify_transfer_customer(self, shangjiType=1):
        shangjiId = self.date_prepare(shangjiType)
        self.kafkaModel.add_customer(shangjiType, shangjiId)
        res = self.apiModel.get_list_by_id(shangjiType, shangjiId)['statusInfos']
        self.isEqual(res[2], '已转录')
        res = self.apiModel.shangji_detail(shangjiId, shangjiType)["data"]['isAbleToTransfer']
        self.isEqual(res, 'false')

    # 校验联系次数计算
    def verify_contact_count(self,shangjiType=1):
        shangjiId = self.dbModel.get_shangji_id(shangjiType)
        count_before = self.apiModel.shangji_detail(shangjiId,shangjiType)["data"]["contactCount"]
        self.apiModel.shangji_contact(shangjiId,shangjiType)
        count_after = self.apiModel.shangji_detail(shangjiId,shangjiType)["data"]["contactCount"]
        self.isEqual(count_after, count_before+1)

    # 校验浏览次数计算
    def verify_browser_count(self, shangjiType=1):
        shangjiId = self.dbModel.get_shangji_id(shangjiType)
        count_before = self.apiModel.shangji_detail(shangjiId, shangjiType)["data"]["browseCount"]
        count_after = self.apiModel.shangji_detail(shangjiId, shangjiType)["data"]["browseCount"]
        self.isEqual(count_after, count_before + 1)

    # ------------------------------------------case等级2--------------------------------------
    # 校验反馈
    def verify_feedback(self,shangjiType=0):
        shangjiId = self.dbModel.get_shangji_id(shangjiType)
        self.apiModel.shangji_feedback(shangjiId, shangjiType)
        self.apiModel.shangji_feedback_selections()

    # 校验筛选
    def verify_selections(self):
        self.apiModel.shangji_select()
        self.apiModel.shangji_select_more()

    # 校验关键字
    def verify_keyword(self):
        self.apiModel.shangji_add_keyword()
        res=self.apiModel.shangji_keyword()['data']['listData']
        self.isEqual(res[0],"关键字1")
        self.isEqual(res[1],"关键字2")

if __name__ == '__main__':
    con = ShangjiService()
    #print con.verify_contact_status()
    print con.verify_shangji_transfer()
    #con.verify_reddot()

