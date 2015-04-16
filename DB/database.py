import json
import os.path
import math
# import string
from index import Index
import inspect

def string_to_key_value(string=""):
	ret = {"key":"", "value":""}
	if len(string) > 0 and len(string.split("=")) == 2:
		split = string.split("=")
		ret["key"] = split[0]
		ret["value"] = split[1]

	return ret

#Database.py
class Database:
	db_extension = "db"
	save_file_name = ""
	key_database_definition = "DATABASE_DEFINITION"
	key_document_store = "DOCUMENT_STORE"
	key_index_store = "INDEX_STORE"
	name = ""
	
	file = None
	properties_to_indicies = dict()
	document_store = [{}]

	next_id = 1

	allowed_types = [str, int]

	def __init__(self, save_file_name="", name="", file=None):
		self.save_file_name = self.format_save_file_name(save_file_name) if len(save_file_name) > 0 else ""
		self.name = name
		self.file = file

		#if there is no file and no	save_file_name but there is a name, then treat the name as the save filename
		if not self.has_file() and not self.has_save_file_name() and self.has_name():
			self.save_file_name = self.format_save_file_name(self.name)

		#if there is no file provided but a filename, then make the file
		if not self.has_file() and self.has_save_file_name() and not os.path.isfile(self.save_file_name):
			self.create_file(self.save_file_name)

		#if there is no file but there is a save_file_name then load it
		print self.save_file_name
		if not self.has_file() and self.has_save_file_name() and os.path.isfile(self.save_file_name):
			self.create_file(self.save_file_name)
			self.unserialize()

	def save(self):
		if self.has_file():
			serialized = self.serialize()
			json.dump(json.loads(serialized), self.get_file())

	def serialize(self):
		s = "{"
		s += "'name':'" + self.name + "'," 
		s += "'next_id':" + str(self.next_id) + "," 
		s += "'" + self.key_document_store + "':" + str(self.document_store) + ","
		s += "'" + self.key_index_store + " : " + "{"
		for prop, index in self.properties_to_indicies.items():
			s += "'" + str(prop) + "':" + index.serialize() + ","
		s = s[:-1] + "}"
		return s

	def unserialize(self):
		if self.has_file():
			json_data = open(self.save_file_name).read()
			data = json.loads(json_data)
			print data
		

	def load_from_file(self, file):
		return False

	def has_name(self):
		return len(self.name) > 0

	def has_file(self):
		return self.file is not None

	def has_save_file_name(self):
		return len(self.save_file_name) > 0

	def property_index_exists(self, property):
		return property in self.properties_to_indicies

	def format_save_file_name(self, save_file_name=""):
		if len(save_file_name) > 0 and save_file_name.split(".")[-1] is not self.db_extension:
			save_file_name = save_file_name + "." + self.db_extension
		return save_file_name

	def create_file(self, save_file_name):
		self.file = open(self.format_save_file_name(save_file_name), "w+")
		self.file.close()

	def get_file(self):
		return open(self.save_file_name, "w+")
		#self.add_database_definition_to_file(self.file)

	# def add_database_definition_to_file(self, file):
	# 	if not self.file_has_database_definition(file) and self.has_name():
	# 		file.seek(0, 0)
	# 		line = self.key_database_definition + "=" + self.name
	# 		file.write(line)

	# def file_has_database_definition(self, file):
	# 	file.seek(0,0) #it will be on the first line
	# 	line = file.readline()
	# 	kv = string_to_key_value(line)
	# 	return kv["key"] == self.key_database_definition

	

	def apply_id_to(self, thing):
		if hasattr(thing, "id"):
			if type(thing.id) is int:
				thing.id = self.next_id
			elif type(thing.id) is str:
				thing.id = str(self.next_id)
			self.next_id += 1

	def add_document(self, id, document):
		self.document_store.insert(id, document)

	def get_document(self, id):
		if id in range(len(self.document_store)):
			return self.document_store[id]
		else: 
			return ""

	def associate(self, master, slaves):
		masterClass = master.__class__.__name__
		slaveIdAttribute = (masterClass + "_id").lower()
		for slave in slaves:
			setattr(slave, slaveIdAttribute, master.id)
		
	def put(self, thing):
		props = thing.__dict__

		if hasattr(thing, "id"):
			#add an auto_increment id if dne
			if (type(thing.id) is int and thing.id <= 0) or (type(thing.id) is str and len(thing.id) <= 0): 
				self.apply_id_to(thing)
				self.add_document(thing.id, thing.serialize())

			for prop in props:
				value = getattr(thing, prop)

				if prop is "id":
					#self.put_thing_property(prop, thing.serialize(), thing.id)
					continue
				elif type(value) is list:
					#if we encounter a list, that means this object owns the list elements, in which case we need to make that foreign reference
					self.associate(thing, value)
					for item in value:
						self.put(item)
				else:
					self.put_thing_property(prop, value, thing.id)

		else:
			print("!!!! Things must have ids to be put !!!!")	
			

	def put_thing_property(self, property, property_value, id):
		if not self.property_index_exists(property):
			#create it
			self.properties_to_indicies[property] = Index(property)

		if property_value:
			self.properties_to_indicies[property].put(str(property_value), id)

	def get(self, prop, q):
		#for now just search with basic strings
		#also for now do it serially
		hits = ()
		if prop in self.properties_to_indicies:
			index = self.properties_to_indicies[prop]
			hits = index.get(q)

		return map(self.get_document, list(hits))

	def has(self, q):
		return False

