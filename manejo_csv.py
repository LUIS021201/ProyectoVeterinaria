import csv

def lee_diccionario_de_csv(archivo:str,llave_columna)->dict:
    diccionario = {}
    try:
        with open(archivo,"r",encoding="utf-8") as fh: #fh: file handle
            csv_reader = csv.DictReader(fh)
            for renglon in csv_reader:
                llave = renglon[llave_columna]
                diccionario[llave] = renglon
    except IOError:
        print(f"No se pudo abrir el archivo {archivo}")
    return diccionario







def graba_diccionario_en_csv(diccionario: dict, llave_dict: str, archivo: str):
    with open(archivo, 'w') as fh:

        lista_campos = obtiene_llaves(diccionario, llave_dict)
        dw = csv.DictWriter(fh, lista_campos)
        dw.writeheader()
        rows = []
        for llave, valor_d in diccionario.items():
            d = {'usuario': llave}  # aquí va llave_dict
            for key, value in valor_d.items():
                d[key] = value
            rows.append(d)
        dw.writerows(rows)


def obtiene_llaves(diccionario: dict, llave_dicc: str) -> list:
    lista = [llave_dicc]
    llaves = list(diccionario.keys())

    k = llaves[0]
    diccionario_adentro = diccionario[k]
    lista_dentro = list(diccionario_adentro.keys())
    lista.extend(lista_dentro)
    # lista.append(llave_dicc)
    # lista_llaves = diccionario.keys()
    # for key, dicc in diccionario.items():
    #     for k,v in dicc.items():
    #         lista.append(k)
    print(lista)
    return lista


if __name__ == '__main__':
    dicc_usuarios = lee_diccionario_de_csv('csv/usuarios.csv')
    print(dicc_usuarios)