import re
from push import  v8push
from zhaobiaoCral.settings import  ORACLE_CONN
import cx_Oracle



class Push():
    def  __init__(self):
        self.conn = cx_Oracle.connect(**ORACLE_CONN)
        # v8oracle连接
        db = {
            "dsn": "200.100.100.151/zydsj",
            "user": "hii",
            "password": "hii"
        }
        self.cur = self.conn.cursor()
        self.v8_push = v8push.V8Push(db)
        self.data = dict()

        # 分词表
        select_article = """
        select t.ftype, t.ftitleword,t.fsourceword,t.ftitlekeyword, t.fisuse from fenci t
        """
        self.cur.execute(select_article)
        self.fenci_list = self.cur.fetchall()
        self.fenci_dct = dict()
        for  row in  self.fenci_list:
            tmp = {row[0]: {
                "title": re.split(r"[ ]+", row[1]) if row[1] else "",
                "source": re.split(r"[ ]+", row[2]) if row[2] else "",
                "titlekeyword": re.split(r"[ ]+", row[3]) if row[3] else ""
            }}
            self.fenci_dct.update(tmp)
        self.tongyong = self.fenci_dct.pop("通用")

    def push(self):
        for values, update_dct in self.extract():
            self.v8_push.push(

            )
            # todo update_dct

    def extract(self):
        select_article = """
        select t.farticleid, t.ftitle, t.fudtime, t.zhaobiao_type, t.fregion,t.fywtype,t.ftime,f.money, f.source_company, t.furl from fzbList t 
            left join fzbKeyword f on t.farticleid = f.farticleid 
        where t.fisuse = '1'
          """
        self.cur.execute(select_article)

        row_data = 'start'
        while row_data:
            row_data = self.cur.fetchone()
            values, update_dct = self.process_data(row_data)
            yield values, update_dct

    def process_data(self, row_data):

        row_data_dct = {
            "articleid": row_data[0],
            "title": row_data[1],
            "uddate": str(row_data[2])[:10],
            "zhaobiao_type": row_data[3] if row_data[3] else '',
            "fregion": row_data[4] if row_data[4] else '',
            "article_type": "",
            "time": row_data[6] if row_data[6] else '',
            "money": row_data[7] if row_data[7] else '',
            "source": row_data[8] if row_data[8] else '',
            "url": row_data[9] if row_data[9] else '',
        }

        row_data_dct, update_dct = self.decide_article_type_n_push(row_data_dct)
        return  row_data_dct, update_dct


    def decide_article_type(self, row_data_dct):
        update_dct = {
            "articleid": row_data_dct["articleid"],
            "isuse": "",
            "article_type": ""
        }
        for type_name, dct in self.fenci_dct.items():
            # 用招标人分类
            if row_data_dct["source"]  != "" and Push.keyword_in_str(dct["source"], row_data_dct["source"]):
                    row_data_dct["article_type"] = type_name
                    update_dct["article_type"] = type_name
                    if Push.keyword_in_str(dct(["title"]) + self.tongyong, row_data_dct["title"]):
                        update_dct["isuse"] = 3
                    else:
                        row_data_dct = None
                        update_dct["isuse"] = 2
            # 若招标人为空 用title 分类
            elif row_data_dct["source"]  == "" and Push.keyword_in_str(dct["title"], row_data_dct["title"]):
                row_data_dct["article_type"] = type_name
                update_dct["article_type"] = type_name
                if Push.keyword_in_str(dct(["title"]) + self.tongyong, row_data_dct["title"]):
                    update_dct["isuse"] = 3
                else:
                    row_data_dct = None
                    update_dct["isuse"] = 2
            # 招标人不为空但不在类别中

        return update_dct

    @staticmethod
    def keyword_in_str(l, s):
        for word in l:
            if re.findall(word, s):
                return True
        return False

if  __name__ == "__main__":
    p = Push()
    p.push()
