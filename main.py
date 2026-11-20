#!/usr/bin/env python3
"""Draw one newspaper front page summing up Friday 20 November 2026.

Standard library only. Fully deterministic: no randomness, no clock,
no network. Every run writes byte-identical output.

Run:  python3 main.py
Writes: $MAKEFUN_OUTPUT_DIR/entry.png  (or ./output/entry.png)
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 24)
BLUE = (29, 78, 137)
NAVY = (22, 42, 72)
GREY = (105, 100, 90)
LIGHT = (228, 222, 208)
GOLD = (176, 132, 32)
WHITE = (255, 255, 255)
SKY = (38, 58, 96)

# ---------------------------------------------------------------- font
# 5x7 bitmap glyphs, written by hand. '#' = on, '.' = off.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", "01100", "01100"),
    ",": (".....", ".....", ".....", ".....", "01100", "01100", "01000"),
    "'": ("00100", "00100", "01000", ".....", ".....", ".....", "....."),
    "-": (".....", ".....", ".....", "01110", ".....", ".....", "....."),
    "!": ("00100", "00100", "00100", "00100", "00100", ".....", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", ".....", "00100"),
    ":": (".....", "01100", "01100", ".....", "01100", "01100", "....."),
    ";": (".....", "01100", "01100", ".....", "01100", "01100", "01000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": (".....", "00100", "00100", "11111", "00100", "00100", "....."),
    "=": (".....", ".....", "11111", ".....", "11111", ".....", "....."),
    '"': ("01010", "01010", "01010", ".....", ".....", ".....", "....."),
    "*": (".....", "10101", "01110", "10101", ".....", ".....", "....."),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "11111"),
    "[": ("01110", "01000", "01000", "01000", "01000", "01000", "01110"),
    "]": ("01110", "00010", "00010", "00010", "00010", "00010", "01110"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
}


def glyph(ch):
    return FONT.get(ch.upper(), FONT["?"])


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap(text, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    char_w = 6 * scale
    max_chars = max(1, max_width // char_w)
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            trial = word if not cur else cur + " " + word
            if len(trial) <= max_chars:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                # very long single word: hard-split it
                while len(word) > max_chars:
                    lines.append(word[:max_chars])
                    word = word[max_chars:]
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = color

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def rect(self, x, y, w, h, color, thick=1):
        self.hline(x, y, w, color, thick)
        self.hline(x, y + h - thick, w, color, thick)
        self.vline(x, y, h, color, thick)
        self.vline(x + w - thick, y, h, color, thick)

    def draw_text(self, text, x, y, scale, color):
        cx = x
        for ch in text:
            g = glyph(ch)
            for row in range(7):
                bits = g[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def draw_centered(self, text, cx, y, scale, color):
        x = cx - text_width(text, scale) // 2
        self.draw_text(text, x, y, scale, color)

    def draw_block(self, text, x, y, max_w, scale, color, leading=None):
        """Wrapped paragraph. Returns y just below the block."""
        if leading is None:
            leading = 7 * scale + 4
        for line in wrap(text, max_w, scale):
            self.draw_text(line, x, y, scale, color)
            y += leading
        return y

    def triangle(self, x0, y0, x1, y1, x2, y2, color):
        # filled triangle by scanline interpolation
        ys = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx_, cy) = ys
        def interp(xa, ya, xb, yb, y):
            if yb == ya:
                return xa
            return xa + (xb - xa) * (y - ya) // (yb - ya)
        for yy in range(ay, cy + 1):
            if yy < by:
                xa = interp(ax, ay, bx, by, yy)
                xb = interp(ax, ay, cx_, cy, yy)
            else:
                xa = interp(bx, by, cx_, cy, yy)
                xb = interp(ax, ay, cx_, cy, yy)
            if xa > xb:
                xa, xb = xb, xa
            self.hline(xa, yy, xb - xa + 1, color)


# ---------------------------------------------------------------- png
def write_png(canvas, path):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * stride
        raw += canvas.px[start:start + stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


# ---------------------------------------------------------------- page
def draw_skyline(c, x, y, w, h):
    """Night skyline over Kyiv: dark sky, lit windows, a blast."""
    c.fill_rect(x, y, w, h, SKY)
    # stars: fixed positions
    for sx, sy in [(18, 14), (52, 30), (96, 10), (140, 26), (180, 12),
                   (220, 32), (262, 16), (40, 48), (200, 46)]:
        c.fill_rect(x + sx, y + sy, 3, 3, WHITE)
    # blast glow
    bx, by = x + w - 108, y + 48
    c.fill_rect(bx - 26, by - 16, 52, 32, GOLD)
    c.triangle(bx - 20, by + 6, bx, by - 24, bx + 20, by + 6, (255, 214, 90))
    c.triangle(bx - 10, by + 5, bx, by - 12, bx + 10, by + 5, RED)
    # buildings, left to right, fixed heights
    base = y + h - 58
    specs = [(0, 120, 150), (62, 96, 120), (122, 132, 170),
             (188, 108, 130), (248, 84, 150)]
    for ox, bw, bh in specs:
        c.fill_rect(x + ox, base - bh + 58, bw, bh, INK)
        # lit windows, fixed grid
        for wy in range(base - bh + 70, base + 44, 18):
            for wx in range(x + ox + 10, x + ox + bw - 12, 20):
                if (wx + wy) % 40 < 20:
                    c.fill_rect(wx, wy, 7, 9, GOLD)
    # river band at the bottom
    c.fill_rect(x, y + h - 58, w, 58, BLUE)
    c.hline(x, y + h - 58, w, WHITE, 2)
    for rx in range(12, w - 20, 46):
        c.hline(x + rx, y + h - 38, 26, WHITE, 2)
        c.hline(x + rx + 10, y + h - 22, 20, (170, 200, 230), 2)


def draw_market_bars(c, x, y, w):
    """Five red down-bars for the day's falls."""
    data = [("NIKKEI", "-5.1%"), ("KOSPI", "-4.7%"), ("TAIWAN", "-6.6%"),
            ("S+P 500", "-2.0%"), ("DOW", "-2.2%")]
    vals = [5.1, 4.7, 6.6, 2.0, 2.2]
    top = y
    base = y + 62
    slot = w // 5
    c.hline(x, base, w, INK, 2)
    for i, (name, lab) in enumerate(data):
        bh = int(vals[i] / 6.6 * 52)
        bx = x + i * slot + 18
        bw = slot - 36
        c.fill_rect(bx, base - bh, bw, bh, RED)
        c.draw_centered(lab, bx + bw // 2, top, 2, RED)
        c.draw_centered(name, bx + bw // 2, base + 8, 2, INK)


def story(c, x, y, w, kicker, headline, body):
    c.draw_text(kicker, x, y, 2, RED)
    y += 20
    y = c.draw_block(headline, x, y, w, 3, INK, leading=24)
    y += 2
    y = c.draw_block(body, x, y, w, 2, INK, leading=17)
    return y


def build():
    c = Canvas(W, H, PAPER)
    m = 28
    right = W - m

    # masthead
    c.hline(m, 14, right - m, RED, 4)
    c.draw_centered("THE WORLD TODAY", W // 2, 30, 8, INK)
    c.draw_centered("THE DAY IN ONE PAGE", W // 2, 96, 2, GREY)
    # date bar
    c.fill_rect(m, 122, right - m, 46, INK)
    c.draw_centered("FRIDAY 20 NOVEMBER 2026", W // 2, 136, 3, WHITE)
    c.hline(m, 176, right - m, RED, 3)

    # ---- lead story (left) + skyline picture (right)
    lx, lw = m, 612
    px, pw = 668, right - 668
    y = 190
    c.draw_text("LEAD STORY - UKRAINE", lx, y, 2, RED)
    y += 24
    y = c.draw_block("MISSILES RAIN ON KYIV HOURS AFTER PEACE SUMMIT",
                     lx, y, lw, 4, INK, leading=34)
    y += 6
    y = c.draw_block(
        "Russia launched a massive missile and drone attack on Ukraine "
        "overnight, lasting more than six hours. At least five people were "
        "killed - three in Kyiv and two in Lviv - and three bridges over "
        "the Dnipro were damaged.",
        lx, y, lw, 2, INK, leading=18)
    y += 4
    y = c.draw_block(
        "The attack came hours after Presidents Trump, Xi and Putin met in "
        "Shenzhen and signed a joint peace declaration.",
        lx, y, lw, 2, INK, leading=18)
    draw_skyline(c, px, 190, pw, 196)
    c.draw_block("KYIV SHELTERS AS STRIKES HIT THE CAPITAL.",
                 px, 394, pw, 2, GREY, leading=18)
    c.hline(m, 452, right - m, INK, 2)

    # ---- markets strip
    y = 466
    c.draw_text("MARKETS: AI SELL-OFF GOES GLOBAL", m, y, 3, RED)
    draw_market_bars(c, m, y + 34, right - m)
    c.draw_block(
        "Anthropic closed up 17% at $97.17 on debut, but it did not stop "
        "the slide.",
        m, y + 126, right - m, 2, INK, leading=18)
    c.hline(m, 612, right - m, INK, 2)

    # ---- middle stories, two columns; rows flow from returned heights
    col_w = (right - m - 24) // 2
    x2 = m + col_w + 24
    end1 = story(c, m, 626, col_w,
                 "JUSTICE - THE HAGUE",
                 "COURT: MYANMAR COMMITTED GENOCIDE",
                 "The World Court ruled Myanmar committed genocide against "
                 "the Rohingya, by nine votes to six - the first such "
                 "finding against a state.")
    end2 = story(c, x2, 626, col_w,
                 "UKRAINE - LONDON",
                 "UK PLEDGES 1,000 DRONES FOR UKRAINE",
                 "Britain pledged more than 1,000 drones for Ukraine in a "
                 "260 million pound package, announced in Berlin.")
    row2 = max(end1, end2) + 12
    c.hline(m, row2 - 10, right - m, LIGHT, 2)
    end3 = story(c, m, row2, col_w,
                 "ASIA - SEOUL",
                 "NORTH KOREA FIRES MISSILE TO SEA",
                 "North Korea launched a ballistic missile towards the Sea "
                 "of Japan, South Korea's military said.")
    end4 = story(c, x2, row2, col_w,
                 "MIDDLE EAST - RIYADH",
                 "HOUTHI MISSILE HITS RIYADH TOWER",
                 "A Houthi missile damaged a skyscraper in Riyadh's "
                 "financial district, including the wealth fund tower.")
    bottom = max(end3, end4) + 10
    c.hline(m, bottom, right - m, INK, 2)

    # ---- bottom strip: sport + also in the news
    y = bottom + 12
    c.draw_text("SPORT - THURSDAY NIGHT FOOTBALL", m, y, 2, RED)
    y += 22
    c.draw_text("TEXANS 26, COLTS 3", m, y, 3, INK)
    y += 28
    c.draw_block("Stroud threw three TD passes.",
                 m, y, 440, 2, INK, leading=18)
    vx = 512
    c.vline(vx, bottom + 12, 76, LIGHT, 2)
    c.draw_text("ALSO IN THE NEWS", vx + 16, bottom + 12, 2, RED)
    c.draw_block("Trump pardoned Pete Rose, the late baseball star. Spain "
                 "held a general strike that hit ports and factories.",
                 vx + 16, bottom + 36, right - vx - 16, 2, INK, leading=18)
    c.hline(m, 996, right - m, INK, 2)
    c.draw_centered("SOURCES: CNN - WSJ - REUTERS - THE HINDU - ONETURN",
                    W // 2, 1004, 1, GREY)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    canvas = build()
    write_png(canvas, path)
    print("wrote", path)


if __name__ == "__main__":
    main()
