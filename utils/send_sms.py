from twilio.rest import Client
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send_sms(to_number, message):
    account_sid = ''
    auth_token = ''
    from_number = '+14122748433'
    if len(to_number) > 10:
        to_number = to_number[-10:]
    logger.info('{} : {}'.format(to_number, message))
    try:
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
    except:
        return


def send_msg(to_number, messages):
    account_sid = ''
    auth_token = ''
    from_number = '+14122748433'

    client = Client(account_sid, auth_token)
    count = 0
    for message in messages:
        try:
            if count == 5:
                break
            if message.get('buttons'):
                body = message['title'] + '\n' + message['subtitle'] + message['buttons'][0]['postback']
            else:
                body = message['title'] + '\n' + message['subtitle']
            if count == 0:
                send_sms(to_number, body)

            message = client.messages.create(
                media_url=message['image_url'],
                body='',
                from_=from_number,
                to=to_number
            )
            count += 1

            logger.info(message)
        except Exception as e:
            logger.info(e)
            continue


def reminder(to_number, message):
    time.sleep(120)
    send_sms(to_number, message)
