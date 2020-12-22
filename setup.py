import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="smtp-send",
    version="0.0.7",
    description="命令行邮件发送工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canovie/smtp-send",
    author="Jerry Chan",
    author_email="jerry@mydream.ink",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["smtp-send", "send-email", "pysendemail", "sendemail", "email"],
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "smtp-send = smtp_send.cli:main"
        ]
    },
)
