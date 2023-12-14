from flask import Blueprint,flash,render_template,request,redirect,session,jsonify,url_for

from src.logger_config import logger
from src.database import login_validation


mod = Blueprint('login', __name__)

# Login button route which will validate the user and render the dashboard page of the user using his 
# registered data.


@mod.route("/login", methods=['GET', 'POST'])
def login():
    
    if 'user' in session  :

        # User is already logged in, redirect them to the profile page.
        active_tab = request.args.get('active_tab','personal')
        
        logger.info('User is in session reloading the page.')
        
        
        user_data=login_validation(session['user'] , session['Password'])
        # mod.config['user_data']=user_data
        if user_data['form_status']=="Submitted":
            return render_template('form_submited.html')
        else:
            return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        # print("Username",Username)
        # print("Password",Password)
        try: 
            # print("we are in try block")
            user_data=login_validation(Username, Password)
            # print("USer_data",user_data)
        except Exception as e: 
            return "Please refresh page database server is slow"
        # user_data=user_data.upper()
        # session['user_data'] = user_data
        logger.info(f'User: {Username} is login to server ')
        
        if user_data:
            active_tab = request.args.get('active_tab', 'personal')
            
            
            session['user'] = Username
            session['Password'] = Password
            if user_data['form_status']=="Submitted":
                logger.info(f'User: {Username} is logged to server and form_status is submitted  ')
                return render_template('form_submited.html')
            else:
                logger.info(f'User: {Username} is successfully logged to server and form_status is not submitted  ')

                return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)
        else:
            logger.error(f'There is database exception in login_validation funtion')
            flash("Please check the password","success")
            return render_template('home.html')

    return render_template('home.html')


@mod.route("/logout")
def logout():
#   print(session['email'] )
    user=session['user']
    logger.info(f'The user is getting logout from session {user}.')
      
    session.pop('user', None)
    # Redirect to the login or home page (replace '/login' with the appropriate URL)
    return redirect("/")