import numpy as np
import cv2
import re

def aplication(x, y, img, mat):

	b, g, r = img[x, y]

	new_r = np.round(r/255)*255
	new_g = np.round(g/255)*255
	new_b = np.round(b/255)*255

	img[x,y] = np.uint8([new_b, new_g, new_r])

	erroR = r - new_r
	erroG = g - new_g
	erroB = b - new_b

	for i, j, erro in mat:

		img[x + i][y + j][0] += int(erroB * erro)
		img[x + i][y + j][1] += int(erroG * erro)
		img[x + i][y + j][2] += int(erroR * erro)
	
	return img

def dithering(img, ymax, xmax, mat, s):

	w, h, d = np.shape(img)
	for y in range(0, h - ymax):

		if y % 2 == 1 and s == 1:
			for x in range(w - (xmax + 1), xmax + 1, -1):
				img = aplication(x, y, img, mat)

		else:
			for x in range(xmax, w - xmax):
				img = aplication(x, y, img, mat)

	return img

def apply(img, y, x, mat, nome):

	imgA = dithering(img.copy(), y, x, mat, 0)
	cv2.imwrite(nome + ' A.png', imgA)

	imgB = dithering(img.copy(), y, x, mat, 1)
	cv2.imwrite(nome + ' B.png', imgB)

def imgGeneratorRGB(images):

	#Técnicas
	floyde = [[1, 0, 7/16],[-1, 1, 3/16], [0, 1, 5/16], [1, 1, 1/16]]

	arce = [[2, 0, 32/200],
	[-3, 1, 12/200], [-1, 1, 26/200], [1, 1, 30/200], [3, 1, 16/200],
	[-2, 2, 12/200], [0, 2, 26/200], [2, 2, 12/200],
	[-3, 3, 5/200],[-1, 3, 12/200], [1, 3, 12/200], [3, 3, 5/200]]

	burkes = [[1, 0, 8/32], [2, 1, 4/32],
	[-2, 1, 2/32], [-1, 1, 4/32], [0, 1, 8/32], [1, 1, 4/32], [2, 1, 2/32]]

	sierra = [[1, 0, 5/32], [2, 0, 3/32],
	[-2, 1, 2/32], [-1, 1, 4/32], [0, 1, 5/32], [1, 1, 4/32], [2, 1, 2/32],
	[-1, 2, 2/32], [0, 2, 3/32], [1, 2, 2/32]]

	stucki = [[1, 0, 8/42], [2, 0, 4/42],
	[-2, 1, 2/42], [-1, 1, 4/42], [0, 1, 8/42], [1, 1, 4/42], [2, 1, 2/42],
	[-2, 2, 1/42], [-1, 2, 2/42], [0, 2, 4/42], [1, 2, 2/42], [2, 2, 1/42]]

	jjn = [[1, 0, 7/48], [2, 0, 5/48],
	[-2, 1, 3/48], [-1, 1, 5/48], [0, 1, 7/48], [1, 1, 5/48], [2, 1, 3/48],
	[-2, 2, 1/48], [-1, 2, 3/48], [0, 2, 5/48], [1, 2, 3/48], [2, 2, 1/48]]

	for nomeImg in images:

		img = cv2.imread(nomeImg)
		nome = re.sub(".png", "", nomeImg)

		print("Trabalhando na img", nome)

		#Floyde e Steinger
		apply(img, 1, 1, floyde, nome + ' - floyde')
		print("Floyde e Steinger pronto!")

		#Arce e Steverson
		apply(img, 3, 3, arce, nome + ' - Arce')
		print("Arce e Steverson pronto!")

		#Burkes
		apply(img, 1, 2, burkes, nome + ' - Burkes')
		print("Burkes pronto!")

		#Sierra
		apply(img, 2, 2, sierra, nome + ' - Sierra')
		print("Sierra pronto!")

		#Stucki
		apply(img, 2, 2, stucki, nome + ' - Stucki')
		print("Stucki pronto!")

		#JJN
		apply(img, 2, 2, jjn, nome + ' - JJN')
		print("JJN pronto!")

def main():
	
	images = ['baboon.png', 'watch.png']
	imgGeneratorRGB(images)

if __name__ == '__main__':
	main()