from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from db import db
from schemas import PlainUserSchema
from models import UserModel


blp = Blueprint("users", __name__, description="USer End-Point")

@blp.route("/register")
class User(MethodView):

    @blp.arguments(PlainUserSchema)
    @blp.response(200, PlainUserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(
                409,
                messgae="User already exists"
            )
        user = UserModel(**user_data)
        user.password = pbkdf2_sha256.hash(user.password)
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )

@blp.route("/user/<string:user_id>")
class UserList(MethodView):

    @blp.response(200, PlainUserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(int(user_id))
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(int(user_id))
        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": " User deleted"}, 200
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )