from application import app

#Menjalankan program utama
if __name__ == "__main__":
	app.secret_key = 'TugasAkhir-1711501559MusPriandi'
	app.run(debug=True, use_reloader=True)