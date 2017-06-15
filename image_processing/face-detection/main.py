import cv2

def read(image_path, cascade_path):
    """

    :param image_path:      The path to the image we want to read
    :param cascade_path:    The path to the cascade classifier XML file
    :return:                the image and classifier objects
    """

    image = cv2.imread(image_path, 0)

    face_cascade = cv2.CascadeClassifier(cascade_path)

    return image, face_cascade

def get_faces(cascade, image):
    """

    :param cascade: The cascade classifier object used to detect faces
    :param image:   The image object we want to detect faces in
    :return:        an 2D array with 1 row for each face and 4 columns

                            - C1 = X coordinate of the upper-left corner of the face
                            - C2 = Y coordinate of the upper-left corner of the face
                            - C3 = the width of the face
                            - C4 = the height of the face
    """

    faces = cascade.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5
    )

    return faces


def draw_rectangle(image, faces):
    """

    :param image:           The image object
    :param faces:           The 2D array representing the faces we identified in the image
    :return:                -
    """

    img = image

    for x, y, w, h in faces:
        img = cv2.rectangle(
            img,
            (x,y),
            (x+w, y+h),
            (0, 255, 0),
            3
        )

    resized_img = cv2.resize(img, (int(img.shape[1]/3), int(img.shape[0]/3)))

    cv2.imshow("test", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = input("specify the path to the image")

    try:
        image, cascade = read(image_path, "Files/haarcascade_frontalface_default.xml")
    except:
        print("the path was not correct.")

    faces = get_faces(cascade, image)
    color_image = cv2.imread(image_path)
    draw_rectangle(color_image, faces)