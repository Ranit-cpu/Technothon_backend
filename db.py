import sqlite3
import csv
import os

try:
    conn = sqlite3.connect('technothon.db')
    
    # Create table if not exists
    conn.execute('''CREATE TABLE IF NOT EXISTS Students
                 (Student_ID TEXT PRIMARY KEY,
                    Name TEXT,
                    Batch TEXT,
                    Overall_Percentage INTEGER)''')
    
    # Check if CSV file exists
    if not os.path.exists('technothon.csv'):
        print("Error: technothon.csv file not found!")
        exit(1)
    
    with open('technothon.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip header row
        print(f"CSV headers: {header}")
        
        for row_num, row in enumerate(csv_reader, start=2):
            try:
                if len(row) < 4:
                    print(f"Row {row_num}: Insufficient columns - {row}")
                    continue
                
                # Remove the '%' symbol from the percentage and convert to integer
                percentage_str = row[3].strip()
                if not percentage_str:
                    print(f"Row {row_num}: Empty percentage value - {row}")
                    continue
                    
                percentage = int(percentage_str.replace('%', ''))
                
                # Create a new row with the cleaned percentage
                cleaned_row = [row[0], row[1], row[2], percentage]
                conn.execute('INSERT OR IGNORE INTO Students (Student_ID, Name, Batch, Overall_Percentage) VALUES (?, ?, ?, ?)', cleaned_row)
                
            except ValueError as e:
                print(f"Row {row_num}: Invalid percentage value '{row[3]}' - {e}")
                continue
            except Exception as e:
                print(f"Row {row_num}: Error processing row {row} - {e}")
                continue
    
    conn.commit()
    print("Data import completed successfully!")

    # Display all students
    cursor = conn.execute('SELECT * FROM Students')
    print("\nAll Students:")
    count = 1
    for row in cursor:
        print(f"{count}. {row}")
        count += 1

    # Display table structure
    print("\nTable Structure:")
    cursor = conn.execute("PRAGMA table_info(Students)")
    for row in cursor:
        print(row)

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
        print("\nDatabase connection closed.")