import os
import json
import re
import pandas as pd

def read_json_files(base_directory: str) -> pd.DataFrame:
    """
    Traverse the directory structure and read all 'data.json' files into a pandas DataFrame.
    Concatenates all data frames into a single DataFrame and excludes entirely empty or NA columns.
    """
    data_frames = []
    for root, dirs, files in os.walk(base_directory):
        for file_name in files:
            if file_name == 'data.json':
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    # Remove comments
                    data.pop('comments', None)
                    # Convert JSON data to a pandas DataFrame
                    data_frame = pd.json_normalize(data)
                    data_frames.append(data_frame)

    # Concatenate all DataFrames into a single DataFrame
    if data_frames:
        concatenated_df = pd.concat(data_frames, ignore_index=True)
        # Remove columns that are entirely empty or NA
        concatenated_df = concatenated_df.dropna(how='all', axis=1)
        return concatenated_df
    else:
        # If no DataFrame is found, return an empty DataFrame
        return pd.DataFrame()

def write_dataframe_to_excel(df: pd.DataFrame, output_path: str) -> None:
    """
    Writes the DataFrame to an Excel file.
    """
    df.to_excel(output_path, index=False)

def clean_text(text: str) -> str:
    """
    Removes HTML tags and illegal characters from the text.
    """
    # Remove HTML tags
    text = re.sub(r'<.*?>', ' ', text)

    # Replace illegal characters with an empty string
    illegal_chars = ['☻', '…', '�', '<', '>', '/']  # List more characters as needed
    for char in illegal_chars:
        text = text.replace(char, ' ')
    return text

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply text cleaning to the specified columns of a DataFrame.
    """
    text_columns = ['title', 'description', 'content']  # Replace with the actual column names
    for col in text_columns:
        # Non-string (float, NaN, etc.) değerleri string'e çevirin
        df[col] = df[col].fillna('')  # NaN değerleri boş string ile değiştirin
        df[col] = df[col].apply(clean_text)
    return df

def main():
    data_dir = './datas'
    output_excel = 'output.xlsx'

    # Read the contents of the JSON files into a DataFrame
    df = read_json_files(data_dir)

    # Clean the DataFrame
    df = clean_dataframe(df)

    # Write the DataFrame to an Excel file
    write_dataframe_to_excel(df, output_excel)
    print(f'Data has been written to {output_excel}')

if __name__ == "__main__":
    main()