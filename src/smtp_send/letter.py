from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

class Letter:
    __slots__ = ('message')

    def __init__(self, subject, **envelope):
        self.message = MIMEMultipart()
        self.message['Subject'] = Header(subject, 'utf-8')
        self.message['From'] = formataddr((Header(envelope['sender'][0], 'utf-8').encode(), envelope['sender'][1]))
        self.message['To'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['to']])
        self.message['Cc'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['cc']])
        self.message['Bcc'] = ','.join([formataddr((Header(i[0], 'utf-8').encode(), i[1])) for i in envelope['bcc']])

    def attach_text(self, text: str):
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))

    def append_attachment(self, content: bytes, filename: str):
        att = MIMEText(content, 'base64', 'utf-8')
        att['Content-Type'] = 'application/octet-stream'
        att['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        self.message.attach(att)