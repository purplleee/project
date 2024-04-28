from flask import Flask, render_template , abort, url_for
import os


SECRET_KEY = os.environ.get('SECRET_KEY')
app = Flask(__name__)


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

if __name__ == '__main__':
    app.run(debug=True)
