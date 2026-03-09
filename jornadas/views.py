from django.shortcuts import render, get_object_or_404
from llenar_quiniela.models import Prediccion, Estadisticas
from tabla_general.models import Equipos, Jornadas, Cartas, Puntos_extra, Colores, Cartas_aux, jugadores_gol, Puntos_cartas, tiempo, PI
import unicodedata
import sqlite3
import traceback
# Create your views here.

Jugadores = ['Felix', 'Victor', 'Manuel', 'Leo', 'Juan Luis', 'Omar', 'Hector', 'Horacio', 'Fernando', 'Bryan', 'Jorge', 'Rafa', 'Erick', 'Miguel', 'Alfonso', 'Saem', 'Brian', 'Josue', 'Angel']

def sec_resultados(nj):
    jornada = f'pJ{nj}'
    
    # Obtener el valor de la jornada desde el modelo Prediccion
    resultado = Prediccion.objects.filter(nombre='Resultados').values_list(jornada, flat=True)
    resultado = str(resultado[0])
    print(resultado)
    return resultado
def marcador_a_secuencia(secuencia):
    elementos = secuencia.split(', ')

    letras_resultado = []

    for elemento in elementos:
        if '-' in elemento:
            numero1, numero2 = map(int, elemento.split('-'))

            if numero1 > numero2:
                letras_resultado.append('L')
            elif numero1 < numero2:
                letras_resultado.append('V')
            else:
                letras_resultado.append('E')
        else:
            letras_resultado.append(elemento)

    return ', '.join(letras_resultado)
def get_card(nj, nombre):
    jornada = f'j{nj}'
    
    # Realizar la consulta utilizando los modelos de Django
    resultados = Cartas.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_predict(nj, nombre):
    jornada = f'pJ{nj}'
    # Realizar la consulta utilizando los modelos de Django
    resultados = Prediccion.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_jugadores_gol(nj):
    jornada = f'j{nj}'
    
    # Obtener el objeto de jugadores_gol
    jugadores_gol_obj = jugadores_gol.objects.first()
    


    if jugadores_gol_obj:
        # Obtener el valor del campo correspondiente (j1, j2, etc.)
        return getattr(jugadores_gol_obj, jornada)
    
    return None
def get_PI(nj):
    jornada = f'j{nj}'

    equipos_PI = PI.objects.first()

    if equipos_PI:
        return getattr(equipos_PI, jornada)

    return None

def get_tiempo(nj):
    jornada = f'j{nj}'
    
    # Obtener el objeto de jugadores_gol
    tiempo_obj = tiempo.objects.first()
    
    if tiempo_obj:
        # Obtener el valor del campo correspondiente (j1, j2, etc.)
        return getattr(tiempo_obj, jornada)
    
    
    return None

def get_estadisticas(nj):
    jornada = f'j{nj}'
    
    # Obtener el objeto de jugadores_gol
    tiempo_obj = Estadisticas.objects.first()
    
    if tiempo_obj:
        # Obtener el valor del campo correspondiente (j1, j2, etc.)
        return getattr(tiempo_obj, jornada)
    
    
    return None

def get_card_aux(nj, nombre):
    jornada = f'j{nj}'
    # Realizar la consulta utilizando los modelos de Django
    resultados = Cartas_aux.objects.filter(nombre=nombre).values_list(jornada, flat=True)
    resultados = str(resultados[0])
    return resultados
