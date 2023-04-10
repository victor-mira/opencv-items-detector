import os
import cv2
import numpy as np


class ImageLoader:

    def __init__(self, images_path):
        self.path = images_path
        self.ref_image = None
        self.mask = None
        self.test_images_names = None
        self.test_images = []
        self.load_images()

    def load_images(self):
        self.ref_image = cv2.imread(self.path + 'Reference.JPG')
        scale_percent = 20  # percent of original size
        width = int(self.ref_image.shape[1] * scale_percent / 100)
        height = int(self.ref_image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # Resize reference image
        self.ref_image = cv2.resize(self.ref_image, dim, interpolation=cv2.INTER_AREA)
        # Load test images paths
        self.test_images_names = os.listdir(self.path)
        self.test_images_names.remove('Reference.JPG')
        # Load or create mask
        if not os.path.isfile(self.path + 'Mask.jpg'):
            self.draw_mask()
        else:
            self.test_images_names.remove('Mask.jpg')
        self.mask = cv2.imread(self.path + 'Mask.jpg')
        # Resize each test images
        for name in self.test_images_names:
            resized = cv2.resize(cv2.imread(self.path + name), dim, interpolation=cv2.INTER_AREA)
            self.test_images.append(resized)

    def draw_mask(self):
        copy = self.ref_image.copy()
        mask_array = []

        # Méthode de callback ajoutant un point au polygone du mask
        def add_point(event, x, y, flags, param):
            # Si click gauche
            if event == cv2.EVENT_LBUTTONUP:
                # Ajout de la coordonnée au tableau
                mask_array.append([x, y])
                pts = np.array(mask_array)
                pts = pts.reshape((-1, 1, 2))
                # Traçage du polygone sur la copie
                cv2.polylines(copy, [pts], False, (0, 255, 0), 3)
                # Reload l'image
                cv2.imshow('mask', copy)

        # On créé une fenêtre pour récupérer les inputs de la souris
        cv2.namedWindow('mask')
        cv2.setMouseCallback('mask', add_point)
        cv2.imshow('mask', copy)

        # Quand une touche est pressée
        if cv2.waitKey(0):
            # On créé une image noire au meme dimension que l'image de ref
            mask_img = self.ref_image.copy()
            mask_img[:] = (0, 0, 0)
            pts = np.array(mask_array)
            pts = pts.reshape((-1, 1, 2))
            # On trace le polygone en blanc pour créer le masque
            cv2.fillPoly(mask_img, [pts], (255, 255, 255))
            cv2.imshow('mask', mask_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            # On sauvegarde le masque dans le path
            cv2.imwrite(self.path + 'Mask.jpg', mask_img)

