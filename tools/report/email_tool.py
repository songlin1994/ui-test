# -*- coding: utf-8 -*- 
# Project: guoya-tools-demo
# Creator: LudvikWoo
# Create time: 2019-09-18 00:26
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart



def test_send_text():
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "wuling1105@126.com"  # 用户名
    mail_pass = "126shouquanma"  # 口令

    sender = 'wuling1105@126.com'
    receivers = ['wuling@guoyasoft.com', 'wuling1105@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText('果芽软件自动代码', 'plain', 'utf-8')
    message['From'] = sender
    message['To'] = ';'.join(receivers)

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def test_send_html():
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "wuling1105@126.com"  # 用户名
    mail_pass = "126shouquanma"  # 口令

    sender = 'wuling1105@126.com'
    receivers = ['wuling@guoyasoft.com', 'wuling1105@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_msg = '''
    <p>Python 邮件发送测试...</p>
    <p><a href="http://www.guoyasoft.com">这是一个链接</a></p>
    '''
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = ';'.join(receivers)

    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def test_send_attach():
    # 第三方 SMTP 服务
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "wuling1105@126.com"  # 用户名
    mail_pass = "126shouquanma"  # 口令

    sender = 'wuling1105@126.com'
    receivers = ['wuling@guoyasoft.com', 'wuling1105@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ';'.join(receivers)
    subject = 'Python SMTP 邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="test.txt"'
    message.attach(att1)

    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open('guoya.txt', 'rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    message.attach(att2)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
