"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = 'cities'

    code = db.Column(
        db.Text,
        primary_key=True,)

    name = db.Column(
        db.Text,
        nullable=False,)

    state = db.Column(
        db.String(2),
        nullable=False,)


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = 'cafes'

    id = db.Column(
        db.Integer,
        primary_key=True,)

    name = db.Column(
        db.Text,
        nullable=False,)

    description = db.Column(
        db.Text,
        nullable=False,)

    url = db.Column(
        db.Text,
        nullable=False,)

    address = db.Column(
        db.Text,
        nullable=False,)

    city_code = db.Column(
        db.Text,
        db.ForeignKey('cities.code'),
        nullable=False,)

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",)

    city = db.relationship("City", backref='cafes')

    # Cafe -> [User, User]
    # liking_users (relationship created in User with backref)

    def __repr__(self):
        return f'<Cafe id={self.id} name="{self.name}">'

    def get_city_state(self):
        """Return 'city, state' for cafe."""

        city = self.city
        return f'{city.name}, {city.state}'




class User(db.Model):
    """User information."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,)

    username = db.Column(
                db.Text,
                unique=True,
                nullable=False,)

    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False,)

    email = db.Column(
            db.Text,
            nullable=True,)

    first_name = db.Column(
                 db.String(30),
                 nullable=False,)

    last_name = db.Column(
                 db.String(40),
                 nullable=False,)

    description = db.Column(
                  db.Text,
                  nullable=True,)

    image_url = db.Column(
                db.Text,
                nullable=False,
                default="/static/images/default-pic.png",)

    hashed_password = db.Column(
                      db.Text,
                      nullable=False,)

    def get_full_name(self):
        '''Return a string of "FIRSTNAME LASTNAME'''

        return f'{self.first_name} {self.last_name}'

    # User -> [Cafe, Cafe]
    liked_cafes = db.relationship('Cafe',
                            secondary='likes',
                            backref='liking_users')

    @classmethod
    def register(cls,
                 username,
                 email,
                 first_name,
                 last_name,
                 description,
                 password,
                 image_url=None,
                 admin=None):
        """Register user and hash password"""

        hashed_password = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            image_url=image_url,
            hashed_password=hashed_password,
            admin=admin)

    @classmethod
    def authenticate(cls, username, password):
        '''Validate that user exists and password is correct.
           Return user if valid, else, return False.
        '''

        u = cls.query.filter_by(username=username).one_or_none()

        if u and bcrypt.check_password_hash(u.hashed_password, password):
            #return user instance
            return u
        else:
            return False

class Like(db.Model):
    """Like information for user and cafe likes."""

    __tablename__ = 'likes'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        primary_key=True,)

    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey("cafes.id"),
        nullable=False,
        primary_key=True,)



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)


