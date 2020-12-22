from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


class Letter:
    """邮件内容
    包括了邮件头部（主题、发件人、收件人、抄送、密送等），邮件正文(文本、附件)
    属性：
        message: 邮件内容

    """
    __slots__ = ('message')

    def __init__(self, subject, **envelope):
        """初始化信封
        参数说明：
            sender: (发件人, 邮箱)
            to: [(收件人, 邮箱)] 或((收件人, 邮箱))
            cc: [(抄送收件人, 邮箱)] 或((抄送收件人, 邮箱))
            bcc: [(密送收件人, 邮箱)] 或((密送收件人, 邮箱))
        """
        self.message = MIMEMultipart()
        self.message['Subject'] = Header(subject, 'utf-8')
        self.message['From'] = formataddr((Header(envelope['sender'][0], 'utf-8').encode(), envelope['sender'][1]))
        self.message['To'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['to']])
        self.message['Cc'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['cc']]) if envelope['cc'] else None
        self.message['Bcc'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['bcc']]) if envelope['bcc'] else None

    def attach_text(self, text: str):
        """添加正文
        参数说明：
            text: 正文内容
        """
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))

    def append_attachment(self, content: bytes, filename: str):
        """添加附件
        参数说明：
            content: 二进制内容
            filename: 邮件中显示的文件名
        """
        att = MIMEText(content, 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        self.message.attach(att)
