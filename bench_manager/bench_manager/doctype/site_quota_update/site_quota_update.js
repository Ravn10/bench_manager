// Copyright (c) 2021, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Site Quota Update', {
	onload: function(frm) {
		cur_frm.fields_dict['site'].get_query = function(doc, cdt, cdn) {
			return {
				filters:{'customer': doc.customer}
			}
		}
	}
});
