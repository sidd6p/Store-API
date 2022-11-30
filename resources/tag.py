
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import TagSchema, PlainTagSchema
from models import TagModel, StoreModel


blp = Blueprint("tags", __name__, description="Tags End-Point")


@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):

    @blp.response(200, PlainTagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(int(store_id))
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == int(store_id), TagModel.name == tag_data["name"]).first():
            abort(
                400,
                "Tag already exists"
            )
        tag = TagModel(**tag_data, store_id=int(store_id))
        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError as error:
            abort(
                500,
                str(error)
            )

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(int(tag_id))
        return tag