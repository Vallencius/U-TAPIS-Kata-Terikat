from bigram import split_words

patterns = [
    'a',
    'ab',
    'adi',
    'aero',
    'alo',
    'ambi',
    'amfi',
    'ana',
    'antar',
    'ante',
    'anti',
    'apo',
    'ato',
    'auto',
    'awa',
    'bi',
    'bio',
    'catur',
    'daktilo',
    'dasa',
    'de',
    'deka',
    'dia',
    'dis',
    'dwi',
    'eka',
    'eks',
    'ekso',
    'ekstra',
    'endo',
    'epi',
    'femto',
    'geo',
    'hagio',
    'heksa',
    'hekto',
    'hemi',
    'hepta',
    'hetero',
    'hidro',
    'hiper',
    'hipo',
    'homo',
    'in',
    'indo',
    'infra',
    'inter',
    'intra',
    'intro',
    'iso',
    'kata',
    'ko',
    'kontra',
    'kuasi',
    'levo',
    'maha',
    'Maha',
    'makro',
    'mala',
    'manca',
    'mega',
    'meso',
    'mikro',
    'mili',
    'mini',
    'mono',
    'multi',
    'nara',
    'nawa',
    'neo',
    'nir',
    'nis',
    'non',
    'oto',
    'paleo',
    'pan',
    'panca',
    'para',
    'pari',
    'pasca',
    'penta',
    'peri',
    'piezo',
    'piko',
    'poli',
    'pra',
    'pramu',
    'pre',
    'pro',
    'proto',
    'pseudo',
    'purba',
    'purna',
    'purwa',
    're',
    'sapta',
    'se',
    'semi',
    'serba',
    'si',
    'sin',
    'sosio',
    'su',
    'sub',
    'super',
    'supra',
    'swa',
    'tak',
    'tan',
    'tele',
    'tera',
    'trans',
    'tri',
    'tuna',
    'ultra',
    'uni',
    'upa',
    'zeta'
]

def validateSatuKata(unique_data, word_list):
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
                        
    return no_detected_kata_terikat

def validateDuaKata(detected_bigram_with_terikat_prefix, word_list):
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
    
    return no_detected_kata_terikat