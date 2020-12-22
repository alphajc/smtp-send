#!/usr/bin/env python3
import smtplib


class MailService():
    """邮件服务器
    提供邮件服务能力
    属性：
        smtp_server: 可用的服务器

    """
    __slots__ = ('smtp_server')

    def __init__(self, ssl_enabled, smtp_addr, smtp_port, smtp_user, smtp_password):
        """初始化smtp_server
        参数：
            ssl_enabled: 布尔值，是否开启 ssl
            smtp_addr: smtp 服务器地址
            smtp_port: smtp 服务器端口
            smtp_user: smtp 登录用户
            smtp_password: smtp 登录密码
        """
        if ssl_enabled:
            self.smtp_server = smtplib.SMTP_SSL(smtp_addr, smtp_port, local_hostname='smtp_send')
        else:
            self.smtp_server = smtplib.SMTP(smtp_addr, smtp_port, local_hostname='smtp_send')
        if smtp_user and smtp_password:
            self.smtp_server.login(smtp_user, smtp_password)

    def __enter__(self):
        return self.smtp_server

    def __exit__(self, exc_ty, exc_val, tb):
        self.smtp_server.quit()
        self.smtp_server = None
