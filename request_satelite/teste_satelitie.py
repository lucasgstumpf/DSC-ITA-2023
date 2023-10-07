
import cv2
import numpy as np

# Carregue a imagem
imagem = cv2.imread("./images/20230501/S11635384_202305010100.jpg")

def calculaPixel():
    grauEntrada = 35
    grauSaida = -24
    somaGraus = (((abs(grauEntrada) + abs(grauSaida)))*7.8)+35
    return int(somaGraus)

def calculaPixe2l():
    grauEntrada = 115
    grauSaida = 48
    somaGraus = (((abs(grauEntrada) - abs(grauSaida)))*7.8)+22
    return int(somaGraus)

def retornaPixel():
    lat = -0.3653223142
    long = -0.7697224924

    latGraus = int(lat * 60)
    longGraus = int(long * 60)
    if(latGraus<0):
        print(f"entrou {latGraus}")
        somalat = (((abs(35) + abs(latGraus)))*7.8)+35
    else:
        somalat = (((abs(35) - abs(latGraus)))*7.8)+35
    
    somaLong = (((abs(115) - abs(longGraus)))*7.8)+22

    print(somalat)
    print(somaLong)

    return int(somalat), int(somaLong)


# Obtenha as dimensões originais da imagem
altura, largura = imagem.shape[:2]

# Redimensione a imagem para a metade do tamanho original
nova_altura = int(altura / 3)
nova_largura = int(largura / 3)
imagem_redimensionada = cv2.resize(imagem, (nova_largura, nova_altura))

print(nova_altura)
print(nova_largura)

# Defina a cor vermelha (BGR)
cor_vermelha = (0, 0, 255)

# Defina as coordenadas para o ponto (23, 50)
x1, y1 = 14, 35 
x2, y2 = 22, 737
#Distancia dos dois é 40

teste = calculaPixel()
teste2 = calculaPixe2l()

cv2.circle(imagem_redimensionada, (teste2,teste ), 10, (0, 255, 0), -1) # 

# Desenhe um círculo vermelho na imagem
cv2.circle(imagem_redimensionada, (x1, y1), 2, cor_vermelha, -1)

cv2.circle(imagem_redimensionada, (x1, 308), 2, (0, 255, 0), -1) # MARCA O 0

# Desenhe um círculo vermelho na imagem
cv2.circle(imagem_redimensionada, (x2, y2), 1, cor_vermelha, -1)

xteste, yteste = retornaPixel()
cv2.circle(imagem_redimensionada, (yteste, xteste), 3,cor_vermelha, -1)

# Defina a opacidade (alfa)
alfa = 0.5  # Um valor entre 0 (transparente) e 1 (opaco)

# Crie uma máscara para o retângulo
mascara = np.zeros_like(imagem)
cv2.rectangle(mascara, (x1, y1), (x2, y2), cor_vermelha, -1)

# Combine a imagem original com a máscara usando a função addWeighted
imagem_com_retangulo = cv2.addWeighted(imagem, 1, mascara, alfa, 0)

# Mostre a imagem com o ponto vermelho
cv2.imshow('Imagem com Ponto Vermelho', imagem_redimensionada)

# Aguarde até que uma tecla seja pressionada para fechar a imagem
cv2.waitKey(0)

# Feche a janela da imagem
cv2.destroyAllWindows()