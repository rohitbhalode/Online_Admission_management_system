from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
from datetime import datetime, timedelta
from src.logger_config import logger
#Environment variable coming from the config module
from src.config import Config
config = Config()
# from src.logger_config import logger

#Environment variable coming from the config module
# config = Config()


class UniqueID():
    uniqueid=0
    def __init__(self):
      type(self).uniqueid=type(self).uniqueid+1
    currentYear = datetime.now().year
    def Create_UniqueId(self):
        a=self.uniqueid
        a=str(a)
        if(len(a)<4):
            empty=""
            for i in range(4-len(a)):
                empty+='0'
            a=empty+a
        UniqueID=str(self.currentYear)+a
        return UniqueID
    



class InterviewScheduler:
    def __init__(self, start_date):
        self.start_date = start_date
        self.current_date = start_date
        self.daily_slot_counter = 0
        self.daily_limit = 20

    def reset_daily_counter(self):
        # Reset the counter at the beginning of each day
        self.current_date += timedelta(days=1)
        self.daily_slot_counter = 0

    def increment_daily_counter(self):
        # Increment the counter when a new interview is scheduled
        self.daily_slot_counter += 1

    def is_daily_limit_reached(self):
        # Check if the daily limit is reached
        return self.daily_slot_counter >= self.daily_limit

    def schedule_interview(self, candidate_id):
        # Check if the daily limit is reached
        if self.is_daily_limit_reached():
            # Move to the next day and reset the counter
            self.reset_daily_counter()

        # Schedule the interview
        scheduled_date = self.current_date
        scheduled_time = self.schedule_interview_for_candidate(candidate_id)

        # Increment the daily counter
        self.increment_daily_counter()

        return f"You Application for admission for applied course has been approved.Your Interview scheduled for candidate on {scheduled_date} at {scheduled_time} at respective Department you applied of St. Maria College"

    def schedule_interview_for_candidate(self, candidate_id):
        # Implement your logic to schedule the interview for the candidate
        # For example, you might want to schedule it at a specific time on the scheduled date
        scheduled_time = "10:00 AM"
        return scheduled_time



def send_otp(email):
    # Generate a new secret key for the user (store this securely)
    
    secret_key = pyotp.random_base32()
    # print('email.',email)
    # Create a TOTP instance (Time-based OTP)
    totp = pyotp.TOTP(secret_key)

    # Generate the OTP (typically done on the server)
    otp = totp.now()
    # print(otp)
    message="Your OTP:"+ str(otp)
    # Send the OTP to the user via email, SMS, or another method
    subject="Verification Code"
    send_email(email,message,subject)
    

    return otp

def send_email(email,message,subject):
    

    msg = MIMEMultipart()
    
    # Set the sender, recipient, and subject
    msg['From'] = "rohitbhalode@gmail.com"
    msg['To'] = email
    msg['Subject'] =subject
    
    # Add the message body
    msg.attach(MIMEText(message, 'plain'))
    
    # Create an SMTP connection
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start the TLS encryption
        server.starttls()
        
        # Login to the email account
        server.login("rohitbhalode@gmail.com", config.EMAIL_APP_PASSWORD)
         
        logger.info("The email has been send successfully to ",email)
        # Send the email
        server.send_message(msg)