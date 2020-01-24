import email
import imaplib
import os
import html2text
import time
from lxml import etree
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
detach_dir = 'locationWhereYouWantToSaveYourAttachments'


def get_body(email_message):
    for payload in email_message.get_payload():
        break
    return payload.get_payload()

def two_way_email(server,uname,pwd):
    username = uname
    password = pwd
    mail = imaplib.IMAP4_SSL(server)
    mail.login(username, password)
    mail.select("inbox")
    try:
        result, data = mail.search(None, 'ALL')
        inbox_item_list = data[0].split()
        for i in reversed(inbox_item_list):
            result2, email_data = mail.fetch(i, '(RFC822)')
            raw_email = email_data[0][1].decode("UTF-8")
            email_message = email.message_from_string(raw_email)
            if('Receipt' in email_message['Subject']):
                if email_message.is_multipart():
                    for payload in email_message.get_payload():
                        print('To:\t\t', email_message['To'])
                        print('From:\t',     email_message['From'])
                        print('Subject:', email_message['Subject'])
                        print('Date:\t',email_message['Date'])
                        for part in email_message.walk():
                            if (part.get_content_type() == 'text/plain'):
                                continue
                            elif(part.get_content_type()=='text/html'):
                                #print('Body2:\t',part.get_content_type())
                                #print('Body2:\t',part.get_payload(None,True))
                                #print(part.get_payload(None,True).decode("utf-8"))
                                strHTML = part.get_payload(None,True).decode("utf-8")
                                #print(strHTML.find('TOTAL'))
                                #print(strHTML)
                                dom = etree.HTML(strHTML)
                                a_tag_text = dom.xpath('body/table/tr/td/table/tr/td/table[2]/tr/td[2]/table/tr[4]/td/table[1]/tr/td/span/text()')
                                print(a_tag_text[0])

                        break
                else:
                    print('To:\t\t', email_message['To'])
                    print('From:\t', email_message['From'])
                    print('Subject:', email_message['Subject'])
                    print('Date:\t', email_message['Date'])
                    print('Thread-Index:\t', email_message['Thread-Index'])
                    text = f"{email_message.get_payload(decode=True)}"
                    html = text.replace("b'", "")
                    h = html2text.HTML2Text()
                    h.ignore_links = True
                    output = (h.handle(f'''{html}''').replace("\\r\\n", ""))
                    output = output.replace("'", "")
                    print(output)

    except IndexError:
        print("No new email")
while True:
    two_way_email("smtp-mail.outlook.com", "lancechao_94@hotmail.com", "kjL060814")
    time.sleep(10)