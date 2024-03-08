import select
import requests
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox
from format_manager import *



headers = {'User-Agent': 'Mozilla/5.0'}
issueHref = ''
bookDownloads = []
compressedChapters = []


def scrapeCover(bookLink, session, selectedHost): 

    coverImage = ""
    imageRequest = session.get(bookLink, headers=headers)

   # Get coverImage from the website source code, xpath differs across different websites
    if selectedHost == "readallcomics.com":
        images = imageRequest.html.xpath('/html/body/center[3]/div/p/img')
        for image in images:
            coverImage = image.attrs['src']
    
    if selectedHost == "comicextra.me":
        images = imageRequest.html.xpath('/html/body/main/div/div/div/div[1]/div[1]/div[1]/div[1]/div/div[1]/div/img')
        for image in images:
            coverImage = image.attrs['src']


    if selectedHost == "mangakomi.io":  
        images = imageRequest.html.xpath('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[3]/div[1]/a/img')
        img_tag = images[0] 
        coverImage = img_tag.attrs['data-src']

    if selectedHost == "mangaread.org":
        images = imageRequest.html.xpath('/html/body/div[1]/div/div[2]/div/div[1]/div/div/div/div[3]/div[1]/a/img')
        img_tag = images[0] 
        coverImage = img_tag.attrs['src']


    return coverImage
    

            


def scrapeTitles(url, selectedHost, requestedBook):
        
        requestedBook = requestedBook.replace(" ", "-")
        bookTitles = {}

   # Retrieve all book titles that contain the same words as those entered by the user
        if selectedHost == "readallcomics.com":
            parsedTitles = url.html.xpath("/html/body/div[2]/div/div/ul/li/a")
            for child in parsedTitles:
             titleHref = child.attrs['href']
             titleName = child.text
             bookTitles[titleName] = titleHref

        if selectedHost == "comicextra.me":
            parsedTitles = url.html.find('div.cartoon-box a')
            for title in parsedTitles:
                if "https://comicextra.me/comic/" in title.attrs['href'] and title.text:
                    titleHref = title.attrs['href']
                    titleName = title.text
                    bookTitles[titleName] = titleHref

        if selectedHost == "mangakomi.io":
            links = url.html.find('.post-title a')
            for link in links:
                titleHref = link.attrs['href']
                titleName = link.text
                bookTitles[titleName] = titleHref

        
        if selectedHost == "mangaread.org":
            h3_elements = url.html.find('h3.h4 a')
            for h3 in h3_elements:
                titleHref = h3.attrs['href']
                titleName = h3.text
                bookTitles[titleName] = titleHref
        
        return bookTitles



def scrapeChapters(url, selectedHost):    
    bookChapters = {}

  # Get all chapters within a book
    if selectedHost == "readallcomics.com":
        parsedChapters = url.html.xpath("/html/body/center[3]/div/div[2]/ul/li/a")
        for chapter in parsedChapters:
             chapterName = chapter.text
             chapterHref =  chapter.attrs['href']
             bookChapters[chapterName] = chapterHref


    if selectedHost == "comicextra.me":
        issues = url.html.find('#list a')

        for issue in issues:
            chapterHref = issue.attrs['href']
            chapterName = issue.text
            bookChapters[chapterName] = chapterHref + "/full"
      

    if selectedHost == "mangakomi.io":
        chapters = url.html.find('li.wp-manga-chapter')
        for chapter in chapters:
             chapterHref = chapter.find('a', first=True).attrs['href']
             chapterName = chapter.find('a', first=True).text
             bookChapters[chapterName] = chapterHref 

    if selectedHost == "mangaread.org":
        chapters = url.html.find('.wp-manga-chapter')
        for chapter in chapters:
             chapterName = chapter.find('a', first=True).text
             chapterHref = chapter.find('a', first=True).attrs['href']
             bookChapters[chapterName] = chapterHref

    return bookChapters


        
    
          
def scrapePages(chapterLink, session, selectedHost, bookName, downloads, isMassDownload, directory, downloading, format, numberofLoops, cbzVerification, zipCompression):
     pageNum = 0 
     imageContents = []
     global compressedChapters
     chapterRequest = session.get(chapterLink, headers=headers)

  # If isMassDownload is True, we don't ask for the directory because the user has already chosen the directory in user_interface.py
     if isMassDownload == False:
        chosenDir = filedialog.askdirectory()
     else:
        chosenDir = directory
     try:
        if chosenDir != '' and chosenDir is not None:
            print(chapterLink)
            print(f'SELECTED HOST {selectedHost}')
            bookDownloads.append(bookName)
            downloading.configure(text="Downloading: ")
            downloads.configure(text=", ".join(list(set(bookDownloads))))

            if selectedHost == "readallcomics.com":                       
                images = chapterRequest.html.xpath('.//img')                     
                for pageNum, image in enumerate(images, 1):
                        if pageNum == 1:
                            continue
                        src = image.attrs['src']
                        pageResponse = requests.get(src)
                        print(f"{chosenDir}/#{pageNum}.jpg")
                        imageContents.append(pageResponse.content)


            if selectedHost == "comicextra.me":
                images = chapterRequest.html.find('div.chapter-container img')
                for image in images:
                    pageNum += 1
                    print(f"#{pageNum}: {src}")            
                    src = image.attrs['src']
                    pageResponse = requests.get(src) 
                    imageContents.append(pageResponse.content)


            if selectedHost == "mangakomi.io":
                images = chapterRequest.html.xpath('//img')  
                for image in images:
                        if 'data-src' in image.attrs:
                         src = image.attrs.get('data-src')
                         src = src.strip()
                         if 'cdn' in src:
                             pageNum += 1 
                             print(f"#{pageNum}: {src}")            
                             pageResponse = requests.get(src) 
                             imageContents.append(pageResponse.content)

            if selectedHost == "mangaread.org":
                images = chapterRequest.html.find('.page-break.no-gaps')
                for div in images:
                    pageNum += 1
                    image = div.find('img', first=True)
                    src = image.attrs['src']
                    print(f"#{pageNum}: {src}")            
                    pageResponse = requests.get(src) 
                    imageContents.append(pageResponse.content)


            if format == ".cbz":
                for page in imageContents:
                    compressedChapters.append(page)

                if cbzVerification == numberofLoops:
                    createCbz(compressedChapters, f"{chosenDir}/{bookName}.cbz")
                    if len(compressedChapters) > 0:
                        compressedChapters = []
 
            if format == ".zip":
                for page in imageContents:
                    compressedChapters.append(page)

                if cbzVerification == numberofLoops:
                    createZip(compressedChapters, f"{chosenDir}/{bookName}.zip", zipCompression)
                    if len(compressedChapters) > 0:
                        compressedChapters = []
 
            if format == ".jpg":
                createJpg(imageContents, chosenDir)

            bookDownloads.remove(bookName)
            downloads.configure(text=", ".join(list(set(bookDownloads))))
     except:
        messagebox.showerror("Error", "There was a problem while downloading. Make sure your directory path is correct.")

     if len(bookDownloads) == 0:
        downloading.configure(text="")
    
     
            
           

 
  

        