#!/usr/bin/env python
################################################################################
# Take a JPG image taken by an Android phone and convert it to a 2D numpy array
# (a bitmap) with RGB values converted to grayscale luminance.
################################################################################

try:
    import argparse
    from PIL import Image
    import os
    import sys

    import numpy as np
    import matplotlib as mpl
    mpl.use('TkAgg')
    import matplotlib.pyplot as plt

    from skimage import measure

    import Blob

#except ImportError,e:
#    print(e)
#    raise SystemExit

except ImportError:
    print('Not all packages found, check dependencies')
    raise SystemExit

def findBlobs(image, threshold, minArea=2.):
    """Pass through an image and find a set of blobs/contours above a set
       threshold value.  The minArea parameter is used to exclude blobs with an
       area below this value."""
    blobs = []
    ny, nx = image.shape

    # Find contours using the Marching Squares algorithm in the scikit package.
    contours = measure.find_contours(image, threshold)
    for contour in contours:
        x = contour[:,1]
        y = ny - contour[:,0]
        blob = Blob.Blob(x, y)
        if blob.area >= minArea:
            blobs.append(blob)
    return blobs

def groupBlobs(blobs, maxDist):
    """Given a list of blobs, group them by distance between the centroids of
       any two blobs.  If the centroids are more distant than maxDist, create a
       new blob group."""
    n = len(blobs)
    groups = []
    if n >= 1:
        # Single-pass clustering algorithm: make the first blob the nucleus of
        # a blob group.  Then loop through each blob and add either add it to
        # this group (depending on the distance measure) or make it the
        # nucleus of a new blob group
        bg = Blob.BlobGroup()
        bg.addBlob(blobs[0])
        groups.append(bg)

        for i in range(1, n):
            bi = blobs[i]
            isGrouped = False
            for group in groups:
                # Calculate distance measure for a blob and a blob group:
                # blob just has to be < maxDist from any other blob in the group
                for bj in group.blobs:
                    if bi.distance(bj) < maxDist:
                        group.addBlob(bi)
                        isGrouped = True
                        break
            if not isGrouped:
                bg = Blob.BlobGroup()
                bg.addBlob(bi)
                groups.append(bg)
        
    return groups

def doThisFirst(imagePath):
    # Load the image and convert pixel values to grayscale intensities
    filename = imagePath
    img = Image.open(filename).convert("L")
    image = []
    pix = img.load()

    # Stuff image values into a 2D table called "image"
    nx = img.size[0]
    ny = img.size[1]
    x0, y0, x1, y1 = (0, 0, nx, ny)
    for y in range(ny):
        image.append([pix[x, y] for x in range(nx)])
    sys.stdout.write("\n")

    image = np.array(image, dtype=float)

    blobs = findBlobs(image, 50, minArea=2)
    return blobs
    # groups = groupBlobs(blobs, 5.distance)
    # title = os.path.basename(filename)
    # fig1 = plt.figure(1, figsize=(8,7))
    # ax = fig1.add_subplot(111)