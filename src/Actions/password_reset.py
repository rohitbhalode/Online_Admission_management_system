from flask import Blueprint,flash,render_template,request,redirect,session,jsonify,url_for

from src.logger_config import logger
from src.database import registered,update_pass
from src.Actions.utils import send_otp

mod=Blueprint('password_reset', __name__,url_prefix='/password_reset')


@mod.route("/password_reset")
def password_reset():
    
    logger.info('Password Reset form is opened')

    return render_template('password_reset.html')
    
@mod.route("/send", methods=['GET'])
def send2():
    email = request.args.get('email')
    logger.info(f'The send button for password reset is clicked for sending otpcode to {email} ')
    if registered(email):
        logger.info(f'The  {email} is registered user ')

        session['email'] = email
        session['otpcode'] = send_otp(session['email'])
        logger.info(f"OTP has been sent {session['otpcode']}")
        return '', 200
    else:
        logger.info(f'{email} is not registered email id  ')
        return  '', 403
    

@mod.route('/update_password', methods=["POST"])
def update_password():
    if request.method=='POST':
        Password =  request.form.get('password')
        logger.info("The password is getting updated")
        Username=session['email']
        update_pass(Username,Password)
        logger.info("The password is updated successfully")
    return render_template('success1.html')