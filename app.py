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

no_detected_kata_terikat = True

print("\nBerikut list kata terikat:")
        
# Search kata terikat 1 word
for pattern, word_without_pattern, word, index in unique_data:
    # Jika bukan maha dan sesuai kata terikat maka pasti benar
    if ('-' not in word and word_without_pattern != ''):
        if (pattern != 'maha' and pattern != 'Maha' and (word_without_pattern in word_list) and word not in word_list):
            no_detected_kata_terikat = False
            print(word + " benar di index " + str(index))
        else:
            if (pattern == 'maha' or pattern == 'Maha'):
                no_detected_kata_terikat = False
                # Jika maha diikuti esa harus di spasi
                if (word_without_pattern == 'esa' or word_without_pattern == 'Esa'):
                    print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + pattern.title() + " " + word_without_pattern.title())
                
                else:
                    # Jika maha diikuti kata dasar, benar
                    if (word_without_pattern in word_list):
                        print(word + " benar di index " + str(index))
                    # Jika maha diikuti kata turunan harus dipisah
                    else:
                        print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + pattern.title() + " " + word_without_pattern.title())

    # Jika ada dash (tanda hubung)
    if ('-' in word and word[0] != '-' and word[-1] != '-'):
        word_without_dash = word.translate(str.maketrans("", "", r"-"))
        word_without_dash_and_pattern = word_without_pattern.translate(str.maketrans("", "", r"-"))

        if (pattern != word_without_dash_and_pattern):
            # Jika ada tanda dash tetapi seharusnya tidak
            if (word_without_dash_and_pattern in word_list):
                no_detected_kata_terikat = False
                print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + word_without_dash)
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
    if (result[1] in word_list) and result[0] != 'kata' and result[0].lower() != 'maha' and word not in word_list and result[0] in patterns:
        no_detected_kata_terikat = False
        print(bigram_text + " salah di index " + str(index) + ". rekomendasi yang diberikan: " + word)

    # Jika terpisah dengan spasi namun seharusnya diberi tanda hubung (-)
    if (result[1][0].isupper()) and result[0] != 'kata' and result[0].lower() != 'maha' and result[0] in patterns and result[1] in word_list:
        no_detected_kata_terikat = False
        print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + result[0] + '-' + result[1])
        
    #Jika ada Maha dan dipisah dengan kata selanjutnya, digabung kecuali Esa
    if result[0] == 'Maha' and result[1].lower() != 'esa':
        no_detected_kata_terikat = False
        if result[1].lower() in word_list:
            print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + result[0] + result[1].lower())

        # Jika Maha dipisah dan diikuti kata turunan
        else:
            print(bigram_text + " benar di index " + str(index))
    else:
        # Jika Maha Esa maka benar
        if result[0] == 'Maha' and result[1] == 'Esa':
            print(bigram_text + " benar di index " + str(index))
        else:
            # Jika Maha esa, maka Maha Esa
            if result[0] == 'Maha' and result[1] == 'esa':
                print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: Maha Esa")

# Jika tidak ada kata terikat
if (no_detected_kata_terikat):
    print("Tidak ada kata terikat yang ditemukan")
