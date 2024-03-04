import os
import tarfile
import json
import pandas as pd
from typing import List

def extract_tar_files(directory: str) -> List[str]:
    """
    Given a directory, this function will find all '.tar.gz' files
    and return a list of their file paths.
    """
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.tar.gz')]

def extract_json_from_tar(tar_path: str, temp_dir: str) -> List[dict]:
    """
    Extracts 'data.json' files from a specified tar.gz file and returns
    a list of dictionaries containing the contents of each 'data.json' file.
    """
    contents = []
    with tarfile.open(tar_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if 'data.json' in member.name:
                tar.extract(member, path=temp_dir)
                json_path = os.path.join(temp_dir, member.name)
                with open(json_path, 'r', encoding='utf-8') as json_file:
                    contents.append(json.load(json_file))
                os.remove(json_path)
    return contents

def create_dataframe_from_contents(contents: List[dict]) -> pd.DataFrame:
    """
    Receives a list of dictionaries and converts them into a pandas DataFrame.
    Avoids concatenating empty or all-NA entries by pre-filtering.
    """
    # Create DataFrames from JSON content and filter out empty or all-NA DataFrames
    dfs = [pd.json_normalize(content) for content in contents if content]
    non_empty_dfs = [df for df in dfs if not df.empty and not df.isna().all().all()]

    # Concatenate the non-empty DataFrames while ignoring empty or all-NA DataFrames
    if non_empty_dfs:
        # Concatenating only non-empty dataframes to avoid FutureWarning
        return pd.concat(non_empty_dfs, ignore_index=True).dropna(how="all")
    else:
        # Return an empty DataFrame with no columns if all DataFrames are empty
        return pd.DataFrame()

def write_dataframe_to_excel(dataframe: pd.DataFrame, output_path: str) -> None:
    """
    Writes the provided DataFrame to an Excel file at the specified output path.
    """
    dataframe.to_excel(output_path, index=False)

def sanitize_cell(cell):
    """
    Cleans a single cell within a DataFrame from unwanted unicode characters and returns the cleaned cell.
    """
    if isinstance(cell, str):
        cell = cell.replace('\u2022', '')  # Remove bullet point unicode character
        cell = cell.replace('â˜»', '')      # Example of another character removal
        return cell
    else:
        return cell

def sanitize_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, List[dict]]:
    """
    Cleans each cell in the DataFrame and returns a tuple of the cleaned DataFrame and a list of error records.
    """
    error_records = []
    for index, row in df.iterrows():
        try:
            df.loc[index] = row.apply(sanitize_cell)
        except ValueError as e:
            error_records.append({'old_id': row.get('old_id'), 'id': row.get('id')})
            df = df.drop(index)

    return df, error_records

def write_errors_to_excel(errors: List[dict], output_path: str) -> None:
    """
    Writes a list of error records to an Excel file at the specified output path.
    """
    if errors:
        errors_df = pd.DataFrame(errors)
        errors_df.to_excel(output_path, index=False)

def main():
    work_dir = './tarfiles'
    temp_dir = './temporary'
    output_excel = 'output.xlsx'
    errors_excel = 'errors.xlsx'

    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)

    tar_files = extract_tar_files(work_dir)
    all_contents = []

    for tar_file in tar_files:
        contents = extract_json_from_tar(tar_file, temp_dir)
        all_contents.extend(contents)

    df_contents = create_dataframe_from_contents(all_contents)
    
    # Sanitize the DataFrame and collect error records
    df_sanitized, error_records = sanitize_dataframe(df_contents)

    write_dataframe_to_excel(df_sanitized, output_excel)
    print(f'Data has been written to {output_excel}')

    # Write error records to Excel file
    write_errors_to_excel(error_records, errors_excel)
    if error_records:
        print(f'Error IDs have been written to {errors_excel}')

if __name__ == "__main__":
    main()