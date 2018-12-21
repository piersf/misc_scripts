#!/usr/bin/env python


"""
This is a class that can be imported as a module. It implements the email sending functionality.
It requires that a logger object is passed when instatiating the class.
Works with Python 2.7+
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText



class SendEmail(object):
	"""
	This class implements the email functionality.
	"""
	
	def __init__(self, logger, message, error_code, error_message="", SUBJECT=""):
		self.logger = logger
		self.message = message
		self.subject = SUBJECT
		self.error = error_code
		self.error_message = error_message
		
		# If an error happened, append the error in the email
		if self.error != 0:
			self.message = self.message + "." + "\nError is:\n\t%s" % (self.error_message)
	
	
	def send_email(self):
		SMTP_SERVER = "smtp.server.com"
		FROM = 'sender.user@company.com'
		TO = ["receiver.user@company.com"]
		smtp_server = None
		
		try:
			self.logger.info("Preparing to send email..")
			MSG = MIMEText(self.message, "plain")
			MSG['Subject'] = self.subject
			MSG['From'] = 'SOME SUBJECT <%s>' % FROM
			MSG['To'] = ", ".join(TO)
			smtp_server = smtplib.SMTP(SMTP_SERVER)
			self.logger.info("Opened connection with SMTP server %s" % SMTP_SERVER)
			smtp_server.sendmail(FROM, TO, MSG.as_string())
		except smtplib.SMTPServerDisconnected as e:
			self.logger.exception("Server unexpectedly disconnected or an attempt was made to use an SMTP instance before connecting to the server")
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPSenderRefused as e:
			self.logger.exception("SMTP server refused the sender address. Reason is: %s" % e.smtp_error)
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPRecipientsRefused as e:
			self.logger.info("SMTP server refused the recipient address(es). Reason: %s" % str(e.smtp_error))
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPDataError as e:
			self.logger.info("SMTP server refused to accept message data")
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPConnectError as e:
			self.logger.exception("Error occurred during establishment of a connection with the server %s" % SMTP_SERVER)
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPResponseException as e:
			self.logger.exception("The SMTP server returned an error. Reason is: %s" % e.smtp_error)
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except smtplib.SMTPException as e:
			self.logger.exception("Unable to send email")
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		except Exception as e:
			self.logger.exception("Unable to send email. Error occurred while trying to send email.")
			self.logger.error("%s %s %s" % ('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e))
			raise
		else:
			self.logger.info("Email sent successfully.")
		finally:
			if smtp_server:
				smtp_server.quit()
				self.logger.info("Closed connection with SMTP server %s" % SMTP_SERVER)

