from flask import Flask, render_template, request, jsonify
from kataTerikat import patterns, validateSatuKata, validateDuaKata
from preprocessing import preprocessing
from rabinKarp import rabinKarp 
from bigram import generate_bigrams
import warnings

app = Flask(__name__, template_folder='html')

@app.route('/', methods=['GET'])
def index():
    return render_template('id/index.html')

@app.route('/en', methods=['GET'])
def indexEN():
    return render_template('en/index.html')
    
@app.route('/result', methods=['GET'])
def result():
    return render_template('id/result.html')
    
@app.route('/en/result', methods=['GET'])
def resultEN():
    return render_template('en/result.html')

@app.route('/<path:lang>/check', methods=['POST'])
def main(lang):
    warnings.filterwarnings("ignore")

    # Baca file txt sebagai input
    # with open('utapis.txt', 'r', encoding='utf-8') as file:
    #     text = file.read()

    text = request.form['paragraph']
        
    # Baca file txt sebagai kata dasar
    with open('kata-dasar.txt', 'r') as file:
        word_list = [line.strip() for line in file.readlines()]

    # Preprocessing di preprocessing.py
    hasil_preprocessing = preprocessing(text)

    # rabinKarp algorithm untuk cari pattern pada input text di rabinKarp.py
    detected_with_terikat_prefix = rabinKarp(hasil_preprocessing, patterns)

    # Sort dari index terkecil
    sorted_data = sorted(detected_with_terikat_prefix, key=lambda x: x[-1])

    # Remove duplicates based on the word
    unique_data = {item[2]: item for item in sorted_data}.values()

    # Deteksi untuk yang dipisah spasi (bigram)
    bigrams = generate_bigrams(hasil_preprocessing)

    detected_bigram_with_terikat_prefix = []

    # Cari pattern di bigram
    for word, index in bigrams:
        result = rabinKarp(word, patterns, True, index)
        if result != []:
            detected_bigram_with_terikat_prefix.append(result)

    result = {}

    result.update(validateSatuKata(unique_data, word_list))

    if (detected_bigram_with_terikat_prefix != []):
        result.update(validateDuaKata(detected_bigram_with_terikat_prefix, word_list, text))

    # Jika tidak ada kata terikat
    if (result == {}):
        errorMessage = "Tidak ada kata terikat yang ditemukan"

        if (lang == 'en'):
            errorMessage = "No kata terikat is found"

        result = {'errormessage': errorMessage}
    
    return render_template(lang + '/result.html', data = {
        'paragraph': text,
        'result': result
    })

@app.route('/check/json', methods=['POST'])
def mainJson():
    warnings.filterwarnings("ignore")

    # Baca file txt sebagai input
    # with open('utapis.txt', 'r', encoding='utf-8') as file:
    #     text = file.read()

    text = request.form['paragraph']
        
    # Baca file txt sebagai kata dasar
    with open('kata-dasar.txt', 'r') as file:
        word_list = [line.strip() for line in file.readlines()]

    # Preprocessing di preprocessing.py
    hasil_preprocessing = preprocessing(text)

    # rabinKarp algorithm untuk cari pattern pada input text di rabinKarp.py
    detected_with_terikat_prefix = rabinKarp(hasil_preprocessing, patterns)

    # Sort dari index terkecil
    sorted_data = sorted(detected_with_terikat_prefix, key=lambda x: x[-1])

    # Remove duplicates based on the word
    unique_data = {item[2]: item for item in sorted_data}.values()

    # Deteksi untuk yang dipisah spasi (bigram)
    bigrams = generate_bigrams(hasil_preprocessing)

    detected_bigram_with_terikat_prefix = []

    # Cari pattern di bigram
    for word, index in bigrams:
        result = rabinKarp(word, patterns, True, index)
        if result != []:
            detected_bigram_with_terikat_prefix.append(result)

    result = {}

    result.update(validateSatuKata(unique_data, word_list))

    if (detected_bigram_with_terikat_prefix != []):
        result.update(validateDuaKata(detected_bigram_with_terikat_prefix, word_list, text))

    # Jika tidak ada kata terikat
    if (result == {}):
        result = {'errormessage': "Tidak ada kata terikat yang ditemukan"}
    
    return jsonify(data = {
        'paragraph': text,
        'result': result
    })

if __name__ == '__main__':
    app.run(debug=True)