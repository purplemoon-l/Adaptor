from flask import Flask, Response
import pandas as pd
import psycopg2 
import pandas.io.sql as psql
import subprocess
from flask import render_template
from flask import request
import tkinter
from tkinter import filedialog
import shutil
from pathlib import Path

import IO
import os
#import test
import json
app = Flask(__name__)
 #

@app.route("/")
def main():
	root = tkinter.Tk()
	filename = filedialog.askopenfile(parent=root,mode='rb',title='Choose a file').name
	os.rename(filename,"test.py")
	mypath = Path().absolute()
	#shutil.copy(filename, mypath)
	import test
	if os.path.exists('data.txt'):
		print("file exists")
		with open('data.txt') as json_file:
			data = json.load(json_file)
			for p in data['data']:
				db_name=p['db_name']
				table_name=p['table_name']
				column_names=p['column_names']
				predict_names=p['predict_names']
				password=p['password']
				print("Passwordddddddddd                ",password)
		data=IO.inp(db_name,table_name,password)
		if(data.empty):
			print("no new data")
		else:	        
			output =test.ml(data,db_name,table_name,column_names,predict_names,password)        
		return render_template('exist.html') 
	
	return render_template('index.html')

# @app.route('/', methods=['POST'])
# def my_form_get():

@app.route('/', methods=['POST'])
def get_database_info(host='localhost', user='postgres'):
	print(request.json['flag'])
	flag = request.json['flag']
	pas=request.json['password']
	# root = tkinter.Tk()
	# filename = filedialog.askopenfile(parent=root,mode='rb',title='Choose a file').name
	# os.rename(filename,"test.py")
	# mypath = Path().absolute()
	#shutil.copy(filename, mypath)
	import test
	if(flag == "1"):
		print("ajshdbsahjdbhsajdbas       ",pas)
		ps="sundar10"
		hs="localhost"
		user="postgres"
		remote_connection_str = 'host={0} user={1} password={2}'.format(hs,user,pas)
		conn=psycopg2.connect( remote_connection_str)
		cursor = conn.cursor()
		cursor.execute("SELECT datname FROM pg_database")
		dbnames = [row[0] for row in cursor]
		return str(dbnames)

	elif(flag== "2"):
		db_name = request.json['db_name']
		print(db_name)
		conn=psycopg2.connect(database=db_name, user = "postgres", password = pas, host = "localhost")
		cur = conn.cursor()
		cur.execute("""SELECT table_name FROM information_schema.tables
			WHERE table_schema = 'public'""")
		ar=[]
		tables=[]
		for table in cur.fetchall():
			ar.append(table)
		for i in ar:
			tables.append(i[0])
		print(tables)
		return str(tables)
	elif(flag == "3"):
		db_name = request.json['db_name']
		table_name=request.json['tbl_name']
		conn=psycopg2.connect(database=db_name, user = "postgres", password = pas, host = "localhost")
		cursor = conn.cursor()
		cursor.execute("select column_name from information_schema.columns where table_name='"+table_name+"'")
		column_names = [row[0] for row in cursor]
		column_names.remove('predictedoutput')
		column_names.remove('id')
		column_names.remove('flag')
		return str(column_names)
	elif(flag == "4"):
		db_name = request.json['db_name']
		table_name=request.json['tbl_name']		
		column_names=request.json['clm_names']
		predict_names=request.json['pred_names']
		param=request.json['param'] 
		file_name=request.json['file_name']
		f= open("filename.txt","w+")
		f.write("%s" % file_name)
		data=IO.inp(db_name,table_name,pas)

		if(data.empty):
			print("no new data")
			flag=0
		else:
			print("pas in App.py     ",pas)
			
			IO.jsonfile(db_name,table_name,predict_names,column_names,pas)	        
			output =test.ml(data,db_name,table_name,column_names,predict_names,pas)
			connection=psycopg2.connect(database=db_name, user = "postgres", password = pas, host = "localhost")
			df=""
			df=pd.read_sql_query("SELECT *FROM "+table_name+" WHERE predictedoutput is not null;",connection)
			df=df.head(10)
			flag=1
			s="<table border=\"1\" style=\"width\">"
			i=1
			for index, row in df.iterrows():
				s+="<tr>"
				if(i<2):
					for j, column in row.iteritems():
						s+="<th>"
						s+=str(j)
						s+="</th>"
				else:
					break
				i=i+1	
				s+="</tr>"	
			for i, row in df.iterrows():
				s=s+"<tr>"
				for j, column in row.iteritems():
					s+="<td>"
					s+=str(column)
					s+="</td>"
				s=s+"</tr>"
			s+="</table>"
			#output.append(df.head(10))
			outp=[output,s]
		IO.flag1(db_name,table_name,column_names,predict_names)
		if(flag==0):
			return ("No new data")
		return str(outp)	
		

if __name__ == "__main__":
    app.run(debug=True)
