import sqlite3
import csv

# Define function to update table with data from CSV
def update_table(db, table, csv_file):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Read data from CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        counter = 1
        for row in reader:
            # Remove trailing and leading whitespaces from each row
            row = [item.strip() for item in row]
            # print(row)
            # exit(0)
            # Prepare SQL statement
            stmt = f"UPDATE {table} SET symptom = ?, description = ?, bugtype = ?, bugpattern = ?, vulnerability = ?, testcase = ? WHERE rowid = {counter}"

            # Execute SQL statement
            cursor.execute(stmt, row)

            # Increase counter for next row
            counter += 1

            # Commit changes
            conn.commit()

            # exit(0)

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return


def get_rec(db, table):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Fetch records for the current page
    stmt = f"SELECT rowid, * FROM {table} where bugtype is not \"\""
    # stmt = (f"SELECT rowid, repo, commit_message, filename, symptom, description, bugtype, bugpattern, "
    #        f"vulnerability, testcase FROM {table} where bugtype is not \"\"")
    cursor.execute(stmt)
    records = cursor.fetchall()

    conn.close()

    return records, cursor

def export_csv():
    # Define the SQLite3 database file and table name
    records, cursor = get_rec('../DATA/qbug.db', 'qbugs')

    # Fetch all rows and get the column names
    column_names = [description[0] for description in cursor.description]

    # Define the CSV file name
    csv_file = '../DATA/bugs_annotated.csv'

    # Write data to CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the column names as the first row
        writer.writerow(column_names)

        # Write all data rows
        writer.writerows(records)

    print(f"Data has been successfully exported to {csv_file}")

def import_csv():
    update_table('../DATA/qbug.db', 'qbugs', '../DATA/MAIN_results.csv')


def main():
    # Export data from the database to a CSV file
    # export_csv()

    # Import data from a CSV file into the database
    import_csv()

if __name__ == '__main__':
    main()
