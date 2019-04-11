# Copyright (c) 2013, IK control and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	return columns, data, None, chart

def get_data(filters):
	
	data = frappe.db.sql("""
		SELECT 
			timestamp, drain_temperature , chamber_pressure , f0_value
		FROM
			`tabPeriodic Sensor Data`""", as_dict=1)

	return data

def get_chart_data(data):
	
	drain_temperature, chamber_pressure, f0_value = [], [], []
	labels = []

	for row in data:
		drain_temperature.append(row.drain_temperature)
		chamber_pressure.append(row.chamber_pressure)
		f0_value.append(row.f0_value)
		labels.append(row.timestamp)

	datasets = [{
		"name": "Drain Temperature",
		"values": drain_temperature
	},
	{
		"name": "Chamber Pressure",
		"values": chamber_pressure	
	},
	{
		"name": "F0 Value",
		"values": f0_value
	}]
	
	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}
	chart["type"] = "line"
	return chart

def get_columns():
	return [{
		"fieldname": "timestamp",
		"label": _("Timestamp"),
		"fieldtype": "Datetime",
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
