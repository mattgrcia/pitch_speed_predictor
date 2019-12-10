import os
from PIL import Image


def frames(inGif, name, outFolder):
    frame = Image.open(inGif)
    nframes = 0
    frame.save('0_%s.png' % name)
    while frame:
        frame.save('1_%s.png' % name)
        nframes += 1
        try:
            frame.seek(nframes)
        except EOFError:
            break
    return outFolder
