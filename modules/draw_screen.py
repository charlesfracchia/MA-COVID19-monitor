import argparse
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
import os

scale_size = 1

# Set up the correct display and scaling factors
inky_display = InkyPHAT("red")

inky_display.set_border(inky_display.BLACK)

width = inky_display.WIDTH
height = inky_display.HEIGHT

img = Image.new("P", (width, height))
draw = ImageDraw.Draw(img)

# Get current path
current_path = os.path.dirname(__file__)

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
science_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/Science_Icons.ttf'), 22)
fat_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/04b_30/04B_30__.TTF'), 12)
vcr_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/vcr_osd_mono/VCR_OSD_MONO_1.001.ttf'), 11)
big_vcr_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/vcr_osd_mono/VCR_OSD_MONO_1.001.ttf'), 15)

#minecraft_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/8bit_wonder/8-BIT WONDER.TTF'), 11)
pixelmix_font_tiny = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/pixelmix/pixelmix.ttf'), 7)
pixelmix_font = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/pixelmix/pixelmix.ttf'), 8)
pixelmix_font_bold = ImageFont.truetype(os.path.join(current_path, '../resources/fonts/pixelmix/pixelmix_bold.ttf'), 10)

intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding_x = 10
padding_y = 5
padding_y_small = 4
top = padding_y
bottom = height-padding_y

#Text Heights
small_text_height = 9

#Header vars
header_height = 19

#Table Header vars
table_header_start_y = header_height+padding_y
table_header_height = 12
table_header_padding = 3

table_width = width-padding_x

table_col_1_width = table_width - 100
table_col_2_width = (table_width-table_col_1_width)/2
table_col_3_width = (table_width-table_col_1_width)/2

# Move left to right keeping track of the current x position for drawing shapes.
left = padding_x
right = width-padding_x

def makeScreen(state_information, locations):

    draw_header(state_information)
    draw_table_header(state_information)
    draw_table_content(locations)
    draw_footer(state_information)

    # Display the logo image
    inky_display.set_image(img)
    inky_display.show()

#Function to make text
def draw_header(state_information):

    #Draw Header Background
    draw.rectangle((0, 0, width, header_height), fill=inky_display.RED)
    draw.rectangle((0, header_height, width, header_height), outline=inky_display.BLACK)

    #Draw Header Title Text
    draw.text((left-2, top-8), 'F', font=science_font, fill=inky_display.WHITE)
    draw.text((left+20, top-1), 'COVID-19', font=fat_font, fill=inky_display.WHITE)

    #Write the State abbreviation and date of last update
    draw.text((left+135, header_height-padding_y-5), 
                state_information["two_letter"] + ' | '+state_information["confirmed_date"].strftime("%m/%d/%y"), 
                font=pixelmix_font_tiny, fill=inky_display.WHITE)

def draw_table_header(state_information):

    #first Column
    draw.rectangle((left, table_header_start_y+table_header_height, table_col_1_width, table_header_start_y+table_header_height), outline=inky_display.BLACK)
    #Second Column
    draw.rectangle((table_col_1_width, table_header_start_y, left+table_col_1_width+table_col_2_width, table_header_start_y+table_header_height), outline=inky_display.BLACK, fill=inky_display.RED)
    #Third Column
    draw.rectangle((table_col_1_width+table_col_2_width, table_header_start_y, table_col_1_width+table_col_2_width+table_col_3_width, table_header_start_y+table_header_height), outline=inky_display.BLACK, fill=inky_display.BLACK)
    #Draw Labels
    draw.text((left+1, table_header_start_y+table_header_padding), state_information["name"], font=pixelmix_font_tiny, fill=inky_display.BLACK)
    draw.text((table_col_1_width+7, table_header_start_y+table_header_padding), 'POSITIVE', font=pixelmix_font_tiny, fill=inky_display.WHITE)
    draw.text((table_col_1_width+table_col_2_width+15, table_header_start_y+table_header_padding), 'SAFE', font=pixelmix_font_tiny, fill=inky_display.WHITE)

def draw_table_content(locations):

    for index, location in enumerate(locations):

        row_offset = (small_text_height+padding_y_small)*index + padding_y_small
        draw.text((left+7, table_header_start_y+table_header_height+padding_y + row_offset), location["name"], font=pixelmix_font, fill=inky_display.BLACK)
        if (location["confirmed"] != 'NaN'):
            draw.text((table_col_1_width+(table_col_2_width/4), table_header_start_y+table_header_height+padding_y + row_offset), '{:,}'.format(location["confirmed"]), font=pixelmix_font, fill=inky_display.BLACK)
        else:
            draw.text((table_col_1_width+(table_col_2_width/4), table_header_start_y+table_header_height+padding_y + row_offset), location["confirmed"], font=pixelmix_font, fill=inky_display.BLACK)
        
        if (location["recovered"] != 'NaN'):
            draw.text((table_col_1_width+table_col_2_width+(table_col_3_width/3), table_header_start_y+table_header_height+padding_y + row_offset), '{:,}'.format(location["recovered"]), font=pixelmix_font, fill=inky_display.BLACK)
        else:
            draw.text((table_col_1_width+table_col_2_width+(table_col_3_width/3), table_header_start_y+table_header_height+padding_y + row_offset), location["recovered"], font=pixelmix_font, fill=inky_display.BLACK)
        
        #Row line
        draw.rectangle((left, table_header_start_y+table_header_height+padding_y + ((small_text_height+padding_y_small)*(index+1)), 
                        table_width, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*(index+1))), 
                        outline=inky_display.BLACK)

def draw_footer(state_information):

    #Second Line
    draw.rectangle((0, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y, width, height),
                    fill=inky_display.RED)
    draw.rectangle((0, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y, width, table_header_start_y+table_header_height+padding_y+((small_text_height+padding_y_small)*3)+padding_y_small+padding_y),
                    outline=inky_display.BLACK)

    draw.text((left, height-11), 
                state_information["two_letter"]+" | POSITIVE "+'{:,}'.format(state_information["confirmed_cases"])+" | SAFE "+'{:,}'.format(state_information["quarantine_released"]),
                font=pixelmix_font, fill=inky_display.WHITE)

if __name__ == "__main__":
    pass
    state_information = {
        "name" : "Massachusetts",
        "two_letter" : "MA",
        "confirmed_date" : "04/13/20",
        "confirmed_cases" : "26,867",
        "quarantine_released" : "5,402"
    }
    locations = [
        { "name" : "Boston", "confirmed" : "2,435", "recovered" : "0" },
        { "name" : "Somerville", "confirmed" : "256", "recovered" : "0" },
    ]
    makeScreen(state_information, locations)