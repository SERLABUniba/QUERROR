from flask import Flask, render_template, request, redirect, url_for, jsonify
from openai import OpenAI
import sqlite3
# import openai
import os
# import re
from similarity_score import *

app = Flask(__name__, template_folder='templates')

# Set your OpenAI API key
api_key = "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"


# List of annotation fields
commit_info = ['Repository', 'Commit Message', 'Filename', 'Code Changes']
annotation_fields_display = ['Symptom', 'Description',  'Bug Type', 'Bug Pattern', 'Vulnerability', 'Test Case']
annotation_fields = ['symptom', 'description',  'bugtype', 'bugpattern', 'vulnerability', 'testcase']

os.chdir('/home/anibrata/Anibrata/PROJECTS/CODE/QUANTUM/QUERROR/APP')

# Number of records per page
RECORDS_PER_PAGE = 1


def paginate(records, page_num):
    start_idx = (page_num - 1) * RECORDS_PER_PAGE
    end_idx = start_idx + RECORDS_PER_PAGE
    return records[start_idx:end_idx]


def get_rec(db, table):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    # cursor1 = conn.cursor()

    # print(f"Table: {table}")
    # print(f"DB: {db}")

    # Fetch records for the current page
    stmt = f"SELECT rowid, * FROM {table}"
    # stmt1 = f"SELECT max(rowid) FROM {table}"
    cursor.execute(stmt)
    # cursor1.execute(stmt1)
    records = cursor.fetchall()
    # print(cursor1.fetchall())

    conn.close()

    return records


def get_sim_records(db, page):
    # Connect to the database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Fetch records from qbugsim where ID = page
    cursor.execute("SELECT tuple_index, value_id, value FROM qbugsim WHERE ID = ? order by value desc", (page,))
    sim_records = cursor.fetchall()
    # print(sim_records)

    conn.close()

    return sim_records


@app.route('/favicon.ico')
def favicon():
    return '', 204


"""@app.route('/')
def non_index():
    # Get page parameter from request, default to 1 if not provided
    page = int(request.args.get('page', 1))

    # Calculate offset to fetch records for the current page
    offset = (page - 1) * RECORDS_PER_PAGE

    # Connect to the database
    conn = sqlite3.connect('qbug.db')
    cursor = conn.cursor()

    # Fetch records for the current page
    cursor.execute(f"SELECT * FROM qbugs LIMIT ? OFFSET ?", (RECORDS_PER_PAGE, offset))
    records = cursor.fetchall()

    # cursor.execute("SELECT * FROM qbugs")
    # records = cursor.fetchall()

    # Calculate total number of pages
    cursor.execute("SELECT COUNT(*) FROM qbugs")
    total_records = cursor.fetchone()[0]

    # Calculate total number of pages
    total_pages = (total_records + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE

    conn.close()

    annotation_fields_length = len(annotation_fields)  # Get the length of annotation_fields
    # return render_template('TEMP_index.html', records=records, annotation_fields=annotation_fields,
    #                       annotation_fields_length=annotation_fields_length)

    # Generate page links
    page_links = generate_page_links(page, total_pages)

    return render_template('TEMP_index.html', records=records, annotation_fields=annotation_fields,
                           total_pages=total_pages, page_links=page_links, current_page=page)"""


