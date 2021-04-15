# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from shutil import copyfile
from frappe.utils import  nowdate #, cstr, flt, cint, now, getdate
import os, json
from frappe import _
from frappe.email import sendmail_to_system_managers

class SiteQuotaUpdate(Document):
	def on_submit(self):
		# if quota.json exists create a bkp
		if os.path.isfile("../sites/{}/quota.json".format(self.site)):
			bkp_file_name = 'quota.json' +'-'+format(nowdate())+'-'+self.name
			bkp_file_path = "../sites/{0}/{1}".format(self.site,bkp_file_name)
			site_quota_file_path = "../sites/{}/quota.json".format(self.site)
			copyfile(site_quota_file_path,bkp_file_path)
			frappe.db.set_value(self.doctype,self.name,"backup_file_path",bkp_file_path)
			with open(site_quota_file_path, "r") as jsonFile:
				data = json.load(jsonFile)
			
			previous_quota = data
			frappe.db.set_value(self.doctype,self.name,"previous_quota",frappe.as_json((previous_quota)))
			data["users"] = self.users
			if self.valid_till:
				data["valid_till"]=self.valid_till
			frappe.db.commit()
			with open(site_quota_file_path, "w") as jsonFile:
				json.dump(data, jsonFile, indent=4)
		
		# else crate a new quota.json

def create_site_quota_update(doc, method=None):
	items = doc.items
	attrubutes_to_be_updated = {}
	for item in items:
		if item.quota_attribute_name:
			attrubutes_to_be_updated.update({item.quota_attribute_name:item.qty})
	
	if attrubutes_to_be_updated:
		quota_update_doc = frappe.get_doc({
											"doctype":"Site Quota Update",
											"customer":doc.customer,
											"site":doc.site,
											"users":int(attrubutes_to_be_updated['users']),
											"reference_doctype":doc.doctype,
											"reference_docname":doc.name
											})
		quota_update_doc.insert(ignore_permissions=True)
		try:
			quota_update_doc.submit()
			# title = _("Site Quota Updated for {0}").format(doc.site)
			# message = _("Quota update against doc {0}").format(quota_update_doc.name)
			# sendmail_to_system_managers(title, message)
		except:
			frappe.db.rollback()
			title = _("Error while submitting quota update doc {0}").format(quota_update_doc.name)
			traceback = frappe.get_traceback()
			frappe.log_error(message=traceback , title=title)
			sendmail_to_system_managers(title, traceback)
