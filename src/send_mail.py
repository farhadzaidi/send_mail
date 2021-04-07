import os
import smtplib
import imghdr
import textwrap
from email.message import EmailMessage
from easy_colors import Colors

class SendMail:
	
	# **All paramters are strings unless otherwise specificied**

	# Required: 'recipients', 'subject', 'message'
		# 'recipients' - list (or string if single recipient) of email addresses that will recieve the email
		# 'subject' - subject of the email
		# 'message' - body of the email (required even if sending HTML message)
		# *'sender'* - email address that sends the email
			# 'sender' defaults to 'EMAIL_ADDRESS' environment variable
			# If no such environment variable exists, 'sender' is required
	# DO NOT USE CONSTRUCTOR TO ATTACH FILES OR ADD HTML --> use methods instead
	def __init__(self, recipients, subject, message, sender=os.environ.get('EMAIL_ADDRESS'), html_message=None, files=None):

		global email
		email = EmailMessage()

		self.recipients = recipients
		self.subject = subject
		self.message = message
		self.sender = sender
		self.html_message = html_message
		self.files = files

		email['From'] = self.sender
		email['To'] = recipients
		email['Subject'] = self.subject
		email.set_content(message)


	# Use to add HTML from a string to the email 
	def add_html_message(self, html_message):
		self.html_message = html_message
		email.add_alternative(html_message, subtype='html')


	# Use to add HTML from a file to email
	# 'html_file' is a string consisting of the absolute or relative path to the desired HTML file 
	def add_html_file(self, html_file):
		f = open(html_file, 'r')

		content = f.read()
		self.html_message = content
		email.add_alternative(content, subtype='html')

		f.close()


	# Use to attach files to email
	# 'files' is a list (or string if attaching single file) of the absolute or relative file path(s) to the files
	def attach_files(self, files):
		if isinstance(files, str):
			self.files = [files]
		else:
			self.files = files

		for file in self.files:
			with open(file, 'rb') as f:
				file_data = f.read()
				file_name = f.name

				if imghdr.what(file):
					maintype = 'image'
					subtype=imghdr.what(file)
				else:
					maintype = 'application'
					subtype = 'octet-string'


			email.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)


	# Use to send the email
	# **'password'** - password to sender's email account
		# 'password' defaults to 'EMAIL_PASSWORD' environment variable
		# If no such environment variable exists, 'password' is required
	def send(self, password=os.environ.get('EMAIL_PASSWORD')):
		with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

			smtp.login(self.sender, password)

			smtp.send_message(email)


	# Use to print contents of email before sending
	def __str__(self):
		if not isinstance(self.recipients, str):
			recipients = ', '.join(self.recipients)
		else:
			recipients = self.recipients

		mail = f'''
			{Colors.INFO}Sender:{Colors.END} {self.sender}
			{Colors.INFO}Recipient(s):{Colors.END} {recipients}\n
			------------------------------\n
			{Colors.INFO}Subject:{Colors.END} {self.subject}
			{Colors.INFO}Message:{Colors.END} {self.message}
			'''
		mail = textwrap.dedent(mail)

		if self.html_message:
			mail += f'{Colors.INFO}HTML Message:{Colors.END} \n{self.html_message}\n'

		attachments = []
		if self.files:
			attachments += self.files

		for i in range(0, len(attachments)):
			for j in range(len(attachments[i])-1, -1, -1):
				if attachments[i][j] == '/':
					attachments[i] = attachments[i][j+1:len(attachments[i])]
					break

		if len(attachments) != 0:
			attachments = ', '.join(attachments)
			mail += f'{Colors.INFO}Attachment(s):{Colors.END} {attachments}\n'

		return mail


