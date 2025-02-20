import openai
# from jupyter_core.version import parts
from openai import OpenAI
import csv
# import json
import time
import re

# Debugging by making program wait for key press
# import keyboard

# from pyarrow import nulls

# Set your OpenAI API key
api_key = "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"

# Function to Open the openQuestions.txt file in read mode,
# and copy the text in a string variable, say <question>.
# Close openQuestions.txt
def get_questions():
    with open('../DATA/openQuestion.txt', 'r') as f:
        question = f.read()
    return question


# Function to get the answers from the OpenAI API with backoff handling
def get_answers(question, max_retries=5, initial_delay=1):
    # Set your OpenAI API key
    client = OpenAI(api_key=api_key)

    if question is None or question.strip() == '':
        print("Text is empty or None")
        return None

    retries = 0
    delay = initial_delay

    while retries < max_retries:
        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # ChatGPT mini - cheaper and faster
                # model="gpt-4o",  # ChatGPT 4 optimized model
                messages=[
                    {"role": "system",
                     "content": "You are a security expert and proficient in quantum computing, who can analyze code changes in detail."},
                    {"role": "user", "content": question}
                ],
                max_tokens=256
            )
            generated_text = completion.choices[0].message.content
            return generated_text

        except openai.RateLimitError as e:
            retries += 1
            print(f"Rate limit error: {str(e)}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except openai.APIError as e:
            print("API error: " + str(e))
            return None
        except Exception as e:
            print("Error: " + str(e))
            return None

    print("Max retries exceeded.")
    return None


# Function to get the answers from the OpenAI API
def get_answers_oai(question):
    # Set your OpenAI API key
    client = OpenAI(api_key=api_key)

    # Check if the text is empty
    if question is None or question.strip() == '':
        print("Text is empty or None")
    else:
        try:
            completion = client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="gpt-4o",
                messages=[
                    {"role": "system",
                     "content": "You are a security expert and proficient in quantum computing, who can analyse code changes in details."},
                    {"role": "user", "content": question}
                ],
                max_tokens=150
            )
            # Extract the generated text from the response
            generated_text = completion.choices[0].message.content

            # Return the generated text
            return generated_text

        except Exception as e:
            print("Error: " + str(e))
            return "None"


# Function to do the following things:
# 1. Open the codes.csv from the DATA folder in read mode
# 2. For every record in the codes.csv file get the all the fields, store in variables, but concatenate the 3rd and 4th fields.
# 3. Then concatenate the already concatenated 3rd and 4th field with the question from the get_questions() function
# 4. Send the concatenated string to the OpenAI API
# 5. Receive the answers in six different parts, separated by a "|" (pipe)
# 6. Store the previously extracted 4 fields and the answers in the list results
# 7. Create a new CSV from the results list and save it in the DATA folder
def process_codes():
    # Set counter to 0
    # counter = 0
    # Open the codes.csv from the DATA folder in read mode
    with open('../DATA/codes_main.csv', 'r') as file:
        reader = csv.reader(file)

        # Create an array of lists results to store the results from OAI
        results = []
        # For every record in the codes.csv file
        for row in reader:

            # Concatenate the 3rd and 4th fields
            concatenated = 'Change in file: ' + row[2] + '\n' + 'Code changes: ' + row[3] + '\n'

            # Concatenate file name and code changes with the questions prepared for the OpenAI API.
            question = concatenated + '\n' + get_questions()

            # Extract the generated text from the response
            generated_text = get_answers(question)

            # Remove the ** from the text, as well as preceding '- '
            generated_text = generated_text.replace("**", "").replace("- ", "")
            # Remove sequence of two or more #'s from text
            generated_text = re.sub(r'#\s*#', '', generated_text)
            # Remove any newline from the text
            generated_text = generated_text.replace('\n', '')

            # If encounters "-------" then delete this and anything below that
            #if "-------" in generated_text:
            #    generated_text = generated_text[:generated_text.index("-------")]

            print("generated_text: ", generated_text)
            # Parse the generated text into parts
            # part = generated_text.split("|")
            # part = generated_text.split("\n")
            #print(generated_text)
            # print(part)
            # exit(0)

            # Wait for key press to continue
            #input("Press Enter to continue...")
            # Wait for a key press
            #keyboard.wait()
            #print("A key has been pressed!")


            #print(row)
            #print(part)
            #exit(0)

            # Store the previously extracted 4 fields and the answers in the list results
            ## results.append([row[0], row[1], row[2], row[3], part[0], part[1], part[2], part[3], part[4], part[5]])
            results.append([generated_text])
            #print(results)
            # exit(0)

    # Create a new CSV from the results list and save it in the DATA folder, always open it in append mode.
    with open('../DATA/results_gpt-4o-mini.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
        # print("Data has been successfully exported to DATA/results_full.csv")

    # Close codes.csv
    # file.close()


def main():
    # Call the process_codes() function
    process_codes()

if __name__ == "__main__":
    main()

