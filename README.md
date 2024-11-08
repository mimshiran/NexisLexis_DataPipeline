# NexisLexis_DataPipeline

This repository provides tools for validating, extracting, processing, and segmenting JSON-formatted media transcripts, specifically tailored for bulk data scraped from Lexis Nexis. It includes functions for parsing text and metadata, identifying errors, handling hierarchical data structures, and segmenting transcripts by speaker, enabling streamlined analysis of media content with structured speaker metadata.

## Features

- **JSON Structure Validation**: Checks each JSON file to ensure required fields are present.
- **Data Extraction**: Extracts key metadata and content, including:
  - `result ID`, `title`, `byline`, `date`, `source name`, `highlights`, `headlines`, `guest names`, and `body content`.
- **Error Detection**: Identifies and logs files with structural issues or missing content for easier debugging.
- **Text Processing**: Cleans and formats extracted text, removing video clips and timestamp markers.
- **Speaker Segmentation**: Segments transcripts by speaker using regex patterns, producing structured text segments with associated metadata.
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

4. **Run Speaker Segmentation**:
   To process and segment speaker data, run the segmentation script:
   ```bash
   python parse_segment_speakers.py
   ```

5. **Output**:
   - Extracted metadata and cleaned content will be stored in the specified output directory.
   - Speaker-segmented data will be saved in a Parquet file, making it efficient for further analysis.

## Folder Structure

- **/data**: Directory to store your JSON files.
- **/output**: (Optional) Directory to save processed data files.
- **/segments**: Optional folder for keeping modularized scripts.

## Error Handling

- Logs files with issues (e.g., decoding errors, missing fields) and stores the list in `error_files` for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
