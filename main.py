import logging
from datetime import datetime
from PIL import Image,ImageDraw,ImageFont

from waveshare import epd2in13_V4

running = True
logging.basicConfig(level=logging.INFO)

try:
    logging.info("Starting EPD")
    epd = epd2in13_V4.EPD()
    logging.info("Initialising EPD")
    epd.init()
    epd.Clear(0xFF)

    # No clue why these are reversed
    width = epd.height
    height = epd.width

    # Create fonts
    font12 = ImageFont.truetype("font.ttf", 12)
    font24 = ImageFont.truetype("font.ttf", 24)
    font48 = ImageFont.truetype("font.ttf", 48)

    # Init time
    time = datetime.now()

    # Create image
    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)
    epd.displayPartBaseImage(epd.getbuffer(image))

    while running:
        # Make sure at least one second has passed
        if datetime.now().second == time.second:
            continue

        # Rereate image
        image = Image.new("1", (width, height), 255)
        draw = ImageDraw.Draw(image)
        # Draw time
        time = datetime.now()
        draw.text((width / 2, height / 2), time.strftime("%H:%M:%S"), fill = 0, font = font48, anchor = "mm")
        # Rotate image
        image = image.rotate(180)

        # Display image
        epd.displayPartial(epd.getbuffer(image))

    epd.sleep()
except IOError as e:
    logging.error(e)
except KeyboardInterrupt:
    logging.info("Exiting")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    running = False
