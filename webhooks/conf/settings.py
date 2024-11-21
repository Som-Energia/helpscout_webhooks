import os

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, 'webhooks/conf/config.yaml')) as f:
    config = yaml.load(f.read(), Loader=yaml.FullLoader)

SCOUTS = config['scouts']

#freescout
FREESCOUT_HOST = config['freescout']['host']
FREESCOUT_API_KEY = config['freescout']['api_key']
FREESCOUT_ADMIN_USER_ID = config['freescout']['admin_user_id']
FREESCOUT_WEBHOOK_SIGNATURE = config['freescout']['webhook_signature']
FREESCOUT_SECRET_KEY = config['freescout']['secret_key']

#helpscout
HELPSCOUT_HOST = config['helpscout']['host']

CLIENT_ID = config['helpscout']['client_id']
CLIENT_SECRET = config['helpscout']['client_secret']

SECRET_KEY = config['helpscout']['secret_key']
HELPSCOUT_WEBHOOK_SIGNATURE = config['helpscout']['webhook_signature']

DATABASE = {
    'database': config['database']['name'],
    'host': config['database']['host'],
    'port': config['database']['port'],
    'user': config['database']['user'],
    'password': config['database']['password']
}

SQL = {
    'energetica_emails': config['sql']['energetica_emails']
}

DOMAIN_EXCEPTION = config['domain_exception']

TOKEN_TIME_REFRESH = 110

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(funcName)s %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(process)d] [%(levelname)s]'
                      '[%(module)s.%(funcName)s:%(lineno)s] %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'log/hp_webhook.log',
            'when': 'midnight',
            'backupCount': 7
        }
    },
    'loggers': {
        'energetica': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'scout_webhook': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'sanic': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
