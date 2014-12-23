# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;file_form

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpFileFormVersion)#
#echo(__FILEPATH__)#
"""

from binascii import hexlify
from os import urandom

from dNG.pas.data.binary import Binary
from dNG.pas.data.tasks.database_proxy import DatabaseProxy as DatabaseTasks
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.runtime.value_exception import ValueException
from .abstract_file_form_processor import AbstractFileFormProcessor

class FileFormMailer(AbstractFileFormProcessor):
#
	"""
FileForm processor that sends an e-mail.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: file_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def execute(self):
	#
		"""
Executes the processor.

:since: v0.1.00
		"""

		if (self.form is None or (not self.validate_settings(self.settings))): raise ValueException("Processor is not configured")

		lang = (self.settings['email_lang']
		        if ("email_lang" in self.settings) else
		        L10n.get_instance().get_lang()
		       )

		sender = (InputFilter.filter_control_chars(self.form.get_input(self.settings['email_sender_field_name']))
		          if ("email_sender_field_name" in self.settings) else
		          None
		         )

		subject = (InputFilter.filter_control_chars(self.form.get_input(self.settings['email_subject_field_name']))
		           if ("email_subject_field_name" in self.settings) else
		           self.settings['email_subject_title']
		          )

		if (subject is None or len(subject.strip()) < 1): raise ValueException("Given e-mail subject is invalid")

		content_list = [ ]
		titles = self.settings.get("form_field_titles", { })

		for field_name in self.settings['email_content_field_names']:
		#
			value = InputFilter.filter_control_chars(self.form.get_input(field_name))

			content_list.append("{0}:\n{1}".format((titles[field_name] if (field_name in titles) else field_name),
			                                       value
			                                      )
			                   )
		#

		content = "\n\n".join(content_list)

		DatabaseTasks.get_instance().add("dNG.pas.http.Form.sendEMail.{0}".format(Binary.str(hexlify(urandom(16)))),
		                                 "dNG.pas.http.Form.sendEMail",
		                                 1,
		                                 lang = lang,
		                                 sender = sender,
		                                 subject = subject,
		                                 content = content
		                                )
	#

	def validate_settings(self, data):
	#
		"""
Called to validate the given settings.

:param data: Setting dict to be verified

:since: v0.1.00
		"""

		_return = False

		if (isinstance(data, dict)
		    and DatabaseTasks.is_available()
		    and "recipient" in data
		    and "email_content_field_names" in data
		    and ("email_subject_field_name" in data or "email_subject_title" in data)
		   ):
		#
			_return = True

			recipient = InputFilter.filter_email_address(data['recipient'])
			if (recipient == ""): _return = False

			if (type(data['email_content_field_names']) != list): _return = False
			if ("email_subject_title" in data and len(data['email_subject_title']) < 1): _return = False
		#

		return _return
	#
#

##j## EOF