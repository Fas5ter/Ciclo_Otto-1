# Programa para hacer la grafica del Ciclo Otto
# Cristian Armando Larios Bravo

import matplotlib.pyplot as plt
import math


def cinematica_del_motor(bore, trazo,biela,cr,manivela_de_arranque,manivela_final):
	
	# Cinematica del motor
	
	#Parametros geometricos
	a=trazo/2
	R=biela/a

	#volumen
	v_s=(math.pi)/4*pow(bore,2)*trazo
	v_c=v_s/(cr-1)

	sc=math.radians(manivela_de_arranque)
	ec=math.radians(manivela_final)

	n_theta=100

	dtheta=(ec-sc)/(n_theta-1)

	V=[]

	for i in range(0,n_theta):
		theta=sc+(i*dtheta)
		terh1=0.5*(cr-1)
		term2=R+1 -math.cos(theta)
		term3=pow(pow(R,2) - pow(math.sin(theta),2),0.5)
		
		
		V.append((1+terh1*(term2-term3))*v_c)

	return V

#Parametros de entrada
p1=100000
t1=290
t3=1304
gamma=2

#Parametros geometricos
bore=0.1
trazo=0.1
biela=0.15
cr=12

#Volumen
v_s=(math.pi)/4*pow(bore,2)*trazo
v_c=v_s/(cr-1)
v1=v_s+v_c
v2=v_c

#Estado 2 p1v1^gamma=p2v2^gamma
p2=p1*pow(cr,gamma)

#p2v2/t2=p3v3/t3 | rhs=p2v2/t2  | t2=p2v2/rhs

rhs=p1*v1/t1
t2=p2*v2/rhs
compresion_V=cinematica_del_motor(bore,trazo,biela,cr,180,0)
# print(len(compresion_V))

constant=p1*pow(v1,gamma)
#compresion_P*compresion_V^gamma=constant

compresion_P=[]
for v in compresion_V:
	compresion_P.append(constant/pow(v,gamma))
#Estado3
v3=v2

#p3v3/t3=p2v2/t2  |   p2v2/t2=rhs | t2=p2v2/rhs
rhs=p2*v2/t2
p3=rhs*t3/v3

expansion_V=cinematica_del_motor(bore,trazo,biela,cr,0,180)

constant=p3*pow(v3,gamma)
#P_expanssion*expansion_V^gamma=constant

expansion_P=[]
for v in expansion_V:
	expansion_P.append(constant/pow(v,gamma))
#Estado4
v4=v1

p4=p3*pow((v3/v4),gamma)

t4=p4*v4/rhs


#Eficiencia termica
eff=1-1/(pow(cr,(gamma-1)))
eff=str(eff*100)


def graficar():
	#plot
	plt.plot([v2,v3],[p2,p3])
	plt.plot(compresion_V,compresion_P)
	plt.plot(expansion_V,expansion_P)
	plt.plot([v4,v1],[p4,p1])
	plt.xlabel('Volumen m3')
	plt.ylabel('Presion Pa')
	plt.title('Diagrama PV ')
	plt.grid(True)
	plt.show()

if __name__ == "main":
	print("Eficiencia termica ="+eff+"%")
	graficar()