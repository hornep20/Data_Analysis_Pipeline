#!/bin/bash
# TextEdit -> Format -> Make Plain Text -> OK
# ---------------------------------------------------------------
#  PostgreSQL: Connection details and psql path
# ---------------------------------------------------------------
host=localhost
port=5432
dbname=cohe_6590_armc
user=cohe_armc
schema=finalproject
postgres=/Library/PostgreSQL/13/bin/psql

# ---------------------------------------------------------------
# PostgreSQL: Password environment variable
# ---------------------------------------------------------------
export PGPASSWORD=cohe_armc_password

# ---------------------------------------------------------------
# Python: Anaconda activate and python paths
# ---------------------------------------------------------------
activate_anaconda=/Users/Patrick/Desktop/MS_Data_Science/anaconda3/bin/activate
python=/Users/Patrick/Desktop/MS_Data_Science/anaconda3/bin/python

# ---------------------------------------------------------------
# Directories
# ---------------------------------------------------------------
data_dir=Data
upload_dir=Scripts/Upload_data
sql_dir=SQL

# ---------------------------------------------------------------
# 2016-2019 Tables
# ---------------------------------------------------------------
schema_init_sql=$sql_dir/table_init.sql 
data_load_py=$upload_dir/load_tables.py
data_combine_py=$upload_dir/combine_tables.py 
export_data_py=$upload_dir/TablesToCSV.py

