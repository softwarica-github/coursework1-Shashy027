from PIL import Image
import sys

def pix_val(image):

	im = Image.open((image), 'r')
	width, height = im.size
	pixel_values = list(im.getdata())
	return pixel_values
	#lendata = len('data')
	#imdata = iter(pixel_values)
	#datalist = ['01100100', '01100001', '01110100', '01100001']

def genData(data):
		# list of binary codes
		# of given data
		newd = []
		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data,img):
	w = newimg.size[0]
	#print(w)
	(x, y) = (0, 0)

	for pixel in modPix(pix_val(img), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode():
	img = input("Enter image name(with extension) : ")
	try:
		image = Image.open(img, 'r')

	except FileNotFoundError:
		print("Image not found try again")
		sys.exit()

	data = input("Enter message to be encoded : ")
	if (len(data) == 0):
		raise ValueError('message is empty')

	newimg = image.copy()
	encode_enc(newimg, data, img)

	new_img_name = input("Enter the name of new image(save as .png extension only) : ")
	newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Decode the data in the image
def decode():
	img = input("Enter image name(with extension) : ")
	try:
		image = Image.open(img, 'r')

	except FileNotFoundError:
		print("Image not found try again")
		sys.exit()

	data = ''
	imgdata = iter(pix_val(img))

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
									 imgdata.__next__()[:3] +
									 imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

# Main Function
def main():
	a = input(" Welcome to stegno script \n""1. Encode\n2. Decode\n""Enter the option number: ")
	if (a == '1'):
		encode()

	elif (a == '2'):
		print("Decoded Word : " + decode())
	else:
		print('Invalid option try again')
		sys.exit()


print('''
 $$$$$$\  $$\                           $$\                                $$\     
$$  __$$\ $$ |                          $$ |                               $$ |    
$$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$$\ $$$$$$$\  $$\  $$\  $$\  $$$$$$\ $$$$$$\   
\$$$$$$\  $$  __$$\  \____$$\ $$  _____|$$  __$$\ $$ | $$ | $$ | \____$$\\_$$  _|  
 \____$$\ $$ |  $$ | $$$$$$$ |\$$$$$$\  $$ |  $$ |$$ | $$ | $$ | $$$$$$$ | $$ |    
$$\   $$ |$$ |  $$ |$$  __$$ | \____$$\ $$ |  $$ |$$ | $$ | $$ |$$  __$$ | $$ |$$\ 
\$$$$$$  |$$ |  $$ |\$$$$$$$ |$$$$$$$  |$$ |  $$ |\$$$$$\$$$$  |\$$$$$$$ | \$$$$  |
 \______/ \__|  \__| \_______|\_______/ \__|  \__| \_____\____/  \_______|  \____/ 
                                                                                   
                                                                                   
                                                       *Made by Shashwat Pandey 2023*                                                                                                                                                                            
				   
		''')
main()
while True:
	
	answer = input('Do you want to try another time?(y or n): ')

	if answer == 'y' or answer == 'Y':
	   main()

	elif answer == 'n':
	   print('Thank you for trying out this tool exiting........ ')
	   sys.exit() 


	else:
	   print('Invalid answer quitting.....') 
	   sys.exit()
