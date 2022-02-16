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
connection=psycopg2.connect(database="test", user = "postgres", password = "sundar10", host = "localhost")
df=""
df=pd.read_sql_query("SELECT *FROM stud",connection)
s=''
# for i in range(0, len(df)):
# 	s=s+df.iloc[i]
s+=str(next(df.iterrows()))
i=1
for index, row in df.iterrows():

	if(i<2):
		for j, column in row.iteritems():
			print(j)
	else:
		break
	i=i+1		
	        
