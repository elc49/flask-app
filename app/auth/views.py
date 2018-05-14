from flask import flash, render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import RegistrationForm, LoginForm
from .. import db
from ..models import Employee

@auth.route("/register", methods=["GET", "POST"])
def register():
	"""
	Handle requests to the /register route
	Add employee to the database through the registration form
	"""
	form = RegistrationForm()
	if form.validate_on_submit():
		employee = Employee(email=form.email.data, username=form.username.data, 
			first_name=form.first_name.data, last_name=form.last_name.data, password=form.password.data)

		# Add employee to the database
		db.session.add(employee)
		db.session.commit()

		flash("You have successfully registered! You may now login")

		# redirect to login page
		return redirect(url_for("auth.login"))

	# load registration page
	return render_template("auth/register.html", form=form, title="Register")

@auth.route("/login", methods=["GET", "POST"])
def login():
	"""
	Handle requests to the /login route
	Log in an employee thro' the login form
	"""
	form = LoginForm()
	if form.validate_on_submit():
		# check whether employee exist in the database and
		# whether the password entered matches the password in the database
		employee = Employee.query.filter_by(email=form.email.data).first()
		if employee is not None and employee.verify_password(form.password.data):
			# login employee
			login_user(employee)
			# redirect to dashboard page
			return redirect(url_for("home.dashboard"))

		# while logins are incorrect
		else:
			flash("Invalid email or password")

	return render_template("auth/login.html", form=form, title="Login")

@auth.route("/logout")
@login_required
def logout():
	"""
	Handle requests to the /logout route
	Log out user through the logout link
	"""
	logout_user()
	flash("You have successfully been logged out!")

	# redirect to login page
	return redirect(url_for("auth.login"))
