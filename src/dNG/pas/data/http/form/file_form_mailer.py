# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.form.FileFormMailer
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpFileFormVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from dNG.data.rfc.email.message import Message
from dNG.data.rfc.email.part import Part
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.net.smtp.client import Client as SmtpClient
from dNG.pas.runtime.value_exception import ValueException
from .abstract_file_form_processor import AbstractFileFormProcessor

class FileFormMailer(AbstractFileFormProcessor):
#
	"""
Service for "s=file_form"

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: file_form
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute(self):
	#
		"""
Executes the processor.

:since: v0.1.00
		"""

		if (self.form == None or (not self.validate_settings(self.settings))): raise ValueException("Processor is not configured")

		sender = (
			InputFilter.filter_control_chars(self.form.get_input(self.settings['mail_sender_field_name']))
			if ("mail_sender_field_name" in self.settings) else
			None
		)

		subject = (
			InputFilter.filter_control_chars(self.form.get_input(self.settings['mail_subject_field_name']))
			if ("mail_subject_field_name" in self.settings) else
			self.settings['mail_subject_title']
		)

		if (subject == None or len(subject.strip()) < 1): raise ValueException("Given e-Mail subject is invalid")

		content_list = [ ]
		titles = (self.settings['form_field_titles'] if ("form_field_titles" in self.settings) else { })

		for field_name in self.settings['mail_content_field_names']:
		#
			value = InputFilter.filter_control_chars(self.form.get_input(field_name))

			content_list.append("{0}:\n{1}".format(
				(titles[field_name] if (field_name in titles) else field_name),
				value
			))
		#

		content = "\n\n".join(content_list)

		part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", content)

		message = Message()
		message.add_body(part)
		if (sender != None): message.set_from(sender)
		message.set_subject(subject)
		message.set_to(self.settings['recipient'])

		smtp_client = SmtpClient()
		smtp_client.set_message(message)
		smtp_client.send()
	#

	def validate_settings(self, data):
	#
		"""
Called to validate the given settings.

:param data: Setting dict to be verified

:since: v0.1.00
		"""

		_return = False

		if (
			isinstance(data, dict) and
			"recipient" in data and
			"mail_content_field_names" in data and
			("mail_subject_field_name" in data or "mail_subject_title" in data)
		):
		#
			_return = True

			recipient = InputFilter.filter_email_address(data['recipient'])
			if (recipient == ""): _return = False

			if (type(data['mail_content_field_names']) != list): _return = False
			if ("mail_subject_title" in data and len(data['mail_subject_title']) < 1): _return = False
		#

		return _return
	#
#

##j## EOF