from app.models.base_model import BaseModel
from app.models.user import User
from app import db

# Tabla intermedia Place <-> Amenity
place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    """Place entity class."""

    __tablename__ = 'places'

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # FOREIGNKEY
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relaciones ORM automáticas
    reviews = db.relationship('Review', backref='place', lazy=True)  # One-to-Many
    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        backref=db.backref('places', lazy=True),
        lazy='subquery'
    )

    def __init__(self, title: str, description: str, price: float, latitude: float, longitude: float, owner: User, user_id: str):
        super().__init__()  # hereda id, created_at, updated_at
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.user_id = user_id

    # Validaciones
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value:
            raise ValueError("Title cannot be empty")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Description must be a non-empty string.")
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Price must be a non-negative number.")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90.")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180.")
        self._longitude = float(value)

    # Métodos auxiliares
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        if review not in self.reviews:
            self.reviews.append(review)

    def __repr__(self):
        return f"<Place {self.title} - Ubicación: {self.latitude}, {self.longitude}>"
