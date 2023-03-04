from PIL import Image
import os, sys

resize_dim = 512

path = r"H:\Downloads\Photos-001(1)\andrew_cropped\"
dest_path = r"H:\Downloads\Photos-001(1)\andrew_cropped"
dest_path = os.path.join(dest_path,str(resize_dim))
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((resize_dim,resize_dim), Image.ANTIALIAS)
            imResize.save(dest_path+'.png', 'png', quality=80)

resize()