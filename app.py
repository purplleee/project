from flask import Flask, render_template, request, abort, url_for, flash, redirect
from forms import TicketForm, MaterielForm
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '1fd34bf367245d1c60c08a5325a2dc72235390ee0a685cf9')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/helpdesk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Ticket(db.Model):
    __tablename__ = 'tickets'
    id_ticket = db.Column(db.Integer, primary_key=True)  # Correct primary key name
    titre = db.Column(db.String(100), nullable=False, unique=True)
    description_ticket = db.Column(db.String(400))
    categorie = db.Column(db.String(10), nullable=False)
    materiel = db.Column(db.String(30))
    statut = db.Column(db.String(7), default='nouveau')


class Materiel(db.Model):
    __tablename__ = 'materiel'
    id_mat = db.Column(db.String(10), primary_key=True)
    marque = db.Column(db.String(100), nullable=False)
    typeMat = db.Column(db.String(20), nullable=False)





@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
   return render_template('500.html'), 500


@app.route('/500')
def error500():
   abort(500)





if __name__ == '__main__':
    app.run(debug=True)
