import requests
import os

from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity

from db import db
from blocklist import BLOCKLIST
from schemas import PlainUserSchema
from models import UserModel


blp = Blueprint("users", __name__, description="USer End-Point")

def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    api_key = os.getenv("MAILGUN_API_KEY")
    return requests.post(
        "https://api.mailgun.net/v3/{0}/messages".format(domain),
        auth=("api", "{0}".format(api_key)),
        data={
            "from": "Excited User <mailgun@{0}>".format(domain),
            "to": [to, "YOU@{0}".format(domain)],
            "subject": subject,
            "text": body
        }
    )
@blp.route("/user")
class User(MethodView):

    @blp.response(200, PlainUserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

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
        

@blp.route("/login")
class Login(MethodView):

    @blp.arguments(PlainUserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access token": access_token,
                "refresh token": refresh_token
            }
        abort(
            401,
            message="Invalid Credentials."
        )

@blp.route("/logout")
class LogOut(MethodView):

    @jwt_required()
    @blp.response(200)
    def post(self):
        jti = get_jwt().get("jti")
        BLOCKLIST.add(jti)
        return {
            "message": "Loged Out"
        }
    
@blp.route("/refresh")
class Refresh(MethodView):

    @jwt_required()
    @blp.response(200)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {
            "access token": new_token
        }