from flask import render_template, request, redirect, session, flash, url_for
from models.login_info import LoginInfo
from models.user_profile import UserProfile
from models import db
from flask_mailman import EmailMessage



def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        gender = request.form['gender']

        if LoginInfo.query.filter_by(username=username).first():
            return "Username already exists."

        if UserProfile.query.filter_by(email=email).first():
            return "Email already registered."

        user = LoginInfo(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            user_id=user.user_id
        )
        db.session.add(profile)
        db.session.commit()

        return redirect('/user/login')

    return render_template('register.html')



def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = LoginInfo.query.filter_by(username=username, password=password).first()

        if user and user.profile.is_deleted == False:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role.value if hasattr(user.role, 'value') else user.role
            return redirect('/')
        else:
            return "Invalid username or password."

    return render_template('login.html')



def view_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/user/login')
    
    user = LoginInfo.query.get(user_id)
    profile = UserProfile.query.filter_by(user_id=user_id).first()
    return render_template('view_profile.html', user=user, profile=profile)



def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/user/login')

    profile = UserProfile.query.filter_by(user_id=user_id).first()

    if request.method == 'POST':
        profile.name = request.form['name']
        profile.phone = request.form['phone']
        profile.email = request.form['email']
        profile.gender = request.form['gender']
        db.session.commit()
        return redirect('/user/profile')

    return render_template('edit_profile.html', profile=profile)


def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        user = LoginInfo.query.filter_by(username=username).first()

        if user:
            subject = "Your Password Recovery"
            message = f"Hello {user.username},\n\nYour password for Blog Website is: {user.password}\n\nPlease keep it safe."
            email = EmailMessage(subject, message, to=[user.profile.email])

            email.send()
            return f"Password sent to your registered email: {user.profile.email}"
        else:
            return "No user found with that username."

    return render_template('forgot_password.html')

def change_password():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('user.login'))

    user = LoginInfo.query.get(user_id)

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if user.password != current_password:
            flash('Incorrect current password.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        else:
            user.password = new_password
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('user.view_profile'))

    return render_template('change_password.html')

def logout():
    session.clear()
    return redirect('/')