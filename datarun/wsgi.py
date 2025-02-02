"""
WSGI config for datarun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

working_env = os.environ.get('DR_WORKING_ENV', 'PROD')

if working_env == 'DEV':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datarun.settings")

    application = get_wsgi_application()
else:
    os.environ["DJANGO_SETTINGS_MODULE"] = "datarun.settings"

    env_variables_to_pass = ['DR_DATABASE_NAME', 'DR_DATABASE_USER',
                             'DR_DATABASE_PASSWORD', 'DIR_DATA',
                             'DIR_SUBMISSION', 'USER_LOGIN', 'USER_PSWD',
                             'CELERY_SCHEDULER_PERIOD', 'NB_LOCAL_WORKER',
                             'DR_EMAIL', 'RMQ_VHOST', 'IP_MASTER',]

    def loading_app(environ, start_response):
        global real_app

        # pass the WSGI environment variables on through to os.environ
        for var in env_variables_to_pass:
            os.environ[var] = environ.get(var, '')
        real_app = get_wsgi_application()
        return real_app(environ, start_response)

    real_app = loading_app
    application = lambda env, start: real_app(env, start)
