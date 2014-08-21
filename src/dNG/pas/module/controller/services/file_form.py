# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;core

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpFileFormVersion)#
#echo(__FILEPATH__)#
"""

from os import path
import os
import re

from dNG.pas.controller.predefined_http_request import PredefinedHttpRequest
from dNG.pas.data.settings import Settings
from dNG.pas.data.cache.json_file_content import JsonFileContent
from dNG.pas.data.http.translatable_error import TranslatableError
from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.data.http.form.abstract_file_form_processor import AbstractFileFormProcessor
from dNG.pas.data.text.input_filter import InputFilter
from dNG.pas.data.text.l10n import L10n
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.notification_store import NotificationStore
from dNG.pas.data.xhtml.form.processor import Processor as FormProcessor
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook
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
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
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

		source = source_iline

		target = target_iline

		if (target_iline == ""):
		#
			target_iline = (source_iline
			                if (source_iline != "") else
			                "s=file_form;dsd=fid+{0}".format(Link.encode_query_value(form_id))
			               )
		#

		Hook.call("dNG.pas.http.l10n.services.FileForm.init", form_id = form_id)
		L10n.init("pas_http_file_form")

		if (self.response.is_supported("html_css_files")): self.response.add_theme_css_file("mini_default_sprite.min.css")

		Link.set_store("servicemenu",
		               Link.TYPE_RELATIVE,
		               L10n.get("core_back"),
		               { "__query__": re.sub("\\_\\_\\w+\\_\\_", "", source_iline) },
		               icon = "mini-default-back",
		               priority = 7
		              )

		file_pathname = path.abspath("{0}/forms/{1}.json".format(Settings.get("path_data"), form_id))

		if ((not path.exists(file_pathname))
		    or (not os.access(file_pathname, os.R_OK))
		   ): raise TranslatableError("pas_http_file_form_not_found", 404)

		file_data = JsonFileContent.read(file_pathname)
		lang = self.request.get_lang()

		if (file_data == None
		    or (("form_{0}".format(lang) not in file_data) and ("form" not in file_data))
		    or "execution" not in file_data
		    or (not isinstance(file_data['execution'], dict))
		    or "processor" not in file_data['execution']
		    or (("title_{0}".format(lang) not in file_data) and ("title" not in file_data))
		   ): raise TranslatableException("pas_http_file_form_not_supported")

		if (source_iline == ""
		    and (("html_back_url_{0}".format(lang) not in file_data) and ("html_back_url" not in file_data))
		   ):
		#
			Link.set_store("servicemenu",
			               Link.TYPE_RELATIVE,
			               L10n.get("core_back"),
			               { "__query__": (file_data["html_back_url_{0}".format(lang)]
			                               if ("html_back_url_{0}".format(lang) in file_data) else
			                               file_data['html_back_url']
			                              )
			               },
			               icon = "mini-default-back",
			               priority = 7
			              )
		#

		form_id = InputFilter.filter_control_chars(self.request.get_parameter("form_id"))

		form = FormProcessor(form_id)
		if (is_save_mode): form.set_input_available()

		processor = NamedLoader.get_instance(file_data['execution']['processor'])

		if ((not isinstance(processor, AbstractFileFormProcessor))
		    or (not processor.validate_settings(file_data['execution']))
		   ): raise TranslatableException("pas_http_file_form_not_supported")

		form.load_definition(file_data["form_{0}".format(lang)] if ("form_{0}".format(lang) in file_data) else file_data['form'])

		if (is_save_mode and form.check()):
		#
			processor.set_form(form)
			processor.set_settings(file_data['execution'])

			processor.execute()

			target_iline = re.sub("\\_\\_\\w+\\_\\_", "", target_iline)

			title = (file_data["title_{0}".format(lang)] if ("title_{0}".format(lang) in file_data) else file_data['title'])

			if ("html_done_message_{0}".format(lang) in file_data): html_info = file_data["html_done_message_{0}".format(lang)]
			elif ("html_done_message" in file_data): html_info = file_data['html_done_message']
			else: html_info = L10n.get("pas_http_core_form_done_message")

			NotificationStore.get_instance().add_completed_info(html_info)

			Link.clear_store("servicemenu")

			redirect_request = PredefinedHttpRequest()
			redirect_request.set_iline(target_iline)
			self.request.redirect(redirect_request)
		#
		else:
		#
			title = (file_data["title_{0}".format(lang)] if ("title_{0}".format(lang) in file_data) else file_data['title'])

			if ("html_title_{0}".format(lang) in file_data): html_title = file_data["html_title_{0}".format(lang)]
			elif ("html_title" in file_data): html_title = file_data['html_title']
			else: html_title = XHtmlFormatting.escape(title)

			content = { "title": html_title }

			content['form'] = { "object": form,
			                    "url_parameters": { "__request__": True,
			                                        "a": "form-save",
			                                        "dsd": { "source": source, "target": target }
			                                      },
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

		self.execute_form(self.request.get_type() == "POST")
	#
#

##j## EOF