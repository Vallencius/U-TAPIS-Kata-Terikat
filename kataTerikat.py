from bigram import split_words

patterns = [
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
    'zeta',
    'Ab',
    'Adi',
    'Aero',
    'Alo',
    'Ambi',
    'Amfi',
    'Ana',
    'Antar',
    'Ante',
    'Anti',
    'Apo',
    'Ato',
    'Auto',
    'Awa',
    'Bi',
    'Bio',
    'Catur',
    'Daktilo',
    'Dasa',
    'De',
    'Deka',
    'Dia',
    'Dis',
    'Dwi',
    'Eka',
    'Eks',
    'Ekso',
    'Ekstra',
    'Endo',
    'Epi',
    'Femto',
    'Geo',
    'Hagio',
    'Heksa',
    'Hekto',
    'Hemi',
    'Hepta',
    'Hetero',
    'Hidro',
    'Hiper',
    'Hipo',
    'Homo',
    'In',
    'Indo',
    'Infra',
    'Inter',
    'Intra',
    'Intro',
    'Iso',
    'Kata',
    'Ko',
    'Kontra',
    'Kuasi',
    'Levo',
    'Maha',
    'Maha',
    'Makro',
    'Mala',
    'Manca',
    'Mega',
    'Meso',
    'Mikro',
    'Mili',
    'Mini',
    'Mono',
    'Multi',
    'Nara',
    'Nawa',
    'Neo',
    'Nir',
    'Nis',
    'Non',
    'Oto',
    'Paleo',
    'Pan',
    'Panca',
    'Para',
    'Pari',
    'Pasca',
    'Penta',
    'Peri',
    'Piezo',
    'Piko',
    'Poli',
    'Pra',
    'Pramu',
    'Pre',
    'Pro',
    'Proto',
    'Pseudo',
    'Purba',
    'Purna',
    'Purwa',
    'Re',
    'Sapta',
    'Se',
    'Semi',
    'Serba',
    'Si',
    'Sin',
    'Sosio',
    'Su',
    'Sub',
    'Super',
    'Supra',
    'Swa',
    'Tak',
    'Tan',
    'Tele',
    'Tera',
    'Trans',
    'Tri',
    'Tuna',
    'Ultra',
    'Uni',
    'Upa',
    'Zeta'
]

def validateSatuKata(unique_data, word_list):
    exception = ['maha', 'se']
    result = {}
    # Search kata terikat 1 word
    for pattern, word_without_pattern, word, index in unique_data:
        if ('-' not in word and word_without_pattern != ''):
            # Jika bukan maha dan sesuai kata terikat maka pasti benar
            if (pattern.lower() not in exception and (word_without_pattern.lower() in word_list) and word.lower() not in word_list):
                result[word] = {
                        "is_correct": True,
                        "suggestion": None
                    }
                # print(word + " benar di index " + str(index))
            else:
                if ((pattern == 'maha' or pattern == 'Maha') and word_without_pattern.lower() in word_list):
                    # Jika maha diikuti esa harus di spasi
                    if (word_without_pattern == 'esa' or word_without_pattern == 'Esa'):
                        result[word] = {
                                "is_correct": False,
                                "suggestion": pattern.title() + " " + word_without_pattern.title()
                        }
                        # print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + pattern.title() + " " + word_without_pattern.title())
                    
                    else:
                        # Jika maha diikuti kata dasar, benar
                        if (word_without_pattern.lower() in word_list):
                            result[word] = {
                                    "is_correct": True,
                                    "suggestion": None
                                }
                            # print(word + " benar di index " + str(index))
                        # Jika maha diikuti kata turunan harus dipisah
                        else:
                            result[word] = {
                                    "is_correct": False,
                                    "suggestion": pattern.title() + " " + word_without_pattern.title()
                                }
                            # print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + pattern.title() + " " + word_without_pattern.title())

        # Jika ada dash (tanda hubung)
        if ('-' in word and word[0] != '-' and word[-1] != '-'):
            word_without_dash_and_pattern = word_without_pattern.translate(str.maketrans("", "", r"-"))

            if (pattern != word_without_dash_and_pattern):
                # Jika ada tanda dash tetapi seharusnya tidak
                if (word_without_dash_and_pattern.lower() in word_list):
                    result[word] = {
                            "is_correct": False,
                            "suggestion": pattern + word_without_dash_and_pattern.lower()
                        }
                    # print(word + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + word_without_dash)
                else:
                    
                    # Jika ada tanda dash tetapi kata kedua diawali dengan huruf kapital
                    if (word_without_dash_and_pattern[0].isupper()):
                        result[word] = {
                                "is_correct": True,
                                "suggestion": None
                            }
                        # print(word + " benar di index " + str(index))
                        
    return result

def validateDuaKata(detected_bigram_with_terikat_prefix, word_list):
    exception = ['kata', 'para', 'dia', 'tak', 'si']
    resultKataTerikat = {}
    for pattern, bigram_text, index in detected_bigram_with_terikat_prefix:
        result = split_words(bigram_text)
        word = bigram_text.replace(" ", "")
        
        # Jika terpisah dengan spasi namun seharusnya digabung
        if (result[1] in word_list) and result[0].lower() not in exception and result[0].lower() != 'maha' and word.lower() not in word_list and result[0] in patterns:
            resultKataTerikat[bigram_text] = {
                    "is_correct": False,
                    "suggestion": word
                }
            # print(bigram_text + " salah di index " + str(index) + ". rekomendasi yang diberikan: " + word)

        if (result[1] in word_list) and result[0].lower() == 'para' and word.lower() in word_list and result[0] in patterns:
            resultKataTerikat[bigram_text] = {
                    "is_correct": False,
                    "suggestion": result[0] + result[1]
                }

        # Jika terpisah dengan spasi namun seharusnya diberi tanda hubung (-)
        if (result[1][0].isupper()) and result[0].lower() not in exception and result[0].lower() != 'maha' and result[0] in patterns and result[1].lower() in word_list:
            resultKataTerikat[bigram_text] = {
                    "is_correct": False,
                    "suggestion": result[0] + '-' + result[1]
                }
            # print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + result[0] + '-' + result[1])
            
        #Jika ada Maha dan dipisah dengan kata selanjutnya, digabung kecuali Esa
        if result[0] == 'Maha' and result[1].lower() != 'esa':
            if result[1].lower() in word_list:
                resultKataTerikat[bigram_text] = {
                        "is_correct": False,
                        "suggestion": result[0] + result[1].lower()
                    }
                # print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: " + result[0] + result[1].lower())

            # Jika Maha dipisah dan diikuti kata turunan
            else:
                resultKataTerikat[bigram_text] = {
                        "is_correct": True,
                        "suggestion": None
                    }
                # print(bigram_text + " benar di index " + str(index))
        else:
            # Jika Maha Esa maka benar
            if result[0] == 'Maha' and result[1] == 'Esa':
                resultKataTerikat[bigram_text] = {
                        "is_correct": True,
                        "suggestion": None
                    }
                # print(bigram_text + " benar di index " + str(index))
            else:
                # Jika Maha esa, maka Maha Esa
                if result[0] == 'Maha' and result[1] == 'esa':
                    resultKataTerikat[bigram_text] = {
                            "is_correct": False,
                            "suggestion": "Maha Esa"
                        }
                    # print(bigram_text + " salah di index " + str(index) + ". Rekomendasi yang diberikan: Maha Esa")
    
    return resultKataTerikat