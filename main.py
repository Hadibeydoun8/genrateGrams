# Hadi Beydoun
# 12/18/2021
# Student Council CSV to Tag Generator


import csv
import os
import shutil
from PIL import Image, ImageFont, ImageDraw
from fpdf import FPDF

nameOfReceiver = []
nameOfGiver = []
teacher = []
imagePaths = []


class PDF(FPDF):
    def imagex(self, x, y, image):
        self.set_xy(x, y)
        self.image(image, link='', type='')


def extractData():
    with open('cvs.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lineCount = 0
        for row in csv_reader:
            if lineCount == 0:
                lineCount = lineCount + 1
            else:
                nameOfReceiver.append(row[0])
                nameOfGiver.append(row[1])
                teacher.append(row[2])


def addTextToImages():
    index = 0
    for _ in nameOfReceiver:
        template = Image.open("template.png")
        font = ImageFont.truetype("Roboto-Black.ttf", 14)
        draw = ImageDraw.Draw(template)
        draw.text((50, 26), f"{nameOfReceiver[index]}", (40, 49, 52), font)
        draw.text((86, 46), f"{teacher[index]}", (40, 49, 52), font)
        draw.text((65, 66), f"{nameOfGiver[index]}", (40, 49, 52), font)
        template.save(f'.\\images\\image{index}.png')
        imagePaths.append(f"image{index}.png")
        index = index + 1


def saveToPdf():
    index = 0
    xPos = [0, 107.95]
    yPos = [0, 63, 126, 189]
    pdf = PDF(orientation='P', unit='mm', format='Letter')
    pdf.add_page()

    xPosIndex = 0
    yPosIndex = 0
    changeX = True
    for _ in nameOfReceiver:
        pdf.imagex(xPos[xPosIndex], yPos[yPosIndex], f".//images//image{index}.png")
        if changeX:
            xPosIndex = xPosIndex + 1
            changeX = False
        else:
            xPosIndex = xPosIndex - 1
            yPosIndex = yPosIndex + 1
            changeX = True
        index = index + 1
        if (index % 8) == 0 and index < len(nameOfReceiver):
            pdf.add_page()
            xPosIndex = 0
            yPosIndex = 0
    pdf.output('test.pdf', 'F')


def deleteImages():
    try:
        shutil.rmtree(".//images")
    except FileNotFoundError:
        print("Folder does not exist")


def makImagesDir():
    try:
        os.mkdir(".//images")
    except FileExistsError:
        print("Folder exists")


def main():
    print("What would you like to do?\n1. Generate only Images\n2. Generate a PDF\n3. Generate a PDF and Save Images\n4. Delete Images Directory")
    choice = int(input())
    if choice == 1:
        makImagesDir()
        extractData()
        addTextToImages()
    elif choice == 2:
        makImagesDir()
        extractData()
        addTextToImages()
        saveToPdf()
        deleteImages()
    elif choice == 3:
        makImagesDir()
        extractData()
        addTextToImages()
        saveToPdf()
    elif choice == 4:
        deleteImages()


if __name__ == "__main__":
    main()
