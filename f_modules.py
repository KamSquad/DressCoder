from schema import Schema, And, Use

from lib.network import net_request


def test_func(*args):
    result = net_request.make_answer_json(answer_code=net_request.answer_codes['success'],
                                          body='ping: ok')
    return result


def user_token_check_func(*args):
    request_json, ldb = args
    user_token = ldb.check_user_token(token=request_json['body'])
    if user_token:
        result = net_request.make_answer_json(answer_code=net_request.answer_codes['success'],
                                              body=user_token)
    else:
        result = net_request.make_answer_json(answer_code=net_request.answer_codes['login_failed'],
                                              body='auth token invalid')
    return result


routes = {'test': test_func,
          'auth': user_token_check_func}


schemas = {'test': Schema({'request': 'test'}),
           'auth': Schema({'request': 'auth',
                           'body': And(Use(str))
                           })
           }
