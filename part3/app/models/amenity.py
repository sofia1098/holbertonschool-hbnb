from app.models.base_model import BaseModel
from app import db
from app.models.place import place_amenity

class Amenity(BaseModel):
    """Amenity entity class."""

    __tablename__ = 'amenities'

    _name = db.Column('name', db.String(50), nullable=False)

    # Relaciones ORM
    places = db.relationship(
        'Place',
        secondary=place_amenity,
        backref=db.backref('amenities', lazy=True),
        lazy='subquery'
    )

    # Getter y setter con validación
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Name must be between 1 and 50 characters.")
        self._name = value

    # Métodos
    def edit_amenity(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key) and key != "id":
                setattr(self, key, value)
        self.save()  # Actualiza updated_at

    def __repr__(self):
        return f"<Amenity {self.name}>"
