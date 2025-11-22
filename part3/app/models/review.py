from app.models.base_model import BaseModel
from app import db

class Review(BaseModel):
    """Review entity class."""

    __tablename__ = 'reviews'

    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relaciones ORM usando strings
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))

    # Validación
    def set_rating(self, value):
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = value

    def set_text(self, value):
        if not value:
            raise ValueError("Text cannot be empty.")
        self.text = value

    # Método para editar review
    def edit_review(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ["id", "user_id", "place_id"]:
                setattr(self, key, value)
        self.save()

    def __repr__(self):
        return f"<Review {self.rating}/5 by {self.user.first_name} for {self.place.title}>"
