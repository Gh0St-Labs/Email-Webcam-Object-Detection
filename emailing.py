import smtplib
import ssl
import os
from email.message import EmailMessage
import imghdr

def send_email(image_message):
    print("send_email() FUNCTION STATUS: Started")
    email_message = EmailMessage()
    email_message['Subject'] = 'New Client Showed Up!'
    email_message.set_content("Hey! A New Customer Entered. Pinging you with the Customer's Image!")

    with open(image_message, 'rb') as file:
        content = file.read()

    email_message.add_attachment(content, maintype='image', subtype=imghdr.what(None, content))

    # Create a Server
    gmail = smtplib.SMTP('smtp.gmail.com', 587)

    # To Start the Server Parameters:
    gmail.ehlo()
    gmail.starttls()

    username = 'syondukeabraham@gmail.com'
    password = 'ocubslvhrmjiipvy'
    reciever = 'syondukeabraham@gmail.com'
    gmail.login(username, password=password)
    gmail.sendmail(username, reciever, msg=email_message.as_string())

    # Quit Server
    gmail.quit()
    print("send_email() FUNCTION STATUS: Ended")

if __name__ == "__main__":
    print("Hello! Don't Worry About Me!")