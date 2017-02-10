#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def buildwelcome(username):
	welcome = """
	<head>
		<title>Unit 2 Signup</title>
	</head>
	<body>
		<h2>Welcome """ + username + """!  </h2>
	</body>"""
	return welcome

def buildpage(userError, passError, verifyError, emailError):
	str_form = """
		<form method = "post">
		<table>
		<tr>
			<td class = "label">
				Username
			</td>
			<td>
				<input type="text" name="username">
			</td>
			<td class="error">
			 """+userError +"""
			</td>
		</tr>
		
		<tr>
			<td class="label">
				Password
			</td>
			<td>
				<input type="password" name="password">
			</td>
			<td class="error">"""+passError+"""
			</td>
		</tr>
		
		<tr>
			<td class="label">
				Verify Password
			</td>
			<td>
				<input type="password" name="verify">
			</td>
			<td class="error">"""+verifyError+"""
			</td>
		</tr>	
		<tr>
			<td class="label">
				Email (optional)
			</td>
			<td>
				<input type="text" name="email">
			</td>
			<td class="error">"""+emailError+"""
			</td>
		</tr>
		</table>
		
		<input type="submit">
	</form>
	"""
	return str_form
	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write(buildpage("","","",""))
		
	def post(self):
		have_error = False
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		
		params = dict(username="", email="",verify="", password="")
		
		if not valid_username(username):
			params["username"] = "That's not a valid username."
			have_error = True
			
		if not valid_password(password):
			params["password"] = "That's not a valid password."
			have_error = True
			
		if password != verify:
			params["verify"] = "You passwords didn't match."
			have_error = True
		
		if not valid_email(email):
			params["email"] = "That's not a valid email."
			have_error = True
		
			
		if have_error:
			self.response.write(buildpage(params["username"], params["password"], params["verify"], params["email"]))
		else:
			self.response.write(buildwelcome(username))				

	
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
	return username and USER_RE.match(username)
	
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)	
	
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
	return not email or EMAIL_RE.match(email)
    
class Welcome(MainHandler):
	def get(self):
		username = self.request.get("username")
		if valid_username(username):
			self.response.write(buildwelcome(username))
		else:
			self.redirect('/unit2/signup')
        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

