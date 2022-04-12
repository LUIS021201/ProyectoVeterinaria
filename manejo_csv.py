# import csv

# def lee_diccionario_de_csv(archivo:str,llave_columna)->dict:
#     diccionario = {}
#     try:
#         with open(archivo,"r",encoding="latin-1") as fh: #fh: file handle
#             csv_reader = csv.DictReader(fh)
#             for renglon in csv_reader:
#                 llave = renglon[llave_columna]
#                 diccionario[llave] = renglon
#     except IOError:
#         print(f"No se pudo abrir el archivo {archivo}")
#     return diccionario



# def guardar_dict_en_csv(dict_data:dict, columns:list, file:str):
#     try:
#         with open(file, 'w') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=columns)
#             writer.writeheader()
#             for data in dict_data:
#                 writer.writerow(data)
#     except IOError:
#         print("I/O error")




# def graba_diccionario_en_csv(diccionario: dict, llave_dict: str, archivo: str):
#     with open(archivo, 'a',encoding='latin1') as fh:

#         lista_campos = obtiene_llaves(diccionario, llave_dict)
#         dw = csv.DictWriter(fh, lista_campos)
#         dw.writeheader()
#         rows = []
#         for llave, valor_d in diccionario.items():
#             d = {llave_dict: llave}  # aquí va llave_dict
#             for key, value in valor_d.items():
#                 d[key] = value
#             rows.append(d)

#         dw.writerows(rows)


# def obtiene_llaves(diccionario: dict, llave_dicc: str) -> list:
#     lista = [llave_dicc]
#     llaves = list(diccionario.keys())

#     k = llaves[0]
#     diccionario_adentro = diccionario[k]
#     lista_dentro = list(diccionario_adentro.keys())
#     lista.extend(lista_dentro)
#     # lista.append(llave_dicc)
#     # lista_llaves = diccionario.keys()
#     # for key, dicc in diccionario.items():
#     #     for k,v in dicc.items():
#     #         lista.append(k)
#     print(lista)
#     return lista


# if __name__ == '__main__':
#     dicc = {'LuisHL': {'password': '123', 'nombre': 'Luis Hernández', 'type': 'admin'},
#             'andrea': {'password': '123', 'nombre': 'Andrea Duarte', 'type': 'cliente'},
#             'david': {'password': '123', 'nombre': 'David Nuñez', 'type': 'usuario'}}
#     dicc_usuarios = lee_diccionario_de_csv('csv/usuarios.csv','email')
#     print(dicc_usuarios)
#     dicc_usuarios['david'] ={'email':'david','password':'123','nombre':'David Nuñez','type':'usuario'}
#     graba_diccionario_en_csv(dicc,'email','csv/usuariosss.csv')
