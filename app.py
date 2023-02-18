from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@127.0.0.1:1521/xe'

db = SQLAlchemy(app)


class Employee(db.Model):
    name = db.Column(db.String(20), unique=False, nullable=False)
    work_mode = db.Column(db.String(20), unique=False, nullable=False)
    tele = db.Column(db.Integer(), primary_key=True)
    city = db.Column(db.String(30), unique=False, nullable=False)


@app.route("/employeeinfo", methods=['GET', 'POST'])
def employeeinfo():
    if request.method == 'POST':
        'add entry to DB'

        name = request.form.get('name')
        work_mode = request.form.get('work_mode')
        tele = request.form.get('tele')
        city = request.form.get('city')

        entry = Employee(name=name, work_mode=work_mode, tele=tele, city=city)
        db.create_all()
        db.session.add(entry)
        db.session.commit()

    # pass the entries to the template
    return render_template('employee.html')


@app.route("/employeedata")
def employeedata():
    # fetch all entries from the Employee table
    entries = Employee.query.all()

    return render_template('empdata.html', entries=entries)


@app.route('/employeeinfo/delete/<int:tele>', methods=['POST'])
def delete_entry(tele):
    entry = Employee.query.get(tele)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('empdata'))


@app.route('/employeeinfo/update/<int:tele>', methods=['GET', 'POST'])
def update_entry(tele):
    entry = Employee.query.get(tele)
    if request.method == 'POST':
        entry.name = request.form.get('name')
        entry.work_mode = request.form.get('work_mode')
        entry.tele = request.form.get('tele')
        entry.city = request.form.get('city')
        db.session.commit()
        return redirect(url_for('empdata'))
    return render_template('update.html', entry=entry)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        admin_name = request.form.get('admin_name')
        admin_pass = request.form.get('admin_pass')

        # check if admin_name and password are correct
        if admin_name == 'admin' and admin_pass == 'admin':
            # redirect to admin page
            return redirect(url_for('empdata'))
        else:
            # show error message
            error = 'Invalid admin name or password'
            return render_template('adminlogin.html', error=error)

    return render_template('adminlogin.html')


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
