import huffman_code as Huff
import Crypto
import os
import pprint


def bitchain_to_ascii(str_bitchain):
    #función para convertiar cadena de bits a cadena ascii

    #convertimos la cadena de bits en multiplo de 8
    numero_de_bits_faltantes = 4 - (len(str_bitchain)%4)
    #print(numero_de_bits_faltantes)

    #si la cantidad de ceros faltante es 8
    #significa que es multiplo de 8
    if numero_de_bits_faltantes == 4:
        numero_de_bits_faltantes = 0

    str_bitchain = str_bitchain + ("0" * numero_de_bits_faltantes)

    #print(len(str), len(str)%8,"\n\n\n")

    #texto de salida en formato ascii
    text_ascii = ""

    #función que convierte cada cadena de 8 bits
    # en un simbolo ascii ej. 97 = 0 1 1 0 0 0 0 1 = "a"
    # 128*0 + 64*1 + 32*1 + 16*0 + 8*0 + 4*0 + 2*0 + 1*1
    # esto nos da 97, lo cual es una letra "a"

    for i in range(int(len(str_bitchain)/4)):
        aux = 8
        sym_value = 0
        for j in range(4):
            sym_value += aux * int( str_bitchain[ 4 * i + j] )
            aux = int(aux/2)
        #print(i, sym_value,"\n")
        sym = chr(sym_value)
        text_ascii += sym

    return text_ascii , numero_de_bits_faltantes


def ascii_to_bitchain(str_ascii,n_bits_f):
    #función para convertir una cadena en un array de bits

    text_bitchain = ""
    for i in str_ascii:
        #print("ord(i):", ord(i))
        num_dec = ord(i)
        if num_dec == 0:
            text_bitchain += "0000"
        elif num_dec < 8:
            ze_ros = 4 - (len("{0:b}".format(num_dec))%4)
            text_bitchain += ("0" * ze_ros) + "{0:b}".format(num_dec)
        else:
            text_bitchain += "{0:b}".format(num_dec)

    if n_bits_f == 4:
        return text_bitchain
    elif n_bits_f == 0:
        return text_bitchain[1:]
    else:
        return text_bitchain[:-1*n_bits_f]


def AES_encrypt(encoded_text,title_of_archive):
    #función para encriptar texto ascii
    # con AES en modo CBC
    import json
    from base64 import b64encode
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from Crypto.Random import get_random_bytes

    data = encoded_text.encode("utf-8") #utf-8
    key = get_random_bytes(16)
    cipher = AES.new(key,AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8") # utf-8
    ct = b64encode(ct_bytes).decode("utf-8")    #utf-8
    result = json.dumps({'iv':iv, 'ciphertext':ct})
    if os.path.exists(title_of_archive):
        os.remove(title_of_archive)

    with open(title_of_archive,"w") as f:
        json.dump(result, f)

    return result, key


def AES_de_encrypt(key,title_of_archive):
    import json
    from base64 import b64decode
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad

    f = open(title_of_archive,"rb")
    data = json.load(f)
    f.close()

    # We assume that the key was securely shared beforehand
    try:
        b64 = json.loads(data)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        #print("The message was: ", pt)

        #print("l: ",len(pt))
        #print("ascii: ",pt.decode("utf-8"))
    except e:
        print("Incorrect decryption")
    else:
        return pt.decode("utf-8") #utf-8


def DES3_encrypt(encoded_text,title_of_archive):
    import json
    from base64 import b64encode
    from Crypto.Cipher import DES3
    from Crypto.Util.Padding import pad
    from Crypto.Random import get_random_bytes

    data = encoded_text.encode("utf-8")
    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(24))
            break
        except ValueError:
            pass

    cipher = DES3.new(key, DES3.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, DES3.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    result = json.dumps({'iv':iv, 'ciphertext':ct})

    if os.path.exists(title_of_archive):
        os.remove(title_of_archive)

    with open(title_of_archive,"w") as f:
        json.dump(result,f)

    return result, key


def DES3_de_encrypt(key,title_of_archive):
    import json
    from base64 import b64decode
    from Crypto.Cipher import DES3
    from Crypto.Util.Padding import unpad

    f = open(title_of_archive,"rb")
    data = json.load(f)
    f.close()

    # We assume that the key was securely shared beforehand
    try:
        b64 = json.loads(data)
        iv = b64decode(b64['iv'])
        ct = b64decode(b64['ciphertext'])
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), DES3.block_size)
        #print("The message was: ", pt)
    except e:
        print("Incorrect decryption")
    else:
        return pt.decode("utf-8")


def read_text(name_text):
    #función para leer un texto de entrada de un archivo de texto
    text = ""
    try:
        f = open(name_text,"r")
    except:
        print("no se pudo abrir el archivo")
    else:
        text = f.read()
        f.close()
    return text


def create_archive_coded(text,title_of_archive):
    if os.path.exists(title_of_archive):
        os.remove(title_of_archive)
    try:
        f = open(title_of_archive,"wb")
    except:
        print("no se pudo escribir el archivo del texto codificado")
    else:
        f.write(bytearray(text,'utf-8'))
        f.close()


def read_json_encripted(encripted_text):
    #función para leer el texto encriptado de un archivo de texto en formato json
    
    from base64 import b64decode
    import json

    data = json.loads(encripted_text)
    #print(data)
    #ct = b64decode(data['ciphertext'])
    ct = data['ciphertext']
    return ct


if __name__ == "__main__":
    #lectura del texto con base a un archivo de texto
    text = read_text("texto_libro.txt")
    text = Huff.modificar_texto(text)

    #cantidad de caracateres del texto de entrada
    #print(text)
    print("cantidad de caracteres en texto de entrada: ", len(text),"\n")

    #creación del diccionario de códigos de huffman
    huffman_codes = Huff.huffman(text)
    #pprint.pprint(huffman_codes)

    #texto codificado con códigos de huffman
    texto_cod_huff = Huff.compress(huffman_codes,text)
    #print("texto_cod_huff:",texto_cod_huff,"\n\n")

    #conversión de texto codificado a caracteres ascii
    texto_ascii, n_bits_f = bitchain_to_ascii(texto_cod_huff)

    #creación del archivo del texto códificado con el codificador de huffman
    create_archive_coded(texto_ascii,"texto_codificado.txt")

    #creación del texto cifrado y su escritura en un archivo

    #encriptación por medio de AES
    name_archive = "AES_encriptado.txt"
    texto_encriptado_AES , key_AES = AES_encrypt(texto_ascii, name_archive)
    ct = read_json_encripted(texto_encriptado_AES)
    print("cantidad de caracteres en texto AES encriptado: ", len(ct),"\n")

    #desencriptación por medio de AES
    texto_desencriptado_AES = AES_de_encrypt(key_AES,name_archive)

    #encriptación por medio de 3DES
    name_archive = "DES3_encriptado.txt"
    texto_encriptado_DES3, key_DES3 = DES3_encrypt(texto_ascii, name_archive)
    ct = read_json_encripted(texto_encriptado_DES3)
    print("cantidad de caracteres en texto 3DES encriptado: ",len(ct),"\n")

    #descencriptación por medio de DES3
    texto_desencriptado_DES3 = DES3_de_encrypt(key_DES3, name_archive)

    #texto en cadena de bits
    #texto_binario = ascii_to_bitchain(texto_desencriptado_AES, n_bits_f)
    texto_binario = ascii_to_bitchain(texto_desencriptado_DES3, n_bits_f)

    #texto decodificado con códigos de huffman
    texto_decodificado = Huff.decompress(huffman_codes, texto_binario)
    #print(texto_decodificado)
