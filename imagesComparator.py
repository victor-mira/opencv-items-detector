import cv2
from matplotlib import pyplot as plt
from skimage.metrics import structural_similarity as compare_ssim
import imutils


def show_img_with_matplotlib(img, title, pos, isBAndW):
    """Shows an image using matplotlib capabilities"""
    if isBAndW:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # Convert BGR image to RGB
    img_RGB = img[:, :, ::-1]

    ax = plt.subplot(3, 2, pos)
    plt.imshow(img_RGB)
    plt.title(title)
    plt.axis('off')


class ImageComparator:
    def __init__(self, ref_image, comparison_image, mask):
        self.ref_img = ref_image
        self.comp_img = comparison_image
        self.mask = mask

    def removeHighLight(self, img):
        # Convert to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Create mask for highlight parts
        mask_light = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)[1]
        # Apply closing
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
        clos_mask = cv2.morphologyEx(mask_light, cv2.MORPH_CLOSE, kernel)
        # Repaint
        result_img = cv2.inpaint(img, clos_mask, 5, cv2.INPAINT_TELEA)
        return result_img

    def img_treatment(self, img, blur=5, pos=1):
        ref_img = self.removeHighLight(self.ref_img)
        comp_img = self.removeHighLight(self.comp_img)

        show_img_with_matplotlib(comp_img, 'Highlight removed', pos, False)

        cla = cv2.createCLAHE(clipLimit=0.55, tileGridSize=(4, 4))
        # Histogram equalization
        H, S, V = cv2.split(cv2.cvtColor(ref_img, cv2.COLOR_BGR2HSV))
        eq_V = cla.apply(V)
        ref_img = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2BGR)

        H, S, V = cv2.split(cv2.cvtColor(comp_img, cv2.COLOR_BGR2HSV))
        eq_V = cla.apply(V)

        comp_img = cv2.cvtColor(cv2.merge([H, S, eq_V]), cv2.COLOR_HSV2BGR)

        show_img_with_matplotlib(comp_img, 'Equalized', pos + 1, False)

        # Blurring
        ref_blur = cv2.medianBlur(ref_img, blur)
        comp_blur = cv2.medianBlur(comp_img, blur)

        # Applying ground mask
        ref_blur = cv2.bitwise_and(ref_blur, self.mask)
        comp_blur = cv2.bitwise_and(comp_blur, self.mask)

        # Convert to grayscale
        ref_gray = cv2.cvtColor(ref_blur, cv2.COLOR_BGR2GRAY)
        comp_gray = cv2.cvtColor(comp_blur, cv2.COLOR_BGR2GRAY)

        # Structural similarity
        (score, diff) = compare_ssim(ref_gray, comp_gray, full=True)
        diff = (diff * 255).astype("uint8")

        # Thresholding
        thresh = cv2.threshold(diff, 0, 256,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        show_img_with_matplotlib(thresh, 'thresh', pos + 2, True)

        # Open & Close to reduce noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 8))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        clos = cv2.morphologyEx(open, cv2.MORPH_CLOSE, kernel2)
        show_img_with_matplotlib(clos, 'open_clos', pos + 3, True)

        # Contour detection
        cnts = cv2.findContours(clos.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)

        # Bounding rectangle drawing
        for cnt in cnts:
            x, y, w, h = cv2.boundingRect(cnt)
            self.comp_img = cv2.rectangle(self.comp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        show_img_with_matplotlib(self.comp_img, 'detection', pos + 4, False)
        return self.comp_img
