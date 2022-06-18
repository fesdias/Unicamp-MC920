import numpy as np
import sys
import cv2

#Gera código binário da mensagem
def textToASCII(text):

	msg = list(text)
	msgB = ''

	for c in msg:
		if len(c) == 1:
			m = ord(c)
			m = np.binary_repr(m, 8)
			msgB = msgB + m

	m = ord('*')
	m = np.binary_repr(m, 8)
	msgB = msgB + m

	return msgB

#Trocar bits
def trocarBit(n, msg, planoBits):

	planoBits = 7 - int(planoBits)

	#int to binary
	n = np.binary_repr(n, 8)
	n = list(n)

	#replace number
	n[int(planoBits)] = msg
	n = ''.join(n)
	n = int(n, 2)

	return n

#Insere código em um dos planos menos significativos
def msgInsertion(msg, img, planoBits):

	msg = list(msg)
	k = 0

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for h in range(3):

				if k < len(msg):
					img[i][j][h] = trocarBit(img[i][j][h], msg[k], planoBits) 
					k = k + 1

				else:
					return 1

#Gerar camada separada
def imgCamada(img, planoBits):

	planoBits = 7 - int(planoBits)
	novaImg = np.empty((img.shape[0], img.shape[1], 3))

	binary_repr_v = np.vectorize(np.binary_repr)
	img = binary_repr_v(img, 8)

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for k in range(3):

				if np.char.equal(img[i][j][k][int(planoBits)], '1'):
					novaImg[i][j][k] = 255

				else:
					novaImg[i][j][k] = 0

	return novaImg

def main(img, text, planoBits, output):

	#Converte a mensagem para ASCII
	msg = open(text, "r").read()
	msg = textToASCII(msg)

	img = cv2.imread(img)

	#Extrair camada sem mensagem
	camada = imgCamada(img, planoBits)
	cv2.imwrite("Camada - Sem mensagem - " + output, camada)

	#Inserir a mensagem na imagem
	msgInsertion(msg, img, planoBits)
	cv2.imwrite(output, img)

	#Extrair camada da mensagem
	camada = imgCamada(img, planoBits)
	cv2.imwrite("camada - Com mensagem - " + output, camada)

if __name__ == '__main__':

	img = sys.argv[1]
	text = sys.argv[2]
	planoBits = sys.argv[3]
	output = sys.argv[4]

	main(img, text, planoBits, output)
