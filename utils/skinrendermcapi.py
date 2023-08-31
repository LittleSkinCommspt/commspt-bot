from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import httpx


async def request_skinrendermc(
    skin_url: str | None, cape_url: str | None, name_tag: str | None
):
    p = {
        "skinUrl": skin_url,
        "capeUrl": cape_url,
        "nameTag": name_tag,
    }

    # 删除值为 None 的键值对
    # （SkinRenderMC 只判断键值对是否存在）
    for x in [k for k in p if not p[k]]:
        p.pop(x)

    async with httpx.AsyncClient(http2=True) as client:
        resp = await client.get(
            f"http://10.50.0.4:57680/url/image/both",
            params=p,
            timeout=30,  # 通常只需要不到 15 秒
        )
        if resp.status_code == 200:
            image = resp.read()
            return image
        else:
            return


def process_image(image_bytes: bytes, text: str) -> bytes:
    # Open the image from the byte representation
    image = Image.open(BytesIO(image_bytes))
    image = image.crop((0, 0, image.width, int(image.height * 0.87)))

    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)

    # Define the font to be used for the watermark
    font = ImageFont.truetype("mojangles.ttf", size=12)

    # Set the margin around the watermark
    margin_x = 20
    margin_y = 10

    # Calculate the width and height of the watermark text
    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3]

    # Calculate the coordinates to place the watermark text
    x = image.width - margin_x - text_width
    y = image.height - margin_y - text_height

    # Draw the watermark text on the image
    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    # Save the modified image as byte representation
    output_bytes = BytesIO()
    image.save(output_bytes, format="PNG")

    # Return the byte representation of the modified image
    return output_bytes.getvalue()
