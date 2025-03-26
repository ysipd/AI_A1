import mysql.connector
 
def get_connected():
    connection = mysql.connector.connect(
        host="pcz218dbl23",
        user="prakashd",
        password="TLzWqu8Kyp",
        database="omni_qa_db"
    )
    
    return connection