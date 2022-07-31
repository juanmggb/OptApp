#Import the 'pymysql' library that allow us work with DDL, DQL, DML, DLC and TLC commands of SQL
from attr import attr
import pymysql
import  streamlit as st 
import pandas as pd 
import ui 

def get_column_names(column, table): 
    if column is None: 
        if table == "Productos": 
            columns = ["id", "producto", "cantidad", "precio"]
        elif table == "Clientes": 
            columns = ["id", "producto","precio"]
        elif table == "Empleados":
            columns = ["id", "nombre", "ventas"]
    else: 
        return [column] 
    return columns

#Define the 'Database' class to work with all operations required to connect with the database
#and querys to retrieve and modify data

class Database:
    def __init__(self):
        #Connect to MySQL database
        self.connection = pymysql.connect(
              host = 'localhost',        #IP adress
              user = 'root',              #Name of the user
              password = '243Legacy#',   #Password
              database = 'empresa_hielo' # The database to connect
            )
        
        self.cursor = self.connection.cursor()
        print('Database connection has been done succesfully\n')
    

#==========================================================================================================
#SELECT Implementation to retrieve data from a table using the following values:
#table : The name of the table you do the query
#column : The attribute you want access, by default is None, this means that all columns will retrieved
#id : The ID of the row, by default is None, this means that all rows will be retrieved
#===========================================================================================================
    def select(self,table,attribute, column = None, value = None):
        
        #Select all the columns and rows of the table
        if column is None and value is None:
            sql_statement = 'SELECT * FROM {}'.format(table)

        #Select all rows from the 'column' of the table
        elif column is not None and value is None:
            sql_statement = 'SELECT {} FROM {}'.format(column,table)  
        
        #Select all column where ID = 'id' of the table
        elif column is None and value is not None:
            sql_statement = "SELECT * FROM {} WHERE {} = '{}'".format(table,attribute,value)
        
        
        else:
            sql_statement = "SELECT {} FROM {} WHERE {} = '{}'".format(column,table,attribute,value)
        
        try:
            self.cursor.execute(sql_statement)

            DQL_SELECT = self.cursor.fetchall()
            
            columns = get_column_names(column,table)
         
            df = pd.DataFrame(columns=columns)
           
            for i in range(len(DQL_SELECT)):
                df.loc[i] = list(DQL_SELECT[i])

            
        except Exception as e:
            raise
        
        else: 
            df.index=df['id']
            
            return df


#=========================================================================================================
#UPDATE Implementation
#=========================================================================================================
    def update(self,table,column,attribute,id,value):
         
         
         sql_statement = "UPDATE {} SET {} = {} WHERE {} = '{}'".format(table,column,value,attribute,id)
         
         try:
             
             self.cursor.execute(sql_statement)
             self.connection.commit()
             
         except Exception as e:
            raise

#========================================================================================================       
#Close the connection from the MySQL server
#=========================================================================================================
    def close(self):
        self.connection.close
        print('Connection has closed')
        
                
        
#Start Connection
#database = Database()

#Select the product with the ID = id and the TABLE = table
#id = 4
#table ='Empleados'
#column = 'ventas_totales'
#print(database.select(table, column))
#value = 9000

#Update the database
#database.update(table=table,column=column,attribute='id',id=id,value=value)
# #View the table in the database
#print(database.select(table,column))
#Close connection
