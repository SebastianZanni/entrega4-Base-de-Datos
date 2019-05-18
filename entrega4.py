import psycopg2

conn= psycopg2.connect(host='201.238.213.114',port=54321,database='grupo5',user='grupo5',password='LTguaC')
cur = conn.cursor()

while True:

    print("[1] Iniciar Sesion\n"
          "[2] Crear Cuenta\n"
          "[3] Recuperar Contraseña\n"
          "[4] Salir\n")

    menu= input("Que deseas hacer: ")
    existe = 'Existe'
    noExiste = 'Eliminado'

    try:
        val = int(menu)

        if (val == 1):
            email = input("\nIngrese email del usuario al que quiere ingresar: ")
            contraseña = input("Ingrese la contraseña del usuario al que quiere ingresar: ")

            cur.execute('SELECT id FROM Usuarios WHERE email=%s AND contraseña=%s AND Existe=%s', (email, contraseña,existe))

            cont1 = cur.fetchone()

            if cont1 == None:
                print(
                    "\nLa contraseña o el mail ingresados no coinciden con algun usuario ( puede que haya sido eliminado ), seras regresado al menu principal\n")
                continue

            usuario= cont1[0]

            print("\nIniciaste sesion exitosamente con el usuario:", usuario)

            while True:

                cur.execute('SELECT nombreperfil FROM Perfiles WHERE idusuario=%s AND Existe=%s', (usuario,existe))

                cont2 = cur.fetchall()

                if cont2==[]:
                    print("\n No tienes ningun perfil, crea uno a continuacion: ")
                    while True:
                        nombrePerfil = input("Ingrese el nombre de su nuevo perfil: ")

                        while True:
                            edad = input("Ingrese su edad")
                            try:
                                edad = int(edad)
                                break

                            except ValueError:
                                print("Tienes que ingresar numeros")
                                continue

                        cur.execute(
                            'SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s AND Existe=%s LIMIT 1)',
                            (nombrePerfil, noExiste))
                        validacion = cur.fetchone()

                        if validacion[0] == True:
                            cur.execute('UPDATE Perfiles SET Existe=%s WHERE nombreperfil=%s', (existe, nombrePerfil))
                            conn.commit()
                            print('\nYa existia un perfil con este nombre pero habia sido eliminado, se ha vuelto a crear\n')
                            break

                        cur.execute(
                            'SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s AND Existe=%s LIMIT 1)',
                            (nombrePerfil, existe))
                        validacion2 = cur.fetchone()

                        if validacion2[0] == True:
                            print("\nYa existe un perfil con este nombre, intentalo nuevamente\n")
                            continue

                        cur.execute('SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s  LIMIT 1)',
                                    (nombrePerfil,))
                        validacion3 = cur.fetchone()

                        if validacion3[0] == False:
                            cur.execute(
                                'INSERT INTO Perfiles(nombreperfil,idusuario,edad,existe)'
                                'VALUES (%s,%s,%s,%s)', (nombrePerfil, usuario, edad, existe))
                            conn.commit()
                            print("\nEl perfil ha sido creado con exito!!!!\n")
                            break

                cur.execute('SELECT nombreperfil FROM Perfiles WHERE idusuario=%s AND Existe=%s', (usuario, existe))

                cont3 = cur.fetchall()

                print("Los perfiles disponibles son: ")

                for perfil in cont3:
                    print(perfil[0])
                perfilElegido= input("\nA cual deseas ingresar: ")

                cur.execute('SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s AND idusuario=%s LIMIT 1)', (perfilElegido,usuario))
                perfilExiste= cur.fetchone()

                if (perfilExiste[0]==True):
                    print("Ingresaste al perfil",perfilElegido,"con exito: ")

                    while True:

                        print("\n[1] Ver Visualizaciones\n"
                              "[2] Ver Contenidos\n"
                              "[3] Ver Favoritos\n"
                              "[4] Manejar Usuario\n"
                              "[5] Manejo de Perfil\n"
                              "[6] Volver al menu principal\n")

                        eleccion= input("Que deseas hacer: ")

                        try:
                            valEleccion= int(eleccion)

                            if (valEleccion==1):
                                cur.execute('SELECT codigo_contenido FROM visto WHERE nombre_perfil = %s',
                                            (perfilElegido,))
                                contenidoVisto = cur.fetchall()
                                for contenido in contenidoVisto:
                                    print(contenido[0])
                                while True:

                                    print("\n[1] Ver Visualizacion\n"
                                          "[2] Agregar Visualizacion\n"
                                          "[3] Eliminar Visualizacion\n")

                                    opcion = input("Que deseas hacer: ")

                                    try:
                                        valopcion = int(opcion)

                                        if (valopcion == 1):
                                            visualizacion = input("Elija una visualizacion: ")
                                            cur.execute(
                                                'SELECT fecha, hora, etapa FROM visto WHERE codigo_contenido=%s',
                                                (visualizacion,))
                                            datosContenido = cur.fetchone()
                                            print("Se vio el contenido el " + datosContenido[0],
                                                  "a las " + datosContenido[1],
                                                  "\nSu estado es: " + datosContenido[2])
                                            break

                                        elif (valopcion == 2):
                                            cur.execute('SELECT codigo FROM contenido')
                                            contenidoTotal = cur.fetchall()
                                            for contenido in contenidoTotal:
                                                print(contenido[0])
                                            while True:
                                                agregarCont = input("Elija un contenido: ")
                                                fechaAgr = input("Inserte la fecha de visualizacion: ")
                                                horaAgr = input("Inserte la hora de visualizacion: ")
                                                while True:
                                                    etapaAgr = input("Inserte la estado del contenido: ")
                                                    if (etapaAgr == "Finalizado" or etapaAgr == "Parcial"):
                                                        break
                                                    else:
                                                        print(
                                                            "El estado ingresado no existe (Solo se puede colocar Finalizado o Parcial), intente nuevamente: ")
                                                        continue
                                                cur.execute(
                                                    'SELECT codigo_contenido FROM visto WHERE codigo_contenido=%s AND nombre_perfil=%s AND fecha=%s AND hora=%s AND etapa=%s'
                                                    , (agregarCont, perfilElegido, fechaAgr, horaAgr, etapaAgr))
                                                verificarCodigo = cur.fetchone()
                                                if (verificarCodigo == None):
                                                    cur.execute(
                                                        'INSERT INTO visto(codigo_contenido, nombre_perfil, fecha, hora, etapa)'
                                                        'VALUES(%s,%s,%s,%s,%s)',
                                                        (agregarCont, perfilElegido, fechaAgr, horaAgr, etapaAgr))
                                                    conn.commit()
                                                    print("\nEL contenido ha sido agregado con exito\n")
                                                    break
                                                else:
                                                    print(
                                                        "El contenido con esos datos ingresados ya existe, volvera al menu anterior\n")
                                                    break
                                            break

                                        elif (valopcion == 3):
                                            eliminarVisualizacion = input("Ingrese visualizacion que desee eliminar: ")
                                            while True:
                                                confirmador = input("Esta seguro?\n"
                                                                    "[1] Si\n"
                                                                    "[2] No\n"
                                                                    "Ingrese su respuesta: ")
                                                try:
                                                    confirmadorint = int(confirmador)
                                                    if (confirmadorint == 1):
                                                        cur.execute('DELETE FROM visto WHERE codigo_contenido=%s',
                                                                    (eliminarVisualizacion,))
                                                        conn.commit()
                                                        print(
                                                            "Se ha borrado la visualizacion y toda su informacion correctamente.")
                                                        break
                                                    else:
                                                        break
                                                except ValueError:
                                                    print("\nLa opcion ingresada no es valida, intentalo denuevo\n")
                                                    continue

                                            break
                                    except ValueError:
                                        print("La opcion ingresada no es valida, intentalo nuevamente\n")
                                        continue
                                continue

                            elif (valEleccion==2):
                                while True:
                                    print("\n[1] Crear contenido\n"
                                          "[2] Editar contenido\n"
                                          "[3] Eliminar contenido\n"
                                          "[4] Volver\n")
                                    accion = input("Que deseas hacer: ")
                                    try:
                                        valAccion = int(accion)
                                        ################################################################################################################################
                                        if (valAccion == 1):
                                            while True:
                                                print("\n[1] Crear Serie\n"
                                                      "[2] Crear Pelicula\n"
                                                      "[3] Crear Documental\n"
                                                      "[4] Volver\n")
                                                tipoContenido = input("Indique el tipo de contenido que desea Crear: ")
                                                try:
                                                    tipoContenido = int(tipoContenido)
                                                    if (tipoContenido == 1):
                                                        cur.execute('SELECT codigo FROM contenido')
                                                        contenidoTotal = cur.fetchall()
                                                        while True:
                                                            codigo = input("Agregar codigo para la nueva serie: ")
                                                            try:
                                                                cur.execute(
                                                                    'SELECT exists (SELECT 1 FROM contenido WHERE codigo = %s AND Existe=%s LIMIT 1)',
                                                                    (codigo,noExiste))
                                                                verificarCodigo = cur.fetchone()

                                                                if (verificarCodigo[0]==True):


                                                                    nombreSerie = input(
                                                                        "Ingrese el nombre de su nueva serie: ")
                                                                    while True:
                                                                        num_temp = input(
                                                                            "Ingrese el numero de temporadas de la nueva serie: ")
                                                                        try:
                                                                            num_temp = int(num_temp)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de la nueva serie: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break

                                                                    cur.execute(
                                                                        'UPDATE contenido SET Existe=%s,duracion=%s,director=%s ,categoria=%sWHERE codigo=%s',
                                                                        (existe,duracion,director,categoria,codigo))
                                                                    conn.commit()

                                                                    n_temp = "1"
                                                                    i = 1
                                                                    while i <= num_temp:
                                                                        capitulo = codigo + str(i) + "1"
                                                                        cur.execute(
                                                                            'INSERT INTO Series(codigo_cap,nombre_s,codigo_contenido,categoria_esp,num_temporadas)'
                                                                            'VALUES (%s,%s,%s,%s,%s)', (
                                                                                capitulo, nombreSerie, codigo,
                                                                                categoria,
                                                                                str(i)))
                                                                        conn.commit()
                                                                        i += 1

                                                                    print("\nLa Serie ha sido creada con exito!!!\n")
                                                                    break


                                                                if (verificarCodigo[0] == False):
                                                                    nombreSerie = input(
                                                                        "Ingrese el nombre de su nueva serie: ")
                                                                    while True:
                                                                        num_temp = input(
                                                                            "Ingrese el numero de temporadas de la nueva serie: ")
                                                                        try:
                                                                            num_temp = int(num_temp)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de la nueva serie: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break
                                                                    cur.execute(
                                                                        'INSERT INTO Contenido(codigo,duracion,director,categoria,existe)'
                                                                        'VALUES (%s,%s,%s,%s,%s)', (
                                                                        codigo, duracion, director, categoria,
                                                                        "Existe"))
                                                                    conn.commit()
                                                                    n_temp = "1"
                                                                    i = 1
                                                                    while i <= num_temp:
                                                                        capitulo = codigo + str(i) + "1"
                                                                        cur.execute(
                                                                            'INSERT INTO Series(codigo_cap,nombre_s,codigo_contenido,categoria_esp,num_temporadas)'
                                                                            'VALUES (%s,%s,%s,%s,%s)', (
                                                                            capitulo, nombreSerie, codigo, categoria,
                                                                            str(i)))
                                                                        conn.commit()
                                                                        i += 1

                                                                    print("\nLa Serie ha sido creada con exito!!!\n")
                                                                    break
                                                            except ValueError:
                                                                print(
                                                                    "El codigo ingresado ya existe, intente nuevamente\n")
                                                        break
                                                    elif (tipoContenido == 2):
                                                        cur.execute('SELECT codigo FROM contenido')
                                                        contenidoTotal = cur.fetchall()
                                                        while True:
                                                            codigo = input("Agregar codigo para la nueva Pelicula: ")
                                                            try:
                                                                cur.execute(
                                                                    'SELECT exists (SELECT 1 FROM contenido WHERE codigo = %s AND Existe=%s LIMIT 1)',
                                                                    (codigo, noExiste))
                                                                verificarCodigo = cur.fetchone()

                                                                if (verificarCodigo[0] == False):
                                                                    nombrePelicula = input(
                                                                        "Ingrese el nombre de su nueva Pelicula: ")
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de la nueva Pelicula: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break
                                                                    cur.execute(
                                                                        'INSERT INTO Contenido(codigo,duracion,director,categoria,existe)'
                                                                        'VALUES (%s,%s,%s,%s,%s)', (
                                                                        codigo, duracion, director, categoria,
                                                                        "Existe"))
                                                                    conn.commit()
                                                                    cur.execute(
                                                                        'INSERT INTO peliculas(nombre_p,codigo_contenido)'
                                                                        'VALUES (%s,%s)', (nombrePelicula, codigo))
                                                                    conn.commit()
                                                                    print("\nLa Pelicula ha sido creada con exito!!!\n")
                                                                    break

                                                                if (verificarCodigo[0] == True):
                                                                    nombrePelicula = input(
                                                                        "Ingrese el nombre de su nueva Pelicula: ")
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de la nueva Pelicula: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break
                                                                    cur.execute(
                                                                        'UPDATE Contenido SET existe=%s,duracion=%s,director=%s,categoria=%s',
                                                                    (existe, duracion, director, categoria))
                                                                    conn.commit()
                                                                    cur.execute(
                                                                        'INSERT INTO peliculas(nombre_p,codigo_contenido)'
                                                                        'VALUES (%s,%s)', (nombrePelicula, codigo))
                                                                    conn.commit()
                                                                    print(
                                                                        "\nLa Pelicula ha sido creada con exito!!!\n")
                                                                    break


                                                            except ValueError:
                                                                print(
                                                                    "El codigo ingresado ya existe, intente nuevamente\n")
                                                        break
                                                    elif (tipoContenido == 3):

                                                        cur.execute('SELECT codigo FROM contenido')
                                                        contenidoTotal = cur.fetchall()
                                                        while True:
                                                            codigo = input("Agregar codigo para el nuevo Documental: ")
                                                            try:
                                                                cur.execute(
                                                                    'SELECT exists (SELECT 1 FROM contenido WHERE codigo = %s AND Existe=%s LIMIT 1)',
                                                                    (codigo, noExiste))
                                                                verificarCodigo = cur.fetchone()
                                                                if (verificarCodigo[0] == False):
                                                                    nombreDocumental = input(
                                                                        "Ingrese el nombre de su nuevo Documental: ")
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de su nuevo Documental: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break
                                                                    cur.execute(
                                                                        'INSERT INTO Contenido(codigo,duracion,director,categoria,existe)'
                                                                        'VALUES (%s,%s,%s,%s,%s)', (
                                                                        codigo, duracion, director, categoria,
                                                                        "Existe"))
                                                                    conn.commit()
                                                                    cur.execute(
                                                                        'INSERT INTO documentales(nombre_d,codigo_contenido)'
                                                                        'VALUES (%s,%s)', (nombreDocumental, codigo))
                                                                    conn.commit()

                                                                    print(
                                                                        "\nEl Documental ha sido creado con exito!!!\n")
                                                                    break

                                                                if (verificarCodigo[0] == True):
                                                                    nombreDocumental = input(
                                                                        "Ingrese el nombre de su nuevo Documental: ")
                                                                    while True:
                                                                        duracion = input(
                                                                            "Ingrese la duracion de su nuevo Documental: ")
                                                                        try:
                                                                            duracion = int(duracion)
                                                                            break
                                                                        except ValueError:
                                                                            print("Tienes que ingresar numeros")
                                                                            continue
                                                                    while True:
                                                                        director = input(
                                                                            "Ingrese el director de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                            (director,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Directores(nombre_director)'
                                                                                'VALUES (%s)', (director,))
                                                                            conn.commit()
                                                                            break
                                                                    while True:
                                                                        categoria = input(
                                                                            "Ingrese la categoria de la nueva serie: ")
                                                                        cur.execute(
                                                                            'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                            (categoria,))
                                                                        validacion = cur.fetchone()
                                                                        if validacion[0] == True:
                                                                            break
                                                                        else:
                                                                            cur.execute(
                                                                                'INSERT INTO Categorias(nombre_categoria)'
                                                                                'VALUES (%s)', (categoria,))
                                                                            conn.commit()
                                                                            break
                                                                    cur.execute(
                                                                        'UPDATE Contenido SET duracion=%s,director=%s,categoria=%s,existe=%s',
                                                                        (duracion,director,categoria,existe))
                                                                    conn.commit()
                                                                    cur.execute(
                                                                        'INSERT INTO documentales(nombre_d,codigo_contenido)'
                                                                        'VALUES (%s,%s)', (nombreDocumental, codigo))
                                                                    conn.commit()

                                                                    print(
                                                                        "\nEl Documental ha sido creado con exito!!!\n")
                                                                    break
                                                            except ValueError:
                                                                print(
                                                                    "El codigo ingresado ya existe, intente nuevamente\n")
                                                        break
                                                    elif (tipoContenido == 4):
                                                        break
                                                except ValueError:
                                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                                    ################################################################################################################################
                                        elif (valAccion == 2):
                                            cur.execute('SELECT codigo FROM contenido')
                                            contenidoTotal = cur.fetchall()
                                            print("Los contenidos de la base de datos son:")

                                            for contenido in contenidoTotal:
                                                print(contenido[0])

                                            while True:
                                                codigo = input("Ingrese el contenido que desea Editar: ")
                                                try:
                                                    cur.execute('SELECT codigo FROM contenido WHERE codigo=%s',
                                                                (codigo,))
                                                    verificarCodigo = cur.fetchone()
                                                    if (verificarCodigo != None):
                                                        print("\n Perfecto!\n"
                                                              "Ahora ingrese los datos que desea cambiar: \n")
                                                        while True:
                                                            nuevaDuracion = input(
                                                                "Ingrese la duracion del nuevo contenido: ")
                                                            try:
                                                                nuevaDuracion = int(nuevaDuracion)
                                                                break
                                                            except ValueError:
                                                                print("Tienes que ingresar numeros")
                                                                continue
                                                        cur.execute('UPDATE contenido SET duracion=%s WHERE codigo=%s',
                                                                    (nuevaDuracion, codigo))
                                                        conn.commit()
                                                        while True:
                                                            nuevoDirector = input(
                                                                "Ingrese el director del nuevo contenido: ")
                                                            cur.execute(
                                                                'SELECT exists (SELECT 1 FROM directores WHERE nombre_director = %s LIMIT 1)',
                                                                (nuevoDirector,))
                                                            validacion = cur.fetchone()
                                                            if validacion[0] == True:
                                                                cur.execute(
                                                                    'UPDATE contenido SET director=%s WHERE codigo=%s',
                                                                    (nuevoDirector, codigo))
                                                                conn.commit()
                                                                break
                                                            else:
                                                                cur.execute(
                                                                    'INSERT INTO Directores(nombre_director)'
                                                                    'VALUES (%s)', (nuevoDirector,))
                                                                conn.commit()
                                                                cur.execute(
                                                                    'UPDATE contenido SET director=%s WHERE codigo=%s',
                                                                    (nuevoDirector, codigo))
                                                                conn.commit()
                                                                break
                                                        while True:
                                                            nuevaCategoria = input(
                                                                "Ingrese la categoria del nuevo contenido: ")
                                                            cur.execute(
                                                                'SELECT exists (SELECT 1 FROM categorias WHERE nombre_categoria = %s LIMIT 1)',
                                                                (nuevaCategoria,))
                                                            validacion = cur.fetchone()
                                                            if validacion[0] == True:
                                                                cur.execute(
                                                                    'UPDATE contenido SET categoria=%s WHERE codigo=%s',
                                                                    (nuevaCategoria, codigo))
                                                                conn.commit()
                                                                break
                                                            else:
                                                                cur.execute(
                                                                    'INSERT INTO Categorias(nombre_categoria)'
                                                                    'VALUES (%s)', (nuevaCategoria,))
                                                                conn.commit()
                                                                cur.execute(
                                                                    'UPDATE contenido SET categoria=%s WHERE codigo=%s',
                                                                    (nuevaCategoria, codigo))
                                                                conn.commit()
                                                                break
                                                        print("\nEl Contenido ha sido editado con exito!!!\n")
                                                        break
                                                except ValueError:
                                                    print("El codigo ingresado no existe, intente nuevamente\n")
                                            break
                                            ################################################################################################################################
                                        elif (valAccion == 3):
                                            cur.execute('SELECT codigo FROM contenido')
                                            contenidoTotal = cur.fetchall()
                                            print("Los contenidos de la base de datos son:")
                                            lista = []
                                            for contenido in contenidoTotal:
                                                lista.append(contenido[0])
                                                print(contenido[0])

                                            eliminarContenido = input(
                                                "Cual de estos contenidos deseas eliminar de tu lista de contenidos: ")
                                            if eliminarContenido in lista:
                                                cur.execute('DELETE FROM series WHERE codigo_contenido=%s',
                                                            (eliminarContenido,))
                                                conn.commit()
                                                cur.execute('DELETE FROM peliculas WHERE codigo_contenido=%s',
                                                            (eliminarContenido,))
                                                conn.commit()
                                                cur.execute('DELETE FROM documentales WHERE codigo_contenido=%s',
                                                            (eliminarContenido,))
                                                conn.commit()
                                                cur.execute('DELETE FROM historial WHERE codigo_contenido=%s',
                                                            (eliminarContenido,))
                                                conn.commit()
                                                cur.execute('UPDATE contenido SET Existe=%s WHERE codigo=%s ',
                                                            (noExiste, eliminarContenido))
                                                conn.commit()
                                                print(
                                                    "\nSe ha eliminado con exito el contenido de tu lista de contenidos!")
                                                break
                                            else:
                                                print(
                                                    "El contenido que quieres borrar no se encuentra en tu lista de contenidos, intentalo denuevo\n")
                                                continue
                                            #break
                                            ################################################################################################################################
                                        elif (valAccion == 4):
                                            break
                                    except ValueError:
                                        print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")

                            elif(valEleccion==3):
                                cur.execute('SELECT codigo_contenido FROM favoritos WHERE nombre_perfil=%s',
                                            (perfilElegido,))
                                favoritos=cur.fetchall()

                                print("Los contenidos favoritos de este perfil son:")
                                for favorito in favoritos:
                                    print(favorito[0])

                                while True:
                                    print('\n[1] Agregar Favorito\n'
                                          '[2] Eliminar Favorito\n')

                                    eleccionFav=input('Que deseas hacer: ')

                                    try:
                                        eleccionFav=int(eleccionFav)

                                        if eleccionFav==1:
                                            cur.execute('SELECT c.codigo FROM contenido c WHERE c.codigo NOT IN (SELECT f.codigo_contenido FROM Favoritos f WHERE f.nombre_perfil=%s)',
                                                        (perfilElegido,))
                                            noFavoritos= cur.fetchall()

                                            while True:
                                                print("Todo los contenidos que no tienes en tus favoritos son: ")
                                                lista=[]

                                                for nofavorito in noFavoritos:
                                                    lista.append(nofavorito[0])
                                                    print(nofavorito[0])

                                                favoritoNuevo= input("\nCual deseas ingresar a tu lista de favoritos:  ")

                                                if favoritoNuevo in lista:
                                                    cur.execute('INSERT INTO Favoritos(nombre_perfil,codigo_contenido)'
                                                                'VALUES (%s,%s)',(perfilElegido,favoritoNuevo))
                                                    conn.commit()
                                                    print("Se ha agregado con exito tu nuevo favorito\n")
                                                    break
                                                else:
                                                    print("El contenido que ingresaste ya esta en tu lista de favoritos o no existe, intentalo nuevamente\n")
                                                    continue

                                        elif eleccionFav==2:

                                            while True:
                                                cur.execute('SELECT codigo_contenido FROM favoritos WHERE nombre_perfil=%s',
                                                            (perfilElegido,))
                                                favoritos = cur.fetchall()

                                                print("Los contenidos favoritos de este perfil son:")
                                                lista2=[]
                                                for favorito in favoritos:
                                                    lista2.append(favorito[0])
                                                    print(favorito[0])

                                                eliminarFav=input("Cual de estos contenidos deseas eliminar de tu lista de contenidos: ")

                                                if eliminarFav in lista2:
                                                    cur.execute('DELETE FROM favoritos WHERE nombre_perfil=%s AND codigo_contenido=%s',
                                                                (perfilElegido,eliminarFav))
                                                    conn.commit()
                                                    print("Se ha eliminado con exito el contenido de tu lista de favoritos\n")
                                                    break
                                                else:
                                                    print("El contenido que quieres borrar no se encuentra en tu lista de favoritos, intentalo denuevo\n")
                                                    continue

                                    except ValueError:
                                        print("La opcion ingresada no es valida, intentalo nuevamente")
                                        continue
                                    break
                                continue

                            elif(valEleccion==4):

                                while True:
                                    print("\n[1] Editar informacion de pago\n"
                                          "[2] Editar suscripcion\n"
                                          "[3] Editar informacion\n"
                                          "[4] Eliminar Usuario\n")
                                    opcionElegida = input("Ingrese una opcion: ")
                                    try:
                                        opcionElegidaI = int(opcionElegida)
                                        if (opcionElegidaI == 1):
                                            cur.execute(
                                                'SELECT metodoPago, numtarjeta FROM pago JOIN Usuarios ON ID=idusuario WHERE email=%s AND contraseña=%s',
                                                (email, contraseña))
                                            infoPago = cur.fetchone()
                                            print("Metodo de pago: " + infoPago[0],
                                                  "\nNumero de tarjeta: " + infoPago[1])
                                            while True:
                                                print("\n[1] Editar metodo de pago\n"
                                                      "[2] Editar numero de tarjeta\n"
                                                      "[3] No se desea editar nada mas\n")
                                                opcionE = input("Ingrese una opcion: ")
                                                try:
                                                    opcionEI = int(opcionE)
                                                    if (opcionEI == 1):
                                                        while True:
                                                            nuevometodop = input(
                                                                "Ingrese nuevo metodo de pago (Mastercard o Visa): ")
                                                            if (nuevometodop == "Mastercard" or nuevometodop == "Visa"):
                                                                break
                                                            else:
                                                                print("Metodo de pago incorrecto, intente nuevamente.")
                                                                continue
                                                        cur.execute(
                                                            'UPDATE pago SET metodopago = %s WHERE idusuario=%s',
                                                            (nuevometodop, usuario))
                                                        conn.commit()
                                                        continue
                                                    elif (opcionEI == 2):
                                                        while True:
                                                            nuevoNum = input(
                                                                "Ingrese nuevo numero de tarjeta (solo numeros): ")
                                                            try:
                                                                nuevoNumI = int(nuevoNum)
                                                                cur.execute(
                                                                    'UPDATE pago SET numtarjeta = %s WHERE idusuario=%s',
                                                                    (nuevoNum, usuario))
                                                                conn.commit()
                                                                break
                                                            except ValueError:
                                                                print(
                                                                    "\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                                        continue
                                                    elif (opcionEI == 3):
                                                        break
                                                except ValueError:
                                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")

                                            break
                                        elif (opcionElegidaI == 2):

                                            cur.execute(
                                                'SELECT subscripcion FROM pago WHERE idusuario=%s',
                                                (usuario,))
                                            subsUsuario = cur.fetchone()
                                            print("Su subscripcion actual es: " + subsUsuario[0])

                                            while True:

                                                cur.execute('SELECT * FROM subscripciones')
                                                subscripciones = cur.fetchall()
                                                print("\nLas subscripciones disponibles son: ")
                                                for subscripcion in subscripciones:
                                                    print(subscripcion[0])

                                                nuevaSubs = input("\nIntroduzca la subscripcion que desea: ")
                                                cur.execute('SELECT exists (SELECT 1 FROM Subscripciones WHERE tipo=%s LIMIT 1)',
                                                            (nuevaSubs,))
                                                subsExiste = cur.fetchone()
                                                if (subsExiste[0] == True):
                                                    cur.execute('UPDATE pago SET subscripcion=%s WHERE idUsuario=%s',
                                                                (nuevaSubs, usuario))
                                                    conn.commit()
                                                    print("\nSe ha actualizado su subcripcion con exito")
                                                    break
                                                else:
                                                    print("\nLa subscripcion ingresada no existe, intentalo nuevamente\n")
                                                    continue
                                            break
                                        elif (opcionElegidaI == 3):
                                            cur.execute(
                                                'SELECT nombre, apellido, telefono, email, calle, num_calle FROM Usuarios WHERE ID=%s',
                                                (usuario,))
                                            infoU = cur.fetchone()
                                            print("Nombre: " + infoU[0],
                                                  "\nApellido: " + infoU[1],
                                                  "\nTelefono: " + infoU[2],
                                                  "\nEmail: " + infoU[3],
                                                  "\nCalle: " + infoU[4],
                                                  "\nNumero de calle: " + str(infoU[5]))
                                            while True:
                                                print("\n[1] Nombre\n"
                                                      "[2] Apellido\n"
                                                      "[3] Telefono\n"
                                                      "[4] Email\n"
                                                      "[5] Calle\n"
                                                      "[6] Numero de calle\n"
                                                      "[7] No se desea editar nada mas\n")
                                                opcionElegida = input("Que desea hacer: ")
                                                try:
                                                    opcionElegidaI = int(opcionElegida)
                                                    if (opcionElegidaI == 1):
                                                        nuevoNombre = input("Ingrese nuevo nombre: ")
                                                        cur.execute('UPDATE Usuarios SET nombre=%s WHERE ID=%s',
                                                                    (nuevoNombre, usuario))
                                                        conn.commit()
                                                        print("Se ha editado el nombre con exito.")
                                                        continue
                                                    elif (opcionElegidaI == 2):
                                                        nuevoApellido = input("Ingrese nuevo apellido: ")
                                                        cur.execute('UPDATE Usuarios SET apellido=%s WHERE ID=%s',
                                                                    (nuevoApellido, usuario))
                                                        conn.commit()
                                                        print("Se ha editado el apellido con exito.")
                                                        continue
                                                    elif (opcionElegidaI == 3):
                                                        nuevoTelefono = input("Ingrese nuevo telefono: ")
                                                        cur.execute('UPDATE Usuarios SET telefono=%s WHERE ID=%s',
                                                                    (nuevoTelefono, usuario))
                                                        conn.commit()
                                                        print("Se ha editado el telefono con exito.")
                                                        continue
                                                    elif (opcionElegidaI == 4):
                                                        nuevoEmail = input("Ingrese nuevo email: ")
                                                        cur.execute('UPDATE Usuarios SET email=%s WHERE ID=%s',
                                                                    (nuevoEmail, usuario))
                                                        conn.commit()
                                                        print("Se ha editado el email con exito.")
                                                        continue
                                                    elif (opcionElegidaI == 5):
                                                        nuevaCalle = input("Ingrese nueva calle: ")
                                                        cur.execute('UPDATE Usuarios SET calle=%s WHERE ID=%s',
                                                                    (nuevaCalle, usuario))
                                                        conn.commit()
                                                        print("Se ha editado la calle con exito.")
                                                        continue
                                                    elif (opcionElegidaI == 6):
                                                        while True:
                                                            nuevoNum = input("Ingrese nuevo numero de calle: ")
                                                            try:
                                                                nuevoNumI = int(nuevoNum)
                                                                cur.execute(
                                                                    'UPDATE Usuarios SET num_calle=%s WHERE ID=%s',
                                                                    (nuevoNumI, usuario))
                                                                conn.commit()
                                                                print("Se ha editado el numero de calle con exito.")
                                                                break
                                                            except ValueError:
                                                                print(
                                                                    "\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                                        continue
                                                    elif (opcionElegidaI == 7):
                                                        break
                                                except ValueError:
                                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                            break
                                        elif (opcionElegidaI == 4):
                                            while True:
                                                print(
                                                    "Esta seguro que desea borrar este usuario con toda su informacion y acciones?\n"
                                                    "[1] Si\n"
                                                    "[2] No\n")
                                                respuesta = input("Cual es su respuesta: ")
                                                try:
                                                    respuestaI = int(respuesta)
                                                    if (respuestaI == 1):
                                                        cur.execute('DELETE FROM Historial WHERE nombre_perfil=%s',
                                                                    (perfilElegido,))
                                                        conn.commit()
                                                        cur.execute('DELETE FROM Favoritos WHERE nombre_perfil=%s',
                                                                    (perfilElegido,))
                                                        conn.commit()
                                                        cur.execute(
                                                            'UPDATE Perfiles SET Existe=%s WHERE nombreperfil=%s ',
                                                            (noExiste, usuario))
                                                        conn.commit()
                                                        cur.execute('DELETE FROM pago WHERE idUsuario=%s', (usuario,))
                                                        conn.commit()
                                                        cur.execute('Delete FROM loginUsuarios WHERE id_usuario=%s',
                                                                    (usuario,))
                                                        conn.commit()
                                                        cur.execute('UPDATE Usuarios SET existe=%s WHERE ID=%s',
                                                                    (noExiste, usuario))
                                                        conn.commit()
                                                        print("\nEl usuario y toda su informacion ha sido eliminada.\n")
                                                        break

                                                    elif (respuestaI == 2):
                                                        break
                                                except ValueError:
                                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                            break
                                    except ValueError:
                                        print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")
                                continue

                            elif(valEleccion==5):
                                print("\n[1] Cambiar de perfil\n"
                                      "[2] Agregar Perfil\n"
                                      "[3] Editar Perfil\n"
                                      "[4] Eliminar Perfil\n")
                                accion= input("Que deseas hacer: ")

                                try:
                                    valAccion=int(accion)

                                    if(valAccion==1):
                                        break

                                    elif(valAccion==2):
                                        while True:
                                            nombrePerfil= input("Ingrese el nombre de su nuevo perfil: ")

                                            while True:
                                                edad= input("Ingrese su edad")
                                                try:
                                                    edad=int(edad)
                                                    break

                                                except ValueError:
                                                    print("Tienes que ingresar numeros")
                                                    continue

                                            cur.execute(
                                                'SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s AND Existe=%s LIMIT 1)',
                                                (nombrePerfil, noExiste))
                                            validacion = cur.fetchone()

                                            if validacion[0]==True:
                                                cur.execute('UPDATE Perfiles SET Existe=%s WHERE nombreperfil=%s',(existe,nombrePerfil))
                                                print('\nYa existia un perfil con este nombre pero hania sido eliminado ')
                                                break

                                            cur.execute('SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s AND Existe=%s LIMIT 1)',
                                                (nombrePerfil,existe ))
                                            validacion2 = cur.fetchone()

                                            if validacion2[0]==True:
                                                print("\nYa existe un perfil con este nombre, intentalo nuevamente\n")
                                                continue

                                            cur.execute('SELECT exists (SELECT 1 FROM Perfiles WHERE nombreperfil = %s  LIMIT 1)',
                                                        (nombrePerfil,))
                                            validacion3=cur.fetchone()

                                            if validacion3[0]==False:
                                                cur.execute(
                                                    'INSERT INTO Perfiles(nombreperfil,idusuario,edad,existe)'
                                                    'VALUES (%s,%s,%s,%s)', (nombrePerfil, usuario, edad, existe))
                                                conn.commit()
                                                print("\nEl perfil ha sido creado con exito!!!!\n")
                                                break

                                    elif(valAccion==3):
                                        nuevoNombrePerfil=input("Ingresa el nuevo nombre de este perfil: ")
                                        while True:
                                            nuevaEdad= input("Ingresa la edad asociada a este perfil: ")
                                            try:
                                                nuevaEdad=int(nuevaEdad)
                                                break
                                            except ValueError:
                                                print("Ingresa una edad valida!\n")
                                                continue

                                        cur.execute('UPDATE Perfiles SET nombreperfil=%s WHERE nombreperfil=%s AND idusuario=%s',
                                                    (nuevoNombrePerfil,perfilElegido,usuario))
                                        conn.commit()
                                        cur.execute('UPDATE Perfiles SET edad=%s WHERE nombreperfil=%s AND idusuario=%s',
                                                    (nuevaEdad,nuevoNombrePerfil,usuario))
                                        conn.commit()
                                        print("Se han actualizado los datos del perfil de forma existosa")
                                        continue

                                    elif(valAccion==4):
                                        while True:
                                            respuesta=input("Estas seguro de querer borrar este perfil y todas las acciones realizadas por este?\n"
                                                            "[1] Si\n"
                                                            "[2] No\n"
                                                            "Cual es tu respuesta ( no hay marcha atras ): ")
                                            try:
                                                respuesta=int(respuesta)

                                                if respuesta==1:
                                                    cur.execute('DELETE FROM Historial WHERE nombre_perfil=%s',(perfilElegido,))
                                                    conn.commit()
                                                    cur.execute('DELETE FROM Favoritos WHERE nombre_perfil=%s',(perfilElegido,))
                                                    conn.commit()
                                                    cur.execute('UPDATE Perfiles SET Existe=%s WHERE nombreperfil=%s ',
                                                                (noExiste,perfilElegido))
                                                    conn.commit()

                                                    print("\nSe ha borrado con exito la informacion y las acciones del perfil")
                                                    break
                                                else:
                                                    break
                                            except ValueError:
                                                print("La opcion ingresada no es valida, intentalo denuevo\n")
                                                continue
                                        continue

                                except ValueError:
                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")

                            elif (valEleccion == 6):
                                break

                            else:
                                print("La opcion ingresada no existe, intentalo nuevamente\n")
                                continue

                        except ValueError:
                            print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")

                else:
                    print("El perfil ingresado no existe para este usuario, intentalo nuevamente\n")
                    continue

                val2 = valEleccion

                if (val2==6):
                    break

            continue
        elif val == 2:

            while True:

                nombreUsuario = input("\nIngrese el nombre de su nuevo usuario: ")
                email = input("Ingrese el mail: ")
                nombre = input("Ingrese su nombre: ")
                apellido = input("Ingrese su apellido: ")
                telefono = input("Ingrese su numero de telefono: ")
                calle = input("Ingrese su direccion sin numero: ")
                while True:
                    numCalle = input("Ingrese el numero de su direccion: ")
                    try:
                        numCalleValidado=int(numCalle)
                        break
                    except ValueError:
                        print("No puedes ingresar letras en el numero de calle,intentelo nuevamente\n")
                        continue

                contraseña = input("Ingrese contaseña: ")
                repetContraseña = input("Ingrese nuevamente la contraseña: ")

                cur.execute('SELECT exists (SELECT 1 FROM Usuarios WHERE id = %s AND Existe=%s LIMIT 1)', (nombreUsuario,noExiste))
                usuarioEliminado= cur.fetchone()

                if usuarioEliminado[0]==True:
                    cur.execute('UPDATE Usuarios SET contraseña=%s,nombre=%s,apellido=%s,telefono=%s,email=%s,calle=%s,num_calle=%s,Existe=%s WHERE ID=%s'
                                ,(contraseña, nombre, apellido, telefono, email, calle, numCalle,existe,nombreUsuario))
                    conn.commit()

                    print("\nEL usuario ha sido creado con exito\n")
                    break

                cur.execute('SELECT exists (SELECT 1 FROM Usuarios WHERE id = %s  LIMIT 1)', (nombreUsuario,))
                usuarioExiste = cur.fetchone()


                if (usuarioExiste[0] == True):
                    print("\nYa existe un usuario con ese ID, intentalo nuevamente\n")
                    continue

                if (contraseña != repetContraseña):
                    print("\nLas contraseñas no coinciden, intentalo nuevamente\n")
                    continue


                else:
                    cur.execute('INSERT INTO Usuarios(id,contraseña,nombre,apellido,telefono,email,calle,num_calle)'
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                                (nombreUsuario, contraseña, nombre, apellido, telefono, email, calle, numCalle))
                    conn.commit()
                    print("\nEL usuario ha sido creado con exito\n")

                    break
            continue

        elif val == 3:

            mail= input("Ingrese el mail asociado a su usuario: ")
            cur.execute('SELECT exists (SELECT 1 FROM Usuarios WHERE email = %s  LIMIT 1)', (mail,))
            existeUsuario= cur.fetchone()

            cur.execute('SELECT id FROM Usuarios WHERE email=%s',(mail,))
            usuario=cur.fetchone()

            if(existeUsuario[0]== True):
                contraseñaNueva=input("Ingrese su nueva contraseña: ")
                cur.execute('UPDATE Usuarios SET contraseña=%s WHERE id=%s',(contraseñaNueva,usuario[0]))
                conn.commit()
                print("Se ha actualizado la contraseña con exito, seras regresado al menu principal\n")
                continue

            else:
                print("Lo sentimos, no existe ningun usuario asociado a ese email,"
                      "seras regresado al menu principal\n")

            continue

        elif val==4:
            cur.close()
            conn.close()
            break

        else:
            print("La opcion ingresada no existe, intentalo nuevamente\n")
            continue


    except ValueError:
        print("Ingresaste una opcion no valida , seras regresado el menu principal\n")
        continue







