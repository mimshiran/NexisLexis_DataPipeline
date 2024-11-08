# NexisLexis_DataPipeline

This repository provides tools for validating, extracting, and processing JSON-formatted media transcripts, specifically tailored for bulk data scraped from Lexis Nexis. It includes functions for parsing text and metadata, identifying errors, and handling hierarchical data structures, enabling streamlined analysis of media content.

## Features

- **JSON Structure Validation**: Checks the structure of each JSON file to ensure required fields are present.
- **Data Extraction**: Extracts key information, including `result ID`, `title`, `byline`, `date`, `source name`, `highlights`, `headlines`, `guest names`, and `body content`.
- **Error Detection**: Identifies and logs files with structural issues or missing content.
- **Text Processing**: Cleans and formats extracted text, including removing video clips and timestamp markers.
- **Multimedia Parsing**: Uses BeautifulSoup to parse and extract text elements from HTML-encoded content within JSON files.

## Prerequisites

- **Python 3.x**
- **Libraries**: Install required libraries using:
  ```bash
  pip install -r requirements.txt
  ```
 
## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mimshiran/NexisLexis_DataPipeline.git
   cd NexisLexis_DataPipeline
   ```

2. **Set Root Folder Path**:
   Define the root directory for JSON files by setting `root_folder_path` in your script.

3. **Run the Script**:
   Execute the script to validate and extract data from JSON files:
   ```bash
   python parse_transcripts.py
   ```

4. **Output**:
   Extracted data will be stored in lists (or can be configured to save to a CSV/Excel file as needed).

## Folder Structure

- **/data**: Directory to store your JSON files.
- **/output**: (Optional) Directory to save processed data files.

## Error Handling

- Logs files with issues (e.g., decoding errors, missing fields) and stores the list in `error_files` for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
