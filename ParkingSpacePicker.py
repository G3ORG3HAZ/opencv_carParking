import cv2
import pickle

width, height = 107, 48
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 0.8
color = (255, 255, 255)
thickness = 1

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open('CarParkPos', 'wb') as f:
        pickle.dump(posList, f)


while True:
    img = cv2.imread('carParkImg.png')
    for index,pos in enumerate(posList):
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
        # Calculate the position to place the number text
        text_pos = (pos[0] + 10, pos[1] + height - 10)  # Adjust the position as needed

        # Draw the number attribute on the image
        cv2.putText(img, str(index), text_pos, font, font_scale, color, thickness)


    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
