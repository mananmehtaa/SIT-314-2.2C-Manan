import cv2
import numpy as np 
import face_recognition
import os
from datetime import datetime
import pyrebase

path = 'photos'
images = []
classNames =[]
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

config = {
    "apiKey" : "VQYhjb1cwc0SHieJdd1dim0LTjctxRyZzIZqFBOT",
    "authDomain" : "attendance-api-62b03.firebase.com",
    "databaseURL" : "https://attendance-api-62b03-default-rtdb.firebaseio.com",
    "storageBucket" : "attendance-api-62b03.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

print("Send Data to firebase using raspberry pi")
print("---------------------------------")



#encodings :-> 
def findEncodings(imges):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList 


def markAttend(name):
    with open('attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  


encodeListKnown = findEncodings(images)
print('ENCODING COMPLETE')


cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS= cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurrent = face_recognition.face_locations(imgS)
    encodeCurrent = face_recognition.face_encodings(imgS ,faceCurrent)

    for encodeFace,faceLoc in zip(encodeCurrent,faceCurrent):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttend(name)
    cv2.imshow('WEBCAM',img)
    cv2.waitKey(1)







# faceloc = face_recognition.face_locations(imgSaksham)[0]
# encodeSaksham = face_recognition.face_encodings(imgSaksham)[0]
# cv2.rectangle(imgSaksham,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]) ,(255 , 0 ,255),2 )


# facelocT = face_recognition.face_locations(imgTest)[0]
# encodetest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(facelocT[3],facelocT[0]),(facelocT[1],facelocT[2]) ,(255 , 0 ,255),2 )

# results = face_recognition.compare_faces([encodeSaksham],encodetest)
# facedis = face_recognition.face_distance([encodeSaksham] ,encodetest)