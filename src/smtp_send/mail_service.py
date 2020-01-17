#!/usr/bin/env python3
import smtplib

class MailService():
    __slots__ = ('ssl_enabled', 'smtp_addr', 'smtp_port', 'smtp_user', 'smtp_password', 'smtp_server')

    def __init__(self, ssl_enabled, smtp_addr, smtp_port, smtp_user, smtp_password):
        self.ssl_enabled = ssl_enabled
        self.smtp_addr = smtp_addr
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_server = None

    def __enter__(self):
        if self.smtp_server is not None:
            raise RuntimeError('Already connected')
        if self.ssl_enabled:
            self.smtp_server = smtplib.SMTP_SSL(self.smtp_addr, self.smtp_port, local_hostname='smtp_send')
        else:
            self.smtp_server = smtplib.SMTP(self.smtp_addr, self.smtp_port, local_hostname='smtp_send')
        if self.smtp_user and self.smtp_password:
            self.smtp_server.login(self.smtp_user, self.smtp_password)

        return self.smtp_server

    def __exit__(self, exc_ty, exc_val, tb):
        self.smtp_server.quit()
        self.smtp_server = None
