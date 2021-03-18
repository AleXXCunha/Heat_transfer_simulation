from matplotlib import cm
import matplotlib.pyplot as plt
import math
import numpy as np

no = 100 #Número de nós na malha decidido arbitrariamente
t = 0
tempo = 10000 #Tempo decidido arbitrariamente
intervalos = 10000 #Número de divisões dentro do período analisado decidido arbitrariamente
anterior = np.zeros((no,no), float) 
atual = np.copy(anterior)
#Criei duas matrizes para determinar a temperatura em um nó em um momento anterior e em um momento atual.

dt = (tempo/intervalos) #Definindo o passo de tempo 
dx = (3/no) #Definindo o incremento infinitesimal em x

#Para a definição do alfa vou considerar que o material do objeto é de cobre
alfa = 117/(10**6) #Difusividade térmica do cobre = 117
fourier = (alfa*dt)/(dx**2)

#Região de código utilizado para análises de domínios de cálculo
def gerar_graf(no, matriz):     #Iremos gerar 5 gráficos de uma vez afim de se economizar tempo e esforço
    altura_analisada = [round(no/2), round(no/1.2)]
    comprimento_analisado = [round(no/6), round(no/2), round(no/1.2)]
    alturas = (1.5,2.5)     #Pontos em Y definidos arbitrariamente
    comprimentos = (0.5,1.5,3)      #Pontos em X definidos arbitrariamente
    intervalo = np.linspace(0,3, num = no)
    atual = matriz

    for x in range(len(comprimento_analisado)):     #Gerando os gráficos analisando os pontos com base no eixo x
        temperaturas = np.array(atual[:,comprimento_analisado[x]])
        plt.plot(intervalo,temperaturas)
        plt.title('Perfil de Temperatura em X = ' + (str)(comprimentos[x]))
        plt.xlabel('Altura Y (m)')
        plt.ylabel('Temperatura (K)')
        plt.savefig('X_'+ (str)(comprimentos[x]) + '.png')
        plt.close('all')

    for y in range(len(altura_analisada)):      #Gerando os gráficos analisando os pontos com base no eixo y
        temperaturas = np.array(atual[altura_analisada[y],:])
        plt.plot(intervalo,temperaturas)
        plt.title('Perfil de Temperatura em Y = ' + (str)(alturas[y]))
        plt.xlabel('Comprimento X (m)')
        plt.ylabel('Temperatura (K)')
        plt.savefig('Y_'+ (str)(alturas[y]) + '.png')
        plt.close('all')


#Aqui plotamos o gráfico da distribuição de temperatura na figura
def gerar_distr():
    plt.figure()
    plt.title('Distribuição de Temperatura ' + (str)(no) + 'X' + (str)(no))
    plt.imshow(np.flipud(atual), cmap = 'twilight_shifted', interpolation = 'none', extent=[0, 3, 0, 3])
    colorbar = plt.colorbar()
    plt.xlabel('Distância horizontal (m)')
    plt.ylabel('Distância vertical (m)')
    plt.show()

#Aqui iremos determinar as condições de contorno na figura

#Primeiro, determinamos nas paredes verticais da figura
for parede_vert in range(no):
    anterior[parede_vert][0] = 300.00
    if(parede_vert < (round(no/3) - 1)):
        anterior[parede_vert][(round(no/3) - 1)] = 250.00
    elif(parede_vert > (round(no/3) - 1) and parede_vert <(2*round(no/3) - 1)):
        anterior[parede_vert][(no - 1)] = 40.00
    else:
        anterior[parede_vert][(round(no/3) - 1)] = 250.00
    

#Em seguida, determinamos nas paredes horizontais da figura
for parede_hz in range(no):
    if(parede_hz < (round(no/3) - 1)):
        anterior[0][parede_hz] = 275.00
        anterior[(no - 1)][parede_hz] = 275.00
    else:
        anterior[(round(no/3) - 1)][parede_hz] = 200.00
        anterior[(2*round(no/3) - 1)][parede_hz] = 100.00

 
#Determinando agora as temperaturas em cada nó da malha       
while t < 100000:    #Loop temporal
    for y in range(no):     #Loop no eixo y
        for x in range(no):     #Loop no eixo x
            if (atual[round(no/2), round(no/3)] > 160): 
                t = 100001       #Condição de parada: quando este nó atingir 160º o corpo se encontra próximo do regime estacionário
            elif(x == 0):
                atual[y, x] = 300.00
            elif((y == 0 or y == (no - 1)) and x <= (round(no/3) - 1)):
                atual[y, x] = 275.00
            elif(y == (round(no/3) - 1) and x > (round(no/3) - 1)):
                atual[y, x] = 200.00
            elif(y == (2*round(no/3) - 1) and x > (round(no/3) - 1)):
                atual[y, x] = 100.00
            elif(x == (round(no/3) - 1) and (y <= (round(no/3) - 1) or y >= (2*round(no/3) - 1))):
                atual[y, x] = 250.00
            elif(x == (no - 1) and (round(no/3) - 1)<y<(2*round(no/3)  - 1)):
                atual[y, x] = 40.00
            elif((x > (round(no/3) - 1) and y < (round(no/3) - 1)) or (y > (2*round(no/3) - 1) and x > (round(no/3) - 1))):
                atual[y, x] = 0.00
            else:
                atual[y, x] = fourier * (anterior[y+1, x] + anterior[y-1, x] + anterior[y, x+1] + anterior[y, x-1]) + (1-(4*fourier))*anterior[y, x]
                anterior[y, x] = atual[y, x]

    t = t+1
    plt.imsave('./imagens/' + str(t) + '.png', np.flipud(atual), cmap='twilight_shifted')
    #Aqui estamos salvando as imagens em uma pasta "Imagens" para cada instante afim de juntá-las posteriormente e gerar um vídeo

#Gerando os perfis de temperatura para 5 pontos diferentes do corpo analisado 
gerar_graf(no, atual)

#Gerando a imagem da distribuição de temperatura
gerar_distr()