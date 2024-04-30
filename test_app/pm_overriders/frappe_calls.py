import frappe
from erpnext.crm.doctype.lead.lead import _set_missing_values
from frappe.model.mapper import get_mapped_doc

############################################################################
## Module Name: Installed Base
############################################################################
@frappe.whitelist()
def testdf(self):
	frappe.throw("Hi From pm")
 
@frappe.whitelist()
def get_customer_installed_base(customer):
	if not frappe.db.exists("Installed Base Assets", {"custom_customer_id": customer}):
		return []

	install_base_list = frappe.db.sql(
		""" Select name from `tabInstalled Base Assets` where
			custom_customer_id = "{}" and (is_group = 1 or is_assets = 1)""".format(
			customer
		),
		as_list = 1
	)

	filter_installed_base_list = [item for sublist in install_base_list for item in sublist]

	return filter_installed_base_list or []

############################################################################
## Module Name: Parason Banking Customisations
############################################################################

@frappe.whitelist()
def supplier_advance_account(supplier=None):
    account = None
    if supplier:
        query = f""" select account_for_advance from `tabParty Account`
            where parent = "{supplier}" and parenttype= "Supplier" """
        account = frappe.db.sql(query, pluck='name')[0]
    return account

############################################################################
## Module Name: Parason CRM
############################################################################

@frappe.whitelist()
def fetch_item_expiry(customer=None, item_code=None):
    expiry_days = None

    if customer and item_code:
        query = f""" select expiry_days from `tabCustomer Item Expiry` 
            where parent = "{customer}" and item = "{item_code}" """
        expiry_days = frappe.db.sql(query, pluck='name')

    return expiry_days


@frappe.whitelist()
def create_lead(doctype, docname):
    customer_doc = frappe.get_doc(doctype, docname)

    doc = frappe.new_doc("Lead")
    doc.first_name = customer_doc.customer_name
    doc.company_name = customer_doc.customer_name
    doc.industry = customer_doc.industry
    doc.market_segment = customer_doc.market_segment
    doc.territory = customer_doc.territory
    doc.source = "Existing Customer"
    doc.customer = docname
    doc.annual_revenue = customer_doc.annual_revenue
    doc.no_of_employees = customer_doc.no_of_employees

    #discovery
    doc.custom_business_size = customer_doc.custom_business_size
    doc.custom_capacity_in_tpd = customer_doc.custom_capacity_in_tpd
    doc.custom_capital_equipments = customer_doc.custom_capital_equipments
    
    #address and conatct
    query = f""" select AD.city, AD.state, AD.country, AD.email_id, AD.phone, AD.custom_zone
        from `tabAddress` as AD
        LEFT JOIN `tabDynamic Link` DL
        ON AD.name = DL.parent
        where DL.link_name = "{docname}"
        and DL.parenttype = "Address"
    """
    address = frappe.db.sql(query, as_dict=1)
    if address:
        doc.city = address[0].get('city')
        doc.state = address[0].get('state')
        doc.country = address[0].get('country')
        doc.email_id = address[0].get('email_id')
        doc.mobile_no = address[0].get('phone')
        doc.custom_zone = address[0].get('custom_zone')

    doc.set(frappe.scrub(doctype), docname)
    return doc

@frappe.whitelist()
def lead_create(source_name, target_doc=None):
	target_doc = get_mapped_doc(
		"Lead Enquiry",
		source_name,
		{"Lead Enquiry": {"doctype": "Lead"}},
		target_doc,
	)

	return target_doc

@frappe.whitelist()
def order_create(source_name, target_doc=None):
	def set_missing_values(source, target):
		_set_missing_values(source, target)

	target_doc = get_mapped_doc(
		"Lead",
		source_name,
		{"Lead": {"doctype": "Sales Order", "field_map": {"name": "party_name"}}},
		target_doc,
		set_missing_values,
	)
	
	source_doc = frappe.get_doc("Lead", source_name)
		
	if source_doc.source == "Existing Customer":
		target_doc.customer = source_doc.customer
		
	for item in source_doc.custom_items:
		target_doc.append("items", {
			"item_code": item.item_code,
			"qty": item.qty
		})
	
	
		
	target_doc.run_method("set_missing_values")
	target_doc.run_method("set_other_charges")
	target_doc.run_method("calculate_taxes_and_totals")

	return target_doc
