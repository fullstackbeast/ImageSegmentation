import cv2
import numpy as np
from skimage import color, measure, io
from matplotlib import pyplot as plt


class Segment:

    def __init__(self, imageName):
        self.imageName = imageName

    def tst(self):
        img = cv2.imread(self.imageName)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        pixelsToUm = 0.5

        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers+1

        # Now, mark the region of unknown with zero
        markers[unknown==255] = 0

        markers = cv2.watershed(img,markers)
        img[markers == -1] = [255,0,0]

        img2 = color.label2rgb(markers, bg_label=0)

        io.imsave(self.imageName.replace(".jpg", " segmented.jpg"), img2)

        regions = measure.regionprops(markers, intensity_image=gray)

        propList = ['Area',
                    'equivalent_diameter',
                    'orientation',
                     'MajorAxisLength',
                    'MinorAxisLength',
                        'Perimeter',
                        'MinIntensity',
                        'MeanIntensity',
                        'MaxIntensity']

        outputFile = open(self.imageName.replace(".jpg", ".csv"), 'w')

        outputFile.write("Measurement #" + "," + "," + ",".join(propList) + '\n')

        measurementNumber = 1

        for regionProps in regions:
            outputFile.write(str(measurementNumber) + ',')

            for i, prop in enumerate(propList):
                if(prop == 'Area'):
                    toPrint = regionProps[prop] * pixelsToUm**2
                elif (prop == 'orientation'):
                    toPrint = regionProps[prop] * 57.2958
                elif (prop.find('Intensity') < 0):
                    toPrint = regionProps[prop] * pixelsToUm
                else:
                    toPrint = regionProps[prop]
                outputFile.write(',' + str(toPrint))
            outputFile.write('\n')
            measurementNumber += 1

        outputFile.close()

        return