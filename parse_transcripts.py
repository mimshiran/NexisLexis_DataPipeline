import os
import json
import re
import pandas as pd
from bs4 import BeautifulSoup

# Define the root directory containing JSON files and output directory for saving results
root_folder_path = '../nexislexis/'
output_directory = '../output/'

# Ensure the output directory exists, creating it if necessary
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def check_json_structure(file_path):
    """
    Checks if a JSON file has the expected structure.
    
    Parameters:
    ----------
    file_path : str
        The path to the JSON file being validated.
    
    Returns:
    -------
    bool
        True if the JSON structure contains a 'value' key associated with a list, False otherwise.
    """
    try:
        # Open the JSON file and load its content
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            # Check if 'value' key exists and is associated with a list
            if 'value' in data and isinstance(data['value'], list):
                return True
            else:
                return False
    except json.JSONDecodeError:
        # Return False if JSON is malformed
        return False

# Initialize lists to store extracted data fields for analysis
error_files = []
all_result_ids = []
all_titles = []
all_bylines = []
all_dates = []
all_word_lengths = []
all_source_names = []
all_body_contents = []
all_highlights = []
all_headlines = []
all_guests = []

# Iterate through all files in the specified root folder and its subdirectories
for root, _, files in os.walk(root_folder_path):
    for filename in files:
        # Process only JSON files, excluding system files and files with 'error' in the name
        if filename.endswith('.json') and not filename.startswith('._') and 'error' not in filename.lower():
            file_path = os.path.join(root, filename)
            
            # Skip files that do not have the required JSON structure
            if not check_json_structure(file_path):
                print(f"Invalid JSON structure in file: {file_path}")
                continue

            try:
                # Open and load the JSON file
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)

                # Loop through each item in the 'value' list of the JSON structure
                for item in data.get('value', []):
                    # Extract core metadata fields
                    result_id = item.get('ResultId', '').replace('urn:contentItem:', '')
                    title = item.get('Title', '')
                    byline = item.get('Byline', '')
                    date = item.get('Date', '')
                    word_length = item.get('WordLength', 0)
                    source_name = item.get('Source', {}).get('Name', '')

                    # Extract document content, ensuring it exists and is a dictionary
                    document = item.get('Document')
                    if document is not None and isinstance(document, dict):
                        # Retrieve the 'Content' field inside 'Document'; handle missing content
                        document_content = document.get('Content', '')
                    else:
                        document_content = ''

                    # Check for missing document content and skip if not present
                    if document_content is None:
                        print(f"Missing document content in file: {file_path}")
                        continue
                    
                    # Use BeautifulSoup to parse and extract specific HTML elements from content
                    soup = BeautifulSoup(document_content, 'html.parser')
                    
                    # Extract highlight text, joining multiple highlights with spaces
                    highlight_text = ' '.join([highlight.get_text() for highlight in soup.find_all('highlight')])
                    
                    # Extract headline text, joining multiple headline elements
                    headline_text = ' '.join([headline.get_text() for headline in soup.find_all('nitf:hl1')])

                    # Extract guest names, if any, and join them with commas
                    guest_names = []
                    guest_name_elements = soup.select('guests nameText')
                    guest_name_list = [name_text.get_text() for name_text in guest_name_elements]
                    guest_names.append(', '.join(guest_name_list))

                    # Extract and clean body content from 'nitf:body.content' tag
                    body_content_match = soup.find('nitf:body.content')
                    if body_content_match:
                        body_content_match = str(body_content_match)
                        # Remove video clips and timestamp markers for cleaner data
                        body_content_match = re.sub(r'\(BEGIN VIDEO CLIP\).*?\(END VIDEO CLIP\)', '', body_content_match, flags=re.DOTALL)
                        body_content_match = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', body_content_match)
                        body_content_match = re.sub(r'<nitf:body.content>|</nitf:body.content>|<bodytext>|</bodytext>', '', body_content_match)
                        all_body_contents.append(body_content_match)
                    else:
                        all_body_contents.append('')

                    # Append extracted data to their respective lists
                    all_result_ids.append(result_id)
                    all_titles.append(title)
                    all_bylines.append(byline)
                    all_dates.append(date)
                    all_word_lengths.append(word_length)
                    all_source_names.append(source_name)
                    all_highlights.append(highlight_text)
                    all_headlines.append(headline_text)
                    all_guests.append(', '.join(guest_names))

            except (UnicodeDecodeError, json.JSONDecodeError, ValueError, KeyError) as e:
                # Catch any file errors during processing and log them
                print(f"Error in file: {file_path}")
                print(f"Error type: {type(e).__name__}")
                print(f"Error message: {e}")
                error_files.append(file_path)
                continue

# Create a DataFrame from the extracted data
main_df = pd.DataFrame({
    'id': all_result_ids,
    'title': all_titles,
    'byline': all_bylines,
    'date': all_dates,
    'wordlength': all_word_lengths,
    'source': all_source_names,
    'content': all_body_contents,
    'highlight': all_highlights,
    'guest': all_guests
})

# Save the DataFrame to a Parquet file
parquet_filename = os.path.join(output_directory, 'main_content.parquet')
main_df.to_parquet(parquet_filename, index=False)
print(f"Data saved to {parquet_filename}")
