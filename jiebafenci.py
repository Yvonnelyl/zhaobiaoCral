# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 10:49
# @Author  : liuyl
# @Email   : nizhidaode2016@163.com
# @File    : zb.py
# @Software: PyCharm

import cx_Oracle
import pandas as pd
import jieba
import re
import collections



jieba.load_userdict("fenci/hzfc.txt")
# # 连接数据库
# conn = {
#     "user": "hiibase",
#     "password": "hiibase",
#     "dsn": "200.100.100.69:1521/dgr"
# }
# conn = cx_Oracle.connect(**conn)
# cursor = conn.cursor()
# cursor.execute ("SELECT hangye hangye,title title,text text FROM zb2")
# rows = cursor.fetchall()  # 得到所有数据集
#
# # 标记序号列
# data_list = []
# for index in enumerate(rows):
#     data_list.append(index)
# das = pd.DataFrame(data_list)
#
# # 转为dataframe，修改列名 ：序号，行业，题目，文章
# data = pd.DataFrame(rows)
# data.columns = ['hangye','title','text']
# data.insert(0,'序号',das[0])
text = """
维西傈僳族自治县农牧和科学技术局2018年石漠化综合治理牧草种子采购项目公开招标公告
2019年03月06日 15:14 来源：中国政府采购网 【打印】 【显示公告概要】

ZD20190010  维西傈僳族自治县农牧和科学技术局2018年石漠化综合治理牧草种子采购项目公开招标公告
一、项目概况

根据《中华人民共和国政府采购法》、《中华人民共和国政府采购法实施条例》等有关规定，云南志达招标有限公司受维西傈僳族自治县农牧和科学技术局的委托，对“维西傈僳族自治县农牧和科学技术局2018年石漠化综合治理牧草种子采购项目”进行公开招标采购，欢迎符合《维西傈僳族自治县农牧和科学技术局2018年石漠化综合治理牧草种子采购项目招标文件》（以下简称《招标文件》）规定条件，具有相应供货或完成项目能力的投标人（供应商）报名参加。

二、招标范围
1、招标编号：ZD20190010

2、招标内容：牧草种子共计13225公斤，采购预算￥52.6万元，具体详见招标文件。

3、项目交付使用时间：合同签订后7个日历日内。

4、项目实施地点: 采购人指定地点。

三、投标人资格要求
1、投标人应具备《中华人民共和国政府采购法》第二十二条规定的条件。具有独立承担民事责任的能力，在专业技术和设备方面具有相应完成本项目的能力。

2、投标人具有草种经营许可证。

3、投标人参加本次政府采购活动前三年内在经营活动中没有重大违法记录的声明。

4、投标人未被列入“信用中国（www.creditchina.gov.cn）”失信被执行人、重大税收违法案件当事人名单、政府采购严重违法失信行为记录名单及“中国政府采购网（www.ccgp.gov.cn）”政府采购严重违法失信行为信息记录，提供网站信用信息查询记录截图。查询截止时点：招标公告发布之日至投标文件递交截止时间。

5、本项目不接受联合体投标。

四、招标文件出售时间及地点

凡有意参加的投标人，请于2019年3月6日至2019年3月13日17:00(北京时间，下同)，登录迪庆州公共资源交易电子服务系统（网址：http://183.224.249.60:8001/），凭企业数字证书（CA）在网上获取采购文件及其它采购资料（电子招标文件，格式为*.ZCZBJ），未办理企业数字证书（CA）的企业详见其办理流程，并在网上申请办理证书，以便获取招标文件，此为获取招标文件的唯一途径（试运行期间，采用网络系统报名和现场报名，系统内报名成功后请持报名截图到采购代理机构进行现场报名并购买纸质招标文件及相关资料，两者均成功报名后才能参与投标，否则视为报名无效）。

投标人应从昆明市日新中路润城第一大道商务办公楼五幢8楼云南志达招标有限公司招标三部获取纸质招标文件和相关资料，获取时间为2019年3月6日至2019年3月13日（法定公休日、法定节假日除外），每天9:00-12:00，14:30-17:00出售。招标文件售价为600元/份；标书售后不退，现场报名，不办理邮购。投标人须按本公告的联系地址，携带下列资料购买招标文件（复印件加盖公章留存）：

1、营业执照（原件或复印件盖单位公章）；

2、草种经营许可证（原件或复印件盖单位公章）

3、法定代表人身份证明文件（原件）、法定代表人授权委托书（原件），法定代表人或委托代理人本人身份证（原件）。

4、网络系统报名截图。

五、开标时间及地点
1、投标文件递交的截止时间为2019年3月27日09:30（北京时间）；

2、网上递交：迪庆州公共资源交易电子服务系统，投标人须在投标截止时间之前完成所有电子投标文件的上传，网上确认电子签名，并打印上传投标文件回执；在投标截止时间之前未完成电子投标文件上传的，视为撤回投标文件。

网上递交投标文件后，还须到开标现场递交刻录投标文件的光盘，逾期送达的或者未送达指定地点的投标文件（光盘），视为撤回投标文件，采购人不予受理。

3、纸质递交（试运行期间）：纸质投标文件现场递交的地点为维西傈僳族自治县三江大道维西县行政中心2楼维西县公共资源交易中心开标厅，逾期送达的或不符合规定的投标文件将被拒绝。

注：（试运行期间）电子投标文件应与纸质文件同时递交，且内容一致，不一致时以纸质文件为准。

现场递交地址：维西傈僳族自治县三江大道维西县行政中心2楼维西县公共资源交易中心开标厅。

4、开标时间：2019年3月27日09:30（北京时间），开标地点：维西傈僳族自治县三江大道维西县行政中心2楼维西县公共资源交易中心开标厅，投标人的法定代表人或其授权代理人应持本人身份证原件准时参加开标会。

六、公告发布网站： 
《云南省政府采购网》、《云南省公共资源交易电子服务系统》、《迪庆州公共资源交易电子服务系统》

采 购 人：维西傈僳族自治县农牧和科学技术局

联系人：王老师

联系电话：0887-8626537 

采购代理机构：云南志达招标有限公司 

联 系 人：张先生  吴先生  杨女士

联系电话：0871-63133097    传真：0871-63116420

邮政编码：650028                   

地    址：昆明市日新中路润城第一大道商务办公楼五幢8楼

开户银行：中国建设银行昆明祥云支行

户    名：云南志达招标有限公司  

账    号：53001875036051002850
"""
data = pd.DataFrame(data=[[text]], columns=['text'])
# load汇总词库
# hzfc_file = open('E:\招标分类\hzfc.txt')
# hzfc_dict = hzfc_file.read()
# print(hzfc_dict)


