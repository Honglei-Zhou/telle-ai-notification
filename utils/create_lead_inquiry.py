from .send_email import send_email
import json
from .create_email_body import create_email_body
from .models import Message, Recipients
from sqlalchemy import desc
from .tools import utc_to_local
from database.db_instance import session_scope


def create_lead_inquiry(data):
    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')
    customer_name = message.get('customer', 'customer')
    email = message.get('email', '')
    phone = message.get('phone', '')

    department = message.get('department', 'sales')

    session_id = message.get('sessionId', '')

    notes_offer = message.get('note', '')
    title = message.get('title', '')

    vin = message.get('vin', '')
    stock = message.get('stock', '')

    notes_offer = '{} Inquiry: {} vin# {} stock# {}'.format(notes_offer, title, vin, stock)
    with session_scope() as session:
        messages = session.query(Message).filter(Message.session_id == session_id, Message.dealer_id == dealer_id).order_by(
            desc(Message.id)).all()

        body = notes_offer

        for message in messages:
            content = json.loads(message.message)
            if message.direction == 'incoming':
                content = content['data']['text']
                body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                message.message_owner, content)

            else:
                for d in content:
                    if 'text' in d:
                        body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                        message.message_owner, d['text']['text'][0])
                    elif 'quickReplies' in d:
                        body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                        message.message_owner, d['quickReplies']['title'])
                    else:
                        body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                        message.message_owner, 'multimedia message')

        if phone == '8008008000':
            phone = ''
            new_body = create_email_body(session_id, customer_name, email, '', body)
        elif email == 'default@telle.ai':
            email = ''
            new_body = create_email_body(session_id, customer_name, '', phone, body)
        else:
            new_body = create_email_body(session_id, customer_name, email, phone, body)

        recipients = session.query(Recipients).filter(Recipients.dealer_id == dealer_id,
                                                      Recipients.department.ilike('%{}%'.format(department))).all()
        # emails = []
        #
        # dealer_name = 'Telle AI Bot'
        #
        # for recipient in recipients:
        #     emails.append(recipient.email)
        #     if recipient.dealer_name:
        #         dealer_name = recipient.dealer_name
        #
        # if len(emails) > 0:
        #     send_email(emails, 'Message details - {}'.format(dealer_name), body=new_body)
        #
        # send_email(['hzhou@blissmotors.com', 'raffayhussain@blissmotors.com'],
        #            'Message details - {}'.format(dealer_name), body=new_body)
        emails = []
        crm_recipients = []

        dealer_name = 'Telle AI Bot'

        for recipient in recipients:
            if recipient.notification == 1:
                emails.append(recipient.email)
            elif recipient.notification == 2:
                crm_recipients.append(recipient.email)
            if recipient.dealer_name:
                dealer_name = recipient.dealer_name

        if len(crm_recipients) > 0:
            send_email(crm_recipients, 'Message details - {}'.format(dealer_name), body=new_body)

        email_body = '''
                        customer: {}
                        email: {}
                        phone number: {}
                        {}
                    '''.format(customer_name, email, phone, body)

        if len(emails) > 0:

            send_email(emails, 'Message details - {}'.format(dealer_name),
                       body=email_body, bcc=['hzhou@blissmotors.com', 'raffayhussain@blissmotors.com'])
        else:
            send_email(['hzhou@blissmotors.com', 'raffayhussain@blissmotors.com'],
                       'Message details - {}'.format(dealer_name), body=email_body)
