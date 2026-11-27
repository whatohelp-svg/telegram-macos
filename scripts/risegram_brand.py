"""Apply the RiseGram logo traced from the owner's supplied image."""
from pathlib import Path
import json
import re
import plistlib
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "Telegram-Mac"
PLANE = [(1051,554),(1054,563),(1057,602),(1054,687),(1051,700),(1051,715),(1048,723),(1045,757),(1029,839),(1020,873),(1017,878),(1013,898),(996,947),(972,1000),(952,1031),(942,1041),(930,1048),(910,1051),(903,1048),(884,1045),(855,1034),(818,1014),(784,989),(749,955),(732,934),(722,916),(721,894),(724,884),(732,871),(829,782),(844,766),(848,758),(851,745),(848,722),(841,711),(831,701),(815,694),(793,694),(777,701),(612,852),(597,858),(540,859),(495,852),(463,841),(451,834),(436,821),(429,809),(426,797),(426,786),(432,768),(445,752),(489,711),(550,666),(594,639),(651,609),(710,583),(765,563),(852,539),(946,525),(1018,525),(1037,535)]

def render(w,h,margin):
    s = min(w,h)*4
    d = s*(1-2*margin)
    x = (w*4-d)/2
    y = (h*4-d)/2
    im = Image.new("RGBA",(w*4,h*4),(0,0,0,0))
    draw = ImageDraw.Draw(im)
    draw.ellipse((x,y,x+d-1,y+d-1),fill="black")
    draw.polygon([(x+(px-192)*d/1151,y+(py-193)*d/1151) for px,py in PLANE],fill="white")
    return im.resize((w,h),Image.Resampling.LANCZOS)

for name,margin in [("AppIcon.appiconset",0.10),("Icon_TelegramLogin.imageset",0.02),("Icon_LoginCap.imageset",0.02),("Icon_loginQRCap.imageset",0.02)]:
    folder=ROOT/"Assets.xcassets"/name
    files=list(folder.glob("*.png"))
    assert files, name
    for p in files:
        with Image.open(p) as old:
            w,h=old.size
        render(w,h,margin).save(p)

# Icon Composer on modern macOS, with the matching monochrome silhouette.
composer=ROOT/"AppIcon.icon"
points=" ".join(f"{101.5+(x-192)*821/1151:.2f},{101.5+(y-193)*821/1151:.2f}" for x,y in PLANE)
(composer/"Assets/Plane.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024"><polygon points="{points}" fill="#FFFFFF"/></svg>',encoding="utf-8")
config=json.loads((composer/"icon.json").read_text())
for group in config["groups"]:
    group["specular"]=False
    for layer in group["layers"]:
        layer["glass"]=False
        if layer["image-name"]=="Oval.svg":
            layer["fill-specializations"]=[{"value":{"linear-gradient":["srgb:0.00000,0.00000,0.00000,1.00000","srgb:0.00000,0.00000,0.00000,1.00000"]}},{"appearance":"dark","value":{"linear-gradient":["srgb:0.00000,0.00000,0.00000,1.00000","srgb:0.00000,0.00000,0.00000,1.00000"]}}]
        elif layer["image-name"]=="Plane.svg":
            layer.pop("fill-specializations",None)
(composer/"icon.json").write_text(json.dumps(config,indent=2),encoding="utf-8")

# Only user-visible values: never rename Swift modules, localization keys or URLs.
def brand(value):
    return re.sub(r'(?<![\w./:@-])(?:TelegramMac|Telegram|Телеграм)(?![\w./:@-])',"RiseGram",value)
for p in ROOT.glob("*.lproj/*.strings"):
    raw=p.read_bytes()
    enc="utf-16" if raw.startswith((b"\xff\xfe",b"\xfe\xff")) else "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
    text=raw.decode(enc)
    text=re.sub(r'(?m)^("(?:(?:\\.)|[^"\\])*"\s*=\s*)("(?:\\.|[^"\\])*")',lambda m:m[1]+brand(m[2]),text)
    p.write_bytes(text.encode(enc))
for p in ROOT.glob("*.lproj/MainMenu.xib"):
    text=p.read_text(encoding="utf-8")
    p.write_text(re.sub(r'(\btitle=")([^"]*)(")',lambda m:m[1]+brand(m[2])+m[3],text),encoding="utf-8")
p=ROOT/"Info.plist"
info=plistlib.loads(p.read_bytes())
info["CFBundleName"]="RiseGram"
info["CFBundleDisplayName"]="RiseGram"
# Do not use official Telegram Sparkle update channels in the experimental port.
info.pop("SUFeedURL",None)
info.pop("SUPublicDSAKeyFile",None)
p.write_bytes(plistlib.dumps(info,sort_keys=False))
print("RiseGram macOS branding applied")
