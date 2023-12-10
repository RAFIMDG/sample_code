import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import logging as logger


class EmailHelper:

    def __init__(self):
        self.logger = logger.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")

    def __build_email_header_body(self, email_df, email_host_df):
        """
        This method is used to generate the email header and body

        """
        message = MIMEMultipart()
        message['From'] = f'{self.config.get("EMAIL", "SENDER_NAME")}<{self.config.get("EMAIL", "SENDER")}>'
        message['To'] = self.config.get("EMAIL", "TO")
        message['Cc'] = self.config.get("EMAIL", "CC")
        message['Bcc'] = self.config.get("EMAIL", "BCC")
        message['Date'] = formatdate(localtime=True)
        message['Subject'] = "DEMO Mail - Daily Lab Status Report"
        Body = f"""<p style="font-family:Calibri;font-size:15px">Hello Team,</br></br>Kindly find the attached Lab status Report, Please find the below device issues and corresponding Device pools. Check manually on all device pools, <strong>If any affected device's or device pool's is not available in this table please let me know</strong></br></br><strong>Host Recovery List :</strong> </br></br>{email_host_df}</br></br><strong>Device Recovery List :</strong> </br></br>{email_df}</br>Thanks,</br>{self.config.get("EMAIL", "SENDER_NAME")}</p>"""
        message.attach(MIMEText(Body, "html"))
        return message

    def send_alert_mail(self, email_df, email_host_df):
        """
        This method is used to send the mail
        """

        try:
            cc = self.config.get("EMAIL", "CC")
            to = self.config.get("EMAIL", "TO")
            bcc = self.config.get("EMAIL", "BCC")
            rcpt = cc.split(",") + bcc.split(",") + [to]
            header_body = self.__build_email_header_body(email_df, email_host_df)
            mailer = smtplib.SMTP('mail-relay.amazon.com')
            mailer.sendmail(self.config.get('EMAIL', 'SENDER'), rcpt, header_body.as_string())
            self.logger.info(" *****Device health status email sent sucessfully******")
        except smtplib.SMTPException as e:
            self.logger.error("Error: unable to send email {}".format(e))