@app.route('/')
def index():
    # Get all records from the database
    records = get_rec('../DATA/qbug.db', 'qbugs')
    # Length of records
    # print(f"Length of records: {len(records)}")

    # If page number received here does not belong to the existing range 1-5044, and is not an integer then redirect
    # to same page and show popup message saying that page does not exist
    # Get page parameter from request, default to 1 if not provided
    try:
        page = int(request.args.get('page', 1))
        # print(f"Page number GET received in TRY: {page}")
        if page < 1 or page > 5044 or not isinstance(page, int):
            pass
    except ValueError:
        # Set page number to the existing page in this exception
        page = 1

    # print(f"Page value GET received: {page}")

    total_pages = (len(records) + RECORDS_PER_PAGE - 1) // RECORDS_PER_PAGE
    # print(f"Total pages: {total_pages}")

    # Calculate start and end indices for the current page
    start_idx = (page - 1) * RECORDS_PER_PAGE
    end_idx = start_idx + RECORDS_PER_PAGE
    paginated_records = records[start_idx:end_idx]
    # Remove extra large image files from the changes fields
    # pattern = r'^"image/png": ".*$'
    # paginated_records[0][4] = re.sub(pattern, '', paginated_records[0][4], flags=re.MULTILINE)

    # Commented the block below to remove the Previous record and Similarity score
    # # Determine the previous record
    # previous_record = records[start_idx - 1] if start_idx > 0 else None
    #
    # # Compute similarity if previous_record exists
    # if previous_record:
    #     # print(f"Paginated records: {paginated_records[0][4]}")
    #     # print(f"Previous record: {previous_record[4]}")
    #     similarity_score = calculate_bert_similarity(records[0][4], previous_record[4])
    #     # similarity_score = calculate_semantic_similarity(records[0][4], previous_record[4])
    #     # similarity_score = calculate_cosine_similarity(records[0][4], previous_record[4])
    # else:
    #     similarity_score = None

    # print(f"Similarity score: {similarity_score}")

    # Create a scheme of color for coloring and text for marking the record for code changes
    # if similarity_score >= 0.9:
    #     sim_color = 'green'
    #     sim_text = 'Similar'
    # else:
    #     sim_color = 'red'
    #     sim_text = 'Different'

    # In the record paginated_records[0][4] remove these types of
    # occurences "image/png": "iVBORw0KGgoAAAANSUhEUgAAA34AAAEiCAYAAACm+gCx..."

    # paginated_records = paginate(records, page)
    # total_pages = len(records) // RECORDS_PER_PAGE + (1 if len(records) % RECORDS_PER_PAGE != 0 else 0)
    # page_links = {
    #     'previous': page - 1 if page > 1 else None,
    #     'next': page + 1 if page < total_pages else None,
    # }
    # return render_template('TEMP_index.html', records=paginated_records,
    #                        annotation_fields=annotation_fields, page_links=page_links)

    page_links = {
        'first': 1,
        'second': 2,
        'previous': page - 1 if page > 1 else None,
        'next': page + 1 if page < total_pages else None,
        'next_1': page + 2 if page < total_pages - 1 else None,
        'next_check': page + 3 if page < total_pages - 2 else None,
        'back_check': page - 3 if page > 3 else None,
        'last': total_pages,
        'prev_1': page - 1 if page > 1 else None,
        'prev_2': page - 2 if page > 2 else None,
        'last_1': total_pages - 1 if page > total_pages - 1 else None,
        'last_2': total_pages - 2 if page > total_pages - 2 else None,
        'last_3': total_pages - 3 if page > total_pages - 3 else None,
        'back_1': total_pages - 1,
        'current': page,
    }

    # return render_template('index.html', records=paginated_records,
    #                        annotation_fields=annotation_fields, page_links=page_links,
    #                        annotation_fields_display=annotation_fields_display, page=page,
    #                        total_pages=total_pages, previous_record=previous_record,
    #                        commit_info=commit_info, similarity_score=similarity_score)

    return render_template('index.html', records=paginated_records,
                           annotation_fields=annotation_fields, page_links=page_links,
                           annotation_fields_display=annotation_fields_display, page=page,
                           total_pages=total_pages, commit_info=commit_info)

    # sim_color=sim_color, sim_text=sim_text)


@app.route('/send_to_popup', methods=['POST'])
def send_to_popup():
    # Get the default message from the form
    default_message = request.form['default_message']

    # Add additional text from Flask
    additional_text = " This text is added by Flask."

    # Concatenate the default message and additional text
    popup_message = default_message + additional_text

    return jsonify({'popup_message': popup_message})


