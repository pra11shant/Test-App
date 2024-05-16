import frappe
from frappe import _


def validate_custom_code(doc):
	# do_something
	frappe.msgprint(_("Message From actual_code_file.py file"))