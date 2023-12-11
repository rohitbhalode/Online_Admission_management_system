from flask import Blueprint,flash,render_template,request,redirect,session,jsonify,url_for

from src.logger_config import logger
from src.Actions.utils import UniqueID
from src.database import registered,insert_registration_data
from src.Actions.utils import send_otp
mod=Blueprint('register', __name__,url_prefix='/register')



@mod.route("/register")
def register():
    
    logger.info('New Registration form is opened.=== ')

    return render_template('register.html')
 
@mod.route("/send", methods=['GET'])
def send():
    email = request.args.get('email')
    logger.info(f'The send button for registration has clicked for sending otpcode to {email} ')
    if registered(email):
        logger.info(f'{email} is registered email')
        return '', 999
    else:
        logger.info(f'{email} is not registered email')
        session['email'] = email
        try:
          otpcode = send_otp(email)
          logger.info(f'The otpcode has been sent to {email} is {otpcode} ')
          session['otpcode'] = otpcode
        except Exception as e:
          logger.info(f"While sending the email smtp error {e}")
          flash("We are having server problem in sending email,please contact admin and wait sometime",'email_error')

    return "Email sent Successful",200


@mod.route('/verify_code', methods=['POST'])
def verify_verification_code():
    # Get the code from the request as JSON
    code = request.json.get('code')
    stored_otpcode = session.get('otpcode')
    logger.info(f'The Code enter by user is {code} and code sent to user is {stored_otpcode}.')
    
    # Check the code (you should implement this logic)
    if code == stored_otpcode:
        logger.info("The verification is successfull")

        return '', 200  # Code is correct, return a 200 status code
    else:
        logger.info("The verification is Unsuccessfull")

        return '', 403  # Code is incorrect, return a 403 status code



@mod.route("/submit", methods=['POST'])
def result():
  
  if request.method=='POST':
    data = request.form.values()
    data=[i for i in data]
    # print(l)
    Id_create=UniqueID()
      
    id=Id_create.Create_UniqueId()
    if insert_registration_data(data,id):
        logger.info(f'New Registration Id has been created {id}. ')
        
        return render_template('success.html')
    else:
        logger.info(f'Database timeout error occur not critical refreshing the page will normalize . ')
        return "Our site is slow  due to much user please refresh,Please wait!"
      
  else:
    
    return redirect('/register')