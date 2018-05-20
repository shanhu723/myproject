#coding=utf-8
'''
created by zhangdongmei
'''

from common_lib.common_config import EnvConfig
from common_lib.linkModel import linkKafkaModel
import json
import time

class ShangjiKafkaModel(linkKafkaModel):

    def __init__(self,env="test-shangji.home.lianjia.com",ucid=2210000000000016):
        self.khost=str(EnvConfig(env).get_config_by_env()['kafka_host'])
        super(ShangjiKafkaModel,self).__init__(kHost=self.khost)
        self.ucid = ucid
        self.kafka_topic = json.loads(EnvConfig(env).get_config_by_env()['kafka_topic'])
        self.sell_topic= str(self.kafka_topic['shangji_sell_topic'])
        self.rent_topic= str(self.kafka_topic['shangji_rent_topic'])
        self.seekbuy_topic= str(self.kafka_topic['shangji_seekbuy_topic'])
        self.seekrent_topic= str(self.kafka_topic['shangji_seekrent_topic'])
        self.transfer_house= str(self.kafka_topic['transfer_house'])
        self.transfer_cust= str(self.kafka_topic['transfer_customer'])

    # 或者当前时间的13位时间戳
    def get_current_time(self):
        millis = int(round(time.time() * 1000))
        return millis

    def get_now_time(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    # 创建出售帖子消息
    def add_sell(self):
        card_id = "http://peixian.baixing.com/ershoufang/a136539676%s.html" % (self.get_current_time())
        title = "No%s 出售帖子测试数据" % (self.get_now_time())
        releasetime = self.get_current_time()
        data={
        "current_floor": "",
        "lastModifiedTime": 1523512771340,
        "memoInfo": "baixingwang-8737-0",
        "house_total_price_max": "",
        "agent_company": "",
        "floor_space": "",
        "restroom_num": "",
        "subway_station": "",
        "taskid": "baixingwang_xuzhou_sell_insert",
        "dbTableName": "xuzhou",
        "house_tag_list_weiyi": "",
        "house_tag_list_maner": "",
        "towards": "",
        "type": "sell",
        "building_age": "",
        "description_sell": "新华家园住宅11万，28、6平，1室1厅多层五楼简​‌‌装阁楼改造的新华家园住宅11万，28、6平，1室1厅多层五楼简​‌‌装阁楼改造的",
        "bedroom_num": "",
        "house_total_price": "110000",
        "out_of_time": "",
        "city_id": "8737",
        "livingroom_num": "",
        "id": card_id,
        "isNeedNewId": "true",
        "house_type": "",
        "house_source": "0",
        "childUrl": {},
        "img_url_list": [
            "http://img4.baixing.net/29312031bd6f59bda14bfb21035f396b.jpg_bi",
            "http://img4.baixing.net/59a380b8d224d75cbc8e5136823d607e.jpg_bi",
            "http://img4.baixing.net/79d4d5b1b7b9a1ef5699ffb2a5270b36.jpg_bi"
        ],
        "parentUrl": "http://peixian.baixing.com/ershoufang/a1365396762.html?from=regular",
        "website_source": "baixingwang",
        "politics_district": "沛县",
        "systemSaveInfo": {
            "update_time": "4月9日",
            "politics_district": "沛县"
        },
        "highest_floor": "",
        "decoration": "",
        "location_detail": "风光地产",
        "community": "新华家园小区",
        "website_source_word": "百姓网",
        "pageType": "-detail",
        "contacts_phone": "15852222136",
        "update_time": releasetime,
        "contacts_img": "http://img4.baixing.net/0f8285d68ea949523f2b93831d1dca13.jpg_180x180",
        "business_district": "",
        "house_total_price_min": "",
        "subway_line": "",
        "thisUrl": "http://peixian.baixing.com/ershoufang/a1365396762.html?from=regular",
        "post_title": title,
        "release_time": releasetime,
        "contacts_name": "人生百态853"
        }
        self.kafka_send(self.sell_topic, data)

    # 创建出租帖子消息
    def add_rent(self):
        card_id = "http://xuzhou.baixing.com/zhengzu/a95933158%s.html" % (self.get_current_time())
        title = "No%s 出租帖子测试数据" % (self.get_now_time())
        releasetime=self.get_current_time()
        data = {
            "current_floor": "中",
            "lastModifiedTime": 1523511695462,
            "memoInfo": "baixingwang-8737-0",
            "browseTimes": "",
            "agent_company": "",
            "floor_space": "92",
            "restroom_num": "1",
            "house_furniture": "床,电视,洗衣机,热水器,独立卫生间,阳台,可做饭",
            "taskid": "baixingwang_xuzhou_rent_insert",
            "dbTableName": "xuzhou",
            "rent_require": "",
            "rent_price": "600",
            "towards": "南",
            "type": "rent",
            "bedroom_num": "3",
            "out_of_time": "",
            "city_id": "8737",
            "livingroom_num": "1",
            "id": card_id,
            "isNeedNewId": "true",
            "rent_room": "",
            "house_type": "",
            "house_source": "0",
            "childUrl": { },
            "img_url_list": [
                "http://img4.baixing.net/Fui9PLTIaUCV5kXu8a-8dLozbokC_bi",
                "http://img4.baixing.net/FqncpSQ-4g716j6ikXVqljAuXdT__bi",
                "http://img4.baixing.net/FqzjlBPyJyZyZXdeMpbqeizIRNCt_bi"
            ],
            "parentUrl": "http://xuzhou.baixing.com/zhengzu/a959331589.html?from=regular",
            "website_source": "baixingwang",
            "politics_district": "金山桥开发区",
            "wechat_contact": "",
            "systemSaveInfo": {
                "livingroom_num": "1",
                "restroom_num": "1",
                "update_time": "4月11日",
                "bedroom_num": "3",
                "politics_district": "金山桥开发区"
            },
            "highest_floor": "26",
            "decoration": "简单装修",
            "location_detail": "高铁站新二院隔壁东贺花园b区",
            "community": "高铁东贺花园b区",
            "description_detail": "自家房子没有中介费。长租优惠​‌‌",
            "website_source_word": "百姓网",
            "rent_type": 1,
            "contacts_phone": "18051922253",
            "rent_pay_type": "押一付三",
            "update_time": releasetime,
            "contacts_img": "http://img4.baixing.net/fb86a7f3c6e9e5a280e00dbcd5991b2c.png_180x180",
            "thisUrl": "http://xuzhou.baixing.com/zhengzu/a959331589.html?from=regular",
            "post_title": title,
            "contacts_name": "石恒柏",
            "release_time": releasetime
        }
        self.kafka_send(self.rent_topic, data)

    def add_seek_buy(self):
        card_id = "http://xz.58.com/ershoufang/3371959895134%s.shtml" % (self.get_current_time())
        title = "No%s 求购帖子测试数据" % (self.get_now_time())
        releasetime = self.get_now_time()
        data = {
            "current_floor": "暂无信息",
            "lastModifiedTime": 1523502526819,
            "memoInfo": "58-8737",
            "house_total_price_max": "",
            "browseTimes": "0",
            "floor_space": "100",
            "restroom_num": "1",
            "taskid": "58_xuzhou_seekSell_insert",
            "dbTableName": "xuzhou",
            "towards": "",
            "type": "seekSell",
            "building_age": "暂无信息",
            "description_sell": "小区环境好，地理位置佳！停车方便！有储藏室！",
            "bedroom_num": "3",
            "house_total_price": "500000",
            "city_id": "8737",
            "livingroom_num": "2",
            "id": card_id,
            "isNeedNewId": "true",
            "time": "18小时前",
            "house_source": "0",
            "childUrl": { },
            "property_right_age": "",
            "parentUrl": "http://xz.58.com/ershoufang/33719598951343x.shtml",
            "website_source": "58",
            "politics_district": "贾汪区",
            "systemSaveInfo": {
                "time": "18小时前",
                "house_source": "个人",
                "contacts_name": "王先生"
            },
            "highest_floor": "",
            "monthly_payment": "1434",
            "decoration": "暂无信息",
            "location_detail": "",
            "community": "暂无信息",
            "down_payment": "150000",
            "website_source_word": "58",
            "house_unit_price": "5000",
            "pageType": "-detail",
            "contacts_phone": "18652215993",
            "update_time": releasetime,
            "business_district": "",
            "house_total_price_min": "",
            "house_tag_list": [
                "新上房源"
            ],
            "thisUrl": "http://xz.58.com/ershoufang/33719598951343x.shtml",
            "post_title": title,
            "contacts_name": "王先生",
            "release_time": releasetime
        }
        self.kafka_send(self.seekbuy_topic, data)

    def add_seek_rent(self):
        pass

    #转录房  出售、出租转录到房源录入
    def add_house(self,shangjiType,shangjiId):
        data = {
            "recordTime": self.get_current_time(),
            "shangjiId": shangjiId,
            "shangjiType": shangjiType,
            "userId": self.ucid
        }
        self.kafka_send(self.transfer_house, data)

    #转录客  求购、求租转录到客源录入
    def add_customer(self,shangjiType,shangjiId):
        data = {
            "recordTime": self.get_current_time(),
            "shangjiId": shangjiId,
            "shangjiType": shangjiType,
            "userId": self.ucid
        }
        self.kafka_send(self.transfer_cust, data)

if __name__ == '__main__':
    con = ShangjiKafkaModel()
    print con.add_rent()
    #print con.shangji_list()
    
