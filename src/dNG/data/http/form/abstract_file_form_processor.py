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

from dNG.data.xhtml.form.processor import Processor
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.value_exception import ValueException

class AbstractFileFormProcessor(object):
#
	"""
"AbstractFileFormProcessor" defines common methods to develop different
processors based on a definition file.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: file_form
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

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

		if (not isinstance(form, Processor)): raise ValueException("Form instance given is not valid")
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