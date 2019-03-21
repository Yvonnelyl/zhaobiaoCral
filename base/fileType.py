"""
@ WHAT：filetype函数 调用时 input 文件字节流 output 文件类型
@ HOW：通过提取 文件头 对比typeList中的字典，索引文件类型
@ PS：若全部不匹配会对比相似度 返回最相似的那个 文件类型
"""
from scrapy.pipelines.files import FileException
from zhaobiaoCral.settings import  ACCEPTFILETYPE

# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少半2字符，长则8字符
def typeList():
    return ACCEPTFILETYPE


# 字节码转16进制字符串
def bytes2hex(bytes):
    print('关键码转码……')
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(bins): # 提取20个字符
    bins = bytes2hex(bins)  # 转码
    bins = bins.lower()  # 小写
    print(bins)
    tl = typeList()  # 文件类型
    ftype = 'unknown'
    print('关键码比对中……')
    for hcode in tl.keys():
        lens = len(hcode)  # 需要的长度
        if bins[0:lens] == hcode:
            ftype = tl[hcode]
            return ftype
    if ftype == 'unknown':  # 全码未找到，优化处理，码表取5位验证
        raise FileException
