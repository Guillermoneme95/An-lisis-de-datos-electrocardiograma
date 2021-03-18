import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import time
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks

def verificar_nombre(nombre):
  for i in nombre:
    if i.isnumeric() or i=='_' or i=='-':
      return False
    else:
      return True

#Ingreso de datos

nombre=input("Ingrese nombre completo del paciente: ")
while(verificar_nombre(nombre)==False):
  nombre=input("Ingrese nombre completo del paciente: ")

edad=input("Ingrese su edad")

while(edad.isnumeric()==False):
  edad = input("Ingrese su edad")

sexo=input("Ingrese M para masculino y F para femenino")
sexo=sexo.upper()

while(sexo != "M" and sexo != "F"):
  sexo = input("Ingrese M para masculino y F para femenino")
  sexo=sexo.upper()



archivo = pd.read_excel("electrocardiograma.xlsx")
#print(archivo)
data = archivo.to_dict("list")
cant = len(data["señal"])
x = []
y = []


for i in range(cant):
  x.append(data["tiempo"][i])
  y.append(data["señal"][i])

peaks,_= find_peaks(data["señal"],height=(0.4,2))

p=[]
t=[]

#Creacion de lista para marcar picos
for i in peaks:
  p.append(data["señal"][i])
  t.append(data["tiempo"][i])

T=t[1]-t[0]
BPM=(1/T)*60

print("Paciente:\n",nombre, "\nEdad\n",edad, "\nSexo\n", sexo )

if(BPM< 60):
  print("Se encuentra durmiendo")
  b=0
elif(BPM<100 and BPM>= 60):
  print("Se encuentra despierto sin realizar actividad fisica")
  b=1
elif(BPM<150 and BPM>= 100):
  print("Se encuentra despierto realizando actividad fisica leve")
  b=2
elif(BPM>=150):
  print("Se encuentra despierto realizando actividad fisica intensa")
  b=3

print("Las pulsaciones por minuto son :", "{0:.3f}".format(BPM))

frec=str(BPM)

file=open("ficha.txt","w")
file.write("Nombre del paciente: ")
file.write(nombre)
file.write("\n")
file.write("Edad: ")
file.write(edad)
file.write("\n")
file.write("Sexo: ")
file.write(sexo)
file.write("\n")
file.write("Frecuencia cardíaca: ")
file.write(frec)
file.write("\n")

if(b==0):
  file.write("Condición: Dormido")
if(b==1):
  file.write("Condición: Normal")
if(b==2):
  file.write("Condición: Actividad fisica leve")
if(b==3):
  file.write("Condición: Actividad fisica intensa")
file.close()

plt.figure(figsize=(12, 4))
plt.plot(x, y,label="Electrocardiograma")
plt.plot(t,p,"ro",label="picos") #marcado de picos dentro del grafico principal
#plt.title("Electrocardiograma")
plt.xticks(x[ : :200]) # Mostrar una de cada 200 fechas
plt.grid( axis='y' )   # Mostrar una grilla horizontal
plt.text(0,1,"Frecuencia Cardiaca" ,fontsize=10)
plt.text(1,1,frec,fontsize=10)
plt.legend() # Mostrar labels
plt.show()


