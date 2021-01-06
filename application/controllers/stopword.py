from application.models import Models
from application.excel import Excel
from flask import request

class StopwordController:
	
	def select_dataStopword(self):
		instance_Model = Models('SELECT * FROM tbl_stopword')
		data_stopword = instance_Model.select()
		return data_stopword
	
	def add_dataStopword(self):
		stopword = request.form['stopword'].strip()
	
		instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
		instance_Model.query_sql(stopword.lower())
	
	def update_dataStopword(self):
		id = request.form['id']
		stopword = request.form['stopword'].strip()
	
		data_ubah = (stopword.lower(), id)	# Membuat tupple dari form data masukan
	
		instance_Model = Models('UPDATE tbl_stopword SET stopword=%s WHERE id_stopword = %s')
		instance_Model.query_sql(data_ubah)
	
	def delete_dataStopword(self):
		id = request.form['id']
	
		instance_Model = Models('DELETE FROM tbl_stopword WHERE id_stopword = %s')
		instance_Model.query_sql(id)
		
	def import_fileExcelStopword(self):
		excel_file = request.files['excel_file']

		instance_Excel = Excel()
		tuples_excel = instance_Excel.make_tuples_stopword(excel_file)
		# Simpan ke Database dengan VALUES berupa tuple
		instance_Model = Models('INSERT INTO tbl_stopword(stopword) VALUES (%s)')
		instance_Model.query_sql_multiple(tuples_excel)
		return None	
	