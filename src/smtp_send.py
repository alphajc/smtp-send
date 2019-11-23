#!/usr/bin/env python3

import os
import smtplib
import argparse

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.getcwd() + '/.env')

def render(template):
    tpl = Template(open(template, 'r').read())
    return tpl.render(datetime=os.environ.get('DATETIME'))

def main():
    parser = argparse.ArgumentParser(prog='send-email', description='邮件发送工具')

    parser.add_argument('--text', help="正文路径")
    parser.add_argument('--attachments', '-a', help='附件', nargs="*")
    parser.add_argument('--subject', '-s', help='主题', required=True)
    parser.add_argument('--recipients', help='收件人，多个收件人间用英文逗号分隔')
    parser.add_argument('--sender', help='发件人')
    parser.add_argument('--smtp-addr', help='SMTP 服务器地址')
    parser.add_argument('--smtp-port', help='SMTP 服务器端口')
    parser.add_argument('--smtp-user', '-u', help='SMTP 用户')
    parser.add_argument('--smtp-password', '-p', help='SMTP 用户密码')
    parser.add_argument('--ssl', help='是否开启ssl', action='store_true')
    parser.add_argument('--cc', help='抄送，多个收件人间用英文逗号分隔')
    parser.add_argument('--bcc', help='密送，多个收件人间用英文逗号分隔')
    parser.add_argument('--render', help='待渲染文件')

    args = parser.parse_args()

    text = args.text
    attachments = args.attachments
    smtp_addr = args.smtp_addr or os.environ.get('SMTP_ADDR')
    smtp_port = args.smtp_port or int(os.environ.get('SMTP_PORT', '0'))
    smtp_user = args.smtp_user or os.environ.get('SMTP_USER')
    smtp_password = args.smtp_password or os.environ.get('SMTP_PASSWORD')
    sender = args.sender or os.environ.get('SENDER') or smtp_user
    recipients_line = args.recipients or os.environ.get('RECIPIENTS')
    recipients = recipients_line.split(',')
    if args.cc: recipients += args.cc.split(',')
    if args.bcc: recipients += args.bcc.split(',')

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = args.recipients
    message['Cc'] = args.cc
    message['Bcc'] = args.bcc
    message['Subject'] = Header(args.subject, 'utf-8')

    if text:
        message.attach(MIMEText(open(text, 'r').read(), 'plain', 'utf-8'))
    else:
        message.attach(MIMEText(render(args.render), 'plain', 'utf-8'))

    for attachment in attachments:
        att = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename="' + os.path.basename(attachment) + '"'
        message.attach(att)

    try:
        if args.ssl:
            server = smtplib.SMTP_SSL(smtp_addr, smtp_port)
        else:
            server = smtplib.SMTP(smtp_addr, smtp_port)
        server.login(smtp_user, smtp_password)
        server.sendmail(sender, recipients, message.as_string())
        server.quit()
    except smtplib.SMTPException:
        print('错误：发送失败！')

if __name__ == '__main__':
    main()