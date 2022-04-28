#!/bin/bash
# ---------------------------------------------------------------
#  PostgreSQL: Connection details and psql path
# ---------------------------------------------------------------
host=localhost
port=5432
dbname=cohe_6590_armc
user=cohe_armc
schema=finalproject
postgres=your-path-here

# ---------------------------------------------------------------
# PostgreSQL: Password environment variable
# ---------------------------------------------------------------
export PGPASSWORD=cohe_armc_password

# ---------------------------------------------------------------
# Python: Anaconda activate and python paths
# ---------------------------------------------------------------
activate_anaconda=your-path-here
python=your-path-here

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

