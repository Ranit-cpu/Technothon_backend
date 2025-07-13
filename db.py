import _sqlite3
import csv
conn=_sqlite3.connect('technothon.db')
'''conn.execute("DROP TABLE IF EXISTS Students")
conn.commit()'''
conn.execute('''CREATE TABLE IF NOT EXISTS Students
             (Student_ID TEXT PRIMARY KEY,
                Name TEXT,
                Batch TEXT,
                Overall_Percentage INTEGER)''')
with open('technothon.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        try:
            # Remove the '%' symbol from the percentage and convert to integer
            percentage = int(row[3].replace('%', ''))  # Assuming Overall_Percentage is the 4th column
            # Create a new row with the cleaned percentage
            cleaned_row = [row[0], row[1], row[2], percentage]
            conn.execute('INSERT OR IGNORE INTO Students (Student_ID, Name, Batch, Overall_Percentage) VALUES (?, ?, ?, ?)', cleaned_row)
        except ValueError:
            print(f"Invalid percentage value in row: {row}")
            continue  # Skip invalid rows
    conn.commit()

cursor = conn.execute('SELECT * FROM Students')
count = 2
for row in cursor:
    print(count,row)
    count += 1

cursor=conn.execute("PRAGMA table_info(students)")
for row in cursor:
    print(row)