# Define a route to handle AI requests
@app.route('/send_to_ai', methods=['POST'])
def send_to_ai():
    client = OpenAI(api_key=api_key)

    # Get the code changes text from the form data
    code_changes_text = request.form.get('code_changes')

    # creating a new string by adding the string "What bugs does this code change resolve?
    # Does this solve any vulnerabilities?: " to code_changes_text
    code_changes_text = ("What bugs does this code change resolve? "
                         "Does this solve any vulnerabilities? "
                         "Is this a classical or quantum fix?: ") + code_changes_text

    # print("code_changes_text: ", code_changes_text)

    # Check if the text is empty
    if code_changes_text is None or code_changes_text.strip() == '':
        return jsonify({'error': 'Please enter some text'})
        # return "error: Please enter some text"
    else:
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a security expert, who can analyse code changes."},
                    {"role": "user", "content": code_changes_text}
                ]
            )
            # Extract the generated text from the response
            generated_text = completion.choices[0].message.content

            # print("generated_text: ", generated_text)

            # Return the generated text as JSON
            return jsonify({'generated_text': generated_text})
            # return generated_text
        except Exception as e:
            return jsonify({'error': str(e)})

    # code_changes = request.form['code_changes']
    # return jsonify({'code_changes': code_changes})

    # if request.method == 'POST':
    #     code_changes = request.form['code_changes']
    #     return jsonify({'code_changes': code_changes})
    # else:
    #     return jsonify({'error': 'Method not allowed'}), 405


@app.route('/generate_text', methods=['POST'])
def generate_text():
    # Set your OpenAI API key
    client = OpenAI(api_key=api_key)

    # Get the text from the form
    code_changes_text = request.form['code_changes_text']
    # print("code_changes_text: ", code_changes_text)

    # Check if the text is empty
    if code_changes_text is None or code_changes_text.strip() == '':
        return jsonify({'error': 'Please enter some text'})
    else:
        try:
            completion = client.chat.completions.create(
                # model="gpt-3.5-turbo",
                # model="gpt-4o",
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a security expert, who can analyse code changes."},
                    {"role": "user", "content": code_changes_text}
                ]
            )
            # Extract the generated text from the response
            generated_text = completion.choices[0].message.content

            # print("generated_text: ", generated_text)

            # Remove the ** from the text, as well as preceding '- '
            generated_text = generated_text.replace("**", "").replace("- ", "")
            # Remove sequence of two or more #'s from text
            generated_text = re.sub(r'#\s*#', '', generated_text)

            # If encounters "-------" then delete this and anything below that
            if "-------" in generated_text:
                generated_text = generated_text[:generated_text.index("-------")]

            # print("generated_text: ", generated_text)

            # Return the generated text as JSON
            return jsonify({'generated_text': generated_text})
        except Exception as e:
            return jsonify({'error': str(e)})


