# -*- coding: utf-8 -*-
# Copyright (c) 2019, IK control and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, now, get_datetime

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

import time

# TODO: Uncomment Modbus communication
# client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

@frappe.whitelist()
def get_sensor_data():
	"""
		Runs every second to get data from PLC and store into Periodic Sensor Data
	"""
	# TODO: Override this function with _get_sensor_data
	# test_data()
	_get_sensor_data()

def test_data():
	# client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)
	# if True:
	if client.connect():
		
		for _ in xrange(60):
			if get_datetime().minute == 0 and get_datetime().second == 0:
				frappe.db.sql(""" DELETE from `tabTEST` """)

			drain_temperature = get_address_value(217, client)
			chamber_pressure = get_address_value(237, client)

			f0_value = get_address_value(241, client)
			# f0_value = "-1.32775488438e+38"
			
			# doc = frappe.new_doc("TEST")
			# doc.one = result.registers[0]
			# doc.two = result.registers[1]
			# doc.three = result.registers[2]
			# doc.four = result.registers[3]
			# doc.five = result.registers[4]
			# doc.six = result.registers[5]
			frappe.get_doc({
				'doctype': "TEST",
				'one': flt(drain_temperature),
				'two': flt(chamber_pressure),
				'three': 0,
				'four': 0,
				'five': 0,
				'six': 0,
			}).insert()
			frappe.db.commit()
			time.sleep(1)

def get_address_value(address, client):
	"""
	Returns float value of PLC address
	:param address : address number in integer
	:param client : client object
	"""
	result = client.read_holding_registers(address, 2, unit=1)
	decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Little, wordorder=Endian.Little)
	return str(decoder.decode_32bit_float())

# TODO: Override function with get_sensor_data
def _get_sensor_data():
	starttime=time.time()
	client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, bytesize=8, parity='N', stopbits=1)

	try:
		client.connect()
	except:
		args = {
			'message': "Cannot connect to PLC. Please check you connection. Trying to reconnect after 1 minute",
			'title': "PLC Connection Error"
		}

		frappe.log_error(**args)
		# Add js to app for frappe.realtime.on
		publish_data(args, 1)
		return

	for _ in range(60):
		""" SENSOR ADDRESSES

		:DRAIN_TEMPERATURE = PLC1[400217]
		:CHAMBER_PRESSURE = PLC1[400237]
		:F0_VALUE = PLC1[400241]
		"""

		# Store sensor values in respected variables

		drain_temperature = get_address_value(217, client)
		chamber_pressure = get_address_value(237, client)
		f0_value = get_address_value(241, client)

		sensor_data = {
			'drain_temperature': drain_temperature,
			'chamber_pressure': chamber_pressure,
			'f0_value': f0_value,
		}

		# doc_dict = {'doctype': "Periodic Sensor Data", 'timestamp': get_datetime().strftime("%Y-%m-%d %H:%M:%S")}
		# doc_dict.update(sensor_data)

		# frappe.get_doc(doc_dict).insert()
		# frappe.db.commit()

		publish_data(sensor_data)
		time.sleep(1 - ((time.time() - starttime)) % 1)

def publish_data(args, error=0):
	if not error:
		event = "periodic_data_results"
	else:
		event = "plc_connectio_error"

	frappe.publish_realtime(event=event, message=args, user=frappe.session.user)