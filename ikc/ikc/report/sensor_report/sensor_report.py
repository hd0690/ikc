# Copyright (c) 2013, IK control and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	if filters.get('from_datetime') and filters.get('to_datetime'):
		if filters.from_datetime > filters.to_datetime:
			frappe.throw(_("From Datetime should be less than To Datetime."))

	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_data(filters):
	
	condition = ''
	frappe.errprint(filters)
	if filters:
		if filters.get('from_datetime') and filters.get('to_datetime'):
			condition = " WHERE timestamp between %(from_datetime)s and %(to_datetime)s"
		elif filters.get('from_datetime'):
			condition = " WHERE timestamp >= %(from_datetime)s "
		elif filters.get('to_datetime'):
			condition = " WHERE timestamp <= %(to_datetime)s "


	data = frappe.db.sql("""
		SELECT 
			timestamp, drain_temperature , chamber_pressure , f0_value
		FROM
			`tabPeriodic Sensor Data`
		{condition}""".format(condition=condition), values=filters, as_dict=1)

	return data

def get_columns():
	return [{
		"fieldname": "timestamp",
		"label": _("Timestamp"),
		"fieldtype": "Data",
		"width": 150
	},
	{
		"fieldname": "drain_temperature",
		"label": _("Drain Temperature"),
		"fieldtype": "Float",
		"width": 150
	},
	{
		"fieldname": "chamber_pressure",
		"label": _("Chamber Pressure"),
		"fieldtype": "Float",
		"width": 150
	},
	{
		"fieldname": "f0_value",
		"label": _("F0 Value"),
		"fieldtype": "Float",
		"width": 150
	}]
