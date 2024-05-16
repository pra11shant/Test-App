(() => {
  // ../test_app/test_app/public/js/todo/todo.js
  frappe.provide("test_app.todo.todo");
  test_app.todo.todo.demo = function(priority) {
    console.log("Priority is: ", priority, "And Call From Inside function Path: apps/test_app/test_app/public/js/todo/todo.js");
  };
  console.log("call from Outer js => Test App");
})();
//# sourceMappingURL=todo.bundle.YKABWWKG.js.map
