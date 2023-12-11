from flask import Blueprint,flash,render_template,request,redirect,session,jsonify,url_for
from bson.binary import Binary
from src.logger_config import logger
from src.database import upload_image,update_data,login_validation,submit,get_image_database


mod = Blueprint('form', __name__,url_prefix='/form')

@mod.route('/save', methods=['POST','GET'])
def save_data():
    logger.info(f'The data is saving as saved button clicked')

    data = request.form  # This will contain the form data from the POST request
    # Process and save the data as needed (e.g., store it in a database)
    # You can return a response, but for now, let's just return a success message
    active_tab=data['tabName']
    logger.debug(f'The data is saving for tab {active_tab}')
    
    if data['tabName']=='document':
        if 'image1' in request.files:
            image0 = request.files['image0']
            image1 = request.files['image1']
            image2 = request.files['image2']
            image3 = request.files['image3']
            image4 = request.files['image4']
            image5 = request.files['image5']
            data = {
                        'User': session['user'],
                        'image0': Binary(image0.read()),
                        'image1': Binary(image1.read()),
                        'image2': Binary(image2.read()),
                        'image3': Binary(image3.read()),
                        'image4': Binary(image4.read()),
                        'image5': Binary(image5.read())}

            # image_name = request.form['image_name']
            upload_image(data)

    # if data['tabName']=='personal':        
            
    else: 
        logger.info("Data is going for mysql database")
        update_data(session['user'],data)
    return render_template('student_profile.html', user_data=session.get('user_data'),active_tab=active_tab)



@mod.route('/confirmation')
def confirmation():
    # Retrieve user data from your database or session
    logger.info(f"Details are confirming. ")

    user_data = login_validation(session['user'], session['Password'])
    return render_template('confirmation.html', user_data=user_data,admin=False)




@mod.route('/submitted')
def submitted():
    
    user_data = login_validation(session['user'], session['Password'])
    
    if len(user_data)==34:
        submit(session['user'])
        logger.info(f"Form is submitted successfully")

        return render_template('form_submited.html')
    else :
        flash('Please save all the details!', 'success1')
        return render_template('confirmation_page.html', user_data=user_data,admin=False)
    




@mod.route('/get_image/<email>/<image_id>',methods=["POST","GET"])
def get_image(image_id,email):
    # Retrieve the image binary data from MongoDB
    
    # print('Image ID:', image_id)
    # print('Email:', session['user'])
    logger.info(f"User is watching image {image_id}")
    # get_image_database(image_id,email)  
    return get_image_database(image_id,email)