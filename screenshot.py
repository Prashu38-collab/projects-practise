import pyscreenshot
# full screen 
image=pyscreenshot.grab()
image.show()
image.save("code.png")

# Capturing part of the screen -we use bbox for that
import pyscreenshot
image=pyscreenshot.grab(bbox=(10,10,400,400))
image.show()
image.save('bboxapplied_ss.png')