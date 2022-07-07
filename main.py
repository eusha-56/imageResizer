import math
import os
import re
from PIL import Image
import keyboard


def resizeInfo():

    folderPath = urlFilter(input('Enter Folder URL:\n'))

    if folderPath == 0:
        print('Enter Folder URL properly')
        return resizeInfo()

    if os.path.exists(folderPath) == False:
        print('URL is not valid')
        return resizeInfo()

    resizeStyle = input('Resize according to:\n1. Width\n2. Height\n3. Percentage\n4. File size\n')

    while True:
        maxWidth = 0
        maxHeight = 0
        percentage = 100
        fileSize = 0

        if resizeStyle == '1':
            maxWidth = input('Enter max width in pixel\n')

        elif resizeStyle == '2':
            maxHeight = input('Enter max height in pixel\n')

        elif resizeStyle == '3':
            percentage = input('Enter percentage from 1 to 100\n')

        elif resizeStyle == '4':
            fileSize = input('Enter approximate file size in MB\n')

        else:
            print('Enter NUMBER properly\n')
            return resizeInfo()

        newName = input('Want to rename images?\nIf yes, enter name otherwise leave blank.\n')

        return [folderPath, newName, int(maxWidth), int(maxHeight), float(percentage), float(fileSize)*10**6]


def resize(url, outputPath, originalName, newName, count, maxWidth, maxHeight, percentage, modifiedFileSize):

    img = Image.open(url + '\\' + originalName)

    originalFileSize = os.stat(url + '\\' + originalName).st_size
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


    imageExtension = originalName.split('.')[-1]

    if newName == '':
        newName = originalName
    else:
        newName = f'{newName}_{count}.{imageExtension}'


    img.thumbnail((maxWidth, maxHeight))

    print(f"saving '{newName}' in '{outputPath}'")

    img.save(f"{outputPath}\\{newName}", optimize=True, quality=90)



def urlFilter(url):
    url = list(url)
    if len(url) == 0 : return 0
    if url[0] == "'" and url[-1] == "'":
        url = url[1:-1]
    elif url[0] == '"' and url[-1] == '"':
        url = url[1:-1]
    return ''.join(url)


def pathFinder(parent, child, count=0):

    childExtension = ''

    if count > 0:
        childExtension = f'({str(count)})'

    path = os.path.join(parent, child + childExtension)
    if os.path.exists(path):
        return pathFinder(parent, child, count + 1)
    else:
        return path


def main():
    
    print('Press Enter to start the program\nPress ESC to close the program')
    
    while True:    
        if keyboard.is_pressed('esc'):
            quit()
        if keyboard.is_pressed('enter'):
            input()
            break

    info = resizeInfo()

    files = os.listdir(info[0])

    imges = list(filter(lambda x: re.search('\.(jpe?g|png|gif|tiff)$', x), files))

    outputPath = pathFinder(info[0], 'Resized_Images')

    os.mkdir(outputPath)

    for i in range(len(imges)):
        resize(info[0], outputPath, imges[i], info[1], i+1, info[2], info[3], info[4], info[5])

    print('\nSuccessfully modified all images\nPress esc to exit\nPress Enter to run the program')



main()


while True:
    if keyboard.is_pressed('esc'):
        print('\nProgram finished')
        quit()
    if keyboard.is_pressed('enter'):
        input()
        print('\nStarting program\n')
        main()
