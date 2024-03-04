import os
import pandas as pd

def read_excel_file(file_path: str) -> pd.DataFrame:
    """A function that reads an Excel file and returns it as a DataFrame."""
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"{file_path} dosyası bulunamadı.")
        raise
    except Exception as e:
        print(f"Dosya okunurken bir hata oluştu: {e}")
        raise

def filter_columns(dataframe: pd.DataFrame, required_columns: list) -> pd.DataFrame:
    """A function that removes unnecessary columns and returns a DataFrame with the required columns."""
    return dataframe[required_columns]

def filter_rows_by_status(dataframe: pd.DataFrame, statuses_to_remove: list) -> pd.DataFrame:
    """A function that removes rows with specific status values."""
    return dataframe[~dataframe['status'].isin(statuses_to_remove)]

def save_to_excel(dataframe: pd.DataFrame, file_path: str) -> None:
    """A function that saves the DataFrame to an Excel file."""
    dataframe.to_excel(file_path, index=False)

def clean_and_save_excel(input_file_path: str, output_file_path: str, required_columns: list, statuses_to_remove: list) -> None:
    """The main function that cleans an Excel file and saves it to a new file."""
    df = read_excel_file(input_file_path)
    filtered_df = filter_columns(df, required_columns)
    cleaned_df = filter_rows_by_status(filtered_df, statuses_to_remove)
    save_to_excel(cleaned_df, output_file_path)
    print(f"Temizlenmiş veriler {output_file_path} dosyasına kaydedildi.")

def save_filtered_data_by_type(df: pd.DataFrame, type_name: str, output_dir: str, base_file_name: str) -> None:
    """A function that filters the DataFrame by the given type and saves it to a new Excel file."""
    filtered_df = df[df['type'] == type_name]
    # Create the full path where the file will be saved by combining the directory path and the file name
    directory = os.path.join(output_dir, 'seperated_datas')
    # Create the 'separated_datas' folder if it does not exist
    os.makedirs(directory, exist_ok=True)
    # Create the complete file path
    file_path = os.path.join(directory, f"{base_file_name}_{type_name}.xlsx")
    # Save the DataFrame to the Excel file
    filtered_df.to_excel(file_path, index=False)

def save_all_types_to_different_files(df: pd.DataFrame, output_dir: str, base_file_name: str, types: list) -> None:
    """A function that filters the DataFrame for each type and saves it to a different Excel file."""
    for type_name in types:
        save_filtered_data_by_type(df, type_name, output_dir, base_file_name)


if __name__ == "__main__":
    INPUT_FILE_PATH = 'output.xlsx'
    BASE_OUTPUT_FILE_PATH = 'cleaned_data'  # Dosya adının sabit kısmı, uzantı eklenmeden
    OUTPUT_FILE_DIR = './seperated_datas'  # Ayrılmış verilerin kaydedileceği dizin
    REQUIRED_COLUMNS = ['id', 'url', 'type', 'title', 'description', 'content', 'status', 'published_at', 'updated_at']
    STATUSES_TO_REMOVE = ['active', 'deleted', 'draft', 'passive', 'pending', 'unpublished']

    # Read and clean the Excel file
    df = read_excel_file(INPUT_FILE_PATH)
    filtered_df = filter_columns(df, REQUIRED_COLUMNS)
    cleaned_df = filter_rows_by_status(filtered_df, STATUSES_TO_REMOVE)

    # Save to different files for each type
    TYPES = ['article', 'photo-post', 'post', 'video-post']
    save_all_types_to_different_files(cleaned_df, OUTPUT_FILE_DIR, BASE_OUTPUT_FILE_PATH, TYPES)

    # Fix the file path and extension to save all cleaned data
    COMPLETE_OUTPUT_FILE_PATH = f"{OUTPUT_FILE_DIR}/cleaned_data_complete.xlsx"  # The complete file path and extension
    save_to_excel(cleaned_df, COMPLETE_OUTPUT_FILE_PATH)
    print(f"Tüm temizlenmiş veriler {COMPLETE_OUTPUT_FILE_PATH} dosyasına kaydedildi.")