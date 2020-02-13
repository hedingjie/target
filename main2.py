import cv2
import imutils
import numpy as np
import math
import time

def getMask(path):
    img=cv2.imread(path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retVal,img_bin=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel=np.ones((5,5),np.uint8)
    return img_bin

def getCenter(path):
    img=cv2.imread(path)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    retVal,img_bin=cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_bin_blur=cv2.GaussianBlur(img_bin,(3,3),1.8)
    cnts=cv2.findContours(img_bin_blur,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0] if imutils.is_cv2() else cnts[1]
    c=cnts[0]
    M=cv2.moments(c)
    cX=int(M["m10"]/M["m00"])
    cY=int(M["m01"]/M["m00"])
    print(str(cX)+" "+str(cY))
    return (cX,cY)

def preProcess(prePath,nextPath,mask):
    preImg=cv2.imread(prePath)
    nextImg=cv2.imread(nextPath)
    
    preGray=cv2.cvtColor(preImg,cv2.COLOR_BGR2GRAY)
    nextGray=cv2.cvtColor(nextImg, cv2.COLOR_BGR2GRAY)
    
    preGray=cv2.medianBlur(preGray,5)
    nextGray=cv2.medianBlur(nextGray,5)
    
    retVal1,preBin=cv2.threshold(preGray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    retVal2,nextBin=cv2.threshold(nextGray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    preEff=preBin+mask
    nextEff=nextBin+mask
    
    diff=nextEff-preEff
    diff=cv2.medianBlur(diff,5)
    
    return diff

def getPoint(diff,path,cX,cY):
    nextImg=cv2.imread(path)
    img_bin_blur=cv2.GaussianBlur(diff,(3,3),1.8)
    cnts=cv2.findContours(img_bin_blur,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=cnts[0] if imutils.is_cv2() else cnts[1]
    if(len(cnts)>0):
        c=cnts[0]
        M=cv2.moments(c)
        x=int(M["m10"]/M["m00"])
        y=int(M["m01"]/M["m00"])
        cv2.circle(nextImg,(cX,cY),2,(0,0,255),2)
        cv2.circle(nextImg,(x,y),2,(0,0,255),2)
        cv2.line(nextImg, (cX,cY), (x,y), (0,255,0), thickness=1)
        length=math.sqrt((x-cX)*(x-cX)+(y-cY)*(y-cY))
        cv2.putText(nextImg,str(length),(int((x+cX)/2),int((y+cY)/2)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        cv2.imwrite('result'+str(int(time.time()))+'.jpg',nextImg)
        time.sleep(1)
        if(0<length and length<=109):
            return 10
        elif(109<length and length<=210):
            return 9
        elif(210<length and length<=318):
            return 8
        elif(318<length and length<=410):
            return 7
        elif(410<length and length<=511):
            return 6
        elif(511<length and length<=759):
            return 5
        else:
            return 0
    else:
        return 0
    
    
    
    
if __name__=="__main__":
    mask=getMask('mask.jpg')
    cX,cY=getCenter('erosion.jpg')
    l=['p1.jpg','p2.jpg','p3.jpg','p4.jpg']
    for i in range(len(l)-1):
        diff=preProcess(l[i], l[i+1], mask)
        score=getPoint(diff, l[i+1], cX, cY)
        print 'score:'+str(score)