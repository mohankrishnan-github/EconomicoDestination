from flask import *
from flask import Flask ,render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import validators, SubmitField, StringField, SelectField, IntegerField, DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired

import predict_review
from flight_search import FlightSearch
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2
import getReviews
import processReviews
import sentiment_analysis
from sqlalchemy import create_engine


app = Flask(__name__)
app.secret_key="secretkey123"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://userVIR:evoQgqPpnHdwC5aU@ed.mohankrishnanvasudevan-dev.svc.cluster.local/ed"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(20))
    location = db.Column(db.String(50))
    destinations = db.Column(db.String(200))
    next_mail_on = db.Column(db.Date)


db.create_all()


class airlineForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    submit = SubmitField()


class SubscribeForm(FlaskForm):

    location = StringField(validators=[DataRequired()])
    destination = StringField(validators=[DataRequired()])
    type = SelectField(validators=[DataRequired()], choices=["Flight Type", "oneway", "round"])
    adults = IntegerField(validators=[DataRequired()])
    children = IntegerField()
    search = SubmitField()


class SignUpForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    name = StringField(validators=[DataRequired()])
    location = StringField(validators=[DataRequired()])
    destination = StringField(validators=[DataRequired()])
    signup = SubmitField()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/search", methods=["GET", "POST"])
def search():
    deals = []
    form = SubscribeForm()
    if form.is_submitted():
        deals = FlightSearch().get_trip_deals(flyFrom=form.location.data.split(" ")[0],
                                              flyTo=form.destination.data.split(" ")[0], flight_type=form.type.data,
                                              adults=form.adults.data, children=form.children.data)
        return render_template('index.html', form = form, deals = deals)

    return render_template('index.html', form = form, deals = deals)


@app.route("/subscribe", methods=["GET", "POST"])
def subscribe():

    form = SignUpForm()
    if form.is_submitted():
        Email = form.email.data
        Name = form.name.data
        Location = form.location.data
        Destinations = form.destination.data
        Today = datetime.now().date()
        if User.query.filter_by(email=Email).first() == None:
            new_user = User(email = Email,name = Name,location = Location,destinations = Destinations, next_mail_on = Today )
            db.session.add(new_user)
            db.session.commit()
        else:
            flash('Email already exist')

        return redirect(url_for('subscribe'))
    return render_template('multiple.html', form=form)


@app.route("/airline_analysis", methods=["GET", "POST"])
def airline_analysis():

    form = airlineForm()
    flag = False
    if form.is_submitted():
        try:
            airline = (form.name.data).lower().replace(" ", "-")
            table = airline.split("-")[0]
            print(airline)
            engine = create_engine(
                "mysql+pymysql://ED@economicodestination:M0han123456@economicodestination.mysql.database.azure.com:3306/ed")
            getReviews.getReviews(airline, engine)
            data = processReviews.processReviews(table, engine)
            sentiment_analysis.sentimentAnalysis(airline, data)
            predict_review.predict(data)

        finally:
            sql = f"DROP TABLE IF EXISTS {table};"
            engine.execute(sql)
        flag = True
        return render_template('analysis.html', form = form, flag=flag)
    return render_template('analysis.html', form = form, flag=flag)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
