import pandas as pd
import json
import os
from typing import Dict, Any

class ExcelToJsonConverter:
    """
    A class for converting Excel files to JSON format.
    """
    
    def __init__(self, input_folder: str):
        """
        The initializer method of the class.

        :param input_folder: The path of the folder where the input Excel files are located
        """
        self.input_folder = input_folder

    @staticmethod
    def read_excel_file(file_path: str) -> pd.DataFrame:
        """
        Reads an Excel file and returns it as a pandas DataFrame.

        :param file_path: The path of the Excel file to be read
        :return: A pandas DataFrame containing the Excel data
        """
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            print(f"Excel dosyası okunurken bir hata oluştu: {e}")
            exit()

    @staticmethod
    def convert_row_to_json(row: pd.Series) -> Dict[str, Any]:
        """
        Converts a DataFrame row to JSON format.

        :param row: DataFrame row
        :return: A dictionary in JSON format
        """
        return {
            'id': row['id'],
            'url': row.get('url', ''),
            'type': row.get('type', ''),
            'title': row.get('title', ''),
            'description': row.get('description', ''),
            'content': row.get('content', ''),
            'status': row.get('status', ''),
            'published_at': row.get('published_at', ''),
            'updated_at': row.get('updated_at', '')
        }

    @staticmethod
    def save_json_to_file(data: Dict[str, Any], output_directory: str, file_name: str):
        """
        Writes JSON data to a file.

        :param data: Data in JSON format
        :param output_directory: The folder where the JSON file will be saved
        :param file_name: The name of the JSON file to be created
        """
        file_path = os.path.join(output_directory, f"{file_name}.json")
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    @staticmethod
    def create_output_directory(directory_name: str):
        """
        Creates the output folder.

        :param directory_name: The name of the folder to be created
        """
        os.makedirs(directory_name, exist_ok=True)

    def process_excel_to_json(self, excel_path: str, output_folder: str):
        """
        Converts Excel data to JSON and saves it to a file.

        :param excel_path: The path of the Excel file to be processed
        :param output_folder: The folder where the JSON files will be saved
        """
        df = self.read_excel_file(excel_path)
        self.create_output_directory(output_folder)
        
        for _, row in df.iterrows():
            json_data = self.convert_row_to_json(row)
            self.save_json_to_file(json_data, output_folder, str(json_data['id']))

        print(f'JSON dosyaları {output_folder} içerisinde başarıyla oluşturuldu.')

    def process_all_excels(self):
        """
        Processes all Excel files in the input folder.
        """
        for file in os.listdir(self.input_folder):
            if file.endswith('.xlsx'):
                file_path = os.path.join(self.input_folder, file)
                folder_name = file.rsplit('.', 1)[0]
                output_folder = os.path.join(self.input_folder, folder_name)
                self.process_excel_to_json(file_path, output_folder)


if __name__ == "__main__":
    # Variables defined by the user
    INPUT_FOLDER = './processed_datas'  # The folder where the input Excel files are located
    converter = ExcelToJsonConverter(INPUT_FOLDER)
    converter.process_all_excels()