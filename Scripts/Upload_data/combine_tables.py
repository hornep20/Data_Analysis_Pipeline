##### INITIALIZE ##################################################################################
# Imports
import getopt
import ioFunctions as fnc
import databaseUtils as db
import sys
import pandas as pd
import psycopg2

##### Combine NC BIRTH DATA ###################################################################
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

    # Care Tables
    table_care_2016 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'care_2016'), con=conn)
    table_care_2017 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'care_2017'), con=conn)
    table_care_2018 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'care_2018'), con=conn)
    table_care_2019 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'care_2019'), con=conn)

    # Gender Tables 
    table_gender_2016 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'gender_2016'), con=conn)
    table_gender_2017 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'gender_2017'), con=conn)
    table_gender_2018 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'gender_2018'), con=conn)
    table_gender_2019 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'gender_2019'), con=conn)

    # Plurality Tables
    table_plural_2016 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'plural_2016'), con=conn)
    table_plural_2017 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'plural_2017'), con=conn)
    table_plural_2018 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'plural_2018'), con=conn)
    table_plural_2019 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'plural_2019'), con=conn)

    # Race Tables
    table_race_2016 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'race_2016'), con=conn)
    table_race_2017 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'race_2017'), con=conn)
    table_race_2018 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'race_2018'), con=conn)
    table_race_2019 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'race_2019'), con=conn)

    # WeightTables
    table_weight_2016 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'weight_2016'), con=conn)
    table_weight_2017 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'weight_2017'), con=conn)
    table_weight_2018 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'weight_2018'), con=conn)
    table_weight_2019 = pd.read_sql_query('SELECT * FROM {}.{};'.format(schema,'weight_2019'), con=conn)

    # Census Table
    table_census_total = pd.read_sql_query('SELECT * FROM {}.{}'.format(schema, 'census'), con=conn)
    table_census_2016 = table_census_total[['counties','pop_2016']]
    table_census_2016['year'] = '2016'
    table_census_2016 = table_census_2016.rename(columns = {'pop_2016' : 'pop'})

    table_census_2017 = table_census_total[['counties','pop_2017']]
    table_census_2017['year'] = '2017'
    table_census_2017 = table_census_2017.rename(columns = {'pop_2017' : 'pop'})

    table_census_2018 = table_census_total[['counties','pop_2018']]
    table_census_2018['year'] = '2018'
    table_census_2018 = table_census_2018.rename(columns = {'pop_2018' : 'pop'})

    table_census_2019 = table_census_total[['counties','pop_2019']]
    table_census_2019['year'] = '2019'
    table_census_2019 = table_census_2019.rename(columns = {'pop_2019' : 'pop'})
    
    # Appending like tables together
    table_care = table_care_2016.append([table_care_2017, table_care_2018,
        table_care_2019], ignore_index=True)
    table_gender = table_gender_2016.append([table_gender_2017, table_gender_2018,
        table_gender_2019], ignore_index=True)   
    table_plural = table_plural_2016.append([table_plural_2017, table_plural_2018,
        table_plural_2019], ignore_index=True)
    table_race = table_race_2016.append([table_race_2017, table_race_2018,
        table_race_2019], ignore_index=True)
    table_weight = table_weight_2016.append([table_weight_2017, table_weight_2018,
        table_weight_2019], ignore_index=True)
    table_census = table_census_2016.append([table_census_2017, table_census_2018,
        table_census_2019], ignore_index=True)

    # Merging tables and dropping total columns
    table_totals = table_care.merge(table_gender, how='inner', on =['counties', 'year'])
    table_totals = table_totals.merge(table_plural, how='inner', on =['counties', 'year'])
    table_totals = table_totals.merge(table_race, how='inner', on =['counties', 'year'])
    table_totals = table_totals.merge(table_weight, how='inner', on =['counties', 'year'])
    table_totals = table_totals.merge(table_census, how='inner', on =['counties', 'year']) 
    table_totals = table_totals.drop(['total_care', 'total_gender', 
        'total_plural', 'total_race', 'total_weight'], axis=1) 
  

    fnc.copyFromDF(schema, 'care_total', table_care, connDetails)
    fnc.copyFromDF(schema, 'gender_total', table_gender, connDetails)
    fnc.copyFromDF(schema, 'plural_total', table_plural, connDetails)
    fnc.copyFromDF(schema, 'race_total', table_race, connDetails)
    fnc.copyFromDF(schema, 'weight_total', table_weight, connDetails)
    fnc.copyFromDF(schema, 'total', table_totals, connDetails)

    # Clear dict
    del connDetails


##### MAIN #####################################################################
if __name__ == "__main__":
    # Help/error text
    help = 'combine_tables.py -h|--host <host> -p|--port <port> -d|--dbname <dbname> -U|--user <user> -P|--password <password>'
    
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