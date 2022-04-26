# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 09:46:22 2021

@author: Ray
"""
import pandas as pd
from sqlalchemy import create_engine
from multipledispatch import dispatch
import csv
from io import StringIO


@dispatch(str, int, str, str, str)
def engine(host='localhost', port='5432', dbname='postgres',
            user=None, password=None):
    """Connect to a database using sqlalchemy and psycopg2. 
    
    Args:
        host     (str) : Host address, default = localhost
        port     (int) : Port number, default = 5432
        dbname   (str) : Database name, default = postgres
        user     (str) : User name
        password (str) : Password
    
    Returns:
        The database engine
        
    Raises:
        Exception: Failed to connect to the database
    """
    try:
        e = create_engine('postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'
                          .format(user, password, host, port, dbname)
                          )
       # print('Connection successful')
        return e
    except Exception as ex:
        #print('Unable to connect', ex)
        raise


@dispatch(dict)
def engine(connDetails):
    """Connect to a database using sqlalchemy and psycopg2. 
    
    Args:
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    
    Returns:
        The database engine
        
    Raises:
        Exception: Failed to connect to the database
    """
    try:
        e = engine(connDetails['host'], connDetails['port'], connDetails['dbname'], 
                   connDetails['user'], connDetails['password'])
        #print('Connection successful')
        return e
    except Exception as ex:
        #print('Unable to connect', ex)
        raise


@dispatch(str, int, str, str, str)
def connect(host='localhost', port='5432', dbname='postgres',
            user=None, password=None):
    """Connect to a database using sqlalchemy and psycopg2. 
    
    Args:
        host     (str) : Host address, default = localhost
        port     (int) : Port number, default = 5432
        dbname   (str) : Database name, default = postgres
        user     (str) : User name
        password (str) : Password
    
    Returns:
        The database connection
        
    Raises:
        Exception: Failed to connect to the database
    """
    try:
        conn = engine(host, port, dbname, user, password).raw_connection()
        '''conn = psycopg2.connect(
                host = host,
                port = port,
                dbname = dbname,
                user = user,
                password = password
            )'''
        #print('Connection successful')
        return conn
    except Exception as ex:
        #print('Unable to connect', ex)
        raise
        

@dispatch(dict)
def connect(connDetails):
    """Connect to a database using sqlalchemy and psycopg2. 
    
    Args:
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    
    Returns:
        The database connection
        
    Raises:
        Exception: Failed to connect to the database
    """
    conn = None
    try:
        conn = engine(connDetails).raw_connection()
        #print('Connection successful')
    except Exception as ex:
        #print('Unable to connect', ex)
        raise
    return conn


@dispatch(str, object)
def fetchall(query, conn):
    """Execute the query and return cursor.fetchall().
    
    Args:
        query (str)        : SQL query to execute
        conn  (connection) : Database connection object
        
    Returns:
        cursor.fetchall()
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as ex:
        raise
    finally:
        if cursor != None: cursor.close()
        

@dispatch(str, dict)
def fetchall(query, connDetails):
    """Execute the query and return cursor.fetchall(). This opens and closes
    the connection.
    
    Args:
        query (str)        : SQL query to execute
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
        
    Returns:
        cursor.fetchall()
    """
    conn = None
    try:
        conn = connect(connDetails)
        return fetchall(query, conn)
    except Exception as ex:
        raise
    finally:
        if conn != None: conn.close()


@dispatch(str, object)
def execute(query, conn):
    """Execute the query without a return (e.g., DDL or DCL statements).
    
    Args:
        query (str)        : SQL query to execute
        conn  (connection) : Database connection object
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    except Exception as ex:
        raise
    finally:
        if cursor != None: cursor.close()


@dispatch(str, dict)
def execute(query, connDetails):
    """Execute the query without a return (e.g., DDL or DCL statements). This 
    opens and closes the connection.
    
    Args:
        query (str)        : SQL query to execute
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
    """
    conn = None
    try:
        conn = connect(connDetails)
        execute(query, conn)
        conn.commit()
    except Exception as ex:
        raise
    finally:
        if conn != None: conn.close()
        

@dispatch(str, object)
def executeQuery(query, conn):
    """Execute the query and return a Pandas DataFrame (e.g., DML).
    
    Args:
        query (str)        : SQL query to execute
        conn  (connection) : Database connection object
        
    Returns:
        Query results in a Pandas DataFrame
    """
    try:
        return pd.read_sql_query(query, con = conn)
    except Exception as ex:
        raise
    
@dispatch(str, dict)
def executeQuery(query, connDetails):
    """Execute the query and return a Pandas DataFrame (e.g., DML). This opens
    and closes the connection.
    
    Args:
        query (str)        : SQL query to execute
        connDetails (dict) : connection details dictionary with value:
            host     (str) : Host address
            port     (int) : Port number
            dbname   (str) : Database name
            user     (str) : User name
            password (str) : Password
        
    Returns:
        Query results in a Pandas DataFrame
    """
    conn = None
    try:
        conn = connect(connDetails)
        return executeQuery(query, conn)
    except Exception as ex:
        raise
    finally:
        if conn != None: conn.close()
    

def psql_insert_copy(table, conn, keys, data_iter):
    """pandas.to_sql "method" for fast copy for databases that support "COPY".
    Example use: df.to_sql('table_name', sqlalchemy_engine, method=psql_insert_copy)

    Args:
        table       : pandas.io.sql.SQLTable
        conn        : sqlalchemy.engine.Engine or sqlalchemy.engine.Connection
        keys        : list of str Column names
        data_iter   : Iterable that iterates the values to be inserted
    """
    # gets a DBAPI connection that can provide a cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)
    
    
    
    