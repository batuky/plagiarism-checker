import os
import json
import pandas as pd
from datetime import datetime

def load_excel_data(file_path):
    """Loads the Excel file and converts 'published_at' column to datetime."""
    df = pd.read_excel(file_path)
    df['published_at'] = pd.to_datetime(df['published_at'])
    return df

def create_directory(path):
    """Creates a directory if it does not exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_to_json(file_path, data):
    """Writes the data to a JSON file in the specified format."""
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

def filter_posts_by_date(df, year, start_month, end_month):
    """Filters the DataFrame for a specific year and range of months."""
    mask = (df['published_at'].dt.year == year) & \
           (df['published_at'].dt.month >= start_month) & \
           (df['published_at'].dt.month <= end_month)
    return df.loc[mask]

def convert_dates_to_string(data):
    """Converts date-times to string format."""
    data['published_at'] = data['published_at'].strftime('%Y-%m-%d %H:%M:%S')
    return data

def main():
    df = load_excel_data('lemma_post_newTexts.xlsx')

    for year in range(2014, 2025):
        for period in ['ilk 6', 'son 6']:
            start_month, end_month = (1, 6) if period == 'ilk 6' else (7, 12)
            filtered_df = filter_posts_by_date(df, year, start_month, end_month)
            directory = f'seperated_posts/{year} {period}'
            create_directory(directory)

            for index, row in filtered_df.iterrows():
                file_path = os.path.join(directory, f"{row['id']}.json")
                data_to_save = convert_dates_to_string(row.to_dict())
                save_to_json(file_path, data_to_save)

    print("İşlem tamamlandı.")

if __name__ == "__main__":
    main()