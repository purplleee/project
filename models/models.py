from uwu.database import db


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
