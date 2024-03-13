from cProfile import label
from csv import reader
from io import BytesIO
from textwrap import fill
from tkinter import BOTTOM, LEFT, RIGHT, TOP
import customtkinter
from PIL import Image
from numpy import imag


fgColor = "#581845"
headers = {'User-Agent': 'Mozilla/5.0'}
currentPage = 0
readingPage = 1
pageLabelText = "Page {} of {}"
pageSize = (0 , 0)

leftButtonImage = customtkinter.CTkImage(light_image=Image.open("./resources/left.png"),
                                            dark_image=Image.open("./resources/left.png"))
rightButtonImage = customtkinter.CTkImage(light_image=Image.open("./resources/left.png"),
                                                dark_image=Image.open("./resources/right.png"))
zoomInButtomImage = customtkinter.CTkImage(light_image=Image.open("./resources/zoom in.png"),
                                                dark_image=Image.open("./resources/zoom in.png"))
zoomOutButtomImage = customtkinter.CTkImage(light_image=Image.open("./resources/zoom out.png"),
                                                dark_image=Image.open("./resources/zoom out.png"))
                                      

def createReaderWindow(imageContent):
    global readingPage
    readerWindow = customtkinter.CTkToplevel()
    readerWindow.geometry("600x600")
    readerWindow.wm_iconbitmap("visual/bookscraper-icon.ico")
    readerWindow.title("Book Scraper")
    labelFont = customtkinter.CTkFont(family="Arial Rounded MT Bold", size=12)
    readingPage = 1


    controlFrame = customtkinter.CTkFrame(readerWindow)
    controlFrame.pack(side=BOTTOM)

    pageNumberDisplay = customtkinter.CTkLabel(controlFrame, width=70, height=40, 
                                               text=pageLabelText.format("1", len(imageContent)), 
                                               fg_color=fgColor,
                                               font=labelFont)
    pageNumberDisplay.pack(side=LEFT)

    pageFrame = customtkinter.CTkScrollableFrame(readerWindow)
    pageFrame.pack(anchor='center', fill="both", expand=True)
    pageLabel = customtkinter.CTkLabel(pageFrame, text="", image=None)
    pageLabel.pack(anchor='center', fill="x")

    leftButton = customtkinter.CTkButton(controlFrame, width=70, height=40, 
                                          image=leftButtonImage,
                                          text="", 
                                          fg_color=fgColor,
                                          command= lambda pages = imageContent, 
                                          pageLabel = pageLabel,
                                          pageNumberDisplay = pageNumberDisplay: getLastPage(pages, pageLabel, pageNumberDisplay))
    leftButton.pack(side=LEFT)

    rightButton = customtkinter.CTkButton(controlFrame, width=70, height=40, 
                                          image=rightButtonImage,
                                          text="", 
                                          fg_color=fgColor,
                                          command= lambda pages = imageContent, 
                                          pageLabel = pageLabel,
                                          pageNumberDisplay = pageNumberDisplay: getNextPage(pages, pageLabel, pageNumberDisplay))
    rightButton.pack(side=RIGHT)

    zoomInButton = customtkinter.CTkButton(controlFrame, width=70, height=40, 
                                           image=zoomInButtomImage, 
                                           text="", 
                                           fg_color=fgColor,
                                           command= lambda pageLabel = pageLabel, pages = imageContent: zoomIn(pageLabel, pages))
    zoomInButton.pack(side=LEFT)

    zoomOutButton = customtkinter.CTkButton(controlFrame, width=70, height=40, 
                                            image=zoomOutButtomImage, 
                                            text="",
                                            fg_color=fgColor,
                                            command= lambda pageLabel = pageLabel, pages= imageContent: zoomOut(pageLabel, pages))
    zoomOutButton.pack(side=RIGHT)


    pageDisplay(imageContent, pageLabel)


def getNextPage(pages, pageLabel, pageNumberDisplay):
    global currentPage
    global readingPage
    if currentPage == len(pages) - 1:
        pass
    else:
        pageLabel.configure(image=(customtkinter.CTkImage(light_image=Image.open(BytesIO(pages[currentPage+1])),
                              dark_image=Image.open(BytesIO(pages[currentPage+1])),
                              size=pageSize)))
        currentPage += 1
        readingPage += 1
        pageNumberDisplay.configure(text=pageLabelText.format(readingPage, len(pages)))
        print(currentPage)
    
def getLastPage(pages, pageLabel, pageNumberDisplay):
    global currentPage
    global readingPage
    if currentPage == 0:
        pass
    else:
        pageLabel.configure(image=(customtkinter.CTkImage(light_image=Image.open(BytesIO(pages[currentPage-1])),
                              dark_image=Image.open(BytesIO(pages[currentPage-1])),
                              size=pageSize)))
        currentPage -= 1
        readingPage -= 1
        pageNumberDisplay.configure(text=pageLabelText.format(readingPage, len(pages)))
        print(currentPage)



def zoomIn(pageLabel, pages):
    global pageSize
    pageSize = (pageSize[0]*1.5, pageSize[1]*1.5)
    pageLabel.configure(image=(customtkinter.CTkImage(light_image=Image.open(BytesIO(pages[currentPage])),
                                                      dark_image=Image.open(BytesIO(pages[currentPage])),
                                                      size=pageSize)))

def zoomOut(pageLabel, pages):
    global pageSize
    pageSize = (pageSize[0]/1.5, pageSize[1]/1.5)
    pageLabel.configure(image=(customtkinter.CTkImage(light_image=Image.open(BytesIO(pages[currentPage])),
                                                      dark_image=Image.open(BytesIO(pages[currentPage])),
                                                      size=pageSize)))

def pageDisplay(imageContent, pageLabel):
    global currentPage
    global pageSize
    firstPage = Image.open(BytesIO(imageContent[0]))
    pageSize = ((firstPage.width / 2), (firstPage.height / 2))
    currentPage = 0
    pageLabel.configure(image=(customtkinter.CTkImage(light_image=firstPage,
                                                     dark_image=firstPage,
                                                     size=pageSize)))

    














