import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from lxml import etree
import logging
import os
import sys

previous_chapter = 0
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='nitianxieshen.log', level=logging.INFO, format=LOG_FORMAT)


def get_content():
    r = requests.get(url="http://www.nitianxieshen.com/")
    r.encoding = 'utf-8'
    return r.text


def get_num(content):
    xpath = '/html/body/div/div[2]/div[2]/div[2]/div[2]/ul/li[1]/a/text()'
    dom = etree.HTML(content)
    newest_str = str(dom.xpath(xpath)[0])
    newest_int = int(newest_str[1:newest_str.index('章')])
    return newest_int


def send_email(sender: str, receiver: str, password: str, message: str):
    # sender: 发送者QQ邮箱地址，比如123@qq.com
    # receiver:收件人的邮箱地址
    # password: 发送者的QQ邮箱授权码，在QQ邮箱网页端开启smtp服务时会自动生成一个授权码
    subject = "逆天邪神更新啦"
    smtp_server = 'smtp.qq.com'
    msg = MIMEText(message, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    smtp = smtplib.SMTP_SSL(smtp_server, port=465)
    try:
        smtp.connect('smtp.qq.com')
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
    except smtplib.SMTPException as smtp_exception:
        logging.error('邮件发送错误', smtp_exception)
        return False
    finally:
        smtp.quit()
    logging.info('发送成功')
    return True


def init():
    global previous_chapter
    if os.path.exists('chapter_config'):
        with open('chapter_config', 'r') as f:
            previous_chapter = int(f.readline())
    else:
        with open('chapter_config', 'a'):
            pass


def save_chapter(chapter: int):
    with open("chapter_config", 'w') as f:
        f.write(str(chapter))


if __name__ == "__main__":
    sender = sys.argv[1]
    receiver = sys.argv[2]
    password = sys.argv[3]
    try:
        init()
        web_content = get_content()
        current_chapter = get_num(web_content)
        if current_chapter > previous_chapter:
            if not send_email(sender, receiver, password, web_content):
                send_email(web_content)
            save_chapter(current_chapter)
        else:
            logging.info("暂无更新")
    except Exception as e:
        logging.exception("获取最新章节异常")
