import cv2

img = cv2.imread(input("Input a QR file to scan: ")) # Such as: "H:\Downloads\Rickrolling_QR_code.png"

qcd = cv2.QRCodeDetector()
retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(img)

print(decoded_info)
