import qrcode 
from PIL import Image
if not hasattr(Image, 'Resampling'):  # Pillow<9.0
    Image.Resampling = Image
from PIL import ImageDraw
from PIL import ImageFont

def getQRcode(strs, name):
    qr = qrcode.QRCode(
        version = 1,
        error_correction = qrcode.constants.ERROR_CORRECT_L,
        box_size = 10,
        border =5
    )
    qr.add_data(strs)
    qr.make(fit = True)
    img = qr.make_image(fill_color = "black", back_color = "white")
    img = img.convert("CMYK")
    icon = Image.open("static/psggroups.png")
    img_w, img_h = img.size
    factor = 6
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.Resampling.LANCZOS)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    # img.paste(icon, (w, h), None)
    img = img.convert('RGB')
    img.save(name)
    return img

def info(name, body, title=""):
    getQRcode(body, name)
    oriImg = Image.open("static/background.png")
    oriImg2 = Image.open(name)
    oriImg2 = oriImg2.resize((1500,1500))
    oriImg.paste(oriImg2, (500,1250))
    draw = ImageDraw.Draw(oriImg)
    oriImg = oriImg.convert('RGB')
    draw = ImageDraw.Draw(oriImg)
    font = ImageFont.truetype("static/j9_bold.ttf", 225)
    W, H = oriImg.size
    msg = title
    w  = draw.textlength(msg)
    wid = (W-w)/3
    if len(msg)>5: wid = (W-w)/4
    if len(msg)>8: wid = (W-w)/6
    if len(msg)>10: wid = (W-w)/10
    draw.text((wid, 750),msg,(0,0,0),font=font)
    oriImg.save(name.replace(".png",".pdf"))

def makeresult(prefill_type, data, BASE_URL="gms.psgtech.ac.in"):
    if prefill_type=="classroom":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"],
                    "room"  : data["room"]
                  }
        title = data["room"]
    elif prefill_type=="department":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"],
                    "department"  : data["department"]
                  }
        title = data["department"]
    elif prefill_type=="restroom":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"]
                  }
        title = f"{data['block']}{data['floor']} W/C"
    elif prefill_type=="water":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"],
                    "disp"  : data["dispenser_no"]
                  }
        title = f"Water Doctor {data['dispenser_no']}"
    elif prefill_type=="lift":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"]
                  }
        title = f"{data['block']} Block Lift"
    elif prefill_type=="misc":
        prefill = {
                    "block" : data["block"],
                    "floor" : data["floor"]
                  }
        title = f"{data['block']} Block | Floor {data['floor']}"
    route = f"/../issue/report?choice={prefill_type}&block={prefill['block']}&floor={prefill['floor']}"
    if prefill.get("room"): route+=f"&room={prefill['room']}"
    if prefill.get("department"): route+=f"&department={prefill['department']}"
    if prefill.get("disp"): route+=f"&disp={prefill['disp']}"
    url = f"{route}"
    info("qrcode_result.png", url, title)

if __name__ == '__main__':
    pass
