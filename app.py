"""Flask App for Flask Cafe."""

from flask import Flask, render_template, redirect, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
import os
from forms import AddCafeForm, SignupForm, LoginForm, ProfileEditForm

from models import db, connect_db, Cafe, City, User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskcafe'
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "shhhh")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)

#######################################
# auth & auth routes

CURR_USER_KEY = "curr_user"
NOT_LOGGED_IN_MSG = "You are not logged in."


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#######################################
# homepage

@app.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


#######################################
# cafes


@app.get('/cafes')
def cafe_list():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by('name').all()

    return render_template(
        'cafe/list.html',
        cafes=cafes,
    )


@app.get('/cafes/<int:cafe_id>')
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)


    # city_codes = [(c.city_code) for c in Cafe.query.all()]

    return render_template(
        'cafe/detail.html',
        cafe=cafe,
    )

@app.route('/cafes/add', methods=["GET", "POST"])
def add_cafe():
    '''Show add cafe form and handle adding'''

    form = AddCafeForm()
    city_codes = [(c.code, c.name) for c in City.query.all()]

    form.city_code.choices = city_codes

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data or None

        cafe= Cafe(name=name,
                description=description,
                url=url,
                address=address,
                city_code=city_code,
                image_url=image_url)
        db.session.add(cafe)
        db.session.commit()

        flash(f'{cafe.name} added')
        return redirect(f'/cafes/{cafe.id}')

    else:
        return render_template('cafe/add-form.html', form=form)

@app.route('/cafes/<int:cafe_id>/edit', methods=["GET", "POST"])
def edit_cafe(cafe_id):
    '''Show edit cafe form and handle editing'''

    cafe = Cafe.query.get_or_404(cafe_id)
    form = AddCafeForm(obj=cafe)

    city_codes = [(c.code, c.name) for c in City.query.all()]

    form.city_code.choices = city_codes

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        url = form.url.data
        address = form.address.data
        city_code = form.city_code.data
        image_url = form.image_url.data

        cafe.name = name
        cafe.description = description
        cafe.url = url
        cafe.address = address
        cafe.city_code = city_code
        cafe.image_url = image_url

        db.session.commit()

        flash(f'{cafe.name} edited')
        return redirect(f'/cafes/{cafe.id}')

    else:
        return render_template('cafe/edit-form.html', form=form, cafe=cafe)

#######################################################
#USERS

@app.route('/signup', methods=["GET", "POST"])
def signup():
    '''Show signup form and handle's form submission/registration of new user
       If valid, logs new user in and redirects to cafe list with flashed
       message -- You are signed up and logged in
    '''

    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        description = form.description.data
        email = form.email.data
        password = form.password.data
        image_url = form.image_url.data or None

        dup_user = User.query.filter_by(username=username).first()

        if dup_user:
            flash('Username already taken')
            return render_template('auth/signup-form.html', form=form)

        if image_url == None:
            image_url = "/static/images/default-pic.png"

        user = User.register(
            username,
            email,
            first_name,
            last_name,
            description,
            password,
            image_url)

        db.session.add(user)
        db.session.commit()

        do_login(user)

        flash('You are signed up and logged in.')
        return redirect('/cafes')

    else:
        return render_template('auth/signup-form.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    '''Show login form and processes login. If valid, logs in user and redirects
       to cafe list with flashed message -- Hello username!
    '''

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            do_login(user)
            flash(f'Hello, {username}')
            return redirect('/cafes')
        else:
            flash('Invalid credentials')

    return render_template('auth/login-form.html', form=form)


@app.post('/logout')
def logout():
    '''Process logout. Redirects to homepage with flashed message-- You have
       successfully logged out
    '''
    if g.user:
        do_logout()
        flash('successfully logged out')

    return redirect('/')


#############################################
#Profile Routes

@app.get('/profile')
def show_profile():
    '''Show user profile'''

    if not g.user:
        return redirect('/login')

    return render_template("profile/detail.html")


@app.route('/profile/edit', methods=["GET", "POST"])
def edit_profile():
    '''Show profile edit form and process profile edit. If successful, redirect
       to profile page with flashed message -- Profile edited.
    '''

    if not g.user:
        return redirect('/login')

    user = User.query.get_or_404(g.user.id)

    form = ProfileEditForm(obj=user)

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        description = form.description.data
        email = form.email.data
        image_url = form.image_url.data

        user.first_name = first_name
        user.last_name = last_name
        user.description = description
        user.email = email
        user.image_url = image_url

        db.session.commit()

        flash('Profile edited.')
        return redirect('/profile')

    else:
        return render_template('profile/edit-form.html', form=form)