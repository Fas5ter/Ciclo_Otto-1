# Cristian Armando Larios Bravo
# Haciendo y probando codigos chidos
# Ciclo Otto en Python

'''
Programar, en el lenguaje de su elección, la solucón para el siguiente problema.

Un ciclo ideal Otto tiene una relacion de compresión de 8. El inicio del proceso de compresion de aire está
a 100kPa y 17ºC, en el proceso de adicion de calor se agregan 800 kJ/kg a volumen constante. 

Determine:
a) Temperatura máxima.
b) Presión máxima.
c) Eficiencia térmica.
d) Presión media efectiva.

Para el código se puede usar calor especifico variable o constantes. Debe decidir.
Datos de entrada:
· Relación de compresión.
· Temperatura y presión al inicio del proceso de compresión.
· Calor añadido.
'''

import pandas as pd
from DiagramaPV import graficar

# Funciones
def celsius_kelvin() -> float:
    celsius = float(input("Introduce la temperatura: "))
    return celsius+273.15

def fahrenheit_kelvin() -> float:
    celsius = float(input("Introduce la temperatura: "))
    return ((celsius-32) / 1.8) + 273

def kelvin() -> float:
    kelvin = float(input("Introduce la temperatura: "))
    return kelvin

if __name__ == "__main__":
    # Datos de entrada
    opc = 0

    p1 = float(input("Introduce el valor inicio del proceso de compresion de aire: "))
    while (opc!=1 or opc!=2 or opc!=3):
        opc = int(input("¿Que tipo de temperatura es?\n1)Celsius.\n2)Fahrenheit.\n3)Kelvin\nDigite la opcion: "))
        if opc==1 or opc==2 or opc==3:
            break
    match opc:
        case 1: 
            t1 = celsius_kelvin()
        case 2: 
            t1 = fahrenheit_kelvin()
        case 3: 
            t1 = kelvin()
        case default: 
            print("Opcion invalida")
    r = float(input("Introduce la relacion de compresion: ")) 
    # vc = float(input("Ingresa cuanto se agrega en el proceso de adicion de calor a volumen constante: "))
    rc = float(input("Introduce la relacion de corte: "))
    R = 0.287
    print("\nDatos de entrada")
    print(f"p1 = {p1}")
    print(f"t1 = {t1}")
    print(f"r = {r}")
    # print(f"vc = {vc}")
    print(f"rc = {rc}")


    # Datos de la tabla de propiedades de gas ideal del aire
    datos = pd.read_excel('HTI - Ciclo Otto Larios\gas_ideal_propiedades.xlsx', header=0)
    t = datos['T']      # Temperatura
    h = datos['h']      #
    Pr = datos['Pr']    #
    u = datos['u']      #
    vr = datos['vr']    #
    s = datos['s']      #

    ''' Proceso 1-2 '''
    # Estado 1
    print("\nEstado 1")
    # Calcular Pr1, h1, Vr1
    for i in range(0,121,1):
        if round(t1) >= t[120]:     # Por si llega al limite de temperatura de la tabla
            pr1 = Pr[120]
            u1 = u[120]
            vr1 = vr[120]
            break

        if round(t1) >= t[i] and round(t1) < t[i+1]:
            pr1 = Pr[i]
            u1 = u[i]
            vr1 = vr[i]
            break
    
    print(f'Pr1 = {pr1}')
    print(f'u1 = {u1}')
    print(f'Vr1 = {vr1}')

    # Estado 2
    print("\nEstado 2")
    # Calculamos Vr2
    # v = vr1/vr2   =>  vr2 = vr1/r
    # r = vr1 / vr2
    vr2 = vr1 / r
    # Calculamos Pr2
    print(f"Vr2 = {vr2}")
    for i in range(0,121,1):
        if vr2 <= vr[i] and vr2 > vr[i+1]:
            taux1_abajo = t[i]
            taux2_arriba = t[i+1]

            vraux1_abajo = vr[i]
            vraux2_arriba = vr[i+1]

            haux1_abajo = h[i]
            haux2_arriba = h[i+1]

            praux1_abajo = Pr[i]
            praux2_arriba = Pr[i+1]

            # y = y0 + ((y1-y0) / (x1-x0)) * (x - x0)
            t2 = taux2_arriba + ( (taux1_abajo - taux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr2 - vraux2_arriba)
            h2 = haux2_arriba + ( (haux1_abajo - haux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr2 - vraux2_arriba)
            pr2 = praux2_arriba + ( (praux1_abajo - praux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr2 - vraux2_arriba)
            break

    print(f"t2 = {t2}")
    print(f"h2 = {h2}")
    print(f"Pr2 = {pr2}")
    # Dado que es una presion icentropica
    # p2 = p1 * (pr2/pr1)
    p2 = p1 * (pr2 / pr1)
    print(f"p2 = {p2}")

    ''' Proceso 2-3 '''
    print("\nEstado 3")
    # Estado 3      p3 = p2
    p3 = p2
    print(f"p3 = {p3}")
    # rc = v3/v2
    # Por la ec. de los gases ideales:
    # (p2*v2) / T2 = (p3*v3) / t3 => t3 = t2(p3/p2)(v3/v2)

    t3 = t2 * rc
    print(f"t3 = {t3}")

    for i in range(0, 121, 1):
        if t3 >= t[i] and t3 < t[i+1]:
            praux1_abajo = Pr[i]
            praux2_arriba = Pr[i+1]

            haux1_abajo = h[i]
            haux2_arriba = h[i+1]

            vraux1_abajo = vr[i]
            vraux2_arriba = vr[i+1]

            taux1_abajo = t[i]
            taux2_arriba = t[i+1]

            pr3 = praux2_arriba + ( (praux1_abajo - praux2_arriba) / (taux1_abajo - taux2_arriba) ) * (t3 - taux2_arriba)
            vr3 = vraux2_arriba + ( (vraux1_abajo - vraux2_arriba) / (taux1_abajo - taux2_arriba) ) * (t3 - taux2_arriba)
            h3 = haux2_arriba + ( (haux1_abajo - haux2_arriba) / (taux1_abajo - taux2_arriba) ) * (t3 - taux2_arriba)

            
            break

    print(f"h3 = {h3}")
    print(f"Pr3 = {pr3}")
    print(f"Vr3 = {vr3}")

    ''' Proceso 3-4 '''
    # Estado 4
    print("\nEstado 4")
    # vr4/vr4 = v4/v3
    # vr4 = vr3(r/rc)

    vr4 = vr3 * (r / rc)
    print(f"Vr4 = {vr4}")

    for i in range(0, 121, 1):
        if vr4 <= vr[i] and vr4 > vr[i+1]:
            praux1_abajo = Pr[i]
            praux2_arriba = Pr[i+1]

            uaux1_abajo = u[i]
            uaux2_arriba = u[i+1]

            vraux1_abajo = vr[i]
            vraux2_arriba = vr[i+1]

            taux1_abajo = t[i]
            taux2_arriba = t[i+1]

            t4 = taux2_arriba + ( (taux1_abajo - taux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr4 - vraux2_arriba)
            pr4 = praux2_arriba + ( (praux1_abajo - praux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr4 - vraux2_arriba)
            u4 = uaux2_arriba + ( (uaux1_abajo - uaux2_arriba) / (vraux1_abajo - vraux2_arriba) ) * (vr4 - vraux2_arriba)

            
            break
    
    print(f"t4 = {t4}")
    print(f"Pr4 = {pr4}")
    print(f"u4 = {u4}")

    # p4 = p3(pr4 / pr3)
    p4 = p3 * (pr4 / pr3)
    print(f"p4 = {p4}")
    # t3 = La temperatura despues del proceso de adicion de calor
    print(f"\n\n######  TEMPERATURA DESPUES DEL PROCESO DE ADICION DE CALOR = {t3}  ######")

    """ 
    a) Temperatura Maxima
    Comparar todas las temperaturas
    """
    lista_temperaturas = [t1, t2, t3, t4]
    temp_mayor = 0
    nums = 4

    for i in range(nums):
        num = lista_temperaturas[i]
        if num > temp_mayor:
            temp_mayor = num



    """ 
    b) Presión Maxima
    Comparar todas las presiones
    """
    if h2 > h3:
        pMayor = h2
    else:
        pMayor = h3

    '''
    c) Eficiencia energetica
    nDiesel = Wnet / qsum  
    · qsum = h3 - h2
    · qcad = u1 - u4
    '''
    qsum = h3 -h2
    qcad = u1 - u4
    wneto = qsum + qcad
    nDiesel = wneto / qsum
    print(f"qsum = {qsum}")
    print(f"qcad = {qcad}")
    print(f"Wneto = {wneto}")

    
    """ 
    d) Presion media efectiva
    pme = wneto / (v1-v2)
    v1 = (R*T) / P
    R = constante universal (0.287)
    v2 = (R * T2) / P2
    """

    v1 = (R * t1) / p1
    v2 = (R * t2) / p2
    v3 = v2
    v4 = v1
    pme = wneto / (v1-v2)
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v3 = {v3}")
    print(f"v4 = {v4}")
    
    

    print("\n\n~~~~~~~~~~~~~~~~ RESULTADOS ~~~~~~~~~~~~~~~~")
    print(f"a) Temperatura máxima = {temp_mayor}ºK")
    print(f"b) Presion Máxima = {pMayor}kJ/kg")
    print(f"c) Eficiencia Térmica: nDiesel = {nDiesel}")
    print(f"d) Presión Media Efectiva: PME = {pme}kPa")

    # Diagrama de PV
    graficar()