from .models import Feedback
from .forms import FeedbackForm
from flask import flash, redirect, render_template, url_for
from . import feedback
from .. import db

@feedback.route('/feedback', methods=['GET', 'POST'])
def feedbacks():
    form = FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        feedback_entry = Feedback(name=name, email=email, message=message)
        db.session.add(feedback_entry)
        db.session.commit()

        flash('Ваш відгук був збережений', 'success')
        return redirect(url_for('feedback.feedback'))

    feedbacks = Feedback.query.all()

    return render_template('feedback.html', form=form, feedbacks=feedbacks)