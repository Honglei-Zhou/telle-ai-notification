username = 'postgres'
password = 'cognitiveati'
host = 'telle-ai-database.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432
prod_db = 'telle_ai_prod'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, prod_db)

redis_host = 'telle-redis.telle.production'
# redis_host = 'redis'

redis_port = 6379

thread_number = 2

mail_settings = {
    "MAIL_SERVER": 'smtp.zoho.com',
    "MAIL_PORT": 587,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": 'noreply@telle.ai',
    "MAIL_PASSWORD": 'blissmotors'
}
