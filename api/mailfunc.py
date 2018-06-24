import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send(id,mail_dic):
    charset       = "iso-2022-jp"
    serverMailaddress = mail_dic["from_address"] #送信元アドレス
    password      = mail_dic["from_pw"] #送信元アドレスのパスワード
    toMailaddress = mail_dic["to_address"] #送信先のアドレス

    msg = MIMEText("%sが入室しました" % (id), "plain", charset)
    msg["subject"] = Header("Test to send mail".encode(charset), charset)
    smtp_obj = smtplib.SMTP_SSL("smtp.mail.yahoo.co.jp", 465)
    smtp_obj.ehlo()
    smtp_obj.login(serverMailaddress, password)
    smtp_obj.sendmail(serverMailaddress, toMailaddress, msg.as_string())

    smtp_obj.quit()

