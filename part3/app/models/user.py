from datetime import datetime
from app import db, bcrypt
from app.models.base_model import BaseModel

class User(BaseModel):
    """User entity class."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password = db.Column("password", db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relaciones
    places = db.relationship('Place', backref='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', cascade='all, delete-orphan')

    # Propiedades
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = bcrypt.generate_password_hash(new_password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        self.validate()

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} ({self.email})>"
