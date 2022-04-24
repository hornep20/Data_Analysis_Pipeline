# ------------------------------------------------------------------
# Load variables file
# ------------------------------------------------------------------
source variables.sh


# ----- Birth Data INIT -------------------------------------------
temp_usr=$user
temp_pwd=$PGPASSWORD
source sh/read_pg_credentials.sh

echo ---------------------------------------------------------------
echo Execute $schema_init_sql
echo ---------------------------------------------------------------
$postgres -h $host -p $port -U $user --dbname=$dbname -f $schema_init_sql

# ------------------------------------------------------------------
# Reset Postrges Credentials
# ------------------------------------------------------------------
user=$temp_usr
export PGPASSWORD=$temp_pwd


# ----- Birth LOAD ------------------------------------------
echo ---------------------------------------------------------------
echo Execute $data_load_py
echo ---------------------------------------------------------------
$activate_anaconda
$python $data_load_py -h $host -p $port -d $dbname -s $schema -U $user -P $PGPASSWORD

# ----- Combine Data LOAD ------------------------------------------
echo ---------------------------------------------------------------
echo Execute $data_combine_py
echo ---------------------------------------------------------------
$activate_anaconda
$python $data_combine_py -h $host -p $port -d $dbname -s $schema -U $user -P $PGPASSWORD

# ----- Write Data ------------------------------------------
echo ---------------------------------------------------------------
echo Execute $export_data_py
echo ---------------------------------------------------------------
$activate_anaconda
$python $export_data_py -h $host -p $port -d $dbname -s $schema -U $user -P $PGPASSWORD


# ------------------------------------------------------------------
# Print press any key to continue
# ------------------------------------------------------------------
echo
source sh/press_any_key.sh

