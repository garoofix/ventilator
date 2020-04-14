from PIL import ImageFont
fontlg = ImageFont.truetype('FreeSans.ttf', 24)
fontsm = ImageFont.truetype('FreeSans.ttf', 16)

class Button():
    def __init__(self, draw, TFT, dims, pos, caption="Button", color="cyan"):
        self._draw = draw
        self._TFT = TFT
        self._dims = dims
        self._pos = pos
        self._caption = caption
        self._color = color
        self.redraw()

    def redraw(self):
        p = self._pos
        d = self._dims
        font = fontlg
        fontsize = 24

        # Set font size
        if len(self._caption) > 1:
            font = fontsm
            fontsize = 16
        # Draw button bg
        self._draw.rectangle((p[0], p[1], p[0]+d[0], p[1]+d[1]), self._color)
        # Write caption
        txt_pos = [
            p[0]+d[0]/2 - len(self._caption)/2*fontsize/2,
            p[1]+d[1]/2 - fontsize/2,
        ]
        if len(self._caption) == 1:
            txt_pos[0] = txt_pos[0] - fontsize/4
            txt_pos[1] = txt_pos[1] - fontsize/4

        self._draw.text(
            txt_pos,
            self._caption, font=font, fill="white")
        self._TFT.display()

    def set_color(self, color):
        self._color = color
        self.redraw()

    def check_pos(self, pos):
        if pos[0] > self._pos[0] and pos[0] < self._pos[0] + self._dims[0]:
            if pos[1] > self._pos[1] and pos[1] < self._pos[1] + self._dims[1]:
                return 1
        return 0
