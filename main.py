import logging
from time import sleep
from datetime import datetime
from date import draw_date,draw_date2
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
    font10 = ImageFont.truetype("font.ttf", 10)
    font12 = ImageFont.truetype("font.ttf", 12)
    font14 = ImageFont.truetype("font.ttf", 14)
    font16 = ImageFont.truetype("font.ttf", 16)
    font24 = ImageFont.truetype("font.ttf", 24)
    font48 = ImageFont.truetype("font.ttf", 48)

    # Create image
    base_image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(base_image)
    draw_date(draw, font16)
    draw_date2(draw, 16, font10)
    epd.displayPartBaseImage(epd.getbuffer(base_image.copy().rotate(180)))

    while running:
        # Make sure at least one minute has passed
        if "time" in locals() and datetime.now().minute == time.minute:
            continue

        # Go to sleep at midnight
        if datetime.now().strftime("%H%M") == "0000":
            image = Image.new("1", (width, height), 255)
            draw = ImageDraw.Draw(image)
            draw.text((width / 2, height / 2), "Sleeping", fill = 0, font = font48, anchor = "mm")
            epd.init()
            epd.display(epd.getbuffer(image))
            sleep(60 * 60 * 6) # 6 hours
            # Create base image again
            base_image = Image.new("1", (width, height), 255)
            draw = ImageDraw.Draw(base_image)
            draw_date(draw, font16)
            draw_date2(draw, 16, font10)
            epd.displayPartBaseImage(epd.getbuffer(base_image.copy().rotate(180)))
            continue

        # Rereate image
        image = base_image.copy()
        draw = ImageDraw.Draw(image)
        # Draw time
        time = datetime.now()
        draw.text((width / 2, height / 2), time.strftime("%H:%M"), fill = 0, font = font48, anchor = "mm")
        # Rotate image
        image = image.rotate(180)

        # Display image
        if time.minute == 0:
            # Full refresh every hour
            epd.init()
            epd.display(epd.getbuffer(image))
        else:
            epd.displayPartial(epd.getbuffer(image))

    epd.sleep()
except IOError as e:
    logging.error(e)
except KeyboardInterrupt:
    logging.info("Exiting")
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    running = False

