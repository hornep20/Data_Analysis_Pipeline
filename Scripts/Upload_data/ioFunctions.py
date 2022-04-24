##### IMPORTS #####################################################################################
import databaseUtils as db
from io import StringIO
import os
import pandas as pd
import requests
import time


##### PRINTERS AND TIMERS #########################################################################
# Use as is.
def printAndStartTimer(action, title):
    """
    Print 'action title...' and return time.time().
    
    Args:
        action (str) : action being taken
        title  (str) : title
    
    Returns:
        The start time as time.time()
    """
    print(action, title, '...')
    return time.time()

# Use as is.
def printCompleteAndTime(action, startTime):
    """
    Print 'action complete: time.time()-startTime seconds'.
    
    Args:
        action            (str) : action being taken
        startTime (time.time()) : start time from time.time()
    """
    print(action, 'complete:', time.time()-startTime, 'seconds')


##### WRITE DATA TO DISK ##########################################################################
# (1) Write a function that writes text data to disk. 
#     Include a title for printing (e.g., NYT COVID data).
#     writeTextToFile(text, file, title)
def writeTextToFile(text, file, title=None):
    """
    Writes the data to the file.
    
    Args:
        data  (str) : text to write
        file  (str) : path and file name
        title (str) : title for printing
    """
    st = printAndStartTimer('Writing', title)
    # If you receive an encoding error, try open(..., encoding='cp1251')
    with open(os.path.join(os.getcwd(), file), 'w') as f:
        f.write(text)
    printCompleteAndTime('Write', st)


# (2) Write a function that writes a pandas.DataFrame to disk as a CSV. 
#     Include a title for printing (e.g., NYT COVID data).
#     writeDFToCSV(df, file, title) - index=False, header=True
def writeDFToCSV(df, file, title=None):
    """
    Writes the data to the file.
    
    Args:
        data  (str) : pandas.DataFrame to write
        file  (str) : path and file name
        title (str) : title for printing
    """
    st = printAndStartTimer('Writing', title)
    df.to_csv(file, index=False, header=True)
    printCompleteAndTime('Write', st)


##### DOWNLOAD FILES ##############################################################################
# (1) Write a function to download and return the contents of a url using requests.get(url).text. 
#     Include a title for printing (e.g., NYT COVID data).
#     downloadText(url, title)
def downloadText(url, title=None):
    """
    Downloads and returns the text (requests.get(url).text) of the URL provided.
    
    Args:
        url   (str) : URL of text to download
        title (str) : title for printing
    
    Returns:
        The text of the URL (requests.get(url).text).
    """
    st = printAndStartTimer('Downloading', title)
    ret = requests.get(url).text
    printCompleteAndTime('Download', st)
    return ret

# (2) Write a function to download and return the contents of a CSV from a url using pandas. 
#     Include a title for printing (e.g., NYT COVID data).
#     downloadCSV(url, title)
def downloadCSV(url, title=None):
    """
    Downloads and returns the CSV at URL as a pandas.DataFrame.
    
    Args:
        url   (str) : URL of CSV data to download
        title (str) : title for printing
        
    Returns:
        A pandas.DataFrame object of the CSV data from URL.
    """
    st = printAndStartTimer('Downloading', title)
    ret = pd.read_csv(url)
    printCompleteAndTime('Download', st)
    return ret

# (3) Write a function to download and write the contents of a url using requests.get(url).content
#     to a file. Include a title for printing (e.g., NYT COVID data).
#     downloadToFile(url, file, title)
def downloadToFile(url, file, title=None):
    """
    Downloads and writes the text (requests.get(url).text) of the URL provided to the file.
    
    Args:
        url   (str) : URL of CSV data to download
        file  (str) : path and file name
        title (str) : title for printing
    """
    st = printAndStartTimer('Downloading and writing to CSV', title)
    resp = requests.get(url).text
    with open(os.path.join(os.getcwd(), file), 'w') as f:
        f.write(resp)
    printCompleteAndTime('Download and write', st)
        

# (3) Write a function to download and write the contents of a url using requests.get(url).content
#     to a file. Include a title for printing (e.g., NYT COVID data).
#     downloadToFileStream(url, file, title)
def downloadToFileStream(url, file, title=None):
    """
    Downloads and writes, in streaming fashion, the binary chunks (requests.get(url, stream=True)) 
    of the URL provided to the file.
    
    Args:
        url   (str) : URL of CSV data to download
        file  (str) : path and file name
        title (str) : title for printing
    """
    st = printAndStartTimer('Downloading and writing, using a stream, to CSV', title)
    with requests.get(url, stream=True) as resp: # use with since it's streaming for safety
        with open(os.path.join(os.getcwd(), file), 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):  # 8*1024B
                f.write(chunk)
    printCompleteAndTime('Download and write with stream', st)



##### COPY FROM CSV ###############################################################################
# (1) Write a function to execute COPY schema.table FROM file CSV HEADER ENCODING 'WIN1251'.
#     The schema and table will be used to construct the print statment.
#     copyFromCSV(schema, table, file, connDetails)
def copyFromCSV(schema, table, file, connDetails):
    """
    Copies (using COPY) the contents of the CSV file to the database as schema.table.
    
    Args:
        schema       (str) : schema
        table        (str) : table
        file         (str) : path and file name
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    """
    st = printAndStartTimer('Copying from CSV to', schema+'.'+table)
    db.execute("COPY {0}.{1} FROM '{2}' CSV HEADER ENCODING 'WIN1251'"
               .format(schema, table, os.path.join(os.getcwd(), file)), connDetails)
    printCompleteAndTime('COPY', st)


# (2) Write a function to create a new table using DataFrame.to_sql and db.psql_insert_copy.
#     The schema and table will be used to construct the print statment.
#     copyFromDF(schema, table, df, connDetails)
def copyFromDF(schema, table, df, connDetails):
    """
    Copies (using COPY) the contents of the DataFrame df to the database as schema.table.
    
    Args:
        schema       (str) : schema
        table        (str) : table
        df     (DataFrame) : path and file name
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    """
    st = printAndStartTimer('Copying from DataFrame to', schema+'.'+table)
    df.to_sql(table, db.engine(connDetails), schema=schema, if_exists='fail', index=False, method=db.psql_insert_copy)
    printCompleteAndTime('COPY', st)


# Use as is.
def copyFromSTDIN(schema, table, text, connDetails):
    """
    Copies (using COPY) from the CSV as text using STDIN to the database as schema.table.
    
    Args:
        schema       (str) : schema
        table        (str) : table
        text         (str) : CSV as text
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    """
    schema_table = schema+'.'+table
    st = printAndStartTimer('Copying from STDIN CSV to', schema_table)
    conn = db.connect(connDetails)
    with conn.cursor() as cur:
        s_buf = StringIO(text)
        sql = 'COPY {} FROM STDIN WITH CSV HEADER'.format(schema_table)
        cur.copy_expert(sql=sql, file=s_buf)
        conn.commit()
    printCompleteAndTime('Copied from STDIN CSV', st)


# Use as is.
def downloadAndCopyFromCSV(schema, table, url, connDetails):
    """
    Copies (using COPY) the downloaded text (requests.get(url).text) from URL to the database as schema.table.
    
    Args:
        schema       (str) : schema
        table        (str) : table
        url          (str) : URL of CSV data to download
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    """
    schema_table = schema+'.'+table
    st = printAndStartTimer('Downloading and copying from CSV to', schema_table)
    conn = db.connect(connDetails)
    with conn.cursor() as cur:
        s_buf = StringIO(requests.get(url).text)
        sql = 'COPY {} FROM STDIN WITH CSV HEADER'.format(schema_table)
        cur.copy_expert(sql=sql, file=s_buf)
        conn.commit()
    printCompleteAndTime('Downloaded and copied from CSV', st)




