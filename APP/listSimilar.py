import sqlite3
import time
import csv

from similarity_score import *


def get_rec_sim(db):
    # Connect to the database
    conn = sqlite3.connect(db)
    return conn


def get_code_changes_from_database(connection, table):
    # Query to retrieve the "code_changes" fields from the table "qbugs"
    cursor = connection.cursor()
    # Fetch records
    stmt = f"SELECT changes FROM {table}"
    cursor.execute(stmt)
    records = cursor.fetchall()
    # Print datatype of records
    # print(f"{records[0]}")
    # print(len(records))
    # Change the list of tuples to a list of strings
    records = [str(record[0]) for record in records]
    # exit(0)
    return records


def text_processing(text):
    # Preprocess the text: accept list of tuples and remove_sp_char from the text
    text = [(t[0], remove_sp_char(t[1])) for t in text]
    return text


def calculate_sim_all(method, text1, text2):
    # Calculate similarity scores with each "code_changes" field
    similarity_scores = []
    for change01 in text1:
        for change02 in text2:
            similarity_score = method(change01[1], change02[1])
            # print(f"Record: {code_changes[0]}, Code Changes: {code_changes}, Similarity Score: {similarity_score}")
            # similarity_scores.append({'id': code_changes[0], 'similarity_score': similarity_score})
            similarity_scores[change01[0]][change02[0]] = similarity_score

    return similarity_scores


def main():
    # Connect to the database
    connection = get_rec_sim('qbug.db')

    # Retrieve the "code_changes" fields from the database
    code_changes = get_code_changes_from_database(connection, 'qbugs')

    # code_changes = text_processing(code_changes)

    # print(type(code_changes))
    # print(code_changes[0])
    # exit(0)

    # Sample text1
    # text1 = "This is the paragraph."

    start = time.time()
    # Calculate similarity scores for text1 with each "code_changes" field
    # similarity_scores = calculate_sim_all(calculate_bert_similarity, text1, code_changes)
    # similarity_scores = calculate_sim_all(calculate_semantic_similarity, text1, code_changes)
    cos_sim_mat = sbert_sim(code_changes)
    cos_sim_best_scores = sbert_sim_best_scores(cos_sim_mat, 10)
    end = time.time()

    print(f"Time taken: {end - start}")

    # # Sort similarity scores in descending order
    # similarity_scores.sort(key=lambda x: x['similarity_score'], reverse=True)
    #
    # # print(similarity_scores)
    #
    # # Print ID and Similarity scored of top 10 most similar fields
    # for i in range(10):
    #     print(f"ID: {similarity_scores[i]['id']}, Similarity Score: {similarity_scores[i]['similarity_score']}")

    # print(cos_sim_best_scores)
    # Store the cos_sim_best_scores in a csv file
    with open('../DATA/cos_sim_best_scores_stackoverflow.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'similarity_score'])
        writer.writerows(cos_sim_best_scores)

    # Close the database connection
    connection.close()


if __name__ == "__main__":
    main()
