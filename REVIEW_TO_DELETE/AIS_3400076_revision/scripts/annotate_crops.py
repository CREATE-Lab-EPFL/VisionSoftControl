"""Draws reviewer-issue highlights on the manuscript's own figures (from the
compiled PDFs), then crops each figure. Words are located with pdftotext -bbox;
panel regions with page fractions."""
import re
from PIL import Image, ImageDraw, ImageFont

OUT = "/home/vigno0405/github/VisionSoftControl/REVIEW_TO_DELETE/AIS_3400076_revision"
PX = 170 / 72.0
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)


def words(fn):
    pages = open(f"{OUT}/pages/{fn}").read().split("<page ")[1:]
    return [[(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in
             re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', p)] for p in pages]


W = {"main": words("main_bbox.html"), "si": words("si_bbox.html")}
IMG = {"main": "main-{:02d}.png", "si": "si-{}.png"}

# (doc, page, crop fractions, word highlights [(regex, ymin_pt, ymax_pt)], region boxes [(x0,y0,x1,y1 page-%, tag)])
SPEC = {
    "fig1": ("main", 3, (4, 1.5, 96, 39.5), [(r"^simultaneously$", 0, 999), (r"^segments,?$", 270, 300)], []),
    "fig2": ("main", 3, (50, 58, 96, 80), [], [(51, 60, 68, 72, "1"), (70, 59, 95, 72, "1")]),
    "fig3": ("main", 4, (4, 1.5, 96, 69), [], [(8, 40, 92, 56, "2"), (60, 27, 96, 39, "1")]),
    "fig4": ("main", 6, (4, 1.5, 96, 31.5), [], [(5, 2, 37, 25, "1"), (61, 2, 96, 25, "2")]),
    "fig5": ("main", 7, (4, 1.5, 96, 39), [(r"^uniform$", 0, 999), (r"^scaling$", 0, 300), (r"^single-segment$", 0, 300)],
             [(55, 2, 79, 31, "1")]),
    "fig6": ("main", 8, (4, 1.5, 96, 43), [(r"^feedforward$", 300, 340), (r"^open-loop$", 270, 290)], []),
    "fig7": ("main", 8, (50, 49, 96, 67), [(r"^Cumulative$", 0, 999)], [(51, 50, 56, 59, "1")]),
    "fig8": ("main", 9, (4, 1.5, 96, 37.5), [(r"^multi-segment$", 240, 300)], []),
    "fig9": ("main", 10, (4, 1.5, 96, 45), [(r"^feedforward$", 300, 345), (r"^open-loop$", 270, 290), (r"^Angular$", 295, 315)], []),
    "fig10": ("main", 11, (4, 1.5, 96, 25), [(r"^feedforward", 175, 200), (r"^Open-loop$", 140, 160)], []),
    "figS1": ("si", 1, (51, 33.5, 96, 57), [(r"^multi-segment$", 390, 410)], []),
    "figS2": ("si", 2, (4, 72, 50, 91), [], [(26, 72.5, 49.5, 85, "1")]),
    "figS3": ("si", 5, (4, 1.5, 96, 33), [], [(14, 2.5, 46, 12, "1"), (58, 3, 78, 12, "1")]),
    "figS4": ("si", 6, (4, 1.5, 50, 23.5), [], [(44, 4, 49, 16, "1")]),
    "figS5": ("si", 6, (4, 41, 50, 72), [], [(43, 43, 49.5, 55, "1"), (43, 57, 49.5, 69, "1")]),
    "figS6": ("si", 6, (50, 1.5, 96, 32.5), [], [(89, 3, 96, 15, "1"), (89, 17, 96, 29, "1")]),
    "alg1": ("main", 7, (4, 50, 50, 74), [], [(6, 58.8, 34, 60.7, "1"), (7.5, 63.2, 32, 65.1, "2")]),
    "table1": ("main", 9, (50, 69.5, 96, 81.5), [], []),
    "tableS6": ("si", 5, (50, 46.5, 96, 58.5), [], []),
}

for name, (doc, page, (x0, y0, x1, y1), hl, boxes) in SPEC.items():
    im = Image.open(f"{OUT}/pages/" + IMG[doc].format(page)).convert("RGB")
    Wd, Hd = im.size
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for rx, ylo, yhi in hl:
        for (a, b, c, e, w) in W[doc][page - 1]:
            if re.search(rx, w) and ylo <= b <= yhi:
                d.rectangle([a * PX - 3, b * PX - 3, c * PX + 3, e * PX + 3], fill=(255, 40, 40, 70), outline=(220, 0, 0, 255), width=3)
    for (bx0, by0, bx1, by1, tag) in boxes:
        X0, Y0, X1, Y1 = Wd * bx0 / 100, Hd * by0 / 100, Wd * bx1 / 100, Hd * by1 / 100
        d.rectangle([X0, Y0, X1, Y1], outline=(220, 0, 0, 255), width=5)
        d.ellipse([X0 - 22, Y0 - 22, X0 + 22, Y0 + 22], fill=(220, 0, 0, 255))
        d.text((X0 - 9, Y0 - 19), tag, fill=(255, 255, 255, 255), font=FONT)
    out = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    out.crop((int(Wd * x0 / 100), int(Hd * y0 / 100), int(Wd * x1 / 100), int(Hd * y1 / 100))).save(f"{OUT}/crops/{name}_annot.png")
print("done")
