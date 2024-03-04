import pandas as pd
import zeyrek
from concurrent.futures import ThreadPoolExecutor

def initialize_analyzer():
    """Start the Zeyrek Analyzer for Morphological Analysis."""
    return zeyrek.MorphAnalyzer()

def lemmatize_text(text, analyzer):
    """Perform lemmatization on the given text."""
    words = text.split()  # Kelimelere ayır
    lemmas = []
    for word in words:
        analyzed = analyzer.lemmatize(word)
        # If the lemmatization result is empty, use the word itself
        lemma = analyzed[0][1][0] if analyzed else word
        lemmas.append(lemma)
    return ' '.join(lemmas)  # Join and return the lemmas

def lemmatize_content_column(df, analyzer):
    """Apply lemmatization to the 'content' column of the DataFrame and store the results in 'lemmatized_content' column."""
    with ThreadPoolExecutor() as executor:
        lemmatized_contents = list(executor.map(lambda text: lemmatize_text(text, analyzer), df['content'].astype(str)))
        
        # Add the new lemmatized results as 'lemmad_content' column
        df['lemmatized_content'] = lemmatized_contents
    
    # Print the lemmatized content in the terminal
    for content in lemmatized_contents:
        print(content)
        
    return df

def save_to_excel(df, filename):
    """Save the DataFrame to an Excel file."""
    df.to_excel(filename, index=False)

def main():
    # Initialize the Zeyrek Analyzer for Morphological Analysis
    analyzer = initialize_analyzer()

    # Read the Excel file
    df = pd.read_excel('tokened_post.xlsx')

    # Apply lemmatization to `content` column and add the new lemmatized content as 'lemmad_content'
    df = lemmatize_content_column(df, analyzer)

    # Save the DataFrame to a new Excel file
    save_to_excel(df, 'lemma_post.xlsx')

if __name__ == "__main__":
    main()
    