import email
import imaplib
import base64
imap_server = "imap-mail.outlook.com"
imap_port = 993
smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
payment_dict = {"no-reply@grab.com": 1, "paylah.alert@dbs.com": 2}


def read_email_from_gmail():
    grabCount = 0
    paylahCount = 0
    mail = imaplib.IMAP4_SSL(smtp_server)
    mail.login("lancechao_94@hotmail.com", "kjL060814")
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()

    for i in reversed(id_list):
        typ, data = mail.fetch(i, '(RFC822)')
        data1 = base64.b64decode(data[0][1])

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_from = msg['from']
                email_date = msg['date']
                fromemail = ((email_from.split())[-1])[1:-1]
                #print('From : ' + fromemail + '\n')
                if (fromemail in payment_dict.keys()) and("Receipt" in email_subject):
                    print(msg)
                    print('----------------------------------------------------------')
                    print('From : ' + fromemail + '\n')
                    print('Subject : '+email_subject+'\n')
                    print('Date : ' + email_date + '\n')
                    print('----------------------------------------------------------')
                else:
                    continue


read_email_from_gmail()
