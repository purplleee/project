@app.route('/cree_ticket/', methods=('GET', 'POST'))
def cree_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(
            titre=form.titre.data,
            description_ticket=form.description.data,
            categorie=form.categorie.data,
            materiel=form.type_material.data
        )
        try:
            db.session.add(new_ticket)
            db.session.commit()
            flash('Ticket créé avec succès! Statut: nouveau', 'success')
            return redirect(url_for('tickets'))
        except Exception as e:
            db.session.rollback()  # Roll back the transaction if there's an error
            flash(f'Erreur lors de la création du ticket: {str(e)}', 'error')
            app.logger.error(f'Error creating ticket: {e}')
            return render_template('creat_ticket.html', form=form)
        finally:
            db.session.close()  # Ensure that the db session is closed
    return render_template('creat_ticket.html', form=form)