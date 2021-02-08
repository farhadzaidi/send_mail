# Send Mail

This package makes it much easier to send emails in python.

# Installation

Install on Linux/MacOS:
`python3 -m pip install send_mail`

Install on Windows:
`python -m pip install send_mail`

# Usage
```python
from send_mail import SendMail

# Create SendMail object
new_mail = SendMail(
	# List (or string if single recipient) of the email addresses of the recipients
	['recipient1@email.com', 'recipient2@email.com'], 
	# Subject of the email
	'Email Subject',
	# Body of the email
	'Email Body', 
	# Email address of the sender
	# Leave this paramter out if using environment variable 'EMAIL_ADDRESS'
	'sender@email.com' 
)

# Add HTML
new_mail.add_html_message('<h1>Hello, World</h1>')

# If using HTML file
# new_mail.add_html_file('/path/to/your/html/file')

# List (or string if attaching single file) of relative or absolute file path(s) to files
new_mail.attach_files(['image.jpg', 'text.txt', 'myPDF.pdf'])

# Print SendMail object to confirm email
print(new_mail)

# Send the email
# Leave this parameter out if using environment variable 'EMAIL_PASSWORD'
new_mail.send('fake_password')

```

Let me know if you would like more email services other than Gmail