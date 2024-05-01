from flask import Flask, render_template, request, abort, url_for, flash, redirect
from forms import TicketForm, MaterielForm
from flask_sqlalchemy import SQLAlchemy
import os
import uuid

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


def generate_unique_id():
    return str(uuid.uuid4())


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
   return render_template('500.html'), 500


@app.route('/500')
def error500():
   abort(500)


@app.route('/')
def index():
    new_tickets = Ticket.query.filter_by(statut='nouveau').count()
    in_progress_tickets = Ticket.query.filter_by(statut='en_cours').count()
    in_repair_tickets = Ticket.query.filter_by(statut='en_reparation').count()
    closed_tickets = Ticket.query.filter_by(statut='ferme').count()

    return render_template('index.html', 
                           new_tickets=new_tickets, 
                           in_progress_tickets=in_progress_tickets, 
                           in_repair_tickets=in_repair_tickets, 
                           closed_tickets=closed_tickets)


@app.route('/cree_ticket/', methods=('GET', 'POST'))
def cree_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(
            id_ticket=generate_unique_id(),
            titre=form.titre.data,
            description_ticket=form.description_ticket.data,
            categorie=form.categorie.data,
            materiel=form.materiel.data
        )
        try:
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket créé avec succès! Statut: nouveau', 'success')
            return redirect(url_for('view_tickets_by_status', status='nouveau'))
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if there's an error
            flash(f'Erreur lors de la création du ticket: {str(e)}', 'error')
            app.logger.error(f'Error creating ticket: {e}')
            return render_template('creat_ticket.html', form=form)
        finally:
            db.session.close()  # Ensure that the db session is closed
    return render_template('creat_ticket.html', form=form)


@app.route('/tickets/<status>')
def view_tickets_by_status(status):
    try:
        tickets_list = Ticket.query.filter_by(statut=status).all()
        return render_template('tickets.html', tickets_list=tickets_list, status=status)
    except Exception as e:
        flash(f'Erreur lors de la récupération des tickets: {str(e)}', 'error')
        app.logger.error(f'Failed to fetch tickets by status {status}: {e}')
        return render_template('tickets.html', tickets_list=[], status=status)
    finally:
        db.session.close()



@app.route('/cree_mat/', methods=('GET', 'POST'))
def cree_mat():
    form = MaterielForm()
    if form.validate_on_submit():
        new_materiel = Materiel(
            id_mat=form.id_mat.data,
            marque=form.marque.data,
            typeMat=form.typeMat.data
        )
        try:
            db.session.add(new_materiel)
            db.session.commit()
            flash('Matériel créé avec succès!', 'success')
            return redirect(url_for('materiel'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la création du matériel: {str(e)}', 'error')
            app.logger.error(f'Error creating material: {e}')
            return render_template('creat_materiel.html', form=form)
        finally:
            db.session.close()
    return render_template('creat_materiel.html', form=form)




@app.route('/materiel/')
def materiel():
    try:
        materiel_list = Materiel.query.all()
        return render_template('materiel.html', materiel_list=materiel_list)
    except Exception as e:
        flash(f'Erreur lors de la récupération du matériel: {str(e)}', 'error')
        app.logger.error(f'Failed to fetch material: {e}')
        return render_template('materiel.html', materiel_list=[])
    finally:
        db.session.close()


@app.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
def edit_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)  # This uses the correct primary key
    form = TicketForm(obj=ticket)
    if form.validate_on_submit():
        ticket.titre = form.titre.data
        ticket.description_ticket = form.description_ticket.data
        ticket.categorie = form.categorie.data
        ticket.materiel = form.materiel.data
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'POST':
        flash('Error updating the ticket. Please check the form data.', 'error')
    return render_template('edit_ticket.html', form=form, ticket=ticket)


@app.route('/update_ticket/<int:ticket_id>', methods=['POST'])
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketForm(request.form)
    if form.validate_on_submit():
        ticket.titre = form.titre.data
        ticket.description_ticket = form.description_ticket.data
        ticket.categorie = form.categorie.data
        ticket.materiel = form.materiel.data
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to a different page upon successful update
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"Error in {fieldName}: {err}", 'error')
        return render_template('edit_ticket.html', form=form, ticket=ticket)  # Re-render the edit page with errors



if __name__ == '__main__':
    app.run(debug=True)
