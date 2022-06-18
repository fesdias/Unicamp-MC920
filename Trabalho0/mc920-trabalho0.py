import cv2
import numpy as np

def negativo(name, img):

	img = 255 - img
	cv2.imwrite(name+'-negativo.png', img)

def espelhamentoVertical(name, img):

	img = img[::-1]
	cv2.imwrite(name+'-espelhamentoVertical.png', img)

def transformada(name, img):

	img = (100*img + 25500)/255
	cv2.imwrite(name+'-transformada.png', img)

def linhasPares(name, img):

	imgNew = img.copy()
	imgNew[::2] = img[::2, ::-1]
	cv2.imwrite(name+'-linhasPares.png', imgNew)

def reflexãoLinhas(name, img):

	rows, cols = img.shape
	rows = int(rows/2)
	img[rows::] = img[rows:0:-1]
	cv2.imwrite(name+'-reflexãoLinhas.png', img)

def ajusteDeBrilho(name, img):

	gama = input("Digite um valor para gama: ")
	gama = float(gama)

	img = ((img/255) ** (1/gama)) * 255

	cv2.imwrite(name+'-ajusteDeBrilho-'+str(gama)+'.png', img)

def planoDeBits(name, img):

	PBits = int(input("Digite o valor do plano desejado: "))
	PBits = 7 - PBits

	binary_repr_v = np.vectorize(np.binary_repr)
	img = binary_repr_v(img, 8)

	a, b = img.shape
	img2 = np.empty((a,b))

	for i in range(a):
		for j in range(b):

			if np.char.equal(img[i][j][PBits], '1'):
				img2[i][j] = 255
			else:
				img2[i][j] = 0

	cv2.imwrite(name+'-PlanoDeBits'+str(PBits-7)+'.png', img2)

def mosaico(name, img):

	ordem2 = [[(1, 1), (2, 2), (3, 0), (0, 2)],
	[(3, 3), (3, 3), (0, 0), (2, 0)],
	[(2, 3), (3, 1), (0, 1), (1, 2)],
	[(0, 3), (3, 2), (2, 1), (1, 0)]]

	ordem = [[6, 11, 13, 3], [8, 16, 1, 9], [12, 14, 2, 7], [4, 15, 10, 5]]

	M = img.shape[0]//4
	N = img.shape[1]//4
	tiles = [img[x:x+M,y:y+N] for x in range(0,img.shape[0],M) for y in range(0,img.shape[1],N)]

	imgNew = np.empty((512, 512))
	imgNew = imgNew.reshape(4, 4, 128, 128)

	for i in range(4):
		for j in range(4):
			imgNew[i][j] = tiles[(ordem[i][j]) - 1]

	imgNew = imgNew.swapaxes(1, 2)
	imgNew = imgNew.reshape(512, 512)

	cv2.imwrite(name+'-mosaico.png', imgNew)

def combinacaoDeImagens(name, img1, img2):

	m1 = float(input("Média ponderada imagem 1 (em decimal): "))
	m2 = float(input("Média ponderada imagem 2 (em decimal): "))

	img = img1 * m1 + img2 * m2
	cv2.imwrite(name+'-ImagemCombinada-img2='+str(m2)+'.png', img)

def main():
	
	c = int(input("Qual operação deseja fazer?\n1 - Transformação de Intensidade\n2 - Ajuste de Brilho\n3 - Planos de Bits\n4 - Mosaico\n5 - Combinação de Imagens\n"))
	
	nome = input("Nome da imagem: ")
	img = cv2.imread(nome, 0)
	img = np.array(img)
	
	if c == 1:
		negativo(nome, img)
		espelhamentoVertical(nome, img)
		transformada(nome, img)
		linhasPares(nome, img)
		reflexãoLinhas(nome, img)

	elif c == 2:
		ajusteDeBrilho(nome, img)

	elif c == 3:
		planoDeBits(nome, img)

	elif c == 4:
		mosaico(nome, img)

	elif c == 5:
		img2 = cv2.imread("butterfly.png", 0)
		img2 = np.array(img2)

		combinacaoDeImagens(nome, img, img2)

	else:
		print("Algo deu errado...")

if __name__ == '__main__':
	main()
