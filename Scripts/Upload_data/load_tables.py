##### INITIALIZE ##################################################################################
# Imports
import getopt
import ioFunctions as fnc
import sys
import pandas as pd 

# Directory
birth_dir = 'Data/'

# Weight Tables
table_weight_2016 = 'weight_2016'
table_weight_2017 = 'weight_2017'
table_weight_2018 = 'weight_2018'
table_weight_2019 = 'weight_2019'

# Weight Files
file_weight_2016 = birth_dir + '2016_birth_weight.csv'
file_weight_2017 = birth_dir + '2017_birth_weight.csv'
file_weight_2018 = birth_dir + '2018_birth_weight.csv'
file_weight_2019 = birth_dir + '2019_birth_weight.csv'

# Gender Tables
table_gender_2016 = 'gender_2016'
table_gender_2017 = 'gender_2017'
table_gender_2018 = 'gender_2018'
table_gender_2019 = 'gender_2019'

# Gender Files
file_gender_2016 = birth_dir + '2016_birth_gender.csv'
file_gender_2017 = birth_dir + '2017_birth_gender.csv'
file_gender_2018 = birth_dir + '2018_birth_gender.csv'
file_gender_2019 = birth_dir + '2019_birth_gender.csv'

# Plurality Tables
table_plural_2016 = 'plural_2016'
table_plural_2017 = 'plural_2017'
table_plural_2018 = 'plural_2018'
table_plural_2019 = 'plural_2019'

# Plurality Files
file_plural_2016 = birth_dir + '2016_birth_plural.csv'
file_plural_2017 = birth_dir + '2017_birth_plural.csv'
file_plural_2018 = birth_dir + '2018_birth_plural.csv'
file_plural_2019 = birth_dir + '2019_birth_plural.csv'

# Race Tables
table_race_2016 = 'race_2016'
table_race_2017 = 'race_2017'
table_race_2018 = 'race_2018'
table_race_2019 = 'race_2019'

# Race Files
file_race_2016 = birth_dir + '2016_birth_race.csv'
file_race_2017 = birth_dir + '2017_birth_race.csv'
file_race_2018 = birth_dir + '2018_birth_race.csv'
file_race_2019 = birth_dir + '2019_birth_race.csv'

# Parental Care Tables
table_care_2016 = 'care_2016'
table_care_2017 = 'care_2017'
table_care_2018 = 'care_2018'
table_care_2019 = 'care_2019'

# Parental Care Files
file_care_2016 = birth_dir + '2016_birth_care.csv'
file_care_2017 = birth_dir + '2017_birth_care.csv'
file_care_2018 = birth_dir + '2018_birth_care.csv'
file_care_2019 = birth_dir + '2019_birth_care.csv'

# Census Table
table_census = 'census'

# Census File
file_census = birth_dir + 'census.csv'

##### LOAD NC BIRTH DATA ###################################################################
schema = 'finalproject'

# Load the data
def load(host, port, dbname, schema, user, password):
    # Set each variable in the dictionary.
    connDetails = {
        'host'      : host,
        'port'      : port,
        'dbname'    : dbname,
        'user'      : user,
        'password'  : password
    }
    
    # Care Tables
    fnc.copyFromCSV(schema, table_care_2016, file_care_2016, connDetails)
    fnc.copyFromCSV(schema, table_care_2017, file_care_2017, connDetails)
    fnc.copyFromCSV(schema, table_care_2018, file_care_2018, connDetails)
    fnc.copyFromCSV(schema, table_care_2019, file_care_2019, connDetails)
    
    # Gender Tables
    fnc.copyFromCSV(schema, table_gender_2016, file_gender_2016, connDetails)
    fnc.copyFromCSV(schema, table_gender_2017, file_gender_2017, connDetails)
    fnc.copyFromCSV(schema, table_gender_2018, file_gender_2018, connDetails)
    fnc.copyFromCSV(schema, table_gender_2019, file_gender_2019, connDetails)

    # Plurality Tables
    fnc.copyFromCSV(schema, table_plural_2016, file_plural_2016, connDetails)
    fnc.copyFromCSV(schema, table_plural_2017, file_plural_2017, connDetails)
    fnc.copyFromCSV(schema, table_plural_2018, file_plural_2018, connDetails)
    fnc.copyFromCSV(schema, table_plural_2019, file_plural_2019, connDetails)

    # Race Tables
    fnc.copyFromCSV(schema, table_race_2016, file_race_2016, connDetails)
    fnc.copyFromCSV(schema, table_race_2017, file_race_2017, connDetails)
    fnc.copyFromCSV(schema, table_race_2018, file_race_2018, connDetails)
    fnc.copyFromCSV(schema, table_race_2019, file_race_2019, connDetails)

    # Weight Tables
    fnc.copyFromCSV(schema, table_weight_2016, file_weight_2016, connDetails)
    fnc.copyFromCSV(schema, table_weight_2017, file_weight_2017, connDetails)
    fnc.copyFromCSV(schema, table_weight_2018, file_weight_2018, connDetails)
    fnc.copyFromCSV(schema, table_weight_2019, file_weight_2019, connDetails)

    # Census Table
    fnc.copyFromCSV(schema, table_census, file_census, connDetails)
         
    # Clear dict
    del connDetails


##### MAIN #####################################################################
if __name__ == "__main__":
    # Help/error text
    help = 'load_data.py -h|--host <host> -p|--port <port> -d|--dbname <dbname> -U|--user <user> -P|--password <password>'
    
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