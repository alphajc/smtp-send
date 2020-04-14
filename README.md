# smtp-send

[![Actions](https://github.com/canovie/smtp-send/workflows/Upload%20Python%20Package/badge.svg)](https://github.com/canovie/smtp-send/actions)
[![PyPI](https://img.shields.io/pypi/v/smtp-send)](https://pypi.org/project/smtp-send)

由于在自动化环境中大量依赖环境变量和命令行参数的行式传参，我想在此基础上去完善一个可发送邮件的命令行工具。主要功能包括：
- 命令行和环境变量传入相关配置
- 支持 SSL
- 支持抄送和密送
- 支持基于环境变量的正文渲染
- 支持多附件
- 支持 HTML *
- 支持 MarkDown *

> 注：「*」为待开发

## 使用说明

```
usage: smtp-send [-h] [--text TEXT]
                  [--attachments [ATTACHMENTS [ATTACHMENTS ...]]] --subject
                  SUBJECT [--recipients RECIPIENTS] [--sender SENDER]
                  [--smtp-addr SMTP_ADDR] [--smtp-port SMTP_PORT]
                  [--smtp-user SMTP_USER] [--smtp-password SMTP_PASSWORD]
                  [--ssl] [--cc CC] [--bcc BCC] [--render RENDER]
                  [--meta META]

邮件发送工具

optional arguments:
  -h, --help            show this help message and exit
  --text TEXT           正文路径
  --attachments [ATTACHMENTS [ATTACHMENTS ...]], -a [ATTACHMENTS [ATTACHMENTS ...]]
                        附件
  --subject SUBJECT, -s SUBJECT
                        主题
  --recipients RECIPIENTS
                        收件人，多个收件人间用英文逗号分隔
  --sender SENDER       发件人
  --smtp-addr SMTP_ADDR
                        SMTP 服务器地址
  --smtp-port SMTP_PORT
                        SMTP 服务器端口
  --smtp-user SMTP_USER, -u SMTP_USER
                        SMTP 用户
  --smtp-password SMTP_PASSWORD, -p SMTP_PASSWORD
                        SMTP 用户密码
  --ssl                 是否开启ssl
  --cc CC               抄送，多个收件人间用英文逗号分隔
  --bcc BCC             密送，多个收件人间用英文逗号分隔
  --render RENDER       待渲染文件
  --meta META           元数据，json格式的文件
```

__注：__
1. `--render`和`--meta`需同时指定，正文渲染才有效
2. 如果`--text`被指定，则正文内容为其所指定项
3. 除了上述两种方式，新添加了从标准输入获取正文的方式

### 正文渲染

1. 待渲染文件中变量以 `jinja2` 的格式指定，详见[官方文档](https://jinja.palletsprojects.com/en/2.10.x/)

    示例：
    ```
    {{ datetime }}
    ```

2. meta 文件格式：

    ```json
    {
        "configmaps": {
            "datetime": "DATETIME"
        }
    }
    ```

3. 呈现：

    假设设置环境变量`DATETIME`为`2019年11月23日`，那么发送的正文内容就将会是
    ```
    2019年11月23日
    ```