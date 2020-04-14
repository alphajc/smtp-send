import os
import sys
import argparse
from dotenv import load_dotenv
from email.utils import parseaddr
from .mail_service import MailService
from .tools import Tools
from .letter import Letter

def main():
    load_dotenv(dotenv_path=os.getcwd() + '/.env')
    parser = argparse.ArgumentParser(prog='smtp-send', description='邮件发送工具')

    parser.add_argument('--text', help="正文路径")
    parser.add_argument('--attachments', '-a', help='附件', nargs="+")
    parser.add_argument('--subject', '-s', help='主题', required=True)
    parser.add_argument('--recipients', help='收件人，多个收件人间用英文逗号分隔')
    parser.add_argument('--sender', help='发件人')
    parser.add_argument('--smtp-addr', help='SMTP 服务器地址')
    parser.add_argument('--smtp-port', help='SMTP 服务器端口')
    parser.add_argument('--smtp-user', '-u', help='SMTP 用户')
    parser.add_argument('--smtp-password', '-p', help='SMTP 用户密码')
    parser.add_argument('--ssl', help='是否开启ssl', action='store_true')
    parser.add_argument('--cc', help='抄送，多个收件人间用英文逗号分隔', default='')
    parser.add_argument('--bcc', help='密送，多个收件人间用英文逗号分隔', default='')
    parser.add_argument('--render', help='待渲染文件')
    parser.add_argument('--meta', help='元数据，json格式的文件')

    args = parser.parse_args()

    text = args.text
    attachments = args.attachments or []
    smtp_addr = args.smtp_addr or os.environ.get('SMTP_ADDR', 'localhost')
    smtp_port = args.smtp_port or int(os.environ.get('SMTP_PORT', '25'))
    smtp_user = args.smtp_user or os.environ.get('SMTP_USER')
    smtp_password = args.smtp_password or os.environ.get('SMTP_PASSWORD')
    sender = args.sender or os.environ.get('SENDER') or smtp_user
    rl = args.recipients or os.environ.get('RECIPIENTS')
    to = [parseaddr(i) for i in rl.split(',')]
    cc = [parseaddr(i) for i in args.cc.split(',')]
    bcc = [parseaddr(i) for i in args.bcc.split(',')]
    recipients = [i[1] for i in to] + [i[1] for i in cc] + [i[1] for i in bcc]

    letter = Letter(args.subject, sender=parseaddr(sender),
                    to=to, cc=cc,
                    bcc=bcc)
    if text:
        with open(text, 'r') as f:
            text_content = f.read()
    elif args.render and args.meta:
        text_content = Tools.render(args.render, args.meta)
    else:
        text_content = sys.stdin.read()
        print(text_content)
        if not text_content:
            print('无法获取邮件正文')
            exit(1)

    letter.attach_text(text_content)

    for attachment in attachments:
        with open(attachment, 'rb') as content:
            letter.append_attachment(content.read(), os.path.basename(attachment))

    mail_service = MailService(args.ssl, smtp_addr, smtp_port, smtp_user, smtp_password)
    try:
        with mail_service as ms:
            ms.sendmail(sender, recipients, letter.message.as_string())
    except Exception as e:
        print('错误：发送失败！', e)

if __name__ == "__main__":
    main()