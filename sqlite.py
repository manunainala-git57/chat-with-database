import sqlite3

## Connect to the SQLite database
conn = sqlite3.connect('student.db')

# create a cursor object to insert records
cursor = conn.cursor()

# create a table
table_info = """
CREATE TABLE student (
    Id INT PRIMARY KEY,
    Name VARCHAR(30),
    Class VARCHAR(10),
    Section VARCHAR(10),
    Marks INT
)
"""

cursor.execute(table_info)


# Insert some records into the table
cursor.execute('''INSERT INTO student values(1, 'Karthik', '10th', 'A', 96)''')
cursor.execute('''INSERT INTO student values(2, 'Sai', '10th', 'B', 87)''')
cursor.execute('''INSERT INTO student values(3, 'Raju', '10th', 'A', 91)''')
cursor.execute('''INSERT INTO student values(4, 'Venkatesh', '10th', 'A', 84)''')
cursor.execute('''INSERT INTO student values(5, 'Suresh', '10th', 'B', 79)''')


# Display all the records in the table
print("The inserted records are:-")
rows = cursor.execute('''SELECT * FROM student''')
for row in rows:
    print(row)


# commit the changes
conn.commit()
conn.close()