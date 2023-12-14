from sqlalchemy import create_engine,Column,Integer,String,Date,Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
# from bson import ObjectId  # Import ObjectId from bson
import io  
from flask import Flask,send_file
from src.config import Config
import bcrypt
from src.logger_config import logger
#Environment variable coming from the config module
config = Config()

# Sqlalchemy  connection to interact with MYsql database
Database_URL_dummy=config.DATABASE_URL
engine=create_engine(Database_URL_dummy)
Session=sessionmaker(bind=engine)
db_session=Session()
Base=declarative_base()

#mongo_db connection 
mongo_db = MongoClient(config.MONGO_URL)

#Registration Table ORM creation.
class User(Base):
    __tablename__='registration'
    F_name=Column(String(25))
    L_name=Column(String(25))
    Mobile_NO=Column(String(10))
    email=Column(String(25),primary_key=True)
    Registration_Id=Column(String(8))
    Password=Column(String(100))
    form_status=Column(String(10))
    Approval=Column(String(50))

#Personal_detail Table ORM creation.
class Personal_detail(Base):
    __tablename__='personal_detail'
    email=Column(String(25),primary_key=True)
    first_name=Column(String(25))
    last_name=Column(String(25))
    father_name=Column(String(10))
    mother_name=Column(String(25))
    DOB=Column(Date)
    gender=Column(String(15))
    category=Column(String(15))
    mobile_no=Column(String(10))
    address=Column(String(80))
    district=Column(String(50))
    state=Column(String(39))
    pincode=Column(String(6))

#Education_detail ORM creation.
class Education_detail(Base):
    __tablename__='education_detail'
    email=Column(String(50),primary_key=True)
    ssc_school_name=Column(String(25))
    ssc_Passing_year=Column(String(25))
    ssc_rollno=Column(String(10))
    ssc_Percentage=Column(Float)
    hsc_school_name=Column(String(25))
    hsc_Passing_year=Column(String(25))
    hsc_rollno=Column(String(10))
    hsc_Percentage=Column(Float)
    exam_name=Column(String(25))
    exam_rollno=Column(String(10))
    exam_Percentage=Column(Float)
    course=Column(String(10))
    















def insert_registration_data(l,unique_id):
    try:
        pwd=bytes(l[5],'utf-8')
        hashed=bcrypt.hashpw(pwd,bcrypt.gensalt())
        new_User=User(F_name=l[0].upper(),L_name=l[1].upper(),Mobile_NO=l[2],email=l[3],Registration_Id=unique_id,Password=hashed,Approval="Pending")
        new_Personal_detail=Personal_detail(first_name=l[0].upper(),last_name=l[1].upper(),email=l[3])
        new_Education_detail=Education_detail(email=l[3])
        # new_Communication_detail=Communication_detail(email=l[3])
        db_session.add(new_User)
        db_session.add(new_Personal_detail)
        db_session.add(new_Education_detail)
        # session.add(new_Communication_detail)


        db_session.commit()
        db_session.close()
    except Exception as e:
    # Handle the exception or log it as needed
        print(f"An error occurred: {e}")
        
        # Rollback the current transaction to clean up
        db_session.rollback() 
        return False  
    return True 

def update_data(email, data):
    if data['tabName']=='personal':
        logger.info("we are in update data personal detail")
        update_personal = db_session.query(Personal_detail).filter(Personal_detail.email == email).first()
        
        # print(data['first_name'])
        update_personal.first_name=data['first_name'].upper()
        update_personal.last_name=data['last_name'].upper()
        update_personal.mother_name=data['mother_name'].upper()
        update_personal.father_name=data['father_name'].upper()
        update_personal.DOB=data['date_of_birth']
        update_personal.gender=data['gender']
        update_personal.category=data['category']
       
        db_session.commit()
        db_session.close()

    if data['tabName']=='communication':
        logger.info("we are in update data communication detail")
        
        update_personal = db_session.query(Personal_detail).filter(Personal_detail.email == email).first()
        
        # print(data['first_name'])
        update_personal.mobile_no=data['phone_number'].upper()
        update_personal.address=data['address'].upper()
        update_personal.district=data['district'].upper()
        update_personal.state=data['State']
        update_personal.pincode=data['pincode']
        
        db_session.commit()
        db_session.close()

    if data['tabName']=='education':
        logger.info("we are in update data education detail")

        update_education = db_session.query(Education_detail).filter(Education_detail.email == email).first()
        
        # print(data['first_name'])
        update_education.ssc_school_name=data['ssc_school_name'].upper()
        update_education.ssc_Passing_year=data['ssc_Passing_year'].upper()
        update_education.ssc_rollno=data['ssc_rollno'].upper()
        update_education.ssc_Percentage=data['ssc_Percentage']
        update_education.hsc_school_name=data['hsc_school_name'].upper()
        update_education.hsc_Passing_year=data['hsc_Passing_year']
        update_education.hsc_rollno=data['hsc_rollno']
        update_education.hsc_Percentage=data['hsc_Percentage']
        update_education.exam_name=data['exam_name'].upper()
        update_education.exam_rollno=data['exam_rollno']
        update_education.exam_Percentage=data['exam_Percentage']
        update_education.course=data['course']

        







        
        session.commit()
        session.close()    
            
        


