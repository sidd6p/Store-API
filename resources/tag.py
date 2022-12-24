from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db
from schemas import TagSchema, PlainTagSchema, TagAndItemSchema
from models import TagModel, StoreModel, ItemModel


blp = Blueprint("tags", __name__, description="Tags End-Point")


@blp.route("/store/<string:store_id>/tag")
class TagAndStore(MethodView):
    @blp.response(200, PlainTagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(int(store_id))
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(
            TagModel.store_id == int(store_id), TagModel.name == tag_data["name"]
        ).first():
            abort(400, "Tag already exists")
        tag = TagModel(**tag_data, store_id=int(store_id))
        try:
            db.session.add(tag)
            db.session.commit()
            return tag
        except SQLAlchemyError as error:
            abort(500, str(error))


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(int(tag_id))
        return tag

    @blp.response(
        200,
        description="Delete tag if no item is linked to it",
        example={"message", "Tag deleted"},
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400,
        description="Item/s linked to this tag exists",
        example={"message": "item/s linked to this tag exists"},
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(int(tag_id))
        if not tag.items:
            try:
                db.session.delete(tag)
                db.session.commit()
            except SQLAlchemyError as error:
                abort(500, str(error))
            return {"message": "Tag deleted"}
        abort(400, message="item/s linked to this tag exists")


@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class TagAndItem(MethodView):
    @blp.response(200, TagSchema)
    def post(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(int(tag_id))
        item = ItemModel.query.get_or_404(int(item_id))
        print(tag.store_id == item.store_id)
        if tag.store_id == item.store_id:
            try:
                item.tags.append(tag)
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError as error:
                abort(500, str(error))
            return tag
        abort(404, message="Not same store")

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        tag = TagModel.query.get_or_404(int(tag_id))
        item = ItemModel.query.get_or_404(int(item_id))
        try:
            item.tags.remove(tag)
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as error:
            abort(500, str(error))
        return {"message": "Item and tag un-linked", tag: tag, item: item}
