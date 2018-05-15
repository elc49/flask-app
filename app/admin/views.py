from flask import flash, redirect, url_for, abort, render_template
from flask_login import current_user, login_required

from . import admin
from .. import db
from .forms import DepartmentForm, RoleForm, EmployeeAssignForm
from ..models import Department, Role, Employee

def check_admin():
	"""
	Prevent non-admin from accessing this route
	"""
	if not current_user.is_admin:
		abort(403)

# Employee views
@admin.route("/employees")
@login_required
def list_employees():
	"""
	List all employees
	"""
	check_admin()

	employees = Employee.query.all()
	return render_template("admin/employees/employees.html", employees=employees, title="Employees")

@admin.route("/employees/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign_employee(id):
	"""
	Assign a department and a role to an employee
	"""
	check_admin()

	employee = Employee.query.get_or_404(id)

	# prevent admin from being assigned a role or department
	if employee.is_admin:
		abort(403)

	form = EmployeeAssignForm(obj=employee)
	if form.validate_on_submit():
		employee.department = form.department.data
		employee.role = form.role.data
		db.session.add(employee)
		db.session.commit()
		flash("You have successfully assigned a department and a role.")

		return redirect(url_for("admin.list_employees"))

	return render_template("admin/employees/employee.html", employee=employee, title="Assign Employee", form=form)

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
			flash("Error: department already exist.")

		return redirect(url_for("admin.list_departments"))

	# load department page
	return render_template("admin/departments/department.html", form=form, title="Add Department", add_department=add_department, action="Add")

@admin.route("/departments/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_department(id):
	"""
	Edit a department
	"""
	check_admin()

	add_department = False

	department = Department.query.get_or_404(id)
	form = DepartmentForm(obj=department)
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

@admin.route("/departments/delete/<int:id>", methods=["GET", "POST"])
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

# Role views
@admin.route("/roles", methods=["GET", "POST"])
@login_required
def list_roles():
	"""
	List all roles
	"""
	check_admin()

	roles = Role.query.all()

	return render_template("admin/roles/roles.html", title="Role", roles=roles)

@admin.route("/roles/add", methods=["GET", "POST"])
@login_required
def add_role():
	"""
	Add role to the database
	"""
	check_admin()

	add_Role = True

	form = RoleForm()
	if form.validate_on_submit():
		role = Role(name=form.name.data, description=form.description.data)

		try:
			# add role to the database
			db.session.add(role)
			db.session.commit()
			flash("Role added.")
		except:
			flash("Error: role already exist.")

		return redirect(url_for("admin.list_roles"))

	return render_template("admin/roles/role.html", add_Role=add_Role, title="Add Role", form=form)

@admin.route("/roles/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_role(id):
	"""
	Edit a role
	"""
	check_admin()

	add_Role = False

	role = Role.query.get_or_404(id)
	form = RoleForm(obj=role)
	if form.validate_on_submit():
		role.name = form.name.data
		role.description = form.description.data
		db.session.add(role)
		db.session.commit()
		flash("Your edit was a success.")

		return redirect(url_for("admin.list_roles"))

	form.name.data = role.name
	form.description.data = role.description
	return render_template("admin/roles/role.html", form=form, title="Edit Role", add_Role=add_Role)

@admin.route("/roles/delete/<int:id>", methods=["GET", "POST"])
@login_required
def delete_role(id):
	"""
	Delete role
	"""
	check_admin()

	role = Role.query.get_or_404(id)
	db.session.delete(role)
	db.session.commit()
	flash("Your delete was a success")

	return redirect(url_for("admin.list_roles"))

	return render_template(title="Delete Role")
