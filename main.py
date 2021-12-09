# Hadi Beydoun
# 12/18/2021
# Student Council CSV to Tag Generator


import csv
from PIL import Image, ImageFont, ImageDraw

nameOfReceiver = []
nameOfGiver = []
teacher = []
imagePaths = []


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
        for x in nameOfReceiver:
            print(x)


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
    pass


def main():
    extractData()
    addTextToImages()


if __name__ == "__main__":
    main()
