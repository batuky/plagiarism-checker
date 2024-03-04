import pandas as pd
from nltk.tokenize import word_tokenize
from nltk import download
download('punkt')  # Necessary dataset for the tokenizer

def tokenize_content(content):
    """Splits the text into tokens and returns a list of tokens."""
    return word_tokenize(content)

def main():
    # Read the Excel file
    df = pd.read_excel('cleaned_data_post.xlsx')

    # Split the `content` column into tokens using NLTK's tokenization function
    df['tokened_content'] = df['content'].astype(str).apply(tokenize_content)

    # Convert the tokenized content to a string
    df['tokened_content'] = df['tokened_content'].apply(lambda tokens: ' '.join(tokens))

    # Save the DataFrame to a new Excel file
    df.to_excel('tokened_post.xlsx', index=False)

if __name__ == "__main__":
    main()