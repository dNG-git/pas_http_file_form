# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.http.form.AbstractFileFormProcessor
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

from dNG.pas.data.text.form_processor import FormProcessor
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.value_exception import ValueException

class AbstractFileFormProcessor(object):
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

	def __init__(self):
	#
		"""
Constructor __init__(AbstractFileFormProcessor)

:since: v0.1.00
		"""

		self.form = None
		"""
Form instance
		"""
		self.settings = { }
		"""
Processing settings dict
		"""
	#

	def execute(self):
	#
		"""
Executes the processor.

:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	def set_form(self, form):
	#
		"""
Sets the given form.

:param form: Form instance

:since: v0.1.00
		"""

		if (not isinstance(form, FormProcessor)): raise ValueException("Form instance given is not valid")
		self.form = form
	#

	def set_settings(self, data):
	#
		"""
Sets the given settings.

:param data: Processing settings dict

:since: v0.1.00
		"""

		if (not self.validate_settings(data)): raise ValueException("Missing required values in given settings dict")
		self.settings = data
	#

	def validate_settings(self, data):
	#
		"""
Called to validate the given settings.

:param data: Setting dict to be verified

:since: v0.1.00
		"""

		raise NotImplementedException()
	#
#

##j## EOF