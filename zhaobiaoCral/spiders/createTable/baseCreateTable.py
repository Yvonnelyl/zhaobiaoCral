from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy.orm import *
from time import strftime
# -------------my-----------------
from base.myio  import *
from base.mydate  import *


Base = declarative_base()


class BaseTable(Base):
    __tablename__ = ''
    # 定义各字段
    fid = sa.Column(sa.String(200), primary_key=True, default=guid)
    fudtime = sa.Column(sa.String(200), default=now)
    fcanuse = sa.Column(sa.Numeric(1),default=1)
    # 定义