def get_points(prediccion_n, prediccion_s, carta, pred_j, carta_aux, jug_gol, tiempos, nj, est_jueg, p_i):
    lightsalmon = "lightsalmon"
    sec_colores = [lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon, lightsalmon]
    correctos = [item.strip() for item in prediccion_s.split(',')]
    pred = [item.strip() for item in pred_j.split(',')]
    p_extra = 0
    print(prediccion_s)
    print(pred_j)
    # Suma de puntos para Opcion doble y Opcion triple
    if carta == 'OD' or carta == 'OT' or carta == 'IQ' or carta == 'NC' or carta == "E" or carta == "PI" or carta =="CM":
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'

            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        
        if carta == "E" or carta == "PI":
            p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos, nj, est_jueg, p_i)
        contador += p_extra

        print(contador)
    elif carta == 'DQ':
        q1 = [elemento[0] for elemento in pred]
        q2 = [elemento[1] for elemento in pred]
        arr_col1 = []
        arr_col2 = []
        contador_q1 = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q1)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador_q1 += 1
                    arr_col1.append(idx)
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador_q1 += 1
                    arr_col1.append(idx)
        contador_q2 = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q2)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador_q2 += 1
                    arr_col2.append(idx)
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador_q2 += 1
                    arr_col2.append(idx)
        if contador_q1 > contador_q2:
            contador = contador_q1
            for i in arr_col1:
                sec_colores[i] = 'lightgreen'
            q = q1
        elif contador_q2 > contador_q1:
            contador = contador_q2
            for i in arr_col2:
                sec_colores[i] = 'lightgreen'
            q = q2
        else:
            contador = contador_q1
            for i in arr_col1:
                sec_colores[i] = 'lightgreen'
            q = q1

        print('Doble Quiniela: ', contador, q)
    elif carta == 'J':
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos, nj, est_jueg, p_i)
        contador += p_extra
        print('Jugador: ', contador)
    elif carta == 'T':
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos, nj, est_jueg, p_i)
        contador += p_extra
    elif carta == 'M':
        pred_M = [letra.upper() for letra in pred]
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, pred_M)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos, nj, est_jueg, p_i)
        contador += p_extra
        print(p_extra, sec_colores)
    elif carta == 'MA':
        q_s = marcador_a_secuencia(pred_j)
        q_s = [item.strip() for item in q_s.split(',')]
        contador = 0
        for idx, (valor1, valor2) in enumerate(zip(correctos, q_s)):
            if len(valor2) == 1:
                if valor1 == valor2 or valor1 in valor2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
            else:
                subvalores2 = [valor2[i:i+1] for i in range(0, len(valor2), 1)]
                if valor1 == valor2 or valor1 in subvalores2:
                    contador += 1
                    sec_colores[idx] = 'lightgreen'
        p_extra, sec_colores = extra_points(carta, carta_aux, jug_gol, correctos, pred, prediccion_n, pred_j, sec_colores, tiempos,nj, est_jueg, p_i)
        contador += p_extra
        print('Marcador: ', contador)
    else:
        contador = 0
        print('No aplica')
    print(correctos, pred)
    cadena_resultante = ', '.join(sec_colores)
    return contador, p_extra, cadena_resultante

