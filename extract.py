import os
import tarfile

def extract_all_tar_gz(source_directory: str, target_directory: str) -> None:
    """
    Extracts all .tar.gz files from the source directory to the target directory.
    Each tar.gz file will be extracted to a subdirectory under the target directory.
    """
    # Make sure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Loop through all files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith('.tar.gz'):
            # Construct the full path to the file
            file_path = os.path.join(source_directory, filename)
            # Define the extraction directory
            extract_dir = os.path.join(target_directory, filename[:-7])  # Removes '.tar.gz' from the name
            
            # Make sure the extraction directory exists
            if not os.path.exists(extract_dir):
                os.makedirs(extract_dir)

            # Extract the tar.gz file
            with tarfile.open(file_path, 'r:gz') as tar:
                tar.extractall(path=extract_dir)
                print(f'Extracted {filename} to {extract_dir}')

# Usage example
source_dir = './tarfiles'  # Replace with your source directory path
target_dir = './datas'  # Replace with your target directory path

extract_all_tar_gz(source_dir, target_dir)