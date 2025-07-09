# app.py

from flask import Flask, render_template, request, url_for
import pandas as pd
import numpy as np
import re
import ast
import matplotlib.pyplot as plt
import seaborn as sns

# Import library machine learning
from imblearn.over_sampling import RandomOverSampler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

app = Flask(__name__)

# ============ 1. DATA LOADING DAN PREPROCESSING ============
# Misalnya file data di "data/data_webtoon_clean.xlsx"
df = pd.read_excel('data/data_webtoon_clean.xlsx')

# Fungsi preprocessing sederhana
def processed_text(text):
    # Contoh membersihkan teks (lowercase, hapus karakter aneh, dll.)
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)  # Hanya huruf, angka, dan spasi
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Terapkan preprocessing pada kolom ringkasan_clean
df['ringkasan_clean'] = df['ringkasan_clean'].apply(processed_text)

# Memisahkan input (X) dan label (y)
X = df[['ringkasan_clean']]
y = df['genre']

# Menangani ketidakseimbangan data dengan RandomOverSampler
ros = RandomOverSampler()
X_res, y_res = ros.fit_resample(X, y)

# Konversi ke Series
X_res_series = pd.Series(X_res['ringkasan_clean'].values)
y_res_series = pd.Series(y_res)

# Ganti X dan y menjadi data oversampled
X = X_res_series
y = y_res_series

# ============ 2. TF-IDF DAN FEATURE SELECTION ============
tf_idf = TfidfVectorizer(ngram_range=(1,1))
tf_idf.fit(X)
X_tf_idf = tf_idf.transform(X).toarray()

# Feature selection
chi2_features = SelectKBest(chi2, k=5000)
X_kbest_features = chi2_features.fit_transform(X_tf_idf, y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_kbest_features, y, test_size=0.2, random_state=42
)

# ============ 3. PEMILIHAN MODEL TERBAIK (LINEAR SVC) ============
model = svm.LinearSVC(random_state=42)
model.fit(X_train, y_train)

# (Opsional) Evaluasi singkat model
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Akurasi model (LinearSVC):", acc)


# ============ 4. FUNGSI PREDIKSI ============
def predict_genre_for_user_input(user_input: str):
    # Preprocessing input
    user_input_processed = processed_text(user_input)

    # Transform TF-IDF
    user_input_tfidf = tf_idf.transform([user_input_processed]).toarray()

    # Feature Selection
    user_input_kbest = chi2_features.transform(user_input_tfidf)

    # Predict
    predicted_genre = model.predict(user_input_kbest)
    return predicted_genre[0]


# ============ 5. ROUTES FLASK ============
@app.route('/')
def home():
    # Halaman utama dengan form input
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Ambil input user dari form
    user_input = request.form.get("komik_input")
    
    if not user_input.strip():
        # Jika kosong, kembalikan ke halaman utama
        return render_template('index.html', error="Teks ringkasan belum diisi!")

    # Lakukan prediksi
    hasil_genre = predict_genre_for_user_input(user_input)

    # Kirim hasil ke halaman result.html
    return render_template('result.html', 
                           ringkasan=user_input, 
                           genre=hasil_genre)


if __name__ == '__main__':
    # Jalankan Flask
    app.run(debug=True)