def quitar_mayusculas_y_acentos(palabra):
    
    if palabra == 'San Luis':
        palabra_sin_acentos = 'san_luis'
    elif palabra == 'Cruz azul':
        palabra_sin_acentos = 'cruz_azul'
    else:
        # Convertir la palabra a minúsculas
        palabra = palabra.lower()
        # Eliminar los acentos
        palabra_sin_acentos = ''.join((c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn'))
    return palabra_sin_acentos

def extra_points(carta, carta_aux, jug_gol, correctos, pred, pred_n, pred_j_n, colo, tiempos, nj, est_jueg, p_i):
    puntos = 0

    if carta == 'E':
       # print("ESTADISTICA")
        for i in est_jueg:
            print(carta_aux.split(' ')[3], i.split(' ')[3])
            if carta_aux.split(' ')[3] == i.split(' ')[3]:
                print("SI")
                if carta_aux.split(' ')[0] == i.split(' ')[0]:
                    puntos += 1
                if carta_aux.split(' ')[1] == i.split(' ')[1]:
                    puntos += 1
                if carta_aux.split(' ')[2] == i.split(' ')[2]:
                    puntos += 1
        print(puntos)
    elif carta == 'PI':
        aux_pi = False
        for p in range(len(p_i)):
            print("CC: ", carta_aux.split(' - ')[0], p_i[p].split(", ")[0])
            if carta_aux.split(' - ')[0] == p_i[p].split(' - ')[0]:
                aux_pi = True
                puntos = int(carta_aux.split(' - ')[1])
        if not aux_pi:
            puntos = -int(carta_aux.split(' - ')[1])
    elif carta == 'J':
        p = 0
        jug = carta_aux.split(" ")
        print(carta_aux.split(" "))
        print(jug_gol)
        for j in jug:
            if j in jug_gol:
                p += 1
        if p == 2:
            puntos = 3
        elif p == 1:
            puntos = 2
            print(carta_aux)
            print('Puntos por jugador que mete gol: ', puntos)
    elif carta == 'T':
        if carta_aux in tiempos:
            carta_aux = carta_aux.split(":")
            ti = int(carta_aux[0].split("-")[1]) - int(carta_aux[0].split("-")[0])
            if ti == 45:
                puntos = 1
            elif ti == 30:
                puntos = 2  
            elif ti == 15:
                puntos = 3
            elif ti == 5:
                puntos = 5 
            else:
                puntos = 0         
        print('Puntos por jugador que mete gol: ', puntos)
    elif carta == 'M':
        #if correctos[int(carta_aux)] == pred[int(carta_aux)]:
        eq = [""]
        jornada = f'j{nj}'
        secuencia = []
        puntos = 0
        reg2 = Equipos.objects.all()
        for registro in reg2:
            secuencia = [item.strip() for item in getattr(registro, jornada).split(',')]
        for i in range(len(secuencia)):
            eq = secuencia[i].split(" vs ")
            print(eq[0], eq[1])
            pal1 = quitar_mayusculas_y_acentos(str(eq[0]))
            pal2 = quitar_mayusculas_y_acentos(str(eq[1]))
            if str(carta_aux) == str(pal1) or str(carta_aux) == str(pal2):
                print("Juego: ", i+1)
                print("Color: ", colo[i])
                if colo[i] == "lightgreen":
                    colo[i] = "goldenrod"
                    puntos = 2
        print("Secuencia: ", secuencia)
        #datos_procesados.append({
        #    'nombre': registro.eq,
        #})
        print("AUX: ", carta_aux)
        #colo[0] = 'goldenrod'
        print('Puntos por el Multiplicador: ', puntos)
    elif carta == 'MA':
        s1 = [item.strip() for item in pred_n.split(',')]
        s2 = [item.strip() for item in pred_j_n.split(',')]
        c = []
        for i in range(len(s1)):
            if s1[i] == s2[i]:
                puntos += 1
                c.append(i)
        for i in c:
            colo[i] = 'aquamarine'
        print('Puntos por el Marcador: ', puntos)
    else:
        print('No hay puntos extra')
        puntos = 0
    print(puntos, colo)
    return puntos, colo

def get_pts_car(carta, nj):
    jornada = f'j{nj}'
    if carta == 'NC':
        pts = 9
    elif carta == 'OD':
        pts = 8
    elif carta == 'T':
        pts = 7
    elif carta == 'J':
        pts = 6
    elif carta == 'DQ':
        pts = 5
    elif carta == 'M':
        pts = 4
    elif carta == 'OT':
        pts = 3
    elif carta == 'MA':
        pts = 2
    else:
        pts = 1
    return pts

def actualizar_puntos_cartas(nombre, pts, nj):
    if nombre != 'Resultados':
        jornada = f'j{nj}'

        # Actualizar los puntos en la tabla Jornadas
        jornada_obj = Puntos_cartas.objects.get(nombre=nombre)
        setattr(jornada_obj, jornada, pts)
        jornada_obj.save()
        print('SI')
def actualizar_puntos(nombre, nj, puntos, puntos_extra):
    if nombre != 'Resultados':
        jornada = f'j{nj}'
        print("8")
        # Actualizar los puntos en la tabla Jornadas
        jornada_obj = Jornadas.objects.get(nombre=nombre)
        print("9")
        setattr(jornada_obj, jornada, puntos)
        print("10")
        jornada_obj.save()
        print("11")
        print('SI')
        # Actualizar los puntos extras en la tabla PuntosExtra
        print("12")
        puntos_extra_obj = Puntos_extra.objects.get(nombre=nombre)
        print("13")
        setattr(puntos_extra_obj, jornada, puntos_extra)
        print("14")
        puntos_extra_obj.save()
        print('NO')
def actualizar_suma_puntos(nombre):
    if nombre != 'Resultados':
        # Obtener el objeto de jornadas
        jornadas_obj = Jornadas.objects.filter(nombre=nombre).first()

        if jornadas_obj:
            # Sumar los valores de las jornadas
            suma = sum([getattr(jornadas_obj, f'j{i}') for i in range(1, 18)])

            # Actualizar el campo suma_j en el objeto de jornadas
            jornadas_obj.suma_j = suma
            jornadas_obj.save()
def actualizar_suma_puntos_cartas(nombre):
    if nombre != 'Resultados':
        # Obtener el objeto de jornadas
        jornadas_obj = Puntos_cartas.objects.filter(nombre=nombre).first()
        jornadas_obj2 = Jornadas.objects.filter(nombre=nombre).first()

        if jornadas_obj:
            # Sumar los valores de las jornadas
            suma = sum([getattr(jornadas_obj, f'j{i}') for i in range(1, 18)])

            # Actualizar el campo suma_j en el objeto de jornadas
            jornadas_obj2.suma_j_c = suma
            jornadas_obj2.save()
def actualizar_colores(nombre, sec_colores, nj):
    if nombre != 'Resultados':
        # Obtener el objeto de colores
        colores_obj = Colores.objects.filter(nombre=nombre).first()

        if colores_obj:
            # Asignar el valor de sec_colores al campo correspondiente (j1, j2, etc.)
            setattr(colores_obj, f'j{nj}', sec_colores)
            colores_obj.save()
def actualizar_DQ_MA(nj, carta, nombre):
    registros = Prediccion.objects.filter(nombre=nombre)
    nombre_campo = f'pJ{nj}'
    print('Jugadores Disponibles')
    if carta == 'DQ':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                setattr(objeto, nombre_campo, 'XX, XX, XX, XX, XX, XX, XX, XX, XX, XX, XX')
                objeto.save()
    elif carta == 'MA':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                setattr(objeto, nombre_campo, '0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0, 0-0')
                objeto.save()
    elif carta == 'T':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Cartas_aux, nombre=nombre)
                nombre_campo = f'j{nj}'
                setattr(objeto, nombre_campo, "0-0:NA")
                objeto.save()
    
    elif carta == 'E':
        for r in registros:
            conteo_X = getattr(r, nombre_campo).split(', ').count('X')
            if conteo_X == 11:
                objeto = get_object_or_404(Cartas_aux, nombre=nombre)
                nombre_campo = f'j{nj}'
                setattr(objeto, nombre_campo, "- - - NA")
                objeto.save()
    
                
    """
    nombres = []
    if carta == 'DQ':
        print(nj, carta)
        for r in registros:
            if r.nombre != 'Resultados':
                #conteo_X = getattr(r, nombre_campo).split(', ').count('X')
                conteo_X = getattr(r, nombre_campo).split(', ').count('XX')
                print(conteo_X)
                if conteo_X == 11:

                    objeto = get_object_or_404(Prediccion, nombre=r.nombre)
                    print("SI")
                    setattr(objeto, nombre_campo, 'X, X, X, X, X, X, X, X, X, X, X')
                    objeto.save()
    """
    
def jornadas(request):

    if request.method == 'POST':

        jor = int(request.POST.get('opciones', 1))
        jugador_seleccionado = request.POST.get('jugador')

    else:

        jor = 1
        jugador_seleccionado = None
    if jor == 1 or jor == 2 or jor == 3:
        ############# ACTUALIZAR QUINIELAS #################
        Resultados = sec_resultados(jor)
        Resultados_s = marcador_a_secuencia(Resultados)
        Jugadores_con_gol = get_jugadores_gol(jor)
        Jugadores_con_gol = Jugadores_con_gol.split(', ')
        Estadisticas_juegos = get_estadisticas(jor)
        Estadisticas_juegos = Estadisticas_juegos.split(', ')
        tiempos = get_tiempo(jor)
        tiempos = tiempos.split(', ')
        partidos_I = get_PI(jor)
        partidos_I = partidos_I.split(', ')
        print(Resultados)
        print(Resultados_s)
        print(Jugadores_con_gol)
        for n in range(len(Jugadores)):
            print('XXXX', jor, Jugadores[n])
            carta = get_card(jor, Jugadores[n])
            print("1")
            actualizar_DQ_MA(jor, carta, Jugadores[n])
            print("2")
            carta_auxiliar = get_card_aux(jor, Jugadores[n])
            print("3")
            prediccion = get_predict(jor, Jugadores[n])
            #pts_cartas = get_pts_car(carta, jor)
            print("4")
            puntos, puntos_extra, sec_colores = get_points(Resultados, Resultados_s, carta, prediccion, carta_auxiliar, Jugadores_con_gol, tiempos, jor, Estadisticas_juegos, partidos_I)
            print("5")
            actualizar_puntos_cartas(Jugadores[n], puntos_extra, jor)
            print("6")
            actualizar_suma_puntos_cartas(Jugadores[n])
            print(Jugadores[n], carta, carta_auxiliar, prediccion)
            print(Jugadores[n], carta, carta_auxiliar, prediccion)
            print("7")
            print(puntos, puntos_extra, sec_colores)
            actualizar_puntos(Jugadores[n], jor, puntos, puntos_extra)
            print("SI")
            actualizar_suma_puntos(Jugadores[n])
            actualizar_colores(Jugadores[n], sec_colores, jor)
            print(puntos, puntos_extra)
            print("*"*50)
            
        ####################################################




        # =========================
        # CONSULTAS
        # =========================
        registros = list(Prediccion.objects.all())
        registros2 = list(Equipos.objects.all())
        reg_puntos = list(Jornadas.objects.all())
        reg_car = list(Cartas.objects.all())
        reg_car_aux = list(Cartas_aux.objects.all())
        reg_extra = list(Puntos_extra.objects.all())
        reg_c = list(Colores.objects.all())

        print("REGISTROS: ", registros)

        def crear_diccionario_puntos(registro_puntos, jor):
            puntos_por_nombre = {}
            for r in registro_puntos:
                puntos_por_nombre[r.nombre] = getattr(r, f'j{jor}')
            return puntos_por_nombre


        def ordenar_nombres(registros, registro_puntos, jor):
            puntos = crear_diccionario_puntos(registro_puntos, jor)

            registros_ordenados = sorted(
                registros,
                key=lambda r: (
                    r.nombre != "Resultados",   # False va primero
                    -puntos.get(r.nombre, 0)    # mayor a menor
                )
            )

            return registros_ordenados

        
        registros = ordenar_nombres(registros, reg_puntos, jor)

        print("R1")

        # =========================
        # ORDEN PERSONALIZADO
        # =========================
        def orden_personalizado(registro):
            if registro.nombre == "Resultados":
                return (0,)
            return (1, registro.nombre)
        
        print("REGISTROS: ", registros)
        #registros = sorted(registros, key=orden_personalizado)
        print("REGISTROS: ", registros)
        # =========================
        # MATCH POR NOMBRE
        # =========================
        def match_por_nombre(base, origen):
            salida = []
            for b in base:
                for o in origen:
                    if b.nombre == o.nombre:
                        salida.append(o)
            return salida

        reg_pts = match_por_nombre(registros, reg_puntos)
        reg_cartas = match_por_nombre(registros, reg_car)
        reg_cartas_aux = match_por_nombre(registros, reg_car_aux)
        reg_ep = match_por_nombre(registros, reg_extra)
        reg_colores = match_por_nombre(registros, reg_c)

        print("R2")

        # =========================
        # CAMPOS DINÁMICOS
        # =========================
        nombre_campo = f"pJ{jor}"
        nombre_campo2 = f"j{jor}"

        # =========================
        # PUNTOS EXTRA
        # =========================
        lis_exp = []
        for reg in reg_ep:
            valor = getattr(reg, nombre_campo2)
            if valor != 0:
                lis_exp.append({
                    "nombre": reg.nombre,
                    "puntos_extra": valor
                })

        print("R3")

        # =========================
        # COLUMNAS
        # =========================
        datos_procesados = []

        # Equipos (columnas fijas)
        for eq in registros2:
            datos_procesados.append({"nombre": eq.eq})

        # Jugadores
        for r in registros:
            datos_procesados.append({"nombre": r.nombre})

        # =========================
        # FILAS (sec_pred)
        # =========================
        sec_pred = []

        # Longitud base segura
        base_seq = getattr(registros2[0], nombre_campo2).split(",")
        total_filas = len(base_seq)

        print("R4")
        print(f"TF: {total_filas}")
        print(f"r2: {registros2}")
        print(f"r: {registros}")


        try:
            for i in range(total_filas):
                print(f"\nITERACIÓN i = {i}")
                fila = []

                # Equipos
                for eq in registros2:
                    seq = getattr(eq, nombre_campo2).split(",")
                    print(f"Equipos -> len(seq): {len(seq)}")

                    fila.append([seq[i].strip(), "lightgreen"])

                # Jugadores
                for idx, r in enumerate(registros):
                    seq = getattr(r, nombre_campo).split(",")
                    print(f"Jugadores -> len(seq): {len(seq)}")

                    if idx == 0:
                        color = "thistle"
                    elif idx - 1 < len(reg_colores):
                        col_seq = getattr(reg_colores[idx - 1], nombre_campo2).split(",")
                        print(f"Colores -> len(col_seq): {len(col_seq)}")
                        color = col_seq[i]
                    else:
                        color = "white"

                    fila.append([seq[i].strip(), color])

                sec_pred.append({"pred": fila})

        except Exception as e:
            print("Error:", e)
            traceback.print_exc()


        # =========================
        # FILAS EXTRA
        # =========================
        print("R5")
        def fila_extra(registros_extra):
            fila = []

            # EQUIPOS (vacíos)
            for _ in registros2:
                fila.append(["", "lightgoldenrodyellow"])

            # RESULTADOS (vacío, MUY IMPORTANTE)
            fila.append(["", "lightgoldenrodyellow"])

            # JUGADORES
            for r in registros_extra:
                fila.append([getattr(r, nombre_campo2), "lightgoldenrodyellow"])

            return {"pred": fila}


        sec_pred.append(fila_extra(reg_pts))
        sec_pred.append(fila_extra(reg_cartas))
        sec_pred.append(fila_extra(reg_cartas_aux))

        # =========================
        # PARTICIONADO EN BLOQUES
        # =========================
        BLOQUE = 6

        columnas = datos_procesados

        num_equipos = len(registros2)
        num_fijas = num_equipos + 1  # EQUIPOS + RESULTADOS

        fijas = columnas[:num_fijas]
        jugadores = columnas[num_fijas:]

        bloques = []

        print("R6")

        for i in range(0, len(jugadores), BLOQUE):
            bloque_cols = fijas + jugadores[i:i + BLOQUE]
            bloque_rows = []

            for fila in sec_pred:
                pred = fila["pred"]

                nueva_pred = (
                    pred[:num_fijas] +
                    pred[num_fijas + i : num_fijas + i + BLOQUE]
                )

                bloque_rows.append({"pred": nueva_pred})

            bloques.append({
                "columnas": bloque_cols,
                "filas": bloque_rows
            })


        # =========================
        # RENDER
        # =========================

        print("*******************+")
        print(bloques)
        print(jor)
        print(lis_exp)

        return render(
            request,
            "jornadas/jornadas.html",
            {
                "bloques": bloques,
                "page": "jornadas",
                "jornada_actual": jor,
                "puntos_extra": lis_exp
            }
        )

    else:
        print("Resultado:")
        print(sec_resultados(jor).split(", "))
        jugadores_fase_final = []
        prediccion_jugadores = []

        for n in range(len(Jugadores)):
            prediccion = get_predict(jor, Jugadores[n])
            jugadores_fase_final.append(Jugadores[n])
            prediccion_jugadores.append({
                'nombre': Jugadores[n],
                'prediccion': prediccion.split(", ")
            })

        # jugador seleccionado
        jugador_seleccionado = request.POST.get("jugador")

        prediccion_actual = None

        if jugador_seleccionado:
            for j in prediccion_jugadores:
                if j["nombre"] == jugador_seleccionado:
                    prediccion_actual = j["prediccion"]
                    break
        
        resultados_correctos = sec_resultados(jor).split(", ")

        puntos = 0
        colores = []

        if prediccion_actual:
            puntos, colores = comparar_predicciones(prediccion_actual, resultados_correctos)
            jornada_obj = Jornadas.objects.get(nombre=jugador_seleccionado)
            print("9")
            setattr(jornada_obj, "j4", puntos)
            print("10")
            jornada_obj.save()
            actualizar_suma_puntos(jugador_seleccionado)
        return render(
            request,
            "jornadas/fase_final.html",
            {
                "jornada_actual": jor,
                "jugadores_fase_final": jugadores_fase_final,
                "jugador_seleccionado": jugador_seleccionado,
                "prediccion_actual": prediccion_actual,
                "colores": colores,
                "puntos": puntos
            }
        )

def comparar_predicciones(prediccion, resultados):
    puntos = 0
    colores = []

    for i in range(len(prediccion)):

        # si aún no hay resultado oficial
        if resultados[i] == "NA":
            colores.append("gris")
            continue

        if prediccion[i] == resultados[i]:

            # asignar puntos según la fase
            if i == 15:
                puntos += 10

            elif i == 14 or i == 16:
                puntos += 5

            elif (12 <= i <= 13) or (17 <= i <= 18):
                puntos += 3

            elif (8 <= i <= 11) or (19 <= i <= 22):
                puntos += 2

            elif (0 <= i <= 7) or (23 <= i <= 30):
                puntos += 1

            colores.append("verde")
        else:
            colores.append("rojo")

    return puntos, colores