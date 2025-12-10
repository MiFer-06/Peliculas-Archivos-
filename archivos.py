import os
import struct

txt_file = "peliculas.txt"
bin_file = "peliculas.bin"

# Crear archivo de texto si no existe
def crear_txt():
    if not os.path.exists(txt_file):
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write("LISTA DE PELICULAS\n")

# Guardar película en archivo de texto
def guardar_pelicula(nombre, genero, año):
    try:
        if nombre == "":
            raise ValueError("El nombre no puede estar vacío")
        with open(txt_file, "a", encoding="utf-8") as f:
            f.write(f"{nombre},{genero},{año}\n")
    except Exception as e:
        print("Error al guardar:", e)

# Leer archivo de texto
def mostrar_peliculas():
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            lineas = f.readlines()
            if len(lineas) <= 1:
                print("No hay peliculas guardadas")
                return
            for linea in lineas[1:]:
                datos = linea.strip().split(",")
                print("Nombre:", datos[0], "| Género:", datos[1], "| Año:", datos[2])
    except FileNotFoundError:
        print("El archivo no existe")

# Buscar película
def buscar(nombre):
    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            for linea in f.readlines()[1:]:
                datos = linea.strip().split(",")
                if datos[0].lower() == nombre.lower():
                    print("Encontrada:", datos)
                    return
            print("No está en la lista")
    except:
        print("Error al leer archivo")

# Guardar datos binarios (popularidad y rating)
def guardar_bin(nombre, popularidad, rating):
    try:
        with open(bin_file, "ab") as f:
            data = struct.pack("20sii", nombre.encode(), popularidad, rating)
            f.write(data)
    except:
        print("No se pudo guardar en binario")

# Leer archivo binario
def mostrar_bin():
    try:
        with open(bin_file, "rb") as f:
            tam = struct.calcsize("20sii")
            bloque = f.read(tam)
            if not bloque:
                print("No hay datos binarios")
                return
            while bloque:
                nombre, pop, rat = struct.unpack("20sii", bloque)
                nombre = nombre.decode().replace("\x00", "")
                print("Película:", nombre, "| Popularidad:", pop, "| Rating:", rat)
                bloque = f.read(tam)
    except FileNotFoundError:
        print("El archivo binario no existe")
    finally:
        print("Lectura binaria terminada")

# ------------------------ MENÚ ------------------------

def menu():
    crear_txt()
    while True:
        print("\n=== COLECCIÓN DE PELÍCULAS ===")
        print("1. Agregar película")
        print("2. Mostrar todas")
        print("3. Buscar por nombre")
        print("4. Mostrar datos binarios")
        print("5. Salir")

        try:
            op = int(input("Opción: "))
        except:
            print("Debes escribir un número")
            continue

        if op == 1:
            nombre = input("Nombre: ")
            genero = input("Género: ")
            año = input("Año: ")
            guardar_pelicula(nombre, genero, año)

            try:
                pop = int(input("Popularidad (1-100): "))
                rat = int(input("Rating (1-100): "))
                if pop < 1 or pop > 100:
                    raise ValueError("Popularidad fuera de rango")
                guardar_bin(nombre, pop, rat)
            except Exception as e:
                print("Error:", e)

        elif op == 2:
            mostrar_peliculas()

        elif op == 3:
            nom = input("Nombre a buscar: ")
            buscar(nom)

        elif op == 4:
            mostrar_bin()

        elif op == 5:
            print("Adiós")
            break

        else:
            print("Opción no válida")

menu()
