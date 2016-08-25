import webapp2
import cgi

def encrypt(text, rot):
	encrypted = ''
	for char in text:
		alphabet = 'abcdefghijklmnopqrstuvwxyz'

		if char in alphabet:
			rotated_index = alphabet.index(char) + rot
			if rotated_index < 26:
				encrypted = encrypted + alphabet[rotated_index]
			else:
				encrypted = encrypted + alphabet[rotated_index % 26]
		else:
			alphabet = alphabet.upper()
			if char in alphabet:
				rotated_index = alphabet.index(char) + rot
				if rotated_index < 26:
					encrypted = encrypted + alphabet[rotated_index]
				else:
					encrypted = encrypted + alphabet[rotated_index % 26]
			elif char == ' ':
				encrypted = encrypted + ' '
			else:
				encrypted = encrypted + char
	return encrypted

header = """
<HTML>
	<head>
		<style>
            form {
                background-color: #eee;
                padding: 20px;
                margin: 0 auto;
                width: 540px;
                font: 16px sans-serif;
                border-radius: 10px;
            }
            textarea {
                margin: 10px 0;
                width: 540px;
                height: 120px;
            }
            .error {
                color: red;
            }
		</style>
	</head>
	<body>
		<form action="/rotate" method="post">
			<br>
    		<label for="rot13">Rotate by:</value>
    		<input type="text" name="rot" value = "13">
    		<br>
    		<textarea type="text" name="text">
"""

close_header = """
    		</textarea>
    		<input type="submit" value="Rotate">  
"""

footer = """
    	</form>
	</body>
</HTML>
"""

class MainHandler(webapp2.RequestHandler):
    """	
    Rotate text input using caeser method
    """

    def get(self):
    	#printself = "<p>" + self.request.get("text") + "</p>"
    	#printresponse = header + printself + footer

    	rot_form = header + close_header + footer	

        self.response.write(rot_form)

class Rotate(webapp2.RequestHandler):

	def post(self):
		rot = self.request.get("rot")

		if not rot.isdigit():
			error_text = """
			<div class="error">
				<p>Invalid Rotate Number</p>
			</div>
			"""
			rot_form = header + cgi.escape(self.request.get("text"), quote=True) + close_header + error_text + footer
		else:
			rot = int(rot)
			encrypted_text = encrypt(cgi.escape(self.request.get("text"), quote=True), rot)
			escaped_text = cgi.escape(encrypted_text, quote=True)
			rot_form = header + escaped_text + close_header + footer

		self.response.write(rot_form)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rotate', Rotate),
], debug=True)
