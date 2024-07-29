# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

# Initialize the database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(200), nullable=False)
    gst_number = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    rate_per_day = db.Column(db.REAL, nullable=False)
    bill_amount = db.Column(db.REAL, nullable=False)

    def __init__(self, client_name, gst_number, start_date,end_date,rate_per_day,bill_amount):
        self.client_name = client_name
        self.gst_number = gst_number
        self.start_date = start_date
        self.end_date=end_date
        self.rate_per_day=rate_per_day
        self.bill_amount=bill_amount


@app.route('/')
def index():
    items = Todo.query.order_by(Todo.id).all()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    client_name = request.form.get('client_name')
    gst_number = request.form.get('gst_number')
    start_date = datetime.datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
    rate_per_day = float(request.form.get('rate_per_day'))

    # Calculate bill amount based on start and end dates
    days_stored = (end_date - start_date).days
    bill_amount = rate_per_day * days_stored

    new_task = Todo(client_name,gst_number,start_date,end_date,rate_per_day,bill_amount)
    
    try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
    except:
            return 'There was an issue adding your task'

    else:
        items = Todo.query.order_by(Todo.id).all()
        return render_template('index.html', items=items)

@app.route('/remove_item/<int:item_id>')
def remove_item(item_id):
    task_to_delete = Todo.query.get_or_404(item_id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update(item_id):
    item = Todo.query.get_or_404(item_id)

    if request.method == 'POST':
        item.client_name = request.form['client_name']
        item.gst_number = request.form['gst_number']
        item.start_date = datetime.datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        item.end_date = datetime.datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        item.rate_per_day = float(request.form['rate_per_day'])

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', item=item)
    

if __name__ == '__main__':
    app.run(debug=True)
    app.config['SQLALCHEMY_ECHO'] = True
