import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

class Email():

    def __init__(self) -> None:
        self.email = os.getenv("EMAIL")
        self.smtp = os.getenv("SMTP")
        self.password = os.getenv("PASSWORD")


    def send_msg(self, to_address, subject, message):
        with smtplib.SMTP(self.smtp) as connection:
                connection.starttls()
                connection.login(user=self.email, password=self.password)
                message = f"Subject:{subject}\n\n{message}"
                connection.sendmail(
                    from_addr=self.email, 
                    to_addrs= to_address,
                    msg= message
                )
