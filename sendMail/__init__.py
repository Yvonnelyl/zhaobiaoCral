import zmail
from base.myio import json_to_dict


class MyMail():
    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        # 使用你的邮件账户名和密码登录服务器
        self.server = zmail.server(self.user, self.pwd)

    def send(self, receive_mail, subject, content):
        # 你的邮件内容
        mail_content = {
            'subject': subject,  # 随便填写
            'content_text': content,  # 随便填写
        }

        # 发送邮件
        self.server.send_mail(receive_mail, mail_content)


def send_mail(subject, content):
    mail_conf = json_to_dict('user_pwd.json')
    user, pwd, receive_mail = mail_conf["user"], mail_conf["pwd"], mail_conf["receive_mail"]
    my_mail = MyMail(user, pwd)
    my_mail.send(receive_mail, subject, content)


if __name__ == '__main__':
    for i in range(5):
        send_mail('猪猪','猪猪呜唔晤嗯地数数：'+ str(i))