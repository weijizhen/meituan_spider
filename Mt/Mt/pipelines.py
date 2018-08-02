# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from Mt.settings import tableName

class MtPipeline(object):

    tableName = tableName

    def __init__(self):
        db = pymysql.connect(host="127.0.0.1",port=3306,user = "root",passwd="123456",db='mt',use_unicode = True,charset = "utf8mb4")
        #因为存在中文，必须设置use_unicode。存特殊符号，必须设置charset="utf8mb4"
        #cursor游标/指针

        cursor = db.cursor()
        self.db = db
        self.cursor = cursor

        sql = """create table if not exists {0}
                (id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                noid VARCHAR(30),
                rid  VARCHAR(30),
                nuiacid  VARCHAR(30),
                oauth_openid  VARCHAR(30),
                open   VARCHAR(30),
                avatar  VARCHAR(2000),
                nickname  VARCHAR(30),
                user_ip VARCHAR(30),
                name  VARCHAR(1000),
                introductron VARCHAR(1000),
                img1  VARCHAR(1000),
                img2  VARCHAR(30),
                img3  VARCHAR(30),
                img4  VARCHAR(30),
                img5  VARCHAR(30),
                datails  VARCHAR(1000),
                joindata VARCHAR(1000),
                frommatdata VARCHAR(1000),
                votenum VARCHAR(30),
                giftcount VARCHAR(30),
                vheat VARCHAR(30),
                status VARCHAR(30),
                locktime VARCHAR(30),
                attestation VARCHAR(30),
                atmsg VARCHAR(1000),
                lastvotetime VARCHAR(10000),
                createtime VARCHAR(30))""".format(self.tableName)
        self.cursor.execute(sql)
        self.db.commit()

    def process_item(self, item, spider):
        try:
            sql = """insert into {0}(avatar,nickname,`name`,img1,datails,joindata,frommatdata) VALUES ("{img1}","{city}","{name}","{img2}","{address}","{phone}","{Dishes}")""".format(self.tableName,**item)
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print("数据已经重复，不存入")
        return item
    def __del__(self):
        self.cursor.close()
        self.db.close()


