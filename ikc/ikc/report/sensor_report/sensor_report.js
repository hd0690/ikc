// Copyright (c) 2016, IK control and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sensor Report"] = {
	"filters": [
		{
			"fieldname": "from_datetime",
			"label": __("From Datetime"),
			"fieldtype": "Datetime"
		},
		{
			"fieldname": "to_datetime",
			"label": __("To Datetime"),
			"fieldtype": "Datetime"
		}
	]
}
