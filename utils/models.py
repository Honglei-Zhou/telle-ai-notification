import sqlalchemy_jsonfield
import ujson
import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from database.db_instance import Base, TelleModelMixin


class Message(Base, TelleModelMixin):

    __tablename__ = 'telle_message'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String(80), nullable=True)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    session_id = Column(String(120), nullable=False)
    direction = Column(String(20), nullable=False)
    message = Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )

    dialogflow_resp = Column(
        sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False,
            json=ujson
        ),
        nullable=True
    )
    is_read = Column(Integer)
    from_bot = Column(Integer)
    message_owner = Column(String(80), nullable=True)

    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)

    def __repr__(self):
        return '<Message %r>' % self.id


class Recipients(Base, TelleModelMixin):

    __tablename__ = 'telle_recipients'

    id = Column(Integer, primary_key=True)
    recipient_name = Column(String(80), nullable=True)

    dealer_id = Column(String(100))
    dealer_name = Column(Text)

    email = Column(String(50))
    phone = Column(String(50))

    department = Column(String(50))

    notification = Column(Integer, default=0)

    deleted = Column(Integer, default=0)

    created_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, **kwargs):
        super(Recipients, self).__init__(**kwargs)

    def __repr__(self):
        return '<Recipients %r>' % self.id
