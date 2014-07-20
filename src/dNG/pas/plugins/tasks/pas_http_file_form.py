# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;file_form

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpFileFormProfileVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.plugins.hook import Hook
from dNG.pas.runtime.value_exception import ValueException
from dNG.pas.tasks.http.form.email import EMail

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.http.Form.sendEMail", send_email)
#

def send_email(params, last_return = None):
#
	"""
Called for "dNG.pas.http.Form.sendEMail"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	if (last_return != None): _return = last_return
	elif ("lang" not in params
	      or "sender" not in params
	      or "subject" not in params
	      or "content" not in params
	     ): raise ValueException("Missing required arguments")
	else:
	#
		EMail(params['lang'], params['sender'], params['subject'], params['content'], params.get("recipient")).run()
		_return = True
	#

	return _return
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.http.Form.sendEMail", send_email)
#

##j## EOF