import cv2

# fname = 'C:\MyProjects\Competition\Embedded_SW\ImageDatas/sample1.jpg'

# original = cv2.imread(fname, cv2.IMREAD_COLOR)


# cv2.imshow('Original', original)

# cv2.waitKey(0)  # 변수값만큼 사용자의 키입력 시간을 대기시킴
# cv2.destroyAllWindows()  # 프로그램 종료전 자원을 해제

path = "C:/MyProjects/Competition/Embedded_SW/ImageDatas/sampleVideo2.mp4"
cap = cv2.VideoCapture(0)
print("go!")

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('video', gray)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break;

    else:
        print('error!')


    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('show', gray)

cv2.waitKey(0)  # 변수값만큼 사용자의 키입력 시간을 대기시킴
cv2.destroyAllWindows()  # 프로그램 종료전 자원을 해제