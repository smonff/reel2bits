import os

#                                 .i;;;;i.
#                               iYcviii;vXY:
#                             .YXi       .i1c.
#                            .YC.     .    in7.
#                           .vc.   ......   ;1c.
#                           i7,   ..        .;1;
#                          i7,   .. ...      .Y1i
#                         ,7v     .6MMM@;     .YX,
#                        .7;.   ..IMMMMMM1     :t7.
#                       .;Y.     ;$MMMMMM9.     :tc.
#                       vY.   .. .nMMM@MMU.      ;1v.
#                      i7i   ...  .#MM@M@C. .....:71i
#                     it:   ....   $MMM@9;.,i;;;i,;tti
#                    :t7.  .....   0MMMWv.,iii:::,,;St.
#                   .nC.   .....   IMMMQ..,::::::,.,czX.
#                  .ct:   ....... .ZMMMI..,:::::::,,:76Y.
#                  c2:   ......,i..Y$M@t..:::::::,,..inZY
#                 vov   ......:ii..c$MBc..,,,,,,,,,,..iI9i
#                i9Y   ......iii:..7@MA,..,,,,,,,,,....;AA:
#               iIS.  ......:ii::..;@MI....,............;Ez.
#              .I9.  ......:i::::...8M1..................C0z.
#             .z9;  ......:i::::,.. .i:...................zWX.
#             vbv  ......,i::::,,.      ................. :AQY
#            c6Y.  .,...,::::,,..:t0@@QY. ................ :8bi
#           :6S. ..,,...,:::,,,..EMMMMMMI. ............... .;bZ,
#          :6o,  .,,,,..:::,,,..i#MMMMMM#v.................  YW2.
#         .n8i ..,,,,,,,::,,,,.. tMMMMM@C:.................. .1Wn
#         7Uc. .:::,,,,,::,,,,..   i1t;,..................... .UEi
#         7C...::::::::::::,,,,..        ....................  vSi.
#         ;1;...,,::::::,.........       ..................    Yz:
#          v97,.........                                     .voC.
#           izAotX7777777777777777777777777777777777777777Y7n92:
#             .;CoIIIIIUAA666666699999ZZZZZZZZZZZZZZZZZZZZ6ov.
#
#                          !!! ATTENTION !!!
# DO NOT EDIT THIS FILE! THIS FILE CONTAINS THE DEFAULT VALUES FOR THE CON-
# FIGURATION! EDIT YOUR OWN CONFIG FILE (based on production.py or development.py or testing.py).
# AND DICTATE THE APP TO USE YOUR FILE WITH ENV VARIABLE:
# APP_SETTINGS='config.yourEnv.Config'
#
# Editing this file is done at your own risks, don't cry if doing that transforms your cat in an opossum.


def bool_env(var_name, default=False):
    test_val = os.getenv(var_name, default)
    if test_val in ("False", "false", "0", "no"):
        return False
    return bool(test_val)


class BaseConfig:
    """ Base configuration, pls dont edit me """

    # Debug and testing specific
    TESTING = bool_env("APP_TESTING", False)
    DEBUG = bool_env("APP_DEBUG", False)

    @property
    def TEMPLATES_AUTO_RELOAD(self):
        return self.DEBUG

    # WTForms CSRF
    WTF_CSRF_ENABLED = bool_env("APP_WTF_CSRF", True)

    # Can users register
    REGISTRATION_ENABLED = bool_env("APP_REGISTRATION", True)

    # Registration, same as upper
    @property
    def SECURITY_REGISTERABLE(self):
        return self.REGISTRATION_ENABLED

    # Secret key, you are supposed to generate one
    # Ex: `openssl rand -hex 42`
    SECRET_KEY = os.getenv("APP_SECRET_KEY", None)
    # Ex: `openssl rand -hex 5`
    SECURITY_PASSWORD_SALT = os.getenv("APP_SEC_PASS_SALT", None)

    # Database stuff
    SQLALCHEMY_DATABASE_URI = os.getenv("APP_DB_URI", "postgresql+psycopg2://postgres@localhost/reel2bits")
    SQLALCHEMY_ECHO = bool_env("APP_DB_ECHO", False)
    # Thoses two shouldn't be touched
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # Flask-Security stuff
    # Should users confirm theire email address ?
    SECURITY_CONFIRMABLE = bool_env("APP_SEC_CONFIRMABLE", True)

    # We have an alternative way
    SECURITY_RECOVERABLE = False
    # Don't change or you will break things
    SECURITY_CHANGEABLE = True
    # Same or I bite you
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = True
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = True

    # Backend default language
    BABEL_DEFAULT_LOCALE = os.getenv("APP_API_DEFAULT_LOCALE", "en")
    # Not sure this one has any effect...
    BABEL_DEFAULT_TIMEZONE = os.getenv("APP_API_DEFAULT_TIMEZONE", "UTC")

    # Uploads directories
    UPLOADS_DEFAULT_DEST = os.getenv("APP_UPLOADS_DEFAULT", "/home/reel2bits/uploads")
    UPLOADED_SOUNDS_DEST = os.getenv("APP_UPLOADS_SOUNDS", "/home/reel2bits/uploads/sounds")
    UPLOADED_WAVEFORMS_DEST = os.getenv("APP_UPLOADS_WAVEFORMS", "/home/reel2bits/uploads/waveforms")

    # Where is audiowaveform located
    AUDIOWAVEFORM_BIN = os.getenv("APP_AUDIOWAVEFORM_BIN", "/usr/local/bin/audiowaveform")

    # If using sentry
    SENTRY_DSN = os.getenv("APP_SENTRY_DSN", None)

    # Broker setup for Celery, same redis base for both
    CELERY_BROKER_URL = os.getenv("APP_CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("APP_CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

    # ActivityPub stuff
    AP_DOMAIN = os.getenv("APP_AP_DOMAIN", "localhost")
    AP_ENABLED = bool_env("APP_AP_ENABLED", False)

    @property
    def SERVER_NAME(self):
        return self.AP_DOMAIN

    @property
    def BASE_URL(self):
        return f"https://{self.AP_DOMAIN}"

    # Sources of that instance, should be your repos if forked
    SOURCES_REPOSITORY_URL = os.getenv("APP_SRCS_REPO_URL", "https://github.com/reel2bits/reel2bits")

    # Mail setup
    MAIL_SERVER = os.getenv("APP_MAIL_SERVER", "localhost")
    MAIL_PORT = os.getenv("APP_MAIL_PORT", 25)
    MAIL_USE_TLS = bool_env("APP_MAIL_USE_TLS", False)
    MAIL_USE_SSL = bool_env("APP_MAIL_USE_SSL", False)
    MAIL_USERNAME = os.getenv("APP_MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("APP_MAIL_PASSWORD", None)

    @property
    def MAIL_DEFAULT_SENDER(self):
        return os.getenv("APP_MAIL_DEFAULT_SENDER", f"postmaster@{self.AP_DOMAIN}")

    # Old stuff while we still have parts of the frontend in the backend
    SECURITY_POST_LOGIN_VIEW = "/home"
    SECURITY_POST_LOGOUT_VIEW = "/home"

    # Don't touch
    SWAGGER_UI_DOC_EXPANSION = "list"

    # Default SPA filename
    REEL2BITS_SPA_HTML = os.getenv("REEL2BITS_SPA_HTML", "../front/dist/index.html")
