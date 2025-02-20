import os
import sqlite3
import csv
import sys

from tokenCount import *


def process_data(filename):
    # Get the current directory
    current_directory = os.getcwd()
    # print(current_directory)
    # Navigate up one level to the parent directory
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    # print(parent_directory)
    # Create filepath to access codes.csv file in DATA directory
    filepath = os.path.join(parent_directory, 'DATA', filename)
    # print(filepath)
    # Load dataset filename from folder DATA
    # filename = os.path.join(filepath)
    # filename = f'DATA/{filename}'
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        dataset = list(reader)

    # Print top 5 rows of dataset
    # print(dataset[:5])

    # Copy dataset to another variable and add 6 more blank fields for each item of the dataset
    dataset_copy = dataset.copy()
    for item in dataset_copy:
        # Add 6 more blank fields to each item
        item.extend([''] * 6)

    # For each item within each item of the dataset --> do the following steps:
    for item in dataset_copy:
        # Print the item number / row number of the item in dataset
        # print(f"Dataset Row Number: {dataset_copy.index(item) + 1}")
        drownum = dataset_copy.index(item) + 1
        for field in item:
            # For the 4th field of each row of the dataset...
            # if item.index(field) == 2:
            #     # Print the field
            #     # print(f"Filename: {field}")
            #     fname = field
            # if item.index(field) == 3:
            #     # print(f"Field: {field}")
            #     # Call the count_tokens function
            #     # If the token count for the complete text sent to chatGPT is larger than 4096, then it might fail.
            #     # Therefore, we limit the token count to 3700, so that including user prompt and response
            #     # will not exceed 4096
            """token_count = count_tokens(field)
            if token_count > 3700:
                print(f"Token count: {token_count}")
                # delete the item from the dataset and go to next field
                dataset_copy.remove(item)
                break"""
            # Count the characters in the field and print the result
            char_count = len(field)
            # if the character count is larger than 31191, then it might fail.
            if char_count > 31191:
                # print(f"Character count: {char_count}")
                # delete the item from the dataset and go to next field
                # dataset_copy.remove(item) # Commented out since those commit messages can be analyzed manually.
                # Store the field in a variable to be used later for reference while updating the dataset
                old_field = field
                # Add a text in front of the main text so that it is not analyzed by chatGPT
                field = (f"Analyze this manually, DO NOT USE 'ANALYZE' button (Above OpenAI token limit) - "
                         f"****************************************************************"
                         f"\n\n {field}")
                item[item.index(old_field)] = field
                # print(f"{drownum},{fname},{char_count}")
                # break
            # if the field has a "'" then replace it with "\'"
            if "'" in field:
                field = field.replace("'", "\'")
                item[item.index(field)] = field
        # Add 6 more blank fields to each item
        # item.extend([''] * 6)

    # print(dataset[:5])
    return dataset_copy


def load_data(db):
    # Create database connection
    conn = sqlite3.connect('../DATA/qbug.db')
    cursor = conn.cursor()

    # Drop table if it exists
    cursor.execute('DROP TABLE IF EXISTS qbugs')
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS qbugs (
                    repo    TEXT,
                    commit_message  TEXT,
                    filename    TEXT,
                    changes TEXT,
                    symptom TEXT,
                    description TEXT,
                    bugtype TEXT,
                    bugpattern  TEXT,
                    vulnerability   TEXT,
                    testcase    TEXT
                    )''')

    # Insert dataset into table
    for row in db:
        cursor.execute("INSERT INTO qbugs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)

    # Commit changes and close connection
    conn.commit()
    conn.close()


def main():
    # Check the argument, if load then run the load_data function else skip it
    print(f"Argument: {sys.argv[1:]}")
    if len(sys.argv) > 1 and sys.argv[1] == 'load':
        condition = True
    else:
        condition = False
    # Change directory to current directory
    os.chdir("/home/anibrata/Anibrata/PROJECTS/CODE/QUANTUM/QUERROR/APP")
    dataset = process_data('codes.csv')
    if condition:
        load_data(dataset)


if __name__ == '__main__':
    main()
