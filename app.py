# from flask import Flask, render_template, request
from kataTerikat import patterns, validateSatuKata, validateDuaKata
from preprocessing import preprocessing
from rabinKarp import rabinKarp 
from bigram import generate_bigrams
import warnings
# app = Flask(__name__, template_folder='html')

warnings.filterwarnings("ignore")

# Baca file txt sebagai input
with open('utapis.txt', 'r', encoding='utf-8') as file:
    text = file.read()

print("\nBerikut isi txt:\n")
print(text)
    
# Baca file txt sebagai kata dasar
with open('kata-dasar.txt', 'r') as file:
    word_list = [line.strip() for line in file.readlines()]

# print("\nBerikut isi txt kata dasar:\n")
# print(word_list)

# Preprocessing di preprocessing.py
hasil_preprocessing = preprocessing(text)

# rabinKarp algorithm untuk cari pattern pada input text di rabinKarp.py
detected_with_terikat_prefix = rabinKarp(hasil_preprocessing, patterns)
# print(detected_with_terikat_prefix)

# Sort dari index terkecil
sorted_data = sorted(detected_with_terikat_prefix, key=lambda x: x[-1])

# print("\nini data setelah di sort:\n")
# print(sorted_data)

# Remove duplicates based on the index
unique_data = {item[3]: item for item in sorted_data}.values()

# print("\nBerikut list kata dengan prefix dalam artikel:\n")
# print(list(unique_data))

# Deteksi untuk yang dipisah spasi (bigram)
bigrams = generate_bigrams(hasil_preprocessing)

detected_bigram_with_terikat_prefix = []

# Cari pattern di bigram
for text, index in bigrams:
    result = rabinKarp(text, patterns, True, index)
    if result != []:
        detected_bigram_with_terikat_prefix.append(result)

no_detected_kata_terikat = True

print("\nBerikut list kata terikat:")
no_detected_kata_terikat = validateSatuKata(unique_data, word_list)

if (detected_bigram_with_terikat_prefix != []):
    no_detected_kata_terikat = validateDuaKata(detected_bigram_with_terikat_prefix, word_list)

# Jika tidak ada kata terikat
if (no_detected_kata_terikat):
    print("Tidak ada kata terikat yang ditemukan")
