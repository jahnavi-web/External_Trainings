from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Employee({self.id}, {self.name}, {self.department})"

# Initialize Database
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    employees = Employee.query.all()
    return render_template('main.html', employees=employees)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        new_employee = Employee(name=name, department=department)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_employee.html')

@app.route('/logout')
def logout():
    return "Logged out successfully!"  # Redirect to login page if needed

if __name__ == '__main__':
    app.run(debug=True)
