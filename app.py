# from flask import Flask, render_template, request
from kataTerikat import patterns
from preprocessing import preprocessing
from rabinKarp import rabinKarp
from rabinKarp import detect_pattern 
from bigram import generate_bigrams
from bigram import split_words
import warnings
# app = Flask(__name__, template_folder='html')

warnings.filterwarnings("ignore")

# Baca file txt sebagai input
with open('utapis.txt', 'r') as file:
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

no_detected_kata_terikat = True

print("\nBerikut list kata terikat:")
        
# Search kata terikat 1 word
for pattern, word_without_pattern, word, index in unique_data:
    
    # Jika kata terikat benar
    if (word_without_pattern in word_list) and word not in word_list:
        no_detected_kata_terikat = False
        print(word + " benar di index " + str(index))

    # Jika ada dash (tanda hubung)
    if ('-' in word):
        word_without_dash = word.translate(str.maketrans("", "", r"-"))
        word_without_dash_and_pattern = word_without_pattern.translate(str.maketrans("", "", r"-"))

        # Jika ada tanda dash tetapi seharusnya tidak
        if (word_without_dash_and_pattern in word_list):
            no_detected_kata_terikat = False
            print(word + " salah di index " + str(index) + " rekomendasi yang diberikan: " + word_without_dash)
        else:

            # Jika ada tanda dash tetapi kata kedua diawali dengan huruf kapital
            if (word_without_dash_and_pattern[0].isupper()):
                no_detected_kata_terikat = False
                print(word + " benar di index " + str(index))

# Deteksi untuk yang dipisah spasi (bigram)
bigrams = generate_bigrams(hasil_preprocessing)

detected_bigram_with_terikat_prefix = []

# Cari pattern di bigram
for text, index in bigrams:
    is_pattern = detect_pattern(text, patterns, index)
    if is_pattern != None:
        detected_bigram_with_terikat_prefix.append(is_pattern)

for pattern, bigram_text, index in detected_bigram_with_terikat_prefix:
    result = split_words(bigram_text)
    word = bigram_text.replace(" ", "")

    # Jika terpisah dengan spasi namun seharusnya digabung
    if (result[1] in word_list) and word not in word_list and result[0] in patterns:
        no_detected_kata_terikat = False
        print(bigram_text + " salah di index " + str(index) + " rekomendasi yang diberikan: " + word)

    # Jika terpisah dengan spasi namun seharusnya diberi tanda hubung (-)
    if (result[1][0].isupper()) and word not in word_list and result[0] in patterns:
        no_detected_kata_terikat = False
        print(bigram_text + " salah di index " + str(index) + " rekomendasi yang diberikan: " + result[0] + '-' + result[1])

if (no_detected_kata_terikat):
    print("Tidak ada kata terikat yang ditemukan")
