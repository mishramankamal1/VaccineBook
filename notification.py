import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

import param
from twilio.rest import Client
from email.mime.multipart import MIMEMultipart


# def mail_send(body):
#     gmail_user = param.gmail_user
#     gmail_password = param.gmail_password
#     msg = EmailMessage()
#     msg['Subject'] = "Alert Vaccine Available"
#     msg['From'] = "Mankamal Misra"
#     msg['To'] = param.user_list
#     msg_body = body
#     msg.set_content(msg_body)
#     try:
#         server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#         server.login(gmail_user, gmail_password)
#         server.send_message(msg)
#         server.quit()
#     except:
#         print('Something went wrong...')


def send_whatsapp_message(center_name, date_available):
    account_sid = param.account_sid
    auth_token = param.auth_token
    client = Client(account_sid, auth_token)
    phone_number = param.number_list
    for number in phone_number:
        client.messages.create(
            from_=f'whatsapp:{param.twilo_number}',
            body=f'Vaccine is available at {center_name} on {date_available}',
            to=f'whatsapp:{number}')
        print(f"WhatsApp notification send to {number}")





def mail_send(df_test):
    emaillist = param.user_list
    msg = MIMEMultipart()
    msg['Subject'] = f"Vaccine Alert Dated: {df_test['Date'].unique()[0]}"
    msg['From'] = "Mankamal Misra"

    html = """\
            <html>
              <head></head>
              <body>
                {0}
              </body>
            </html>
    """.format(df_test.to_html(index=False))

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    try:
        """Checking for connection errors"""

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()  # NOT NECESSARY
        server.starttls()
        server.ehlo()  # NOT NECESSARY
        server.login(param.gmail_user, param.gmail_password)
        server.sendmail(msg['From'], emaillist, msg.as_string())
        print("Mail Sent")
        server.close()

    except Exception as e:
        print("Error for connection: {}".format(e))
