from flask_restful import  reqparse


class UserInputAdapter():
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    COMPANY_NAME = 'company_name'
    CITY = 'city'
    STATE = 'state'
    ZIP = 'zip'
    EMAIL = 'email'
    WEB = 'web'
    AGE = 'age'

    def parse(self):
        parser = reqparse.RequestParser()
        parser.add_argument(self.FIRST_NAME, required=False, type=str)
        parser.add_argument(self.LAST_NAME, required=False, type=str)
        parser.add_argument(self.COMPANY_NAME, required=False, type=str)
        parser.add_argument(self.CITY, required=False, type=str)
        parser.add_argument(self.STATE, required=False, type=str)
        parser.add_argument(self.ZIP, required=False, type=int)
        parser.add_argument(self.EMAIL, required=False, type=str)
        parser.add_argument(self.WEB, required=False, type=str)
        parser.add_argument(self.AGE, required=False, type=int)
        return parser.parse_args()


class BaseInputAdapter():

    LIMIT = 'limit'
    OFFSET = 'offset'
    NAME = 'name'
    SORT = 'sort'

    def parse_limit_offset(self):
        parser = reqparse.RequestParser()

        parser.add_argument(self.LIMIT, required=False, type=str, default=10)
        parser.add_argument(self.OFFSET, required=False, type=str, default=0)
        parser.add_argument(self.NAME, required=False, type=str)
        parser.add_argument(self.SORT, required=False, type=str)

        return parser.parse_args()
