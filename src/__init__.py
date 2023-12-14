from flask import flash,current_app,Flask,render_template,request,redirect,session,jsonify,url_for
from src.logger_config import logger
from src.customexception import Custom_Exception
from src.Actions import login,register,password_reset,form,admin


app=Flask(__name__)
app.config['SECRET_KEY']='Rohit_Bhalode'

#creating the different blueprints
app.register_blueprint(register.mod)
app.register_blueprint(login.mod)
app.register_blueprint(password_reset.mod)
app.register_blueprint(form.mod)
app.register_blueprint(admin.mod)



@app.route('/')
def home():
    if "user" in session:
        user=session['user']
        logger.info(f'The user is getting logout from session {user}.')
        
        session.pop('user', None)
    #Here college website home page is rendering 
    logger.info("Home page is opened")
    return render_template('home.html')




