import os
import re
import tkinter as tk
from tkinter import filedialog

# Patterns to identify unwanted details
REMOVE_PATTERNS = [
    r'\b\d{3,4}p\b',               # Resolutions like 720p, 1080p
    r'\bbluray\b|blu-ray',         # BluRay variations
    r'\bweb[-_. ]?dl\b',           # Variations of WEBDL
    r'\bx264\b|h264\b|aac\d+(\.\d+)?', # Encoding types and AAC variations
    r'\[.*?\]',                    # Content inside square brackets
    r'\{.*?\}',                    # Content inside curly braces
    r'[-_.]',                      # Dashes, underscores, and dots
    r'\b(?:yts|ganool|shaanig)\b', # Group names
    r'\b\d+mb\b|\b\d+gb\b',        # File sizes
    r'\s*[\[\]{}()\-_.,]\s*',      # Lone brackets, symbols, or special characters
]

# Function to clean up the movie name
def clean_movie_name(filename):
    # Remove the file extension
    name, _ = os.path.splitext(filename)
    
    # Apply all removal patterns
    for pattern in REMOVE_PATTERNS:
        name = re.sub(pattern, ' ', name, flags=re.IGNORECASE)
    
    # Remove any leading or trailing spaces, extra spaces between words
    name = re.sub(r'\s+', ' ', name).strip()

    # Final sanitization to remove empty parentheses and extra symbols
    name = re.sub(r'\(\)', '', name)  # Remove empty parentheses
    name = re.sub(r'\s*[\[\]{}()\-_.,]\s*', ' ', name)  # Remove lone symbols and parentheses
    name = re.sub(r'\s+', ' ', name).strip()  # Clean up extra spaces

    # Ensure the naming convention is Movie title (Year)
    name = correct_naming_convention(name)

    return name

# Function to enforce the naming convention "Movie title (Year)"
def correct_naming_convention(name):
    # Look for a year pattern like (2023)
    match = re.search(r'(\d{4})', name)
    if match:
        year = match.group(1)
        title = name[:match.start()].strip()  # Title is everything before the year

        # Ensure that the title is correctly formatted as "Movie title (Year)"
        name = f"{title} ({year})"
    else:
        # If no year found, add "(unknown year)"
        name = f"{name} (unknown year)"
        
    return name

# Function to rename video files in a given directory
def rename_video_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            # Clean up the movie name
            cleaned_name = clean_movie_name(filename)

            # Check for movie info using your external sources (e.g., OMDb or custom logic)
            # If movie info is found, the cleaned name will be used
            if cleaned_name != filename:
                # Form the new file path with the cleaned name
                new_file_path = os.path.join(directory, cleaned_name + os.path.splitext(filename)[1])
                
                # Perform the rename operation
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {filename} -> {cleaned_name}")
                except OSError as e:
                    print(f"Error renaming {filename}: {e}")
            else:
                print(f"Skipping: {filename} (Movie info not found)")

# Function to allow user to select a folder
def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title="Select Folder")
    return folder_path

# Run the renaming function
if __name__ == "__main__":
    folder = select_folder()  # Let the user select the folder
    if folder:
        rename_video_files(folder)  # Run the renaming process
    else:
        print("No folder selected. Exiting...")
