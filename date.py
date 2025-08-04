from hijridate import Hijri
from datetime import datetime

def date_parts():
    hijri = Hijri.today()
    part1 = hijri.day_name("ar")
    part2 = f"{hijri.day}"
    part3 = hijri.month_name("ar")
    part4 = f"{hijri.year}"
    return (part1, part2, part3, part4)


def draw_date(draw, font):
    offset = 0
    for part in date_parts():
        draw.text((offset, 0), part, fill = 0, font = font, anchor = "lt")
        offset = offset + draw.textlength(f"{part} ", font)

def draw_date2(draw, offset, font):
    draw.text((0, offset), datetime.now().strftime("%a %m/%d/%Y"), fill = 0, font = font, anchor = "lt") 
