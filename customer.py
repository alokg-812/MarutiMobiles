import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from models import db, RepairRequest
from forms import RepairBookingForm, ProfileForm

customer_bp = Blueprint('customer', __name__)

@customer_bp.before_request
@login_required
def require_login():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

@customer_bp.route('/dashboard')
def dashboard():
    active = RepairRequest.query.filter(
        RepairRequest.user_id == current_user.id,
        RepairRequest.status != 'Delivered'
    ).order_by(RepairRequest.created_at.desc()).all()
    return render_template('customer/dashboard.html', active_repairs=active)

@customer_bp.route('/book', methods=['GET', 'POST'])
def book_repair():
    form = RepairBookingForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            ext = os.path.splitext(form.image.data.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        repair = RepairRequest(
            user_id=current_user.id,
            brand=form.brand.data,
            model=form.model.data,
            problem=form.problem.data,
            image_filename=filename,
            pickup_address=form.pickup_address.data,
            pickup_date=form.pickup_date.data,
            pickup_time_slot=form.pickup_time_slot.data,
            contact_phone=form.contact_phone.data,
            contact_email=form.contact_email.data,
        )
        db.session.add(repair)
        db.session.commit()
        flash('Repair request booked successfully!', 'success')
        return redirect(url_for('customer.dashboard'))
    return render_template('customer/book_repair.html', form=form)

@customer_bp.route('/repairs')
def repair_history():
    repairs = RepairRequest.query.filter_by(user_id=current_user.id)\
        .order_by(RepairRequest.created_at.desc()).all()
    return render_template('customer/repair_history.html', repairs=repairs)

@customer_bp.route('/repair/<int:repair_id>')
def repair_detail(repair_id):
    repair = RepairRequest.query.get_or_404(repair_id)
    if repair.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('customer.dashboard'))
    return render_template('customer/repair_detail.html', repair=repair)

@customer_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('customer.profile'))
    return render_template('customer/profile.html', form=form)
