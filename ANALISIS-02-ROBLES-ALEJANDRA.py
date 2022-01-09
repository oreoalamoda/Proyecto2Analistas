# Librerias necesarias
import pandas as pd
# creamos nuestro dataframame dado el archivo CSV
datos = pd.read_csv("synergy_logistics_database.csv")
#######################################
# register_id : id
# direction : exportación o importación
# origin : país de origen
# destination: país de destino
# year : año
# date : fecha
# product : producto
# transport_mode : metodo de transporte
# company_name : nombre de la compañia
# total_value :  costo total
# El primer paso sera dos nuevos dataframe de importaciones y exportaciones
# el cual solo considerara los paises de origen y de destino
exportaciones = datos[datos.direction.isin(["Exports"])]
importaciones = datos[datos.direction.isin(["Imports"])]
# para cada una de las listas filtramos los origenes y los destinos posibles
eorigen = exportaciones.origin.unique()
edestino = exportaciones.destination.unique()
iorigen = importaciones.origin.unique()
idestino = importaciones.destination.unique()

# concatenamos todos los origenes posibles a todos los destinos posibles
# guardamos cada uno de esos en una nueva lista
# reservamos un espacio en la lista 
eposibles = []
iposibles = []

for i in eorigen:
    for j in edestino:
        ea = "Origen:"+i + "--" +"Destino:"+ j
        eposibles.append(ea)
for i in iorigen:
    for j in idestino:
        ia = "Origen:"+i + "--" +"Destino:"+ j
        iposibles.append(ia)
# Una vez realizado esto tenemos todos los posibles viajes de importación y de exportacion

# lo sigueinte sera contar el numero de veces que se realiza  cada unos de estos viajes
# para eso  realizar esto filtraremos el dataframe a dos columnas
# y crearemos dos bucles anidados , el resultado sera una lista 
# la longitud de la lista sera igual a las ya antes creadas 
# y su valor indicara el numero de veces que se realizo alguno de esos viajes

# exportaciones
exp = []
for i in eorigen:
    for j in edestino:
        x = len(exportaciones[exportaciones.origin.isin([i]) & exportaciones.destination.isin([j])])
        exp.append(x)
#importaciones
imp = []
for i in iorigen:
    for j in idestino:
        x = len(importaciones[importaciones.origin.isin([i]) & importaciones.destination.isin([j])])
        imp.append(x)

# agregamos la lista concatenada y los resultados obtenidos a una nueva lista
totalexp = []
for i in range(0,len(exp)):
    x = [[exp[i]],[eposibles[i]]]
    totalexp.append(x)
totalimp = []
for i in range(0,len(imp)):
    y = [[imp[i]],[iposibles[i]]]
    totalimp.append(y)
# ordenamos ambas lista 
totalexp.sort()
totalimp.sort()

print("######################################################################")
print("LAS 10 RUTAS DE EXPORTACIONES MÁS POPULARES SON:")
for i in range(len(totalexp)-10,len(totalexp)):
    print(totalexp[i][1], "con un total de :",totalexp[i][0],"exportaciones")
print("######################################################################")
print("LAS 10 RUTAS DE IMPORTACIONES MÁS POPULARES SON:")
for i in range(len(totalimp)-10,len(totalimp)):
    print(totalimp[i][1], "con un total de :",totalimp[i][0],"exportaciones")
    
# Para saber si conviene esta estrategia contaremos el total de importaciones y exportaciones 
exp.sort()
esuma = 0
for i in range(len(totalexp)-10,len(totalexp)):
    x = int(exp[i])
    esuma = x + esuma
imp.sort()
isuma = 0
for i in range(len(totalimp)-10,len(totalimp)):
    x = int(imp[i])
    isuma = x + isuma

#ahora el total
eesuma = 0
for i in range(0,len(totalexp)):
    x = int(exp[i])
    eesuma = x + eesuma
iisuma = 0
for i in range(0,len(totalimp)):
    x = int(imp[i])
    iisuma = x + iisuma
print("######################################################################")
print("Las 10 rutas de exportación más populares generaron un total de:",esuma, "exportaciones")
print("Lo cual representa un :",(esuma/eesuma)*100,"% de las exportaciones totales")
print("######################################################################")
print("Las 10 rutas de importaciones más populares generaron un total de:",isuma, "importaciones")
print("Lo cual representa un :",(isuma/iisuma)*100,"% de las exportaciones totales")
print("######################################################################")
print("Por lo cual si valdria la pena implementar la estrategia para las importaciones peor no para las exportaciones")

# Medios de transporte más usados
# para cada una de las listas filtramos los diferentes medios de transportes posibles
emedio = exportaciones.transport_mode.unique()
imedio = importaciones.transport_mode.unique()

# calculamos cuando dinero genera cada medio de transporte
expmedio= []
for i in emedio:
    x = exportaciones[exportaciones.transport_mode.isin([i])]
    n =x.total_value.sum()
    s = [[n],[i]]
    expmedio.append(s)
impmedio= []
for i in imedio:
    x = importaciones[importaciones.transport_mode.isin([i])]
    n =x.total_value.sum()
    s = [[n],[i]]
    impmedio.append(s)
    
impmedio.sort()
expmedio.sort()

print("######################################################################")
print("3 MEDIOS DE TRANSPORTE MÁS USADOS Y SU VALOR GENERADO(EXPORTACIONES)")
for i in range(1,len(expmedio)):
    print("medio de transporte:",expmedio[i][1],", valor generado :",expmedio[i][0])
print("######################################################################")
print("3 MEDIOS DE TRANSPORTE MÁS USADOS Y SU VALOR GENERADO(IMPORTACIONES)")
for i in range(1,len(impmedio)):
    print("medio de transporte:",impmedio[i][1],", valor generado :",impmedio[i][0])
    
# paises que generan el 80% de las exportaciones e importaciones
# primero calculamos el valor total de las exportaciones e importaciones
valor = datos.total_value.sum()
# ahora calculamos todos los paises que aparecen en origen
origen = datos.origin.unique()

origen
# filtramos el total del valor generado por cada pais de origen
paises=[]
for i in origen:
    x = datos[datos.origin.isin([i])]
    n = x.total_value.sum()
    s = [n,i]
    paises.append(s)


# ordenamos los datos filtrados
paises.sort()
# invertimos el orden
paises.reverse()


# creamos un ciclo while que se detendra hasta que el valor total supere el 80%
print("PAISES CON EL 80% DEL VALOR DE LAS EXPORTACIONES E IMPORTACIONES")
porcentaje  = 0
i = 0
while porcentaje <= 80.0:
    x = (paises[i][0]/valor)*100
    porcentaje = x + porcentaje
    i=i+1
    print("Pais:",paises[i][1],", suma de porcentajes:",porcentaje)
    
    
