import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Import kelas-kelas kustom dari model.py
from model_randomforest import *

def accuracy(y_true, y_pred):
    """
    Calculates the accuracy of predictions.

    Args:
        y_true (numpy.ndarray): True target labels.
        y_pred (numpy.ndarray): Predicted target labels.

    Returns:
        float: Accuracy score.
    """
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy

# Memuat dataset
data_obesitas = pd.read_csv('ObesityDataSet_raw_and_data_sinthetic.csv')

# Menghapus duplikat
data_obesitas.drop_duplicates(inplace=True)

# Encoding label dengan LabelEncoder terpisah untuk setiap kolom
label = ['Gender','family_history_with_overweight','FAVC','CAEC','SMOKE','SCC','CALC','MTRANS','NObeyesdad']
label_encoders = {}
for col in label:
    le = LabelEncoder()
    data_obesitas[col] = le.fit_transform(data_obesitas[col])
    label_encoders[col] = le

# Menghitung BMI
data_obesitas['BMI'] = round(data_obesitas['Weight'] / (data_obesitas['Height']) ** 2, 2)

# Menyimpan label_encoders untuk digunakan di app.py
joblib.dump(label_encoders, 'label_encoders.joblib')

# Memisahkan fitur dan target
X = data_obesitas.drop(columns=['NObeyesdad'])
y = data_obesitas.pop('NObeyesdad')

# Membagi data menjadi training dan testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Melatih model RandomForest
clf = RandomForest(n_trees=300,max_depth=20,min_samples_split=2)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Menghitung akurasi menggunakan fungsi manual
acc =  accuracy(y_test, y_pred)
print(acc)

# Menghitung akurasi dan laporan klasifikasi menggunakan sklearn
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)
print("Akurasi:", accuracy)
print("Laporan Klasifikasi:\n",report )

conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=np.unique(y_test), yticklabels=np.unique(y_test))
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Menyimpan model menggunakan joblib
joblib.dump(clf, 'model_random_forest.joblib')

print("Model berhasil dilatih dan disimpan sebagai 'model_random_forest.joblib'")
print("Label encoders berhasil disimpan sebagai 'label_encoders.joblib'")
