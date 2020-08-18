from collections import Counter
from heapq import heappush, heappop, heapify
from graphviz import Digraph
import pprint
import math

#función para conseguir las probabilidades de cada caracter en un texto
def get_probabilities(content):
    total = len(content) + 1
    c = Counter(content)
    res = {}
    for char, count in c.items():
        #if char == "\n":
        #    continue
        res[char] = float(count)/total
    res['end'] = 1.0/total
    return res

#función para crear el árbol de codificación
def make_tree(symb2probs):

    heap = []

    for sym, pr in symb2probs.items():
        heappush(heap, (pr, 0, sym))

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        nw_e = (left[0]+right[0], max(left[1], right[1])+1, [left, right])
        heappush(heap, nw_e)

    return heap[0]

#función para crear diccionario
def make_dictionary(tree):
    res = {}
    search_stack = []
    search_stack.append(tree+("",))

    while len(search_stack) > 0:
        elm = search_stack.pop()
        if type(elm[2]) == list:
            prefix = elm[-1]

            search_stack.append(elm[2][0]+(prefix+"0",))

            search_stack.append(elm[2][1]+(prefix+"1",))

            continue
        else:
            code = elm[-1]
            res[elm[2]] = code
        pass
    return res

#función para códificar
def compress(dic, content):
    res = ""
    for ch in content:
        code = dic[ch]
        res = res + code

    res = "1" + res + dic['end']

    res_8 = res + ("0" * (len(res) % 8))

    #res = res + ("0" * (len(res) % 8))
    #print("numero de bits: ", len(res)%8)

    return int(res_8, 2), res

#función para decodificar
def decompress(dic,content):
    message_decoded = ""
    sym_decoded = ""
    for b in content[1:len(content)-1]:
        sym_decoded += b
        if sym_decoded in dic.values():
            for item in dic.items():
                if item[1] == sym_decoded:
                    message_decoded += item[0]
                    sym_decoded = ""
    return message_decoded

#función para obtener los códigos de huffman apartir de un texto
def huffman(textinput):
    return make_dictionary(make_tree(get_probabilities(textinput)))

#función para quitar acentos, mayusculas, mayusculas acentuadas y caracteres especiales
def modificar_texto(text_input):

    diccionario_vocales_minus_acentos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u'}

    diccionario_vocales_mayus_acentos = {'Á':'a', 'É':'e', 'Í':'i', 'Ó':'o', 'Ú':'u'}

    diccionario_mayus_minus = {'A':'a', 'B':'b', 'C':'c', 'D':'d', 'E':'e',
        'F':'f', 'G':'g','H':'h', 'I':'i', 'J':'j',
        'K':'k', 'L':'l', 'M':'m', 'N':'n', 'Ñ':'ñ',
        'O':'o', 'P':'p', 'Q':'q', 'R':'r',
        'S':'s', 'T':'t', 'U':'u', 'V':'v', 'W':'w',
        'X':'x', 'Y':'y', 'Z':'z'}

    lista_de_letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z']

    text_output = ""

    for ch in text_input:
        if ch in lista_de_letras:
            text_output += ch
        elif ch in diccionario_vocales_mayus_acentos.keys():
            text_output += diccionario_vocales_mayus_acentos[ch]
        elif ch in diccionario_vocales_minus_acentos.keys():
            text_output += diccionario_vocales_minus_acentos[ch]
        elif ch in diccionario_mayus_minus.keys():
            text_output += diccionario_mayus_minus[ch]

    return text_output


if __name__ == "__main__":

    f = open("texto_libro.txt","r")
    text = f.read()
    f.close()

    text = modificar_texto(text)

    huffman_codes = huffman(text)
    print("\nhuffman codes:\n\n")
    pprint.pprint(huffman_codes)
    
    #pruebas de mensaje codificado
    num_bits, mensaje_codificado = compress(huffman_codes, text)
    #print("\n numero de bits: ", num_bits,"\n")
    #print("\n mensaje codificado:\n",mensaje_codificado)
    
    #prueba de mensaje decodificado
    mensaje_decodificado = decompress(huffman_codes, mensaje_codificado)
    #print("\n mensaje decodificado \n\n",mensaje_decodificado)


    caracteres_probabilidades = get_probabilities(text)
    pprint.pprint(caracteres_probabilidades)
    
    #obtenemos una el rango absoluto
    R = math.log2(27)
    
    #definimos el rango del lenguaje
    r = [1.2, 1.5]
    print("\n r: ",r)
    #calculamos la redundancia del lenguaje
    D = [R - x for x in sorted(r,reverse=True) ]
    print("\n D: ",D)
    
    #obtenemos la cantidad de bits por cada symbolo
    for x,y in huffman_codes.items():
        print(x,"\t\t",y,"\t\tnumero de bits del simbolo: ",len(y))
    
    #obtenemos la entropia de nuestro mensaje codificado
    h = 0.0

    for p in caracteres_probabilidades.values():
        #print(p * math.log2(1/p))
        h += p * math.log2((1/p))

    print("\n\n\n entropia H :",h, "\n\n\n")
