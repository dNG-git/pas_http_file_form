# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.module.blocks.services.FileForm
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

from os import path
import os
import re

from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.cached_json_file import CachedJsonFile
from dNG.pas.data.settings import Settings
from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.data.http.form.abstract_file_form_processor import AbstractFileFormProcessor
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.notification_store import NotificationStore
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hooks import Hooks
from .module import Module

class FileForm(Module):
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

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.1.00
		"""

		self.execute_form()
	#

	def execute_form(self, is_save_mode = False):
	#
		"""
Action for "form"

:since: v0.1.00
		"""

		form_id = InputFilter.filter_file_path(self.request.get_dsd("fid", ""))

		source_iline = InputFilter.filter_control_chars(self.request.get_dsd("source", "")).strip()
		target_iline = InputFilter.filter_control_chars(self.request.get_dsd("target", "")).strip()

		source = (Link.query_param_encode(source_iline) if (source_iline != "") else "")
		target = ""

		if (target_iline != ""): target = Link.query_param_encode(target_iline)
		else:
		#
			target_iline = (
				source_iline
				if (source_iline != "") else
				"s=file_form;dsd=fid+{0}".format(Link.query_param_encode(form_id))
			)
		#

		Hooks.call("dNG.pas.http.l10n.services.FileForm.init", form_id = form_id)
		L10n.init("pas_http_file_form")

		Link.store_set("servicemenu", Link.TYPE_RELATIVE, L10n.get("core_back"), { "__query__": re.sub("\\[\\w+\\]", "", source_iline) }, image = "mini_default_back", priority = 2)

		file_pathname = path.abspath("{0}/forms/{1}.json".format(Settings.get("path_data"), form_id))

		if (
			(not path.exists(file_pathname)) or
			(not os.access(file_pathname, os.R_OK))
		): raise TranslatableException("pas_http_file_form_not_found", 404)

		file_data = CachedJsonFile.read(file_pathname)
		lang = self.request.get_lang()

		if (
			file_data == None or
			(("form_{0}".format(lang) not in file_data) and ("form" not in file_data)) or
			"execution" not in file_data or
			(not isinstance(file_data['execution'], dict)) or
			"processor" not in file_data['execution'] or
			(("title_{0}".format(lang) not in file_data) and ("title" not in file_data))
		): raise TranslatableException("pas_http_file_form_not_supported", 500)

		if (
			source_iline == "" and
			(("html_back_url_{0}".format(lang) not in file_data) and ("html_back_url" not in file_data))
		):
		#
			Link.store_set(
				"servicemenu",
				Link.TYPE_RELATIVE,
				L10n.get("core_back"),
				{ "__query__": (file_data["html_back_url_{0}".format(lang)] if ("html_back_url_{0}".format(lang) in file_data) else file_data['html_back_url']) },
				image = "mini_default_back",
				priority = 2
			)
		#

		form = NamedLoader.get_instance("dNG.pas.data.xhtml.form.Processor")
		if (is_save_mode): form.set_input_available()

		processor = NamedLoader.get_instance(file_data['execution']['processor'])

		if (
			(not isinstance(processor, AbstractFileFormProcessor)) or
			(not processor.validate_settings(file_data['execution']))
		): raise TranslatableException("pas_http_file_form_not_supported", 500)

		form.set_data(file_data["form_{0}".format(lang)] if ("form_{0}".format(lang) in file_data) else file_data['form'])

		if (is_save_mode and form.check()):
		#
			processor.set_form(form)
			processor.set_settings(file_data['execution'])

			processor.execute()

			target_iline = re.sub("\\[\\w+\\]", "", target_iline)

			title = (file_data["title_{0}".format(lang)] if ("title_{0}".format(lang) in file_data) else file_data['title'])

			if ("html_done_message_{0}".format(lang) in file_data): html_info = file_data["html_done_message_{0}".format(lang)]
			elif ("html_done_message" in file_data): html_info = file_data['html_done_message']
			else: html_info = L10n.get("pas_http_file_form_done_message")

			NotificationStore.get_instance().add_completed_info(html_info)

			Link.store_clear("servicemenu")

			redirect_request = PredefinedHttpRequest()
			redirect_request.set_iline(target_iline)
			self.request.redirect(redirect_request)
		#
		else:
		#
			title = (file_data["title_{0}".format(lang)] if ("title_{0}".format(lang) in file_data) else file_data['title'])

			if ("html_title_{0}".format(lang) in file_data): html_title = file_data["html_title_{0}".format(lang)]
			elif ("html_title" in file_data): html_title = file_data['html_title']
			else: html_title = Formatting.escape(title)

			content = { "title": html_title }

			content['form'] = {
				"object": form,
				"url_parameters": { "__request__": True, "a": "form-save", "dsd": { "source": source, "target": target } },
				"button_title": "core_continue"
			}

			self.response.init()
			self.response.set_title(title)
			self.response.add_oset_content("core.form", content)
		#
	#

	def execute_form_save(self):
	#
		"""
Action for "form-save"

:since: v0.1.00
		"""

		self.execute_form(True)
	#
#

##j## EOF