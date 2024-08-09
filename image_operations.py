from PIL import Image, ImageDraw, ImageFont

def create_text_to_image(width, height, text, font_path="MontserratBlack-3zOvZ.ttf", font_size=35, text_color=(255, 255, 255), background_color=(0, 0, 0), output_file="latest_price.png"):

    image = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    draw.text((text_x, text_y), text, font=font, fill=text_color)
    image.save(output_file)