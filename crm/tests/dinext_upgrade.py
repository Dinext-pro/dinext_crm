"""Synthetic upgrade fixtures, available only through Frappe's test-server gate."""
import frappe
from frappe import _
from frappe.tests.ui_test_helpers import whitelist_for_tests
from frappe.utils.password import update_password

USER = "upgrade-crm@example.com"
TITLE = "Dinext upgrade smoke"


def _require_test_site():
	if not frappe.conf.allow_tests or not (frappe.flags.in_test or getattr(frappe.local, "dev_server", False)):
		frappe.throw(_("Upgrade fixtures require an enabled development test site"), frappe.PermissionError)
	frappe.only_for("System Manager")


@whitelist_for_tests
def csrf():
	_require_test_site()
	return frappe.sessions.get_csrf_token()


@whitelist_for_tests
def cleanup():
	_require_test_site()
	if frappe.db.get_value("CRM Form Script", "Dinext upgrade form script", "owner") == USER:
		frappe.delete_doc("CRM Form Script", "Dinext upgrade form script", force=True, ignore_permissions=True)
	for name in frappe.get_all("CRM Lead", filters={"first_name": TITLE, "owner": USER}, pluck="name"):
		frappe.delete_doc("CRM Lead", name, force=True, ignore_permissions=True)
	if frappe.db.exists("User", USER):
		frappe.delete_doc("User", USER, force=True, ignore_permissions=True)


@whitelist_for_tests
def prepare():
	_require_test_site()
	cleanup()
	password = frappe.generate_hash(length=24)
	user = frappe.get_doc({
		"doctype": "User", "email": USER, "first_name": "Administrator Upgrade Test",
		"send_welcome_email": 0, "user_type": "System User", "language": "en",
	})
	user.insert(ignore_permissions=True)
	roles = [r for r in ['System Manager', 'Sales User', 'Sales Manager'] if frappe.db.exists("Role", r)]
	user.add_roles(*roles)
	update_password(USER, password)
	result = {"user": USER, "password": password, "title": TITLE}
	lead = frappe.get_doc({"doctype": "CRM Lead", "first_name": TITLE, "owner": USER}).insert()
	frappe.get_doc({
		"doctype": "CRM Form Script", "name": "Dinext upgrade form script",
		"dt": "CRM Lead", "view": "Form", "enabled": 1, "owner": USER,
		"script": '''class CRMLead {
  onLoad() {
    this.actions = [{ label: "Verify form script", onClick: () => this.toast.success("Form script verified") }]
  }
}''',
	}).insert()
	result["lead"] = lead.name
	return result
