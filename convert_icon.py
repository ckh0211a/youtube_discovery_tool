from PIL import Image
import os

img_path = r'C:\Users\GONI0\.gemini\antigravity\brain\7392050c-5e45-40b2-bf2f-52099f2ab5ab\app_icon_1774694216932.png'
img = Image.open(img_path)
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
img.save('app_icon.ico', sizes=icon_sizes)
print("Icon conversion successful!")
