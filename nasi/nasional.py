import cv2
import numpy as np

def createBGR(frame):
    bgr = frame

    # Atas-Bawah
    bgr = cv2.line(bgr, (e,e), (w+e,e), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e,h+e), (w+e,h+e), color=putih, thickness=5)
    # Kanan-Kiri
    bgr = cv2.line(bgr, (e,e), (e,h+e), color=putih, thickness=5)
    bgr = cv2.line(bgr, (w+e,e), (w+e,h+e), color=putih, thickness=5)
    # Tengah
    bgr = cv2.line(bgr, (e+w12,e), (e+w12,h+e), color=putih, thickness=5)
    #Lingkaran
    bgr = cv2.circle(bgr, (e+w12,e+h12), 130, color=putih, thickness=5)

    # penalti kecil kiri
    bgr = cv2.line(bgr, (e,e+h12-150), (e+50,e+h12-150), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e,e+h12+150), (e+50,e+h12+150), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+50,e+h12-150), (e+50,e+h12+150), color=putih, thickness=5)

    # penalti kecil kanan
    bgr = cv2.line(bgr, (e+w,e+h12-150), (e+w-50,e+h12-150), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w,e+h12+150), (e+w-50,e+h12+150), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w-50,e+h12-150), (e+w-50,e+h12+150), color=putih, thickness=5)

    # penalti besar kiri
    bgr = cv2.line(bgr, (e,e+h12-250), (e+180,e+h12-250), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e,e+h12+250), (e+180,e+h12+250), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+180,e+h12-250), (e+180,e+h12+250), color=putih, thickness=5)

    # penalti besar kanan
    bgr = cv2.line(bgr, (e+w,e+h12-250), (e+w-180,e+h12-250), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w,e+h12+250), (e+w-180,e+h12+250), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w-180,e+h12-250), (e+w-180,e+h12+250), color=putih, thickness=5)

    # corner kiri atas
    bgr = cv2.ellipse(bgr, (e,e), (50,50), 0, 0, 90, color=putih, thickness=5)

    # corner kanan atas
    bgr = cv2.ellipse(bgr, (e+w,e), (50,50), 0, 90, 180, color=putih, thickness=5)

    # corner kiri bawah
    bgr = cv2.ellipse(bgr, (e,e+h), (50,50), 0, 0, -90, color=putih, thickness=5)

    # corner kanan bawah
    bgr = cv2.ellipse(bgr, (e+w,e+h), (50,50), 0, -90, -180, color=putih, thickness=5)

    # gawang kiri
    bgr = cv2.line(bgr, (e,e+h12-100), (e-50,e+h12-100), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e,e+h12+100), (e-50,e+h12+100), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e-50,e+h12-100), (e-50,e+h12+100), color=putih, thickness=5)

    # gawang kanan
    bgr = cv2.line(bgr, (e+w,e+h12-100), (e+w+50,e+h12-100), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w,e+h12+100), (e+w+50,e+h12+100), color=putih, thickness=5)
    bgr = cv2.line(bgr, (e+w+50,e+h12-100), (e+w+50,e+h12+100), color=putih, thickness=5)

    # Save bgr to .jpg
    cv2.imwrite('bgr.jpg', bgr)

    return bgr

def createDistanceMatrix(bgr):
    # Menggrayscale kan bgr
    gray_map = cv2.cvtColor(bgr_map,cv2.COLOR_BGR2GRAY)
    ret, bin_map = cv2.threshold(gray_map, 200, 255, cv2.THRESH_BINARY)

    # Membalik warna bin_map (putih ke hitam)
    bin_map = (255-bin_map)

    # Membuat matriks jarak
    dist = cv2.distanceTransform(
        bin_map, 
        distanceType=cv2.DIST_L2, 
        maskSize=3, 
        dstType=cv2.CV_8U
    )
    dist_normalized = cv2.normalize(
        dist, 
        None, 
        alpha=0, 
        beta=255, 
        norm_type=cv2.NORM_MINMAX, 
        dtype=cv2.CV_8U
    )

    # membalik matriks jarak (putih ke hitam)
    # Hasil terahir yang berupa Image
    dist_normalized = 255-dist_normalized

    # Save dist_normalized to .jpg
    cv2.imwrite('distMat.jpg', dist_normalized)

    # Perhitungan NUMPY
    data_bin = dist_normalized.flatten()
    data_bin_dob = data_bin.astype(np.double)

    # Save array of data_bin_dob to file.bin
    file=open("12x8WithGoal.bin","wb")
    array=bytearray(data_bin_dob)
    file.write(array)
    file.close()

    return dist_normalized

# ######################################################################## MAIN

w = 1200 +2
w12 = 600 +2
h = 800 +2
h12 = 400 +2
e = 100 +2
putih = (255,255,255)

bgr = np.zeros((800+2*100, 1200+2*100, 3), np.uint8)
bgr[:] = (0, 255, 0)

bgr_map = createBGR(bgr)
dm_map = createDistanceMatrix(bgr_map)

cv2.imshow("BGR", bgr_map)
cv2.imshow("Final", dm_map)

if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()