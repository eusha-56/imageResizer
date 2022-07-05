import math
import os
from PIL import Image

def resizeStyleFun():
    resizeStyle = input(
'''
Resize according to:
1. Width
2. Height
3. Percentage

(Enter number. Press 0 to quit)\n
'''
    )
    

    while True:
        maxWidth = 0
        maxHeight = 0
        percentage = 100

        if resizeStyle == '0':
            break

        elif resizeStyle == '1':
            maxWidth = input('Enter max width in pixel\n')

        elif resizeStyle == '2':
            maxHeight = input('Enter max height in pixel\n')

        elif resizeStyle == '3':
            percentage = input('Enter percentage from 1 to 100\n')

        else:
            print('Enter NUMBER properly\n')
            return resizeStyleFun()
        rename = input(
'''
Want to rename images?
If yes, enter name otherwise leave blank.\n
'''
            )
        return [rename,int(maxWidth),int(maxHeight),int(percentage)]


def resize(originalName, newName, count, maxWidth, maxHeight, percentage):
    img = Image.open('inputImages/'+originalName)
    width, height = img.size
    area = width*height*percentage/100
    aspectRatio = width/height
    width = math.floor(math.sqrt(area*aspectRatio))
    height = math.floor(width/aspectRatio)
    
    if maxWidth == 0:
        maxWidth = width
    if maxHeight == 0:
        maxHeight = height
    if newName == '':
        newName = originalName.split('.')[0]
        count = ''
    else:
        count = str(count)+'_'

    img.thumbnail((maxWidth,maxHeight))
    newImageName = 'outputImages/'+count+newName+'.'+originalName.split('.')[-1]
    print('saving '+newImageName)
    img.save(newImageName)


def main():
    imges =  os.listdir('inputImages')
    status = resizeStyleFun()
    print(status)

    for i in range(len(imges)):
        resize(imges[i], status[0], i+1, status[1], status[2], status[3])



main()

while True:
    if input('Successfully modified all images. Press enter to exit') == '':
        break

