frappe.ui.form.on("ToDo", {
	validate(frm) {
		console.log(" Trigger function FROM apps/test_app/test_app/test_app/customization/todo/todo.js");
		test_app.todo.todo.demo(frm.doc.priority)
	}
});

