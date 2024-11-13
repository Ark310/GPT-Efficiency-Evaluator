import pandas as pd
import json
import os
import sys

# Check if the user provided an Excel file name as an argument
if len(sys.argv) < 2:
    print("Usage: python excel_to_json.py <excel_file_name>")
    sys.exit(1)

# Get the Excel file name from the command-line argument
input_file = sys.argv[1]

# Verify if the specified file exists
if not os.path.isfile(input_file):
    print(f"Error: File '{input_file}' not found.")
    sys.exit(1)

# Read the Excel sheet using pandas
try:
    df = pd.read_excel(input_file, header=0)
    # Strip any leading or trailing whitespace from column names
    df.columns = df.columns.str.strip()
    print("Columns:", df.columns)  # Debugging line to check column names
except Exception as e:
    print(f"Error reading the Excel file: {e}")
    sys.exit(1)

# Define the output folder name
output_folder = 'output_json'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Created folder: {output_folder}")
else:
    print(f"Using existing folder: {output_folder}")

# Iterate through each row of the DataFrame
for index, row in df.iterrows():
    try:
        # Extract the question (first column)
        question = row[df.columns[0]]

        # Extract options from columns 1 to 4 (B to E)
        options = [row[df.columns[i]] for i in range(1, 5)]

        # Extract the answer key (last column)
        answer_key = row[df.columns[-1]].strip()

        # Determine the correct answer based on the answer key ('A', 'B', 'C', 'D')
        answer_index = ord(answer_key.upper()) - ord('A')  # Convert 'A' -> 0, 'B' -> 1, etc.
        if 0 <= answer_index < 4:
            anticipated_answer = options[answer_index]
        else:
            print(f"Invalid answer key in row {index + 1}. Skipping.")
            continue

        # Create a JSON object with the required format, including the 'options' field
        json_data = {
            "question": question,
            "options": options,
            "anticipated_answer": anticipated_answer,
            "gpt_response": ""
        }

        # Define the output file name (e.g., question_1.json, question_2.json, etc.)
        output_file = os.path.join(output_folder, f"{input_file} question_{index + 1}.json")

        # Write the JSON data to a file
        with open(output_file, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        print(f"Successfully created: {output_file}")

    except Exception as e:
        print(f"Error processing row {index + 1}: {e}")

print("All questions processed and JSON files generated.")
