import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
azure_mysql_username = os.getenv("AZURE_MYSQL_USERNAME")
azure_mysql_password = os.getenv('AZURE_MYSQL_PASSWORD')
azure_mysql_host = os.getenv("AZURE_MYSQL_HOST")
azure_mysql_port = 3306
azure_mysql_database = os.getenv("AZURE_MYSQL_DATABASE")


# Function to fetch data from MySQL database
def fetch_data(query):
    # Connect to MySQL database
    connection = mysql.connector.connect(user=azure_mysql_username,
                                  password=azure_mysql_password,
                                  host=azure_mysql_host,
                                  port=azure_mysql_port,
                                  database=azure_mysql_database,
                                  ssl_disabled=True)

    cursor = connection.cursor()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]  # Get column names
    data = cursor.fetchall()  # Get data
    cursor.close()
    return columns, data