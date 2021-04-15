from __future__ import unicode_literals
from frappe import _


def get_data():
	bench_setup = {
		"label": _("Bench Setup"),
		"icon": "octicon octicon-briefcase",
		"items": [
			{
				"name": "App",
				"type": "doctype",
				"label": _("App"),
				"description": _("Frappe Apps")
			},
			{
				"name": "Site",
				"type": "doctype",
				"label": _("Site"),
				"description": _("Bench Sites")
			}
		]
	}

	bench_management = {
		"label": _("Bench Management"),
		"type": "module",
		"items": [
			{
				"name": "Site Backup",
				"type": "doctype",
				"label": _("Site Backup"),
				"description": _("Site Backup")
			},
			{
				"name": "Prepare Site Request",
				"type": "doctype",
				"label": _("Prepare Site Request"),
				"description": _("Prepare Site Request")
			},
			{
				"name": "Quota Setting",
				"type": "doctype",
				"label": _("Quota Setting"),
				"description": _("Quota Setting")
			},
			{
				"name": "Site Quota Update",
				"type": "doctype",
				"label": _("Site Quota Update"),
				"description": _("Site Quota Update")
			},
			{
				"name": "Bench Manager Cmd",
				"type": "doctype",
				"label": _("Bench Manager Cmd"),
				"description": _("Bench Manager Cmd")
			},
			{
				"name": "Bench Settings",
				"type": "doctype",
				"label": _("Bench Settings"),
				"description": _("Bench Settings")
			}
		]
	}

	return [
		bench_setup,
		bench_management
	]
