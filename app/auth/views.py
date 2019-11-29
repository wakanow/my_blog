from . import auth
from ..import db
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_user
from flask import request, url_for, redirect, flash, render_template

@auth.route('/login', method=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startwith('/'):
                next = url_for('main_index')
            return redirect(next)
        flash('无效的邮箱或者密码')
    return render_template('auth/login.html', form=form)

@auth.route('/register', methon=['GET', 'POST'])
def register():
    form = RegistrationForm
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)