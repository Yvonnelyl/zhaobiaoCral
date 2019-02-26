# # from .baseCreateTable import *
# import sqlalchemy as sa
# import json
#
# from sqlalchemy.ext.declarative import declarative_base
# import sqlalchemy as sa
# from sqlalchemy.orm import *
# from time import strftime
# # -------------my-----------------
# from base.myio  import *
# from base.mydate  import *
#
# Base = declarative_base()
#
# class BaseTable(Base):
#     __tablename__ = ''
#     # 定义各字段
#     fid = sa.Column(sa.String(200), primary_key=True, default=guid)
#     fudtime = sa.Column(sa.String(200), default=now)
#     fcanuse = sa.Column(sa.String(1))
#
# class __TableCreator(type):
#     """
#     创建所有表
#     """
#     def __new__(cls, engine_info=None, dct=None, bases=(BaseTable,), *args, **kwargs):
#         engine = sa.create_engine(engine_info, echo=True)
#         table = dict()
#         for table_name, table_dct in dct['table'].items():
#             columns_dct = cls.__create_columns(table_dct)
#             table[table_name] = type.__new__(cls, table_name, bases, columns_dct)
#             table[table_name].__tablename__ = table_name
#         Base.metadata.create_all(engine)
#
#     @classmethod
#     def __create_columns(cls,dct):
#         create_table_dct = dict()
#         for cln_name, cln_param_dct in dct.items():
#             create_table_dct.update(
#                 {cln_name: cls.__create_cln(cln_param_dct)}
#             )
#
#     @classmethod
#     def __create_cln(cls, cln_param_dct):
#         cln_param_dct = cln_param_dct['Column']
#         param_dct = dict()
#         for cln_param_nm, cln_param in cln_param_dct.items():
#             if isinstance(cln_param, dict):
#                 param_dct.update(
#                     {cln_param_nm : getattr(sa, cln_param_nm)(**cln_param)}
#                 )
#             else: param_dct.update({cln_param_nm: cln_param})
#         return sa.Column(**param_dct)
#
# def get_cral_conf():
#     with open(r'C:\Users\Admin\PycharmProjects\scrapyProjects\zhaobiaoCral\test.json','rb') as f:
#         return json.loads(f.read())
#
# __TableCreator(**get_cral_conf())
#
#
# if __name__  == '__main__':
#     wechat_table_info = {
#         "engine_info": "oracle+cx_oracle://hiibase:hiibase@200.100.100.69:1521/dgr",
#         "dct": {
#             "wechatCrawler": {
#                 "ftitle": {"Column": {"String": {"length": 2000}}},
#                 "faccountname": {"Column": {"String": {"length": 2000}}},
#                 "fimgpath": {"Column": {"String": {"length": 2000}}},
#                 "farticle": {"Column": {"CLOB": ""}},
#                 "freleasetime": {"Column": {"String": {"length": 2000}}},
#                 "fsummary": {"Column": {"String": {"length": 2000}}}}}
#     }
#
