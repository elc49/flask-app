from flask import flash, redirect, url_for, abort, render_template
from flask_login import current_user, login_required

from . import admin
from .. import db
from .forms import DepartmentForm
from ..models import Department

def check_admin():
	"""
	Prevent non-admin from accessing this route
	"""
	if not current_user.is_admin:
		abort(403)

# Department views
@admin.route("/departments", methods=["GET", "POST"])
@login_required
def list_departments():
	"""
	List all departments
	"""
	check_admin()

	departments = Department.query.all()

	return render_template("admin/departments/departments.html", departments=departments, title="Departments")

@admin.route("/departments/add", methods=["GET", "POST"])
@login_required
def add_department():
	"""
	Add a department to the database
	"""
	check_admin()

	add_department = True

	form = DepartmentForm()
	if form.validate_on_submit():
		department = Department(name=form.name.data, description=form.description.data)

		try:
			# add department to the database
			db.session.add(department)
			db.session.commit()
			flash("You have successfully added a department.")
		except:
			# if department already exist in the database
			flash("Sorry! Department name already exist.")

		return redirect(url_for("admin.list_departments"))

	# load department page
	return render_template("admin/departments/department.html", form=form, title="Add Department", add_department=add_department, action="Add")

@admin.route("/departments/edit/<int:id", methods=["GET", "POST"])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_admin()

	add_department = False

	department = Department.query.get_or_404(id)
	form = Department(obj=department)
	if form.validate_on_submit():
		department.name = form.name.data
		department.description = form.description.data
		db.session.commit()
		flash("Your edit was a success.")

		# redirect to department lists page
		return redirect(url_for("admin.list_departments"))

	form.name.data = department.name
	form.description.data = department.description
	return render_template("/admin/departments/department.html", action="Edit", form=form, add_department=add_department, department=department, title="Edit Department")

@admin.route("/departments/delete/<int:id", methods=["GET", "POST"])
@login_required
def delete_department(id):
	"""
	Delete a department from the database
	"""
	check_admin()

	department = Department.query.get_or_404(id)
	db.session.delete(department)
	db.session.commit()
	flash("You delete was a success.")

	# redirect to departments page
	return redirect(url_for("admin.list_departments"))

	return render_template(title="Delete Department")

