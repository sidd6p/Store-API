from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    description = db.Column(db.String(200))

    store = db.relationship("StoreModel", back_populates="item")
    tags = db.relationship(
        "TagModel", back_populates="items", secondary="tags_in_items"
    )
