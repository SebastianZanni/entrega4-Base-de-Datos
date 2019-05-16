import psycopg2

conn= psycopg2.connect(host='201.238.213.114',port=54321,database='grupo5',user='grupo5',password='LTguaC')
cur = conn.cursor()

while True:

    print("[1] Iniciar Sesion\n"
          "[2] Crear Cuenta\n"
          "[3] Recuperar Contraseña\n"
          "[4] Salir\n")

    menu= input("Que deseas hacer: ")

    try:
        val = int(menu)

        if (val == 1):
            email = input("\nIngrese email del usuario al que quiere ingresar: ")
            contraseña = input("Ingrese la contraseña del usuario al que quiere ingresar: ")

            cur.execute('SELECT id FROM Usuarios WHERE email=%s AND contraseña=%s', (email, contraseña))

            cont1 = cur.fetchone()

            if cont1 == None:
                print(
                    "La contraseña o el mail ingresados no coinciden con algun usuario, seras regresado al menu principal\n")
                continue

            usuario= cont1[0]

            print("\nIniciaste sesion exitosamente con el usuario:", usuario)

            while True:
                cur.execute('SELECT nombreperfil FROM Perfiles WHERE idusuario=%s', (usuario,))
                cont2 = cur.fetchall()
                print("Los perfiles disponibles son: ")

                for perfil in cont2:
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
                                cur.execute('SELECT codigo_contenido FROM visto WHERE nombre_perfil = %s', (perfilElegido,))
                                contenidoVisto = cur.fetchall()
                                for contenido in contenidoVisto:
                                    print (contenido[0])
                                while True:
                                    
                                    print("\n[1] Ver Visualizacion\n"
                                          "[2] Agregar Visualizacion\n"
                                          "[3] Eliminar Visualizacion\n")
                                    
                                    opcion = input("Que deseas hacer: ")
                                    
                                    try:
                                        valopcion = int(opcion)
                                        
                                        if (valopcion==1):
                                            visualizacion = input("Elija una visualizacion: ")
                                            cur.execute('SELECT fecha, hora, etapa FROM visto WHERE codigo_contenido=%s',(visualizacion,))
                                            datosContenido = cur.fetchone()
                                            print ("Se vio el contenido el " + datosContenido[0], 
                                                    "a las " + datosContenido[1], 
                                                    "\nSu estado es: " + datosContenido[2])
                                            break
                                        
                                        elif (valopcion==2):
                                            cur.execute('SELECT codigo FROM contenido')
                                            contenidoTotal = cur.fetchall()
                                            for contenido in contenidoTotal:
                                                print (contenido[0])    
                                            while True:
                                                agregarCont = input("Elija un contenido: ")
                                                fechaAgr = input("Inserte la fecha de visualizacion: ")
                                                horaAgr = input("Inserte la hora de visualizacion: ")
                                                while True:
                                                    etapaAgr = input("Inserte la estado del contenido: ")
                                                    if (etapaAgr=="Finalizado" or etapaAgr=="Parcial"):
                                                        break
                                                    else:
                                                        print ("El estado ingresado no existe (Solo se puede colocar Finalizado o Parcial), intente nuevamente: ")
                                                        continue
                                                cur.execute('SELECT codigo_contenido FROM visto WHERE codigo_contenido=%s AND nombre_perfil=%s AND fecha=%s AND hora=%s AND etapa=%s'
                                                            , (agregarCont,perfilElegido, fechaAgr, horaAgr, etapaAgr))
                                                verificarCodigo = cur.fetchone()
                                                if (verificarCodigo == None):
                                                    cur.execute('INSERT INTO visto(codigo_contenido, nombre_perfil, fecha, hora, etapa)'
                                                                'VALUES(%s,%s,%s,%s,%s)',
                                                                (agregarCont, perfilElegido, fechaAgr, horaAgr, etapaAgr))
                                                    conn.commit()
                                                    print("\nEL contenido ha sido agregado con exito\n")
                                                    break
                                                else:
                                                    print ("El contenido con esos datos ingresados ya existe, volvera al menu anterior\n")
                                                    break
                                            break
                                        
                                        elif (valopcion==3):
                                            eliminarVisualizacion = input("Ingrese visualizacion que desee eliminar: ")                                           
                                            while True:
                                                confirmador = input("Esta seguro?"
                                                                    "[1] Si\n"
                                                                    "[2] No\n"
                                                                    "Ingrese su respuesta: ")
                                                try:
                                                    confirmadorint = int(confirmador)
                                                    if (confirmadorint == 1):
                                                        cur.execute('DELETE FROM visto WHERE codigo_contenido=%s',(eliminarVisualizacion,))
                                                        conn.commit()
                                                        print ("Se ha borrado la visualizacion y toda su informacion correctamente.")
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
                                continue
                            elif(valEleccion==3):
                                continue
                            elif(valEleccion==4):
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
                                            'INSERT INTO Perfiles(nombreperfil,idusuario,edad)'
                                            'VALUES (%s,%s,%s)',(nombrePerfil,usuario,edad))
                                        conn.commit()
                                        print("\nEl perfil ha sido creado con exito!!!!\n")
                                        continue


                                    elif(valAccion==3):
                                        nuevoNombrePerfil=input("Ingresa el nuevo nombre de este perfil: ")
                                        while True:
                                            nuevaEdad= input("Ingresa la edad asociada a este perfil: ")
                                            try:
                                                nuevaEdad=int(nuevaEdad)
                                                break
                                            except ValueError:
                                                print("Igresa una edad valida!\n")
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
                                                    cur.execute('DELETE FROM Perfiles WHERE nombreperfil=%s ',
                                                                (perfilElegido,))
                                                    conn.commit()

                                                    print("Se ha borrado con exito la informacion y las acciones del perfil")
                                                    continue
                                                else:
                                                    break
                                            except ValueError:
                                                print("La opcion ingresada no es valida, intentalo denuevo\n")
                                                continue
                                        continue

                                except ValueError:
                                    print("\nLa opcion ingresada no es valida, intentalo nuevamente\n")

                            elif (valEleccion == 6):
                                input("\nPresiona ENTER para volver al menu principal\n")
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







