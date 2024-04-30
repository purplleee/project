from flask import Flask, render_template ,request, abort, url_for, flash, redirect
from forms import TicketForm ,MaterielForm
import mysql.connector
import os

app = Flask(__name__)
SECRET_KEY = os.environ.get('SECRET_KEY')
app.config['SECRET_KEY'] = '1fd34bf367245d1c60c08a5325a2dc72235390ee0a685cf9'

def get_db_connection():
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'helpdesk'
    }
    return mysql.connector.connect(**mysql_config)

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
    new_tickets = 5
    in_progress_tickets = 5
    in_repair_tickets = 5
    closed_tickets = 5

    return render_template('index.html', 
                           new_tickets=new_tickets, 
                           in_progress_tickets=in_progress_tickets, 
                           in_repair_tickets=in_repair_tickets, 
                           closed_tickets=closed_tickets)



@app.route('/cree_ticket/', methods=('GET', 'POST'))
def cree_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO tickets (`titre`, `description_ticket`, `categorie`, `type materiel`) 
                              VALUES (%s, %s, %s, %s)''',
                           (form.titre.data, form.description.data, form.categorie.data, form.type_material.data))
            conn.commit()
            flash('ticket créé\nstatut : nouveau ', 'success')
            return redirect(url_for('tickets'))  
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            #flash('Failed to create course.', 'error')
            #app.logger.error(f"Database Error: {err}")
            flash(f'Échec de la création du ticket: {err}', 'error')
            return render_template('creat_ticket.html', form=form)
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('tickets'))
    return render_template('creat_ticket.html', form=form)



@app.route('/tickets/')
def tickets():
    conn = get_db_connection()
    tickets_list = []
    try:
        cursor = conn.cursor(dictionary=True)  # Ensure cursor returns dictionaries
        cursor.execute("SELECT * FROM tickets")  # Adjusted to the 'tickets' table
        tickets_list = cursor.fetchall()
        app.logger.info(f"Fetched tickets: {tickets_list}")  # Log the fetched data
    except mysql.connector.Error as err:
        app.logger.error(f"Failed to fetch tickets: {err}")
        flash(f"Error fetching tickets: {err}", 'error')
    finally:
        cursor.close()
        conn.close()
    return render_template('tickets.html', tickets_list=tickets_list)


@app.route('/cree_mat/', methods=('GET', 'POST'))
def cree_mat():
    form = MaterielForm()
    if form.validate_on_submit():
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO materiel (`id_mat`, `marque`, `typeMat`) 
                              VALUES (%s, %s, %s)''',
                           (form.id_mat.data, form.marque.data, form.typeMat.data))
            conn.commit()
            flash('materiel créé ', 'success')
            return redirect(url_for('materiel'))  
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            #flash('Failed to create course.', 'error')
            #app.logger.error(f"Database Error: {err}")
            flash(f'Échec de la création du materiel: {err}', 'error')
            return render_template('creat_materiel.html', form=form)
        finally:
            cursor.close()
            conn.close()
        return redirect(url_for('materiel'))
    return render_template('creat_materiel.html', form=form)


@app.route('/materiel/')
def materiel():
    conn = get_db_connection()
    materiel_list = []
    try:
        cursor = conn.cursor(dictionary=True)  # Ensure cursor returns dictionaries
        cursor.execute("SELECT * FROM materiel")  # Adjusted to the 'tickets' table
        materiel_list = cursor.fetchall()
        app.logger.info(f"Fetched materiel: {materiel_list}")  # Log the fetched data
    except mysql.connector.Error as err:
        app.logger.error(f"Failed to fetch materiel: {err}")
        flash(f"Error fetching materiel: {err}", 'error')
    finally:
        cursor.close()
        conn.close()
    return render_template('materiel.html', materiel_list=materiel_list)



if __name__ == '__main__':
    app.run(debug=True)
