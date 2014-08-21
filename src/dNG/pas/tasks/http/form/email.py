# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;http;user

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpFileFormVersion)#
#echo(__FILEPATH__)#
"""

from dNG.data.rfc.email.message import Message
from dNG.data.rfc.email.part import Part
from dNG.pas.data.settings import Settings
from dNG.pas.data.text.email_renderer import EMailRenderer
from dNG.pas.data.text.l10n import L10n
from dNG.pas.net.smtp.client import Client as SmtpClient
from dNG.pas.tasks.abstract import Abstract as AbstractTask

class EMail(AbstractTask):
#
	"""
The "EMail" task will send a given e-mail based on a parsed form.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: file_form
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, lang, sender, subject, content, recipient = None):
	#
		"""
Constructor __init__(EMail)

:param lang: e-mail language
:param sender: e-mail sender
:param subject: e-mail subject
:param content: e-mail content
:param recipient: e-mail recipient

:since: v0.1.00
		"""

		AbstractTask.__init__(self)

		self.content = content
		"""
e-mail content to send
		"""
		self.l10n = L10n.get_instance(lang)
		"""
L10n instance
		"""
		self.recipient = recipient
		"""
e-mail recipient if not "pas_email_recipient_notifications"
		"""
		self.sender = sender
		"""
e-mail sender
		"""
		self.subject = subject
		"""
e-mail subject
		"""

		Settings.read_file("{0}/settings/pas_email.json".format(Settings.get("path_data")))
	#

	def run(self):
	#
		"""
Task execution

:since: v0.1.00
		"""

		content = EMailRenderer(self.l10n).render(self.content, EMailRenderer.REASON_ON_DEMAND)
		part = Part(Part.TYPE_MESSAGE_BODY, "text/plain", content)

		recipient = (Settings.get("pas_email_recipient_notifications") if (self.recipient == None) else self.recipient)

		message = Message()
		message.add_body(part)
		if (self.sender != None): message.set_from(self.sender)
		message.set_subject(self.subject)
		message.set_to(recipient)

		smtp_client = SmtpClient()
		smtp_client.set_message(message)
		smtp_client.send()
	#
#

##j## EOF