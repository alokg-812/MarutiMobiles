from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, RepairRequest, User, Role
from forms import AdminRepairUpdateForm

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total = RepairRequest.query.count()
    active = RepairRequest.query.filter(RepairRequest.status.notin_(['Delivered'])).count()
    completed = RepairRequest.query.filter_by(status='Delivered').count()

    # Status counts for chart
    statuses = ['Requested', 'Picked Up', 'Under Repair', 'Ready', 'Delivered']
    status_counts = []
    for s in statuses:
        status_counts.append(RepairRequest.query.filter_by(status=s).count())

    return render_template('admin/dashboard.html',
        total=total, active=active, completed=completed,
        statuses=statuses, status_counts=status_counts)

@admin_bp.route('/repairs')
@admin_required
def repairs():
    status_filter = request.args.get('status', '')
    query = RepairRequest.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    repairs = query.order_by(RepairRequest.created_at.desc()).all()
    return render_template('admin/repairs.html', repairs=repairs, current_filter=status_filter)

@admin_bp.route('/repair/<int:repair_id>', methods=['GET', 'POST'])
@admin_required
def repair_detail(repair_id):
    repair = RepairRequest.query.get_or_404(repair_id)
    form = AdminRepairUpdateForm(obj=repair)
    if form.validate_on_submit():
        repair.status = form.status.data
        repair.repair_cost = form.repair_cost.data
        repair.admin_notes = form.admin_notes.data
        db.session.commit()
        flash('Repair updated.', 'success')
        return redirect(url_for('admin.repair_detail', repair_id=repair_id))
    return render_template('admin/repair_detail.html', repair=repair, form=form)

@admin_bp.route('/customers')
@admin_required
def customers():
    customer_role = Role.query.filter_by(name='customer').first()
    users = User.query.filter_by(role_id=customer_role.id).order_by(User.created_at.desc()).all()
    return render_template('admin/customers.html', customers=users)

@admin_bp.route('/customer/<int:user_id>')
@admin_required
def customer_detail(user_id):
    user = User.query.get_or_404(user_id)
    repairs = RepairRequest.query.filter_by(user_id=user_id).order_by(RepairRequest.created_at.desc()).all()
    return render_template('admin/customer_detail.html', customer=user, repairs=repairs)
