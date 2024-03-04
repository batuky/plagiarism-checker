import pandas as pd
import os
import string

class TextCleaner:
    def __init__(self):
        self.stop_words = [
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
        
        self.unnecessary_phrases = [
    'devam etmek i̇çi̇n tiklayiniz',
    'haberi̇n devami di̇ğer sayfadagtgtgt',
    'haberi̇n devami di̇ğer sayfada',
    'gt','---'
    ]
        self.punctuation_marks = ".,:;\'\"’’?!…“”()'’–%&/=*‘"
        self.input_folders = {
            'articles': 'seperated_datas/seperated_datas/cleaned_data_article.xlsx',
            'posts': 'seperated_datas/seperated_datas/cleaned_data_post.xlsx',
            'photo-posts': 'seperated_datas/seperated_datas/cleaned_data_photo-post.xlsx',
            'video-posts': 'seperated_datas/seperated_datas/cleaned_data_video-post.xlsx'
        }
        self.output_folder = 'processed_datas'
    
    def create_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def clean_text(self, text):
        if pd.isnull(text):
            return ''
        text = text.lower()
        for phrase in self.unnecessary_phrases:
            text = text.replace(phrase, '')
        text = text.translate(str.maketrans('', '', self.punctuation_marks))
        words = text.split()
        return ' '.join(word for word in words if word.lower() not in self.stop_words)

    def process_file(self, input_path, output_path):
        df = pd.read_excel(input_path)
        df['title'] = df['title'].apply(self.clean_text)
        df['description'] = df['description'].apply(self.clean_text)
        df['content'] = df['content'].apply(self.clean_text)
        new_df = df[['id', 'url', 'type', 'title', 'description', 'content', 'status', 'published_at', 'updated_at']]
        new_df.to_excel(output_path, index=False)

    def clean_files(self):
        self.create_output_folder()

        for key, input_path in self.input_folders.items():
            file_name = os.path.basename(input_path).split('.')[0] + '_processed.xlsx'
            output_path = os.path.join(self.output_folder, file_name)
            self.process_file(input_path, output_path)
            print(f'Processed and saved: {output_path}')

if __name__ == "__main__":
    cleaner = TextCleaner()
    cleaner.clean_files()