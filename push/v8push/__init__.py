v8_conf = {
    "fpmid": "",
    "fmessageid": "",
    "ftemplateid": "JzI4KiKCFROzSjjv9EkYDtWy-_l2hLlyxDtmNXnBfqs",
    "ftype": "template",
    "ftitle": "招标推送",
    "ffirst": "请查看招标信息",
    "fremark": "",
    "fkeyword": "",
    "furl": "",
    "fopenid": ""
}

import cx_Oracle, uuid

class V8Push():

    def __init__(self, conn_dct=None):
        self.push_dct = v8_conf
        if "oracle" in self.push_dct.keys():
            self.conn = cx_Oracle.connect(**self.push_dct["oracle"])
        else:
            self.conn = cx_Oracle.connect(**conn_dct)

        self.cur = self.conn.cursor()
        cols = ','.join(self.push_dct.keys())
        val = ",".join([":%s" % str(num+1) for num in range(len(self.push_dct.keys()))])

        self.person_info  = self.__get_push_person()

        prepare_sql = f"insert into hii.wxMsg_tbs_content ({cols}) values ({val})"
        self.cur.prepare(prepare_sql)

    def  __get_push_person(self):
        self.cur.execute("select t.fpmid, t.fopno from hii.wxMsg_tbs_send t")
        persons = self.cur.fetchall()

        result = []
        for row in persons:
            tmp =  {
                "pmid":  row[0],
                "opno": row[1],
            }
            result.append(tmp)
        return  result

    def push(self, url, title, money, source, time, article_type):
        """
        """
        for person in self.person_info:
            self.push_dct["fmessageid"] = uuid.uuid4().hex
            self.push_dct["fpmid"] = person["fpmid"]
            self.push_dct["fopenid"] = person["fopenid"]
            self.push_dct["url"] = url
            self.push_dct["fremark"] = "招标类型：" + article_type
            self.push_dct["fkeyword"] = f"项目名称:  {title}\n预算:  {money}\n招标方：{source}\n时间：{time}"

            values = tuple(self.push_dct.values())
            self.cur.execute(None, values)