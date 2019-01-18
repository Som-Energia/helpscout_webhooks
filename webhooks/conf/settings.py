import os

import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open(os.path.join(BASE_DIR, 'webhooks/conf/config.yaml')) as f:
    config = yaml.load(f.read())


CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']

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
        }
    },
    'loggers': {
        'energetica': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'hs_webhook': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'sanic': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
