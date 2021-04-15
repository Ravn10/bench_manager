import frappe
from frappe.model.document import Document
from subprocess import Popen, PIPE, STDOUT
import re, shlex

@frappe.whitelist(allow_guest=True)
def run_command(commands, doctype, key, cwd='..', docname=' ',site=None,domain=None,after_command=None):
	start_time = frappe.utils.time.time()
	console_dump = ""
	logged_command = " && ".join(commands)
	logged_command += " " #to make sure passwords at the end of the commands are also hidden
	sensitive_data = ["--mariadb-root-password", "--admin-password", "--root-password"]
	for password in sensitive_data:
		logged_command = re.sub("{password} .*? ".format(password=password), '', logged_command, flags=re.DOTALL)
	doc = frappe.get_doc({'doctype': 'Bench Manager Cmd', 'key': key, 'source': doctype+': '+docname,
		'command': logged_command, 'console': console_dump, 'status': 'Ongoing'})
	if site:
		doc.site = site
	if domain:
		doc.domain = domain
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	try:
		for command in commands:
			terminal = Popen(shlex.split(command), stdin=PIPE, stdout=PIPE, stderr=STDOUT, cwd=cwd)
			for c in iter(lambda: safe_decode(terminal.stdout.read(1)), ''):
				console_dump += c
		if terminal.wait():
			doc.status = 'Failed'
			doc.time_taken = start_time
			_close_the_doc(start_time, key, console_dump, status='Failed')
		else:
			doc.status = 'Success'
			doc.time_taken = start_time
			_close_the_doc(start_time, key, console_dump, status='Success')
	except Exception as e:
		_close_the_doc(start_time, key, "{} \n\n{}".format(e, console_dump), status='Failed')
	finally:
		frappe.db.commit()
		frappe.enqueue('bench_manager.bench_manager.custom_utils._refresh',
		doctype=doctype, docname=docname, commands=commands)


def _close_the_doc(start_time, key, console_dump, status):
	time_taken = frappe.utils.time.time() - start_time
	final_console_dump = ''
	console_dump = console_dump.split('\n\r')
	for i in console_dump:
		i = i.split('\r')
		final_console_dump += '\n'+i[-1]
	# frappe.db.sql('''update `tabBench Manager Cmd` set status=%s where key=%s''',(status,key))
	frappe.set_value('Bench Manager Cmd', key, 'console', final_console_dump)
	frappe.set_value('Bench Manager Cmd', key, 'status', status)
	frappe.set_value('Bench Manager Cmd', key, 'time_taken', time_taken)
	
def _refresh(doctype, docname, commands):
	frappe.get_doc(doctype, docname).run_method('after_command', commands=commands)

@frappe.whitelist()
def verify_whitelisted_call():
	if 'bench_manager' not in frappe.get_installed_apps():
		raise ValueError("This site does not have bench manager installed.")

def safe_decode(string, encoding = 'utf-8'):
	try:
		string = string.decode(encoding)
	except Exception:
		pass
	return string

@frappe.whitelist(allow_guest=True)
def setup_nginx_conf():
	import subprocess
	process = subprocess.Popen("bench setup nginx", stdin=subprocess.PIPE, shell=True)
	process.stdin.write(b"y\n")
	process.stdin.flush()
	stdout, stderr = process.communicate()
	subprocess.call('sudo service nginx reload',shell=True)