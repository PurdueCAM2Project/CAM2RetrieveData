import cv2
import sys
import time
import threading
threadList=[]
numCores = 7

streamQueue = []
def loadStreams():
    print ("Loading Streams")
    tick = time.time()
    inputFile = open("m3u8s.txt", 'r')
    for line in inputFile:
        opened=False
        while (not opened):
            if (len(threadList)<numCores):
                t = threading.Thread(target=addFeed, args=(line,))
                t.start()
                # print ("Thread Started")
                threadList.append(t)
                opened=True
            else:
                time.sleep(0.1)
    while (len(threadList) != 0):
        time.sleep(0.1)
    print ("Ellapsed time: " + str(time.time() - tick))
    downloadImages(streamQueue)

def addFeed(url):
    cap = cv2.VideoCapture(url)
    if (cap.isOpened()):
        streamQueue.append(cap)
    threadList.pop()
    # print ("Thread Released")

def downloadImages(streamQueue):
    raw_input("Press enter to download images")
    sys.stdout.flush()
    tick = time.time()
    imageData = []
    # framesSaved = 0
    breaker = False
    totalNumImages = 500
    print len(streamQueue)
    for x in range(len(streamQueue)):
        #
        opened = False
        while (not opened):
            if (len(threadList)<numCores):
                t = threading.Thread(target=saveFrame, args=(streamQueue[x], imageData, totalNumImages, len(streamQueue),))
                t.start()
                # print ("Thread Started")
                threadList.append(t)
                opened = True
            else:
                time.sleep(0.1)
    while (len(threadList) != 0):
        time.sleep(0.1)
        # while (True):
        #     try:
        #         saveFrame(streamQueue[x], imageData, totalNumImages, len(streamQueue))
        #     except Exception as e:
        #         print ("Breaking Exception: " + str(e))
                # breaker=True
                # break
            # if breaker:
            #     break
    print ("Ellapsed time: " + str(time.time()-tick))
    saveImages(imageData)


def saveFrame (stream, imageData, images, streams):
    for x in range(images/streams):
        image = stream.read()[1]
        imageData.append(image)
    # print ("Thread freed")
    threadList.pop()


def saveImages(imageData):
    raw_input("Press enter to save images")
    sys.stdout.flush()
    tick = time.time()
    fileNumber = 0
    # for frame in imageData:
    #
    #     fileName = ("z_img no" + str(fileNumber) + ".jpg")
    #     cv2.imwrite(fileName, frame)
    #     fileNumber += 1
    #

    for threadNo in range (numCores):
        opened = False
        while (not opened):
            if (len(threadList)<numCores):
                t = threading.Thread(target=saveImage, args=(imageData, threadNo,))
                t.start()
                # print ("Thread Started")
                threadList.append(t)
                opened = True
            else:
                time.sleep(0.1)

    # Sleep until all threads are released
    while (len(threadList) != 0):
        time.sleep(0.1)

    print ("Ellapsed time: " + str(time.time() - tick))


def saveImage(imageData, threadNo):
    for fileNumber in range (100):
        try:
            frame = imageData.pop()
            fileName = ("z_" + "threadNumber" + str(threadNo) + "iamgeNumber" + str(fileNumber) + ".jpg")
            cv2.imwrite(fileName, frame)
        except:
            break
    threadList.pop()


if __name__ == '__main__':
    print ("Starting")
    loadStreams()
    print ("Ending")


