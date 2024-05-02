from uwu.database import db
from flask_login import UserMixin

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



class User(UserMixin):
    def __init__(self, id, roles):
        self.id = id
        self.active_role = roles[0]  
        self.roles = roles

    def switch_role(self, new_role):
        if new_role in self.roles:
            self.active_role = new_role
            return True
        return False

    @property
    def is_admin(self):
        return self.active_role == 'admin'

    @property
    def is_employee(self):
        return self.active_role == 'employee'

    @property
    def is_super_admin(self):
        return self.active_role == 'super_admin'
