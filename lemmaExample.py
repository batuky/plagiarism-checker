import zeyrek

# Morfologik Analiz için Zeyrek Analyzer'ı başlat
analyzer = zeyrek.MorphAnalyzer()

# Lemmatization uygulamak istediğiniz kelimeler
words = ["köpekler", "kitapları", "geliyor", "yazdılar", "okuyorsunuz"]

# Kelimelerin lemma hallerini bul
lemmas = [analyzer.lemmatize(word)[0][1][0] for word in words]
print(lemmas)