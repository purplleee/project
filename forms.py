from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,RadioField,FieldList, SelectField)
from wtforms.validators import InputRequired, Length

class TicketForm(FlaskForm):
    titre = StringField('Titre', validators=[InputRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description Ticket', validators=[Length(max=400)])
    categorie = SelectField('Categorie', validators=[InputRequired()], choices=[
                            ('panne_inconnue', 'Panne Inconnue'),
                            ('reseau', 'Réseau'), 
                            ('si_erp', 'système d\'information - ERP'),
                            ('si_crm', 'système d\'information - CRM'),
                            ('si_bi', 'système d\'information - BI'), 
                            ('panne_hard', 'Panne Hard'),
                            ('AD', 'AD'), 
                            ('thunder_bird', 'ThunderBird'), 
                            ('panne_soft', 'Panne Soft')])
    type_material = SelectField('Type Materiel', choices=[('panne_soft', 'Panne Soft')])
