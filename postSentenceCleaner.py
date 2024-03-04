import pandas as pd
import string
import re

# List of unnecessary words
stop_words = [
    'acaba', 'ama', 'ancak', 'artık', 'asla', 'aslında', 'az', 'bana', 'bazen', 
    'bazı', 'bazıları', 'bazısı', 'belki', 'ben', 'beni', 'benim', 'beş', 'bile', 
    'bir', 'birçoğu', 'birçok', 'birçokları', 'biri', 'birisi', 'birkaç', 
    'birkaçı', 'birşey', 'birşeyi', 'biz', 'bize', 'bizi', 'bizim', 'böyle', 
    'böylece', 'bu', 'buna', 'bunda', 'bundan', 'bunu', 'bunun', 'burada', 'bütün',
    'çoğu', 'çoğuna', 'çoğunu', 'çok', 'çünkü', 'da', 'daha', 'de', 'değil', 
    'demek', 'diğer', 'diğeri', 'diğerleri', 'diye', 'dolayı', 'elbette', 'en', 
    'fakat', 'falan', 'felan', 'filan', 'gene', 'gibi', 'hangi', 'hangisi', 
    'hani', 'hatta', 'hem', 'henüz', 'hep', 'hepsi', 'hepsine', 'hepsini', 
    'her', 'her biri', 'herkes', 'herkese', 'herkesi', 'hiç', 'hiç kimse', 
    'hiçbiri', 'hiçbirine', 'hiçbirini', 'için', 'içinde', 'ile', 'ise', 
    'işte', 'kaç', 'kadar', 'kendi', 'kendine', 'kendini', 'ki', 'kim', 
    'kime', 'kimi', 'kimin', 'kimisi', 'madem', 'mı', 'mi', 'mu', 'mü', 
    'nasıl', 'ne', 'ne kadar', 'ne zaman', 'neden', 'nedir', 'nerde', 
    'nerede', 'nereden', 'nereye', 'nesi', 'neyse', 'niçin', 'niye', 
    'ona', 'ondan', 'onlar', 'onlara', 'onlardan', 'onların', 'onu', 
    'onun', 'orada', 'oysa', 'oysaki', 'öbürü', 'ön', 'önce', 'ötürü', 
    'öyle', 'sana', 'sen', 'senden', 'seni', 'senin', 'siz', 'sizden', 
    'size', 'sizi', 'sizin', 'son', 'sonra', 'seobilog', 'şayet', 'şey', 
    'şimdi', 'şöyle', 'şu', 'şuna', 'şunda', 'şundan', 'şunlar', 'şunu', 
    'şunun', 'tabi', 'tamam', 'tüm', 'tümü', 'üzere', 'var', 've', 'veya', 
    'veyahut', 'ya', 'ya da', 'yani', 'yerine', 'yine', 'yoksa', 'zaten', 'zira'
]

# Phrases to be removed
unnecessary_phrases = [
    'devam etmek i̇çi̇n tiklayiniz',
    'haberi̇n devami di̇ğer sayfadagtgtgt',
    'haberi̇n devami di̇ğer sayfada',
    'gt','---'
]

# Punctuation marks to be removed
# punctuation_marks = ".,:;\'\"’’?!…“”()'’–%&/=*‘"
punctuation_marks = ":;'\"’…“”()'’–%&/=*‘"


def clean_whitespace(text):
    # Function to correct extra spaces and tabs
    text = re.sub(r'\s+', ' ', text) # Replace extra whitespaces with a single space
    text = re.sub(r'\t', ' ', text)  # Replace tabs with spaces
    text = text.strip()              # Remove leading and trailing spaces
    return text

def turkish_lower(s):
    # Convert Turkish characters to lowercase correctly
    replacements = {
        'I': 'ı', 'İ': 'i',
        'Ç': 'ç', 'Ş': 'ş',
        'Ü': 'ü', 'Ö': 'ö',
        'Ğ': 'ğ'
    }
    for original, replacement in replacements.items():
        s = s.replace(original, replacement)
    return s.lower()

def remove_unnecessary_words_and_punctuations(text):
    # If text is NaN (float) or None, return an empty string
    if pd.isnull(text):
        return ''
    
    text = turkish_lower(text)
    
    # Remove unnecessary phrases
    for phrase in unnecessary_phrases:
        text = text.replace(phrase, '')

    # Remove punctuation marks
    text = text.translate(str.maketrans('', '', punctuation_marks))
    
    words = text.split()
    # Remove unnecessary words and punctuation marks
    filtered_words = [word for word in words if word.lower() not in stop_words]
    # Correct extra spaces and line ends
    cleaned_text = ' '.join(filtered_words)
    return clean_whitespace(cleaned_text)

# Path of the Excel file to be read
input_excel_path = 'cleaned_data_post.xlsx'
# Path of the Excel file to be written
output_excel_path = 'postNewTexts.xlsx'

# Read the Excel file
df = pd.read_excel(input_excel_path)

# Remove unnecessary words and punctuation marks from `title`, `description`, and `content` columns
df['title'] = df['title'].apply(remove_unnecessary_words_and_punctuations)
df['description'] = df['description'].apply(remove_unnecessary_words_and_punctuations)
df['content'] = df['content'].apply(remove_unnecessary_words_and_punctuations)

# Copy the relevant columns to a new DataFrame
new_df = df[['id', 'url', 'title', 'description', 'content']]

# Write to a new Excel file
new_df.to_excel(output_excel_path, index=False)

print('İşlem tamamlandı. Yeni dosya "{}" olarak kaydedildi.'.format(output_excel_path))