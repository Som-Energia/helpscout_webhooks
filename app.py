
from sanic import Sanic

from energetica.labeler import labeler

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
        'sanic': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}

# logging.config.dictConfig(LOGGING)

app = Sanic(log_config=LOGGING)

app.blueprint(labeler)

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
