import sys
import json
import asyncio
import asyncpg as asyncpg

from lib import config

from lib import strings


class Database:
    """
    Interaction with postgres server
    """

    def __init__(self):
        self.conf = config.JsonConfig('./config.json')
        self.conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self.close()
        except:
            pass

    async def close(self):
        await self.conn.close()

    def get_request(self, request, args=None):
        async def run():
            conn = await asyncpg.connect(user=self.conf.value['db']['db_user'],
                                         password=self.conf.value['db']['db_pass'],
                                         database=self.conf.value['db']['db_name'],
                                         host=self.conf.value['db']['host'])
            value = await conn.fetch(request, *args)
            return value

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(run())
        return result

    def insert_request(self, request, args=None):
        async def run():
            conn = await asyncpg.connect(user=self.conf.value['db']['db_user'],
                                         password=self.conf.value['db']['db_pass'],
                                         database=self.conf.value['db']['db_name'],
                                         host=self.conf.value['db']['host'])

            await conn.execute(request, *args)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(run())

    def check_user_token(self, user_token):
        cmd_str = strings.check_token_cmd
        db_res = self.get_request(request=cmd_str,
                                  args=[user_token])
        if len(db_res):
            if db_res[0][0]:
                res_keys = strings.token_result_keys
                res_values = list(db_res[0][0])
                db_res_dict = dict(zip(res_keys, res_values))
                db_res_dict_str = json.dumps(db_res_dict)
                return db_res_dict_str
        return None

    '''
    def check_user_exist(self, user_name):
        # cmd_str = "SELECT id FROM user_login WHERE username=$1"
        cmd_str = strings.check_user_exist_cmd
        db_res = self.get_request(request=cmd_str,
                                  args=[user_name])
        if db_res:
            if db_res[0][0]:
                return db_res[0][0]
        return None

    def check_user_hash_pass(self, user_name, inp_hash_pass):
        user_id = self.check_user_exist(user_name)
        cmd_str = strings.check_user_hash_pass_cmd
        if user_id:
            pass_query = self.get_request(request=cmd_str,
                                          args=[user_id])
            pass_query = pass_query[0][0]
            pass_crypted = pass_query[0]
            pass_clear = crypt_pass.decrypt_password(pass_crypted)
            db_pass_hash = creds.gen_md5(pass_clear + pass_query[1])
            return db_pass_hash == inp_hash_pass
        else:
            return False

    def gen_and_save_token(self, user_name):
        user_id = self.check_user_exist(user_name)
        if user_id:
            user_token = lib.creds.gen_uid()
            cmd_str = strings.gen_and_save_token_cmd
            self.insert_request(request=cmd_str,
                                args=[user_id, user_token])
            return user_token
        return False
    '''


if __name__ == '__main__':
    with Database() as db:
        token = sys.argv[1]
        user_perm = db.check_user_token(user_token=token)
        print()
