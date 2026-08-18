import qrcode

data = 'Hi its me prashamsa and i am learning python and machine learning. This seems so fun that i build something that can be seen. the day i build this qr code is 18 august 2026. Its 11:11 now one of the strongest number.'
img=qrcode.make(data)


# change the color and box of qr code 

qr=qrcode.QRCode(version=1,box_size=10,border=5)
qr.add_data(data)
qr.make(fit=True)
img=qr.make_image(fill_color='green',back_color='white')
img.save('/Users/prashamsaghimire/Desktop/Projects/myqrcode1.png')