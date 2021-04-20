# -*- coding: utf-8 -*-
# Copyright (c) 2021, firsterp and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
import os, json
from frappe import _

class QuotaSetting(Document):
	def populate_quota(self):
		site_path = "../sites/{}/".format(self.name)
		usage = {}
		if os.path.isfile("../sites/{}/quota.json".format(self.site)):
			with open(os.path.join(site_path, 'quota.json')) as jsonfile:
				parsed = json.load(jsonfile)

			for key, value in parsed.items():
				usage[key] = value

			for key, value in usage.items():
				if key in self.as_dict().keys():
					self.db_set(key, value)
			# frappe.set_value(self.doctype,self.name,"site_usage",parsed)
			frappe.db.commit()
		else:
			frappe.log_error(_('quota.json does not exist for site {}').format(self.site),"Quota Setting Creation Error")
	
	def onload(self):
		self.populate_quota()	

	def after_insert(self):
		self.populate_quota()
