from matplotlib import pyplot as plt

import imagesLoader as il
import imagesComparator as ic

loader = il.ImageLoader('Images/Salon/')

fig = plt.figure(figsize=(9, 9))

for i in range(len(loader.test_images)):

    comparator = ic.ImageComparator(loader.ref_image, loader.test_images[i], loader.mask)
    comparator.img_treatment(loader.test_images[i])
    plt.show()

    #
    # ax = plt.subplot(len(loader.test_images), 3, 2 * (i + 2))
    # plt.imshow(tresh)
    # plt.title('tresh_' + str(i))
    # plt.axis('off')