# 分词
each_fclist = []
for i in range(len(data)):
    each_text = data['text'][i]
    # each_text = each_text.read()
    # 去除标点符号
    # line = re.sub(r"[\s+\.\!\/_,$%^*()?;；:+\"\']+|[+——！，;:。？、~@#￥%……&*（）：《 》 | = 【】-]+", " ", each_text)
    each_fc = jieba.cut(each_text, cut_all=False)
    qckg = [x for x in each_fc if x != ' ']

    # 停用词
    object_list = []
    remove_words = open("fenci/tyc.txt", encoding="gbk")
    remove_words = remove_words.read()
    for word in qckg:  # 循环读出每个分词
        if word not in remove_words:  # 如果不在去除词库中
            object_list.append(word)  # 分词追加到列表
    each_fclist.append(object_list)

    # each_fclist.append(qckg)

# print(each_fc)
data['分词'] = each_fclist
print(data['分词'] )

for i in range(len(each_fclist)):
    word_counts = collections.Counter(each_fclist[i]) # 对分词做词频统计
    word_counts_top10 = word_counts.most_common(20) # 获取前10最高频的词
    print(word_counts_top10) # 输出检查
#
# result = [i for i in data['分词'][0]]
# print(result)

# print(data['分词'][0])

# print(data['text'][0])
# df = data.values.tolist()
# for i in range(len(df)):
#     if df[i][1] == ''
#     print(df[i][1])
#     # if df[i][0]


# data1_gg = data1.hangye
# df = data1.drop('hangye',axis=1)
# df = pd.DataFrame(columns = ["hy", "tm", "nr"])
# # df['hy'] = data1.hangye
# # df['tm'] = data1[['title']]
# df['nr'] = data1.text

# print(data1['hangye'])
# col_name = data1.columns.tolist()
# col_name.insert(0,1)
# data1.reindex(columns=col_name)
# print(data)

# col_name = data1.columns.tolist()
# col_name.insert(col_name.index('B'),'D')# 在 B 列前面插入
# df.reindex(columns=col_name)


