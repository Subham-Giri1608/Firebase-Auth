from flask import Flask,request,redirect,render_template,session
import pyrebase
from flask_mail import Mail, Message

app = Flask(__name__)

firebaseConfig = {
    "apiKey": "AIzaSyD8kfRNvhNz6eaEzPIk2ji34ZG508XmZyM",
    "authDomain": "flask-auth-3f0ad.firebaseapp.com",
    "projectId": "flask-auth-3f0ad",
    "storageBucket": "flask-auth-3f0ad.appspot.com",
    "messagingSenderId": "271788688834",
    "appId": "1:271788688834:web:b5e6435cd397ae3fce425b",
    "measurementId": "G-G52T40E2LE",
    "databaseURL":''
}

firebase_app = pyrebase.initialize_app(firebaseConfig)
auth = firebase_app.auth()

app.secret_key = "secret"

@app.route("/", methods=["GET","POST"])
def login():
    error_message = None

    if 'user' in session:
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.sign_in_with_email_and_password(email, password)
            session["user"] = email
            return redirect("/dashboard")
        except Exception as e:
            if "EMAIL_NOT_FOUND" in str(e):
                return redirect("/register")
            else:
                error_message = str(e)

    return render_template('login.html',error=error_message)


@app.route("/dashboard")
def dashboard():
    user_info = {'email': session['user']}
    return render_template('dashboard.html',user=user_info)

@app.route("/register", methods=["GET","POST"])
def register():
    error_message = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/")
        except Exception as e:
            error_message =str(e)

    return render_template('register.html',error=error_message)

@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect("/")

def send_reset_email(email, token):
    try:
        msg = Message('Password Reset Request', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
        reset_link = url_for('reset_password', token=token, _external=True)
        msg.body = f"Click the following link to reset your password: {reset_link}"
        mail.send(msg)
        return True  
    except Exception as e:
        print(f"Error sending reset email: {str(e)}")
        return False


@app.route('/reset', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']

        try:
            auth.send_password_reset_email(email)
            flash('Password reset email sent. Check your inbox.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred while sending the reset email. Please try again later.', 'error')

    return render_template('reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            try:
                if is_valid_token(token):
                    auth.update_user(uid, password=new_password)
                    return True  
            except auth.AuthError as e:
                    
                    print(f"Password update error: {e}")
                    return False
        elif():
                flash('Invalid or expired reset token. Please request a new reset email.', 'error')
        else:
                flash('An error occurred while resetting the password. Please try again later.', 'error')

    return render_template('reset_request.html', token=token)



if __name__ == "__main__":
    app.run(debug=True)