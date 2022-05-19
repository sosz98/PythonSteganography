# W plikach *.bmp zaszyte zostały wiadomości tekstowe (w każdym pliku inna).
# Uzupełnij funkcję `extract_message` tak, aby przujmując nazwę pliku zwracała
# wiadomość w nim zakodowaną.
#
# * Wiadomość znajduje się w bajtach odpowiadających pixelom obazka.
# * Wiadomość składa się ze znaków z tabeli ASCII.
# * Do ukrycia wiadomości wykorzystano LSB powyższych bajtów.
# * Każdy pixel składa się z 4 bajtów.
# * Każdy znak ukrytej wiadomości reprezentowany jest jako 1 bajt (8 bitów).
# * Każdy znak ukrytej wiadomości zajmuje 2 pixele, 2 * 4 bajty = 8 bajtów (1 bajt na 1 bit znaku).
# * LSB pierwszego bajtu pierwszego z pary pixeli staje sie MSB ukrytego znaku.
# * Wiadomość kończy się ciągiem 'EOF'.
# * Pomimo iż znaki z tabeli ASCII zajmują 7 bitów, do zakodowania znaków wykorzystano 8 bitów.
#   Można więc założyć, że MSB znaku jest zawsze równy 0.
#
# Przykład:
#
# Dla dwóch kolejnych pixeli odczytanych z pliku:
# pixel 1 - 254 255 254 255
# pixel 2 - 254 255 254 254
#
# Otrzymujemy ciąg 8 bajtów:
# 254 255 254 255 254 255 254 254
#
# W reprezentacji bitowej wygląda to następująco:
# 0b11111110 0b11111111 0b11111110 0b11111111 0b11111110 0b11111111 0b11111110 0b11111110
#
# Po wyodrębnieniu LSB ze wszystkich bajtów i połączeniu w 1 bajt otrzymujemy:
# 0b01010100
# Co odpowiada znakowi `T` w tabeli ASCII
#
# Przydatne linki:
# https://en.wikipedia.org/wiki/Steganography
# https://en.wikipedia.org/wiki/BMP_file_format
# https://www.geeksforgeeks.org/check-whether-k-th-bit-set-not
#
# Przydatne metody / operatory:
# https://docs.python.org/3.8/library/stdtypes.html#int.from_bytes
# https://docs.python.org/3.8/library/stdtypes.html#int.to_bytes
# https://docs.python.org/3.8/library/stdtypes.html#bytes
# https://wiki.python.org/moin/BitwiseOperators
#
# Podpowiedź: W pliku `white-small.bmp` zaszyta jest wiadomość `TESTEOF`.


def extract_message(filename: str) -> str:
    with open(filename, 'rb') as img:
        data = bytearray(img.read())

    helplist = []

    data_length = len(data)
    i = 0

    for element in range(0, 2):
        data.remove(data[0])

    while data_length > 1:
        new_list = []
        for j in range(i, i + 8):
            new_list.append(data[j])
        helplist.append(new_list)
        i += 8
        if i == len(data):
            break
        data_length -= 8

    list_of_int_values = []
    for element in helplist:
        k = 7
        result = 0
        for x in element:
            var = x % 2
            result += (var*(2**k))
            k -= 1
        list_of_int_values.append(result)

    ascii_list = []

    for another_element in list_of_int_values:
        if another_element <= 127:
            ascii_list.append(another_element)

    string_list = []
    for var in ascii_list:
        string_list.append(str(chr(var)))

    x = 0
    var_x = 0

    while var_x < len(string_list) - 2:
        if string_list[var_x] == 'E' and string_list[var_x+1] == 'O' and string_list[var_x+2] == 'F':
            x = var_x
            break
        else:
            var_x += 1

    result_list = []

    while x > 0:
        if ord(string_list[x-1]) >= 32:
            result_list.insert(0, string_list[x-1])
        else:
            break
        x -= 1

    resultat = ""
    for x in result_list:
        resultat += x
    resultat += "EOF"

    return resultat