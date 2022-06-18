import numpy as np
import cv2
import sys
import math

def pixel(x, y, angulo, escala):

	if angulo != 0:
		xn = x * math.cos(math.radians(angulo)) - y * math.sin(math.radians(angulo))
		yn = x * math.sin(math.radians(angulo)) + y * math.cos(math.radians(angulo))
		return (xn, yn)

	elif escala != 0:
		return (x/escala, y/escala)

def vizinho(img, imgOut, dimensao, angulo, escala):

	for i in range(dimensao):
		for j in range(dimensao):

			try:
				x, y = pixel(i, j, angulo, escala)
				imgOut[i, j] = img[round(x), round(y)]

			except IndexError:
				continue
			
def bilinear(img, imgOut, dimensao, angulo, escala):

	for i in range(dimensao):
		for j in range(dimensao):

			try:
				x, y = pixel(i, j, angulo, escala)
				dx = x - int(x)
				dy = y - int(y)

				x = round(x)
				y = round(y)

				imgOut[i, j]  = ((1 - dx) * (1 - dy) * img[x, y]) + (dx * (1 - dy) * img[x + 1, y]) + ((1 - dx) * dy * img[x, y + 1]) + (dx * dy * img[x + 1, y + 1])

			except IndexError:
				continue

def bicubica(img, imgOut, dimensao, angulo, escala):

	def P(t):
		if t > 0:
			return t
		else:
			return 0

	def R(s):

		return 1/6 * (pow(P(s + 2), 3) - 4*pow(P(s + 1), 3) + 6*pow(P(s), 3) - 4*pow(P(s -1), 3))

	for i in range(1, dimensao):
		for j in range(1, dimensao):

			try:
				x, y = pixel(i, j, angulo, escala)

				dx = x - int(x)
				dy = y - int(y)

				x = round(x)
				y = round(y)

				sum = 0

				for m in range(-1, 2):
					for n in range(-1, 2):
						sum = sum + img[x + m, y + n] * R(m - dx) * R(dy - n)

				imgOut[i, j] = sum

			except IndexError:
				continue

def lagrange(img, imgOut, dimensao, angulo, escala):

	def L(n, dx, img, x, y):

		return  (-dx * (dx - 1) * (dx - 2) * img[x -1, y + n - 2])/6 + ((dx + 1) * (dx - 1) * (dx - 2) * img[x, y + n - 2])/2 + ((-dx * (dx + 1) * (dx - 2) * img[x + 1, y + n - 2])/2) + ((dx * (dx + 1) * (dx - 1) * img[x + 2, y + n - 2])/6)
	
	for i in range(dimensao):
		for j in range(dimensao):

			try:
				x, y = pixel(i, j, angulo, escala)

				dx = x - int(x)
				dy = y - int(y)

				x = round(x)
				y = round(y)

				imgOut[i, j] = (-dy * (dy - 1) * (dy - 2) * L(1, dx, img, x, y))/6 + ((dy + 1) * (dy - 1) * (dy - 2) * L(2, dx, img, x, y))/2 + (-dy * (dy + 1) * (dy - 2) * L(3, dx, img, x, y))/2 + (dy * (dy + 1) * (dy - 1) * L(4, dx, img, x, y))/6

			except IndexError:
				continue

def main(angulo, escala, dimensao, metodo, imagem, output):
	
	img = cv2.imread(imagem, 0)
	imgOut = np.zeros((dimensao, dimensao))

	if metodo == "vizinho":
		vizinho(img, imgOut, dimensao, angulo, escala)

	elif metodo == "bilinear":
		bilinear(img, imgOut, dimensao, angulo, escala)

	elif metodo == "bicubica":
		bicubica(img, imgOut, dimensao, angulo, escala)

	elif metodo == "lagrange":
		lagrange(img, imgOut, dimensao, angulo, escala)

	else:
		print("Método não encontrado.")

	cv2.imwrite(output, imgOut)

if __name__ == '__main__':

	a = float(sys.argv[1])
	e = float(sys.argv[2])
	d = int(sys.argv[3])
	m = sys.argv[4]
	i = sys.argv[5]
	o = sys.argv[6]

	main(a, e, d, m, i, o)