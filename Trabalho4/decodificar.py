import numpy as np
import sys
import cv2

def selecionarPlano(n, planoBits):

	planoBits = 7 - int(planoBits)

	#int to binary
	n = np.binary_repr(n, 8)

	#Trocar o bit
	n = list(n)
	n = n[int(planoBits)]

	return str(n)

def decodificador(img, planoBits):

	msg = []
	caracter = ''

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for k in range(3):

				if caracter == '00101010':
					msg = ''.join(msg)
					msg = int(msg, 2)
					msg = msg.to_bytes((msg.bit_length() + 7) // 8, 'big').decode('utf-8', 'surrogatepass')
					return msg

				if len(caracter) == 8:
					msg.append(caracter)
					caracter = selecionarPlano(img[i][j][k], planoBits)

				else:
					caracter = caracter + selecionarPlano(img[i][j][k], planoBits)

def main(img, planoBits, output):

	#Receber a mensagem na imagem
	img = cv2.imread(img)
	msg = decodificador(img, planoBits)

	#Gerar mensagem
	f = open(output, "w")
	f.write(msg)
	f.close()

if __name__ == '__main__':

	img = sys.argv[1]
	planoBits = sys.argv[2]
	output = sys.argv[3]

	main(img, planoBits, output)
