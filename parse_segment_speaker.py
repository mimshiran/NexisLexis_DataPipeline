import re
import pandas as pd

# Load the transcript data from a Parquet file created using parse_transcripts.py

df = pd.read_parquet('../output/main_content.parquet')

# Initialize a list to store segmented data
segmented_data = []

# Track the current speaker to identify changes in speaker within each transcript
current_speaker = None

# Iterate through each row in the DataFrame, where each row represents a transcript
for index, row in df.iterrows():
    # Preprocess the byline to remove extra spaces and split by commas for each speaker
    processed_byline = [part.strip() for part in row['experts'].split(',')]
    
    # Extract last names from the byline and convert to uppercase for pattern matching
    last_names = [name.split()[-1].upper() for name in processed_byline if name]
    
    # Define regular expressions to match either full names or last names followed by a colon
    full_name_pattern = rf'\b({"|".join(re.escape(name) for name in last_names)}),'
    last_name_pattern = rf'\b({"|".join(re.escape(name.split()[-1]) for name in last_names)}):'
    
    # Split transcript content into paragraphs
    paragraphs = row['content'].split('</p><p>')
    
    # Initialize the current segment and metadata for each segment
    current_segment = ""
    segment_metadata = {
        'id': row['id'],
        'experts': row['experts']
    }
    
    # Iterate through each paragraph to identify speaker changes and segment content
    for paragraph in paragraphs:
        # Remove "<p nitf:lede="true">" tag if present
        paragraph = paragraph.replace('<p nitf:lede="true">', '')
        
        # Skip paragraphs that start with "UNIDENTIFIED MALE:" or "UNIDENTIFIED FEMALE:"
        if paragraph.strip().startswith("UNIDENTIFIED MALE:") or paragraph.strip().startswith("UNIDENTIFIED FEMALE:"):
            continue
        
        # Check if the paragraph contains a full name or last name followed by a colon to identify the speaker
        speaker_match = re.search(full_name_pattern, paragraph) or re.search(last_name_pattern, paragraph)
        
        if speaker_match:
            # Extract and clean the speaker name
            new_speaker = speaker_match.group(0).strip(':')
            
            # If a new speaker is identified, finalize the previous segment
            if new_speaker != current_speaker:
                # Append the completed segment to the list if it contains content
                if current_segment.strip():
                    segment_data = {
                        'Segment': current_segment.strip(),
                        **segment_metadata
                    }
                    segmented_data.append(segment_data)
                
                # Start a new segment with the current paragraph as content
                current_segment = paragraph
                current_speaker = new_speaker
            else:
                # Append the paragraph to the current segment if the speaker remains the same
                current_segment += paragraph
        else:
            # Append the paragraph to the current segment if no speaker is identified
            current_segment += paragraph
    
    # Append the last segment after finishing all paragraphs for the current row
    if current_segment.strip():
        segment_data = {
            'Segment': current_segment.strip(),
            **segment_metadata
        }
        segmented_data.append(segment_data)

# Convert the list of segments into a DataFrame
segment_df = pd.DataFrame(segmented_data)

# Save the segmented data to a new Parquet file
parquet_filename = '../output/segment_speaker_transcript.parquet'
segment_df.to_parquet(parquet_filename, index=False)
