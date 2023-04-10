import sys
import cv2
import imagesLoader as il
import imagesComparator as ic

path = sys.argv[1]
loader = il.ImageLoader(path)

for i in range(len(loader.test_images)):
    comparator = ic.ImageComparator(loader.ref_image, loader.test_images[i], loader.mask)
    img = comparator.img_treatment(loader.test_images[i])
    cv2.imshow("Objects Detection", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

