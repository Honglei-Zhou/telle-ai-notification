from .send_email import send_email
import json
from .create_appt_email_body import create_appt_email_body
from .models import Message, Recipients
from sqlalchemy import desc
from .tools import utc_to_local
from database.db_instance import session_scope


def create_appt_intent(data):
    message = data['message']
    dealer_id = message.get('dealerId', '2019123456001')

    department = message.get('department', 'sales')

    session_id = message.get('sessionId', '')

    with session_scope() as session:

        messages = session.query(Message).filter_by(session_id=session_id, dealer_id=dealer_id).order_by(desc(Message.id)).all()

        body = ''

        for message in messages:

            content = json.loads(message.message)
            if message.direction == 'incoming':
                content = content['data']['text']
                body += '[{}] {}\t {}\n'.format(utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                                                message.message_owner, content)
            else:
                for d in content:
                    if 'text' in d:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, d['text']['text'][0])
                    elif 'quickReplies' in d:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, d['quickReplies']['title'])
                    else:
                        body += '[{}] {}\t {}\n'.format(
                            utc_to_local(message.created_time).strftime("%Y-%m-%d %I:%M %p"),
                            message.message_owner, 'multimedia message')

        new_body = create_appt_email_body(data, body)

        recipients = session.query(Recipients).filter(Recipients.dealer_id == dealer_id,
                                                      Recipients.department.ilike('%{}%'.format(department))).all()
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
                        Vehicle Year: {}
                        VehicleMake:  {}
                        VehicleModel: {}
                        VehicleDrivetrain: {}
                        VehicleType:  {}
                        VehicleInteriorColor: {}
                        VehicleColor: {}
                        VehicleFeatures: {}
                        customer: {}
                        email: {}
                        phone number: {}
                        {}
                        '''.format(data.get('VehicleYear', 'any'),
                                   data.get('VehicleMake', 'any'),
                                   data.get('VehicleModel', 'any'),
                                   data.get('VehicleDrivetrain', 'any'),
                                   data.get('VehicleType', 'any'),
                                   data.get('VehicleInteriorColor', 'any'),
                                   data.get('VehicleColor', 'any'),
                                   data.get('VehicleFeatures', 'any'),
                                   data.get('person', 'customer'),
                                   data.get('email', 'NA'),
                                   data.get('phone-number', 'NA'),
                                   body)

        if len(emails) > 0:

            send_email(emails, 'Message details - {}'.format(dealer_name),
                       body=email_body, bcc=['hzhou@blissmotors.com', 'raffayhussain@blissmotors.com'])
        else:
            send_email(['hzhou@blissmotors.com', 'raffayhussain@blissmotors.com'],
                       'Message details - {}'.format(dealer_name), body=email_body)
