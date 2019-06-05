from flask import Flask, request
from database import MYSQL
import json
from flask_restful import Api
from flask_restful import Resource
from api.input_adapters import UserInputAdapter, BaseInputAdapter
from werkzeug.exceptions import BadRequest
from api.output_adapters import UserOutputAdapter
from sqlalchemy import Integer, Column, String, or_, desc
from api.user_details import users


app = Flask(__name__)
db = MYSQL().load(app)


class Users(db.Model):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    company_name = Column(String(255))
    age = Column(Integer)
    city = Column(String(255))
    state = Column(String(255))
    zip = Column(Integer)
    email = Column(String(255))
    web = Column(String(255))


class UserRepository():

    def add_user(self, parsed_user):
        new_user = Users()
        new_user.first_name = self.check_parameter(parsed_user[UserInputAdapter.FIRST_NAME])
        new_user.last_name = self.check_parameter(parsed_user[UserInputAdapter.LAST_NAME])
        new_user.company_name = self.check_parameter(parsed_user[UserInputAdapter.COMPANY_NAME])
        new_user.age = self.check_parameter(parsed_user[UserInputAdapter.AGE])
        new_user.city = self.check_parameter(parsed_user[UserInputAdapter.CITY])
        new_user.state = self.check_parameter(parsed_user[UserInputAdapter.STATE])
        new_user.zip = self.check_parameter(parsed_user[UserInputAdapter.ZIP])
        new_user.email = self.check_parameter(parsed_user[UserInputAdapter.EMAIL])
        new_user.web = self.check_parameter(parsed_user[UserInputAdapter.WEB])


        try:
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()
        return new_user

    def check_parameter(self, parameter):
        if parameter:
            return parameter
        raise BadRequest("Please Enter all the details ")

    def get_users(self, limit=10, offset=0, name=None, sort=None):
        users = db.session.query(Users)
        if name:
            users = users.filter(or_(Users.first_name.contains(name), Users.last_name.contains(name)))
        if sort and sort[len(sort)-1] == '~':

            users = users.order_by(desc(sort[:len(sort)-1]))
        else:
            users = users.order_by(sort)
        users = users.limit(limit).offset(offset).all()
        result = []
        if users:
            for user in users:
                result.append(user)
            return result
        raise BadRequest("NO record available")

    def add_users_by_dict(self, users):
        count = 0
        for user in users:
            new_user = Users()
            new_user.first_name = user['first_name']
            new_user.last_name = user['last_name']
            new_user.company_name = user['company_name']
            new_user.age = user['age']
            new_user.city = user['city']
            new_user.state = user['state']
            new_user.zip = user['zip']
            new_user.email = user['email']
            new_user.web = user['web']

            try:
                db.session.add(new_user)
                db.session.commit()
                count += 1
            except:
                db.session.rollback()
        if count >= 50:
            return count
        raise BadRequest("No user Added")

    def get_user_by_id(self, user_id):
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if user:
            return user
        raise BadRequest("user not available ")

    def update_user(self, user_id, parsed_user):
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if user:
            user.first_name = parsed_user[UserInputAdapter.FIRST_NAME]
            user.last_name = parsed_user[UserInputAdapter.LAST_NAME]
            user.company_name = parsed_user[UserInputAdapter.COMPANY_NAME]
            user.age = parsed_user[UserInputAdapter.AGE]
            user.city = parsed_user[UserInputAdapter.CITY]
            user.state = parsed_user[UserInputAdapter.STATE]
            user.zip = parsed_user[UserInputAdapter.ZIP]
            user.email = parsed_user[UserInputAdapter.EMAIL]
            user.web = parsed_user[UserInputAdapter.WEB]

            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
            return user

    def delete_user(self, user_id):
        user = db.session.query(Users).filter(Users.id == user_id).first()
        if user:
            try:
                db.session.delete(user)
                db.session.commit()
            except:
                db.session.rollback()
            return user
        raise BadRequest("User NOt Deleted")


class User(Resource):

    def post(self):
        parsed_user = UserInputAdapter().parse()
        user = UserRepository().add_user(parsed_user)
        if user:
            return UserOutputAdapter().parse(user)
        raise BadRequest("User not Added ")

    def get(self):
        parsed_request = BaseInputAdapter().parse_limit_offset()
        users = UserRepository().get_users(parsed_request[BaseInputAdapter.LIMIT], parsed_request[BaseInputAdapter.OFFSET], parsed_request[BaseInputAdapter.NAME], parsed_request[BaseInputAdapter.SORT])
        if users:
            result = []
            for user in users:
                result.append(UserOutputAdapter().parse(user))
            return result
        raise BadRequest("No user Found ")


class AddUsers(Resource):

    def post(self):
        new_users = UserRepository().add_users_by_dict(users)
        if new_users:
            return "Users Added To Database"
        raise BadRequest("Error in adding Users")


class UserId(Resource):
    def get(self, user_id):
        user = UserRepository().get_user_by_id(user_id)
        if user:
            return UserOutputAdapter().parse(user)
        raise BadRequest("No User Found")

    def put(self, user_id):
        parsed_user = UserInputAdapter().parse()
        user = UserRepository().update_user(user_id, parsed_user)
        if user:
            return UserOutputAdapter().parse(user)
        raise BadRequest("Error Occurred")

    def delete(self, user_id):
        user = UserRepository().delete_user(user_id)
        if user:
            return {
                "message": "User Deleted Successfully"
            }
        raise BadRequest("Error Occurred")


class Routes():

    def __init__(self, a):
        self.api = Api(a)

    def load(self):
        self.api.add_resource(User, '/api/users')
        self.api.add_resource(AddUsers, '/api/add_users')
        self.api.add_resource(UserId, '/api/users/<user_id>')


routes = Routes(app)
routes.load()


@app.after_request
def parse(response):
    try:
        if response.get_data():
            data = json.loads(response.get_data())
            if not (type(data)) is dict or type(data) is list:
                response.set_data(json.dumps({'message':data}))
            elif 'message' in data:
                response.set_data(json.dumps(data))
            else:
                response.set_data(json.dumps({'data':data}))
                if response.status_code == 200 and (request.method == 'POST'):
                    response.status_code = 201

            return response

    except:
        return response
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8081)


