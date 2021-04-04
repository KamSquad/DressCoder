from sqlalchemy.orm.exc import NoResultFound

from lib.db import base as dbm


class EchoDB(dbm.DatabaseInstance):
    def check_user_token(self, token):
        try:
            # get user id
            user_auth_res = self.session.query(dbm.UserAuth).filter_by(
                token=token).one()
            # get user role
            user_login_res = self.session.query(dbm.UserLogin).filter_by(
                user_id=user_auth_res.user_id).one()
            # get user role table
            user_role_res = self.session.query(dbm.UserRole).filter_by(
                role_id=user_login_res.role_id).one()
            user_role_res_dict = user_role_res.__dict__
            del user_role_res_dict['_sa_instance_state']
            return user_role_res_dict
        except NoResultFound:
            return None

