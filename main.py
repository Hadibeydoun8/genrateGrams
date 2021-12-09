# Hadi Beydoun
# 12/18/2021
# Student Council CSV to Tag Generator


import csv
import os
import requests
import shutil
from PIL import Image, ImageFont, ImageDraw
from fpdf import FPDF

nameOfReceiver = []
nameOfGiver = []
teacher = []
imagePaths = []
amountOrdered = []

class PDF(FPDF):
    def imagex(self, x, y, image):
        self.set_xy(x, y)
        self.image(image, link='', type='')



def extractData(csvFile):
    with open(csvFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lineCount = 0
        for row in csv_reader:
            if lineCount == 0:
                lineCount = lineCount + 1
            else:
                nameOfReceiver.append(row[0])
                nameOfGiver.append(row[1])
                teacher.append(row[2])
                amountOrdered.append(int(row[3]))


def addTextToImages():
    index = 0
    deleteImages()
    makImagesDir()
    for _ in nameOfReceiver:
      amount = 0
      template = Image.open("template.png")
      font = ImageFont.truetype("Roboto-Black.ttf", 14)
      draw = ImageDraw.Draw(template)
      draw.text((50, 26), f"{nameOfReceiver[index].title()}", (40, 49, 52), font)
      draw.text((86, 46), f"{teacher[index].title()}", (40, 49, 52), font)
      draw.text((65, 66), f"{nameOfGiver[index].title()}", (40, 49, 52), font)
      template.save(f'.//images/image{index}_{amount}.png')
      imagePaths.append(f"image{index}.png")
      index = index + 1
      amount = amount + 1
      print("hi")


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
      amount = 0
      for x in range(1, amountOrdered[index]):
        pdf.imagex(xPos[xPosIndex], yPos[yPosIndex], f".//images/image{index}_{x}.png")
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
        amount = amount + 1
    pdf.output('output.pdf', 'F')


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


def getCSV():
    index = 1
    csvOptions = []
    print("Please pick one: \n1. Use existing file\n2. Pull a csv from google drive")
    choiceA = int(input())
    if choiceA == 1:
        for file in os.listdir(".//"):
            if file.endswith(".csv"):
                csvOptions.append(os.path.join(".//", file))
        if len(csvOptions) == 1:
            print(f"Using  {csvOptions[0]}")
            return csvOptions[0]
        else:
            for x in csvOptions:
                print(f"{index}. {x.replace('.//', '')}")
                index = index + 1
            choice = int(input())
        return csvOptions[choice - 1]
    elif choiceA == 2:
        sheetLink = input("please enter link to sheet: ")
        #sheetLink = input()
        response = requests.get(
            f'{sheetLink}&output=csv')
        assert response.status_code == 200, 'Wrong status code'
        print(response.content)

def rmFiles():
  for x in range(0, 37):
    os.remove(f".\images\\image{x}.png")


def rmPDF():
  try:
    os.remove("./output.pdf")
  except:
    print("File does not exist")


def main():
    print("What would you like to do?\n1. Generate only Images\n2. Generate a PDF\n3. Generate a PDF and Save Images\n4. Delete Images Directory\n5. Delete Images and Files")
    choice = int(input())
    if choice == 1:
        extractData(getCSV())
        addTextToImages()
    elif choice == 2:
        extractData(getCSV())
        addTextToImages()
        saveToPdf()
        deleteImages()
    elif choice == 3:
        extractData(getCSV())
        addTextToImages()
        saveToPdf()
    elif choice == 4:
        deleteImages()
    elif choice == 5:
      deleteImages()
      rmPDF()
    elif choice == 6:
        getCSV()
    elif choice == 7:
      rmFiles()

if __name__ == "__main__":
    main()