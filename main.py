import logging
import random
from time import sleep
from datetime import datetime
from date import draw_date,draw_date2
from PIL import Image,ImageDraw,ImageFont

from waveshare import epd2in13_V4


# Create fonts
font10 = ImageFont.truetype("font.ttf", 10)
font12 = ImageFont.truetype("font.ttf", 12)
font14 = ImageFont.truetype("font.ttf", 14)
font16 = ImageFont.truetype("font.ttf", 16)
font24 = ImageFont.truetype("font.ttf", 24)
font48 = ImageFont.truetype("font.ttf", 48)


def main():
    running = True
    logging.basicConfig(level=logging.INFO)

    try:
        # Setup epd
        logging.info("Starting EPD")
        epd = epd2in13_V4.EPD()
        logging.info("Initialising EPD")
        epd.init()
        epd.Clear(255)

        # No clue why these are reversed
        width = epd.height
        height = epd.width

        # Create sleep image
        sleep_image = create_sleep_image(width, height)

        # Create image
        base_image = create_base(width, height)
        epd.displayPartBaseImage(epd.getbuffer(base_image.copy().rotate(180)))
        reprint_base = False

        while running:
            # Make sure at least one minute has passed
            if "time" in locals() and datetime.now().minute == time.minute:
                continue

            # Reprint base
            if reprint_base:
                base_image = create_base(width, height)
                epd.displayPartBaseImage(epd.getbuffer(base_image.copy().rotate(180)))
                reprint_base = False

            time = datetime.now()

            # Go to sleep at midnight
            if time.strftime("%H%M") == "0000":
                epd.displayPartBaseImage(epd.getbuffer(sleep_image))
                logging.info("Going to sleep")
                sleep(60 * 60 * 6) # 6 hours
                logging.info("Waking up")
                reprint_base = True
                continue

            # Show adhkar
            if time.minute % 5 == 0 and random.random() < 0.5:
                logging.info("Printing dhikr")
                epd.displayPartBaseImage(epd.getbuffer(dhikr(width, height)))
                reprint_base = True
                continue

            # Rereate image
            image = base_image.copy()
            draw = ImageDraw.Draw(image)
            # Draw time
            time = datetime.now()
            draw_time(time, draw, width, height)
            # Rotate image
            image = image.rotate(180)

            # Display image
            if time.minute == 0:
                # Full refresh every hour
                epd.displayPartBaseImage(epd.getbuffer(base_image.copy().rotate(180)))

            epd.displayPartial(epd.getbuffer(image))

        epd.sleep()
    except IOError as e:
        logging.error(e)
    except KeyboardInterrupt:
        logging.info("Exiting")
        epd2in13_V4.epdconfig.module_exit(cleanup=True)
        running = False


adhkar = ["الله أكبر", "الحمد لله", "سبحان الله", "لا إله إلا الله", "لا حول ولا قوة إلا بالله"]
def dhikr(width, height):
    image, draw = blank_image(width, height)
    draw.text((width / 2, height / 2), random.choice(adhkar), fill = 0, font = font24, anchor = "mm")
    return image.rotate(180)



def create_base(width, height):
    image, draw = blank_image(width, height)
    draw_date(draw, font16)
    draw_date2(draw, 16, font10)
    return image


def draw_time(time, draw, width, height):
    draw.text((width / 2, height / 2), time.strftime("%H:%M"), fill = 0, font = font48, anchor = "mm")


def create_sleep_image(width, height):
    image, draw = blank_image(width, height)
    draw.text((width / 2, height / 2), "Sleeping", fill = 0, font = font48, anchor = "mm")
    return image.rotate(180)

def blank_image(width, height):
    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)
    return image, draw


if __name__ == "__main__":
    main()