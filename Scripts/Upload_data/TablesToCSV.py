##### INITIALIZE ##################################################################################
# Imports
import getopt
import ioFunctions as fnc
import databaseUtils as db
import sys
import pandas as pd
import psycopg2

##### Write Tables ###################################################################
schema = 'finalproject'

# Load the data
def load(host, port, dbname, schema, user, password):
    # Set each variable in the dictionary.
    conn = None
    try:
        conn = psycopg2.connect(
            host = host,
            port = port,
            dbname = dbname,
            user = user,
            password = password
    )
        print('Connection Successful')
    except:
        print(host, port, dbname, schema, user, password)

    connDetails = {
        'host'      : host,
        'port'      : port,
        'dbname'    : dbname,
        'user'      : user,
        'password'  : password
    }
    #Reading in total table
    table1 = 'total'
    table_total = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,table1), con = conn)

    #Reading in census table
    table2 = 'census'
    table_census = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,table2), con = conn)

    #Write total to csv
    table_total.to_csv('Output/table_total.csv', index=False)
    table_census.to_csv('Output/table_census.csv', index=False)
    
    # Clear dict
    del connDetails


##### MAIN #####################################################################
if __name__ == "__main__":
    # Help/error text
    help = 'combine_data.py -h|--host <host> -p|--port <port> -d|--dbname <dbname> -U|--user <user> -P|--password <password>'
    
    # Variables
    host = ''
    port = 0
    dbname = ''
    schema = ''
    user = ''
    password = ''
    
    # Verify arguments
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"h:p:d:s:U:P:",["help=","host=","port=","dbname=","schema=","user=","password="])
    except getopt.GetoptError:
        print(help)
        sys.exit(2)
    
    # Extract arguments
    for opt, arg in opts:
        if opt == '--help':
            print(help)
            sys.exit()
        elif opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-d", "--dbname"):
            dbname = arg
        elif opt in ("-s", "--schema"):
            schema = arg
        elif opt in ("-U", "--user"):
            user = arg
        elif opt in ("-P", "--password"):
            password = arg
    
    # Load data
    load(host, port, dbname, schema, user, password)
    
    # Clear memory
    del host
    del port
    del dbname
    del schema
    del user
    del password
