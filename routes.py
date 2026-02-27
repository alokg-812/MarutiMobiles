from flask import Blueprint, render_template, redirect, url_for, flash, request
from models import db, RepairRequest, Feedback
from forms import QuickBookingForm, FeedbackForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    booking_form = QuickBookingForm()
    feedback_form = FeedbackForm()
    
    # Handle Quick Booking
    if 'full_name' in request.form and booking_form.validate_on_submit():
        repair = RepairRequest(
            full_name=booking_form.full_name.data,
            contact_phone=booking_form.contact_phone.data,
            brand=booking_form.brand.data,
            model=booking_form.model.data,
            problem=booking_form.problem.data,
            pickup_address=booking_form.pickup_address.data,
            status='Requested'
        )
        db.session.add(repair)
        db.session.commit()
        flash('Cyber-protocol initiated. Your repair request has been logged.', 'success')
        return redirect(url_for('main.home'))
        
    # Handle Feedback
    if 'message' in request.form and feedback_form.validate_on_submit():
        feedback = Feedback(
            name=feedback_form.name.data,
            message=feedback_form.message.data,
            rating=int(feedback_form.rating.data)
        )
        db.session.add(feedback)
        db.session.commit()
        flash('Transmission received. Thank you for your feedback.', 'success')
        return redirect(url_for('main.home'))

    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template('home.html', 
                         booking_form=booking_form, 
                         feedback_form=feedback_form,
                         feedbacks=feedbacks)

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')
