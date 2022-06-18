import numpy as np
from skimage import filters
from skimage.exposure import rescale_intensity
import matplotlib.pyplot as plt
import cv2
import re

def save_histogram(image, nome):
	fig = plt.hist(image.ravel(), 256, [0, 256])
	plt.title("Histograma: " + nome + ".pgm ", fontsize = 16)
	plt.xlabel("Nível de cinza")
	plt.ylabel("Quantidade de Pixels")
	plt.tight_layout()
	plt.savefig(nome + "- Histograma.png")

def blackPixels(image, nome):
	black_pixels = np.count_nonzero(image == 0)
	total = np.size(image)
	print(nome + ": " + str(black_pixels/total))

def Global(image, nome):
	image[image <= 128] = 1
	image[image > 128] = 0

	image = image * 255
	cv2.imwrite(nome + ' - Global.png', image)

	blackPixels(image, 'Global')

def BernsenFunc(v):
	minimo = np.min(v)
	maximo = np.max(v)

	return (minimo + maximo)/2

def Bernsen(image, nome, n):
	
	img1 = filters.threshold_local(image, n, method='generic', param=BernsenFunc)
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - Bernsen ' + str(n) + '.png', img1)

	blackPixels(img1, 'Bernsen ' + str(n))

def Niblack(image, nome, n):
	
	img1 = filters.threshold_niblack(image, window_size=n, k=0.2)
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - Niblack ' + str(n) + '.png', img1)

	blackPixels(img1, 'Niblack ' + str(n))
	
def Sauvola(image, nome, n):
	
	img1 = filters.threshold_sauvola(image, window_size=n, k=0.5, r=128)
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - Sauvola ' + str(n) + '.png', img1)

	blackPixels(img1, 'Sauvola ' + str(n))

def MoreFunc(v):
	media = np.mean(v)
	desvioPadrao = np.std(v)
	k = 0.25
	R = 0.5
	p = 2
	q = 10

	return media * (1 + p * np.exp((-q) * media) + k * ((desvioPadrao/R) - 1))

def More(image, nome, n):

	image_rescale = rescale_intensity(image, in_range=(0, 1))

	img1 = filters.threshold_local(image_rescale, n, method='generic', param=MoreFunc)
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - More ' + str(n) + '.png', img1)

	blackPixels(img1, 'More ' + str(n))

def ContrasteFunc(v):

	minimo = np.min(v)
	maximo = np.max(v)
	
	x = v.shape
	x = x[0] // 2

	if (v[x] - minimo) > (maximo - v[x]):
		return 1
	else:
		return 0

def Contraste(image, nome, n):
	
	img1 = filters.threshold_local(image, n, method='generic', param=ContrasteFunc)
	img1 = img1 * 255
	cv2.imwrite(nome + ' - Contraste ' + str(n) + '.png', img1)

	blackPixels(img1, 'Contraste ' + str(n))

def Média(image, nome, n):
	
	img1 = filters.threshold_local(image, n, method='mean')
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - Média ' + str(n) + '.png', img1)

	blackPixels(img1, 'Média ' + str(n))

def Mediana(image, nome, n):

	img1 = filters.threshold_local(image, n, method='median')
	img1 = np.uint8(image > img1)*255
	cv2.imwrite(nome + ' - Mediana ' + str(n) + '.png', img1)

	blackPixels(img1, 'Mediana ' + str(n))

def main():
	
	nomeImg = input("Nome da imagem: ")
	img = cv2.imread(nomeImg, 0)
	imgGlobal = cv2.imread(nomeImg, 0)
	nome = re.sub(".pgm", "", nomeImg)
	n = int(input("Número da vizinhança: "))

	save_histogram(img, nome + "")

	Global(imgGlobal, nome)
	Bernsen(img, nome, n)
	Niblack(img, nome, n)
	Sauvola(img, nome, n)
	More(img, nome, n)
	Contraste(img, nome, n)
	Média(img, nome, n)
	Mediana(img, nome, n)

if __name__ == '__main__':
	main()