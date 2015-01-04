import datetime
# mongodb settings
DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = 'wang_fm'
TEST_DB_NAME = 'test_wang_fm'

# app secret key
# use this to generate
# >>> import os
# >>> os.urandom(24)
SECRET_KEY = '\x0f\x18\xb5\xeeP6\x84\xd5\x1b\x1b\xe7"\x98\xb8XV\x80M\xd50\xabO-\x85'
# admin
ADMIN_NAME = 'admin'
ADMIN_PASSWORD = 'admin'

# crawler settings
DOUBAN_USER_NAME = 'admin@doufm.info'
DOUBAN_USER_PASSWORD = '7MRrbGozZkrx'

# oatuh
APP_ID = 'doufm_appid'
APP_SECRET = 'c2cc7f9542e61b7e61d7'
REDIRECT_URL = 'http://115.29.140.122:5001/api/oauth/access/'
SERVER_URL = 'http://dev.xidian.me/'
GET_REQUEST_URL = SERVER_URL + 'appauth.php?ac=getRequest_token&app_id=%s&app_secret=%s'
GET_ACCESS_URL = SERVER_URL + 'appauth.php?ac=getAccess_token&request_token=%s&app_id=%s&app_secret=%s'
GET_LOGIN_USER_ID_URL =SERVER_URL + 'appauth.php?ac=getUser&access_token=%s&app_id=%s&app_secret=%s'
AUTHORIZE_URL = SERVER_URL + 'appauth.php?ac=authorize&request_token=%s&redirect_url=%s'
APP_AUTH_URL = SERVER_URL + 'appauth.php?mod=applogin&key=a4b9602e099ce418dcfe&username=%s&password=%s'

#session
PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours = 30 * 24)
SESSION_REFRESH_EACH_REQUEST = False

