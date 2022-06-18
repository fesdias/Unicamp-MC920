import cv2
import re
import numpy as np

def filterh1(img, nome):
	h = np.array([[0,0,-1,0,0],[0,-1,-2,-1,-0],[-1,-2,16,-2,-1],[0,-1,-2,-1,0],[0,0,-1,0,0]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h1.png', dst)
	print(dst)

def filterh2(img, nome):
	h = np.array([[1,4,6,4,1],[4,16,24,16,4],[6,24,36,24,6],[4,16,24,16,4],[1,4,6,4,1]])/256
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h2.png', dst)

def filterh3(img, nome):
	h = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h3.png', dst)

def filterh4(img, nome):
	h = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h4.png', dst)

def filterh3_h4(img, nome):
	h3 = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
	dst3 = cv2.filter2D(img, -1, h3)
	dst3 = np.array(dst3)
	dst3 = np.square(dst3)

	h4 = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])
	dst4 = cv2.filter2D(img, -1, h4)
	dst4 = np.array(dst4)
	dst4 = np.square(dst4)

	dst = np.add(dst3, dst4)
	dst = np.sqrt(dst)
	dst = dst.astype(int)
	
	cv2.imwrite(nome+'-h3_h4.png', dst)

def filterh5(img, nome):
	h = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h5.png', dst)

def filterh6(img, nome):
	h = np.ones((3,3),np.float32)/9
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h6.png', dst)

def filterh7(img, nome):
	h = np.array([[-1,-1,2],[-1,2,-1],[2,-1,-1]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h7.png', dst)

def filterh8(img, nome):
	h = np.array([[2,-1,-1],[-1,2,-1],[-1,-1,2]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h8.png', dst)

def filterh9(img, nome):
	h = np.array([[1,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0],[0,0,1,0,0,0,0,0,0],[0,0,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0],[0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,0,1]])/9
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h9.png', dst)

def filterh10(img, nome):
	h = np.array([[-1,-1,-1,-1,-1],[-1,2,2,2,-1],[-1,2,8,2,-1],[-1,2,2,2,-1],[-1,-1,-1,-1,-1]])/8
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h10.png', dst)

def filterh11(img, nome):
	h = np.array([[1, 1, 0],[1, 0,-1],[0,-1,-1]])
	dst = cv2.filter2D(img, -1, h)
	cv2.imwrite(nome+'-h11.png', dst)

def main():
	nome = input("Nome da imagem: ")
	img = cv2.imread(nome, 0)
	img = np.array(img)

	nome = re.sub(".png", "", nome)

	filterh1(img, nome)
	filterh2(img, nome)
	filterh3(img, nome)
	filterh4(img, nome)
	filterh5(img, nome)
	filterh6(img, nome)
	filterh7(img, nome)
	filterh8(img, nome)
	filterh9(img, nome)
	filterh10(img, nome)
	filterh11(img, nome)
	filterh3_h4(img, nome)

if __name__ == '__main__':
	main()