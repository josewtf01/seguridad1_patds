import encription as Encp
import huffman_code as Huff
import pprint
import bitstring
import random
import statistics

def cod_enc_texto(title_archive):
    #función para crear la codificación del texto plano,
    #así como sus encriptaciones en AES Y 3DES con sus codificaciones
    
    #lectura del texto del archivo
    texto_plano = Encp.read_text(title_archive)
    
    #numero de caracteres del texto de entrada
    numero_car_ent = len(texto_plano)
    
    #eliminar acentos y caracteres especiales
    texto_plano = Huff.modificar_texto(texto_plano)
    
    #crear el diccionario de los codigos de huffman
    huffman_dic_plain = Huff.huffman(texto_plano)
    
    #creación del texto codificado en binario
    texto_plano_cod = Huff.compress(huffman_dic_plain,texto_plano)
    
    #conversión de la cadena binaria en caracteres ascii
    texto_ascii , n_bits_f = Encp.bitchain_to_ascii(texto_plano_cod)
    
    #print("Diccionario de los caracteres codificados del texto de entrada: " + title_archive)
    #pprint.pprint(huffman_dic_plain)
    
    print("Estadisticas del texto del archivo: " + title_archive)
    Huff.language_statistics(huffman_dic_plain, texto_plano)
    
    # crear el archivo con texto ascii a partir de la codificación de huffman del texto
    # de entrada
    Encp.create_archive_coded(texto_ascii, "cod_" + title_archive)
    
    # Creación de los cifrados para el texto de entrada

    #cifrado AES


    name_archive_aes = "AES_encriptado_" + title_archive
    texto_encriptado_aes, key_aes = Encp.AES_encrypt(texto_ascii, name_archive_aes)
    ct_aes = Encp.read_json_encripted(texto_encriptado_aes)
    print("cantidad de caracteres del texto AES encriptado", len(ct_aes))
    
    #
    texto_huff_cifrado_aes = ct_aes
    texto_huff_cifrado_aes = Huff.modificar_texto(texto_huff_cifrado_aes)
    huff_dic_aes = Huff.huffman(texto_huff_cifrado_aes)
    texto_cod_huff_aes = Huff.compress(huff_dic_aes,texto_huff_cifrado_aes)
    #impresión
    #print("Diccionario del texto codificado y cifrado AES")
    #pprint.pprint(huff_dic_aes)
    print("\n")
    Huff.language_statistics(huff_dic_aes,texto_cod_huff_aes)
    
    # 3DES
    
    name_archive_des = "DES3_encriptado_" + title_archive
    texto_encriptado_des, key_des = Encp.DES3_encrypt(texto_ascii, name_archive_des)
    ct_des = Encp.read_json_encripted(texto_encriptado_des)
    print("cantidad de caracteres del texto 3DES encriptado", len(ct_des))
    
    #
    texto_huff_cifrado_des = ct_des
    texto_huff_cifrado_des = Huff.modificar_texto(texto_huff_cifrado_des)
    huff_dic_des = Huff.huffman(texto_huff_cifrado_des)
    texto_cod_huff_des = Huff.compress(huff_dic_des,texto_huff_cifrado_des)
    #impresión
    #print("Diccionario del texto codificado y cifrado 3DES")
    #pprint.pprint(huff_dic_des)
    print("\n")
    Huff.language_statistics(huff_dic_des,texto_cod_huff_des)


def message_16():
    mes_16 = b'holamundotareat2'
    mensaje = bitstring.BitArray(bytes = mes_16)

    f = open("bytes_16.txt","wb")
    mensaje.tofile(f)
    f.close()
    
    f = open("bytes_16.txt","r")
    aux = f.read()
    f.close()
    
    aes_f_json_16 , aes_key_16 = Encp.AES_encrypt(aux,"aes_bytes_16.txt")
    des3_f_json_16, des3_key_16 = Encp.DES3_encrypt(aux,"des3_bytes_16.txt")
    
    aes_message = bytes(Encp.read_json_encripted(aes_f_json_16),"utf-8")
    des3_message = bytes(Encp.read_json_encripted(des3_f_json_16),"utf-8")

    aes_message_bc = bitstring.BitArray(bytes=aes_message)
    des3_message_bc = bitstring.BitArray(bytes=des3_message)
    #print(aes_message,"\n")
    #print(des3_message,"\n")    
    #print(mensaje.__len__())

    for i in range(31):
        mensaje_modificado = bitstring.BitArray(bytes = mes_16)
        mensaje_modificado.invert(random.randint(0,127))
        filename = "bytes_16_" + str(i+1) + ".txt"
        f = open(filename,"wb")
        mensaje_modificado.tofile(f)
        f.close()
    
    dic_keys_aes = dict()
    dics_keys_des3 = dict()
    aes_modificado = list()
    des3_modificado = list()

    for i in range(31):
        filename = "bytes_16_" +str(i+1) + ".txt"
        f = open(filename,"rb")
        texto = f.read()
        #print("texto_"+str(i+1)+" : ", texto)
        #print(str(texto,"unicode-escape"),"\n")
        f.close()
    
        json_file_aes , aes_key = Encp.AES_encrypt(str(texto,"unicode-escape"),"aes_"+filename)
        #dic_keys_aes["aes_"+filename] = aes_keys
        aes_modificado.append(bytes(Encp.read_json_encripted(json_file_aes),"utf-8"))

        json_file_des3 , des3_key = Encp.DES3_encrypt(str(texto,"unicode-escape"),"des3_"+filename)
        #dics_keys_des3["des3_"+filename] = des3_key
        des3_modificado.append(bytes(Encp.read_json_encripted(json_file_des3),"utf-8"))
    
    h_aes = list()
    h_des3 = list()

    for i in range(31):
        count_bit_aes = 0
        count_bit_des3 = 0
        aes_modificado_bc = bitstring.BitArray(bytes=aes_modificado[i])
        des3_modificado_bc = bitstring.BitArray(bytes=des3_modificado[i])
        for j in range(128):
            if aes_message_bc[j] == aes_modificado_bc[j]:
                count_bit_aes += 1
            if des3_message_bc[j] == des3_modificado_bc[j]:
                count_bit_des3 += 1
        h_aes.append(count_bit_aes)
        h_des3.append(count_bit_des3)

    for i in range(31):
        print(str(i+1) + " archivo aes : cantidad de bits diferentes: " + str(h_aes[i]))
        print(str(i+1) + " archivo 3des : cantidad de bits diferentes: " + str(h_des3[i]),"\n")
    
    print("AES hamming median: ",statistics.median(h_aes))
    print("AES starndar deviation: ",statistics.stdev(h_aes),"\n")
    
    print("3DES hamming median: ",statistics.median(h_des3))
    print("3DES starndar deviation: ",statistics.stdev(h_des3),"\n")


cod_enc_texto("texto_1000.txt")

cod_enc_texto("texto_10000.txt")

cod_enc_texto("texto_50000.txt")

message_16()

'''
f1 = open("bytes_16.txt","rb")
print(f1.read())
f1.close()

f2 = open("bytes_16.txt","r")
print(f2.read())
f2.close()
'''