def generate_page_links(current_page, total_pages):
    """
    A function to generate page links for pagination based on current page and total pages.
    Parameters:
        current_page (int): The current page number.
        total_pages (int): The total number of pages available.
    Returns:
        list: A list of tuples containing page numbers and labels for the links.
    """
    # Maximum number of page links to display
    max_page_links = 5

    # Calculate start and end page numbers for the pagination
    start_page = max(1, current_page - max_page_links // 2)
    end_page = min(total_pages, start_page + max_page_links - 1)

    # Adjust start and end page numbers if necessary
    if end_page - start_page + 1 < max_page_links:
        start_page = max(1, end_page - max_page_links + 1)

    # Generate page links
    page_links = []
    if current_page > 1:
        page_links.append((current_page - 1, 'Previous'))
    for page_num in range(start_page, end_page + 1):
        page_links.append((page_num, str(page_num)))
    if current_page < total_pages:
        page_links.append((current_page + 1, 'Next'))

    return page_links


def update_record(db, table_name, fields_to_update, new_values, rowid):
    # Connect to the SQLite database
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Construct the SQL UPDATE query dynamically
    sql = f"UPDATE {table_name} SET "
    sql += ', '.join([f'{field} = ?' for field in fields_to_update])
    sql += " WHERE rowid = ?;"

    # Combine values for the UPDATE statement
    update_values = tuple(new_values) + (rowid,)

    # Execute the SQL UPDATE statement with parameterized query
    cursor.execute(sql, update_values)

    # Commit the transaction
    conn.commit()

    # Close the connection
    conn.close()


def data_process(annotations, annotation_indexes):
    """ Check the indexes where there are annotations and remove any empty indexes """
    # Remove any empty indexes from the annotation_indexes list
    annotation_indexes = [index for index in annotation_indexes if annotations[annotation_indexes.index(index)] != '']

    # Remove all empty items from annotations
    annotations = [item for item in annotations if item != '']

    # print(f"Annotation indexes: {annotation_indexes}")
    # print(f"Annotations: {annotations}")

    return annotation_indexes, annotations


@app.route('/annotate', methods=['POST'])
def annotate():
    # record_id = request.form.get('record_id', type=int, default=request.form.getlist('record_id'))
    record_id = request.form['record_id']
    # print(f"Record ID received: {record_id}")

    # Get the page number from the request
    page = request.form.get('page', 1, type=int)
    # print(f"Page value received: {page}")

    # For calculating the table fields
    table_fields = []

    # Get the list of annotation indexes and their corresponding values
    annotation_indexes = request.form.getlist('annotation_indexes[]')
    annotations = request.form.getlist('annotations[]')

    annotation_indexes, annotations = data_process(annotations, annotation_indexes)

    if annotation_indexes == [] or annotations == []:
        print("No annotations found in the form data")
        # return render_template('update_noannotate.html', page=page)
        # return redirect(url_for('update_success', page=page))
        return redirect(url_for('index', page=page))
        # return jsonify({'success': True, 'message': 'No Annotations Added'})

    # print(f"Field index received: {annotation_indexes}")
    # print(f"Annotation received: {annotations}")

    # Process the annotations (for demonstration purpose, just printing here)
    for ann_index, in annotation_indexes:
        # create a list of values of the annotation fields
        table_fields.append(annotation_fields[int(ann_index)-1])

    # print(f"Fields: {table_fields}")

    update_record('../DATA/qbug.db', 'qbugs', table_fields, annotations, record_id)

    # Refresh the same page and show the updated annotations
    # return redirect(url_for('index', page=page))

    # Return with render template
    # return render_template('update_success.html', page=page)
    return redirect(url_for('index', page=page))

    # Redirect to the success template with the page number
    # print(f"Page value received: {page}")
    # return redirect(url_for('update_success', page=page))
    # Return a JSON response indicating success
    # return jsonify({'success': True, 'message': 'Annotations added successfully'})


#@app.route('/update_success/<int:page>')
#def update_success(page):
#    page = request.args.get('page')
#    str_value = request.args.get('str')
#    return render_template('update_success.html', page=page)


#@app.route('/update_noannotate/<int:page>')
#def update_noannotate(page):
#    page = request.args.get('page')
#    str_value = request.args.get('str')
#    return render_template('update_noannotate.html', page=page)


"""@app.route('/update_success')
def update_success():
    return render_template('update_success.html')


@app.route('/update_success', methods=['POST'])
def return_to_main_page():
    # Handle form submission here if needed
    return redirect(url_for('index', page=request.args.get('page', 1)))"""


@app.route('/get_record_info', methods=['POST'])
def get_record_info():
    record_id = request.form.get('record_id', type=int)

    conn1 = sqlite3.connect('../DATA/qbug.db')
    cursor = conn1.cursor()

    cursor.execute(f"SELECT * FROM qbugs WHERE rowid = ?", (record_id,))
    record = cursor.fetchone()

    columns = [desc[0] for desc in cursor.description]  # Get column names

    """if record is None:
        response = {'error': 'Record not found'}
    else:
        messages = [record['Repository'], record['Commit Message'], record['Filename'], record['Code Changes']]
        annotations = [record['Symptom'], record['Description'], record['Bug Type'], record['Bug Pattern'],
                       record['Vulnerability'], record['Test Case']]
        response = {'messages': messages, 'annotations': annotations}"""

    if record:
        messages = record[:4]  # First four fields
        annotations = record[4:]  # Remaining fields
        response = {
            'messages': messages,
            'annotations': annotations,
            'columns': columns
        }
    else:
        response = {
            'error': 'Record not found'
        }

    conn1.close()

    return jsonify(response)


@app.route('/get_sim_records', methods=['POST'])
def get_sim_records_route():
    page = int(request.form.get('page', 1))

    # Get the similarity records for the current page
    sim_records = get_sim_records('../DATA/qbug.db', page)

    # print(sim_records)

    # Return the similarity records as JSON
    return jsonify({'sim_records': sim_records})


if __name__ == '__main__':
    app.run(debug=True)
