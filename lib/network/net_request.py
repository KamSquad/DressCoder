answer_codes = {'success': 200,  # OK. Успешный запрос.
                                 # Ответ в виде успешного запроса.
                'object_created': 201,  # Успешный запрос. Был создан объект.
                                        # Используется, если были проведены действия на стороне сервера(добавлен объект)
                'failed': 400,  # Запрос отклонен. Запрос отклонен по причине какой-то ошибки. Смотри тело ответа.
                'login_failed': 401,  # Ошибка авторизации. Если авториз. провален.
                                      # Актуально при проверке токенов.
                'bad_url': 404,  # Ошибка написания URL. Такого адреса не существует. Если указал неправильный адрес.
                }


def make_answer_json(answer_code, body):
    ans_json = {'code': answer_code,
                'body': body}  # form answer as json
    return ans_json
