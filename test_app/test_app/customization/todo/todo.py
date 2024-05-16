import frappe
from test_app.test_app.customization.todo.doc_event.actual_code_file import validate_custom_code
from frappe.desk.doctype.todo.todo import ToDo

def validate(doc, method=None):
	validate_custom_code(doc)

class CustomToDo(ToDo):
	def validate(self):
		frappe.msgprint("Massage From Override Class Method")