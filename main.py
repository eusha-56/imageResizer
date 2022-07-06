import math
import os
import re
from PIL import Image


def resizeStyleFun():
    resizeStyle = input(
        '''
Resize according to:
1. Width
2. Height
3. Percentage
4. File size

(Enter number. Press 0 to quit)\n
'''
    )

    while True:
        maxWidth = 0
        maxHeight = 0
        percentage = 100
        fileSize = 0

        if resizeStyle == '0':
            break

        elif resizeStyle == '1':
            maxWidth = input('Enter max width in pixel\n')

        elif resizeStyle == '2':
            maxHeight = input('Enter max height in pixel\n')

        elif resizeStyle == '3':
            percentage = input('Enter percentage from 1 to 100\n')

        elif resizeStyle == '4':
            fileSize = input('Enter approximate file size in MB\n')

        else:
            print('Enter NUMBER properly\n')
            return resizeStyleFun()

        rename = input(
            '''
Want to rename images?
If yes, enter name otherwise leave blank.\n
'''
        )
        return [rename, int(maxWidth), int(maxHeight), float(percentage), float(fileSize)*1024*1024]


def resize(originalName, newName, count, maxWidth, maxHeight, percentage, modifiedFileSize):

    img = Image.open('inputImages/'+originalName)
    originalFileSize = os.stat('inputImages/'+originalName).st_size
    width, height = img.size

    if modifiedFileSize == 0 or modifiedFileSize > originalFileSize:
        modifiedFileSize = originalFileSize

    if percentage > 100:
        percentage = 100

    area = width*height*percentage/100*modifiedFileSize/originalFileSize
    aspectRatio = width/height

    width = math.ceil(math.sqrt(area*aspectRatio))
    height = math.ceil(width/aspectRatio)

    if maxWidth == 0 or maxWidth > width:
        maxWidth = width
    if maxHeight == 0 or maxHeight > height:
        maxHeight = height
    if newName == '':
        newName = originalName.split('.')[0]
        count = ''
    else:
        count = str(count)+'_'

    img.thumbnail((maxWidth, maxHeight))

    newImageName = 'outputImages/'+count + \
        newName+'.'+originalName.split('.')[-1]
    print('saving ' + count + newName + '.' +
          originalName.split('.')[-1] + ' in outputImages/')
    print(width)
    print(height)
    img.save(newImageName, optimize=True, quality=85)


def main():

    files = os.listdir('inputImages')
    imges = list(filter(lambda x: re.search(
        '\.(jpe?g|png|gif|tiff)$', x), files))
    status = resizeStyleFun()

    for i in range(len(imges)):
        resize(imges[i], status[0], i+1, status[1],
               status[2], status[3], status[4])


main()


while True:
    if input('Successfully modified all images. Press enter to exit') == '':
        break
