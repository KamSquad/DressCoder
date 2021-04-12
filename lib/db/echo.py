from sqlalchemy.orm.exc import NoResultFound

from lib.db import base as dbm


class EchoDB(dbm.DatabaseInstance):
    def check_user_token(self, token):
        try:
            # get token permission by view
            user_role_res = self.session.query(dbm.TokenPerm).filter_by(
                token=token).one()
            # prepare result
            user_role_res_dict = dbm.make_dict_result(user_role_res)
            # remove token field
            del user_role_res_dict['token']
            # return
            return user_role_res_dict
        except NoResultFound:
            return None

