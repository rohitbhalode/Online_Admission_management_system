from flask import Blueprint,flash,render_template,request,redirect,session,jsonify,url_for
from datetime import datetime
from src.logger_config import logger
from src.database import student_list,retrive_data,User,db_session
from src.Actions.utils import InterviewScheduler,send_email

start_date = datetime(2023, 11, 1)  # Set your desired start date here
scheduler = InterviewScheduler(start_date)
mod = Blueprint('admin', __name__,url_prefix="/admin")

@mod.route('/admin_login')
def admin_login():
    logger.info("We are in admin login page now")
    return render_template("/admin_login.html")


@mod.route("/login",methods=['GET', 'POST'])
def login():
    keys_to_display = ['F_name', 'L_name', 'email','Mobile_NO','form_status','Approval']

    if "user" in session:
        data=student_list()
        return render_template('student_list.html', data=data, keys=keys_to_display)
    if request.method == 'POST' :
        Username = request.form.get("admin_id")
        Password = request.form.get("password")
        print(Username)
        
        try: 
            if Username=="admin" and Password=="admin123":
                logger.info("Admin logged in successfully")
                session["user"]=Username
                session["Password"]=Password
                data=student_list()

                return render_template('student_list.html', data=data, keys=keys_to_display)
            else:
                flash("Please check the Password ","success2")
                return redirect("/admin/admin_login")
        except Exception as e:
            logger.info(f"the exception is {e}")
            return "We are having trouble in database server please refresh again press F5"
    flash("Please contact to system admin","success2")


@mod.route("/action",methods=["POST","GET"])
def action():
    email=request.form['email']
    user_data=retrive_data(email)
    
    return render_template('confirmation.html', user_data=user_data,admin=True)


@mod.route("/approval/<email>",methods=["POST","GET"])
def approval(email):
    approval=request.form['approval']
    user = db_session.query(User).filter(User.email == email).first()
    user.Approval=approval
    db_session.commit()
    if approval=="Approved":
        result = scheduler.schedule_interview(email)
        subject="Form Status"
        logger.info("The form is approved and schedule is ",result)
        send_email(email,result,subject)
    
    # return "SUcceessful"
    return redirect("/admin/login")



@mod.route("/logout")
def logout():
#   print(session['email'] )
    session.pop("user")
    # Redirect to the login or home page (replace '/login' with the appropriate URL)
    return redirect("/")