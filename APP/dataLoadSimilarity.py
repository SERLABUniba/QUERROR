"""
Load the similarity data into database to access it later in the app

Usage:
    python dataLoadSimilarity.py

author: @anibrata
"""

import os
import sqlite3
import csv
import sys
import ast


def process_data_sim(filename):
    """
    Load dataset filename from folder DATA
    :param filename:
    :return: dataset
    """
    # Get the current directory
    current_directory = os.getcwd()
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    filepath = os.path.join(parent_directory, 'DATA', filename)

    # Load dataset filename from folder DATA without the first row
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        dataset = list(reader)

        # Remove the first row
        dataset.pop(0)

        # Print top 5 rows of dataset
        # print(dataset[0][0])

    return dataset


def load_data_sim(data):
    """
    Load data from dataset into database qbugsim table
    :param data:
    :return:
    """

    # Create database connection
    conn = sqlite3.connect('../DATA/qbug.db')
    cursor = conn.cursor()

    # Drop table if it exists
    cursor.execute('DROP TABLE IF EXISTS qbugsim')
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS qbugsim (
                        id INTEGER,
                        tuple_index INTEGER,
                        value_id INTEGER,
                        value REAL
                    )''')

    # Insert data into database table
    for row_id, row in enumerate(data):
        # print(row_id, row)
        for (tuple_index, value) in enumerate(row):
            # Separate the items in value
            value = ast.literal_eval(value)
            value_id = value[0]
            value = value[1]
            # print(row_id+1, tuple_index+1, value_id, value)
            cursor.execute('''
            INSERT INTO qbugsim (id, tuple_index, value_id, value) VALUES (?, ?, ?, ?)
            ''', (row_id+1, tuple_index+1, value_id, value))

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
    data = process_data_sim('cos_sim_best_scores_stackoverflow.csv')
    if condition:
        load_data_sim(data)


if __name__ == '__main__':
    main()