def login_validation(Username, Password):
    print("we are in login_validation")
    user = db_session.query(User).filter(User.email == Username).first()
    if user is None : 
        return False
    try:
        stored_password=user.Password
    except Exception as e:
        print(e)
    stored_password_bytes = stored_password.encode('utf-8')
    if bcrypt.checkpw(Password.encode('utf-8'),stored_password_bytes):
        return retrive_data(Username)
    else :
        logger.info("Username and Password does found")
        return False
    
    

def registered(email):
       try:
            user = db_session.query(User).filter(User.email == email).first()
            # print(user.Fname)
            if user : 
                logger.info("User is registered already")   
                db_session.close()              
                return True 
            else :
                logger.info(f"User is not registered {email} and we can send the otp.")
                return False
       except Exception as e:
            logger.error(f"An error occured: {e}")  
            db_session.rollback()
            return False     

def upload_image(data):
    user = data['User']
    query = {'User': user}
    existing_data = mongo_db.db.images.find_one(query)

    if existing_data:
        # If data for the user already exists, update it
        mongo_db.db.images.update_one(query, {'$set': data})
        print("Updated successfully")
        logger.info("Imgaes updated successfully")
    else:
        # If data for the user does not exist, insert a new document
        mongo_db.db.images.insert_one(data)
        print("Inserted successfully")
        logger.info("Inserted succesfully")


def update_pass(email, new_password):
    try:
        user = db_session.query(User).filter(User.email == email).first()
        if user:
            # Hash the new password before updating it in the database
            new_password_bytes = bytes(new_password, 'utf-8')
            hashed = bcrypt.hashpw(new_password_bytes, bcrypt.gensalt())
            
            user.Password = hashed
            db_session.commit()
            db_session.close()
            return True
        else:
            return False  # User not found
    except Exception as e:
        logger.info(f"An error occured of : {e}")
        db_session.rollback()
        return False
    
def submit(email):
    try:
        user = db_session.query(User).filter(User.email == email).first()
        user.form_status='Submitted'
        logger.info("The form has been submitted successfully")
        db_session.commit()
        db_session.close()
        return True
    except Exception as e: 
        logger.info(f"There is some exception {e} while submiting the form")


def get_image_database(image_id,email):
    # Retrieve the image binary data from MongoDB
    
    image_data = mongo_db.db.images.find_one({'User':email })
    # image_data = mongo.db.images.find_one({'User': 'virat@gmail.com'})
    if image_data:
        # Convert the binary data to a bytes-like object
        image_bytes = image_data[image_id]
        # Send the image as a response with the correct MIME type
        return send_file(io.BytesIO(image_bytes), mimetype='image/png')
    else:
        return "Image not found", 404    
    


def student_list():

    student_list=db_session.query(User).all()
    student_data=[]
    for i in student_list:
        
        if i.__dict__['form_status']=="Submitted" and i.__dict__['Approval']=='Pending':
            student_data.append(i)
    return student_data
    
    

def retrive_data(Username):
    try:
        user = db_session.query(User).filter(User.email == Username).first()
        personal_detail=db_session.query(Personal_detail).filter(Personal_detail.email == Username).first()
        education_detail=db_session.query(Education_detail).filter(Education_detail.email == Username).first()
        print(user)
        db_session.close()
        user_data={"name" :user.F_name+" "+user.L_name,'id': user.Registration_Id,"form_status":user.form_status,"first_name":personal_detail.first_name,
                   "last_name":personal_detail.last_name,"father_name":personal_detail.father_name,"mother_name":personal_detail.mother_name,
                   "DOB":personal_detail.DOB , "gender":personal_detail.gender,"category":personal_detail.category,
                   "mobile_no":personal_detail.mobile_no,"address":personal_detail.address,"district":personal_detail.district,"state":personal_detail.state,"pincode":personal_detail.pincode
                   ,"email":Username,
                       'ssc_school_name':education_detail.ssc_school_name,
        'ssc_Passing_year':education_detail.ssc_Passing_year,"ssc_rollno":
        education_detail.ssc_rollno,"ssc_Percentage":
        education_detail.ssc_Percentage,"hsc_school_name":
        education_detail.hsc_school_name,"hsc_Passing_year":
        education_detail.hsc_Passing_year,"hsc_rollno":
        education_detail.hsc_rollno,"hsc_Percentage":
        education_detail.hsc_Percentage,"exam_name":
        education_detail.exam_name,"exam_rollno":
        education_detail.exam_rollno,"exam_Percentage":
        education_detail.exam_Percentage,
        "course":education_detail.course  
        
        }

        try:
            documents = mongo_db.db.images.find_one({'User': Username})
            
            user_data['image0']= documents.get('image0', ''),
            user_data['image1']= documents.get('image1', ''),
            user_data['image2']= documents.get('image2', ''),
            user_data['image3']= documents.get('image3', ''),
            user_data['image4']=documents.get('image4', ''),
            user_data['image5']=documents.get('image5', ''),
        except   Exception as e:
            print(f"An error occurred in nested try: {e}")  
        
        return user_data 
    except Exception as e:
        print(f"An error occurred2321: {e}")   
        db_session.rollback()
        