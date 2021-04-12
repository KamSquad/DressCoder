import sys

import f_modules as fm
from lib.db import echo
from lib import config

conf = config.JsonConfig('../config.json')
ldb = echo.EchoDB(db_host=conf.value['db']['host'],
                  db_name=conf.value['db']['db_name'],
                  db_user=conf.value['db']['db_user'],
                  db_pass=conf.value['db']['db_pass'])
token = sys.argv[1]
request = {'request': 'auth', 'body': token}


result = fm.user_token_check_func(request, ldb)
print(result)
