from PIL import ImageFont
from Button import Button
from time import sleep
import math
fontlg = ImageFont.truetype('FreeSans.ttf', 18)
fontmd = ImageFont.truetype('FreeSans.ttf', 14)

# VARS
GRAPH_HEIGHT = 40

class WFAdjust():
    def __init__(self, draw, TFT):
        # TFT.clear()
        self._draw = draw
        self._TFT = TFT
        # State variables
        self._running = 1
        self._active_pt = 1
        # Define waveform array
        self._wf = [
            1.0,
            1.0,
            1.0,
            2.0,
            4.0,
            5.0,
            6.0,
            7.0,
            7.0,
            4.0,
            3.0,
            1.0
        ]
        # Draw scene
        TFT.clear()
        self.setup()
        self.redraw()
        self.start()

    def setup(self):
        self._draw.text((10, 10), "Stroke Adjustment", font=fontmd, fill="white")
        self.prev_pt_btn = Button(self._draw, self._TFT, (50, 50), (10, 35), "Prev", "purple")
        self.next_pt_btn = Button(self._draw, self._TFT, (50, 50), (70, 35), "Next", "blue")

        self.adj_n_btn = Button(self._draw, self._TFT, (50, 50), (130, 35), "-", "purple")
        self.adj_p_btn = Button(self._draw, self._TFT, (50, 50), (190, 35), "+", "blue")

        self.ok_btn = Button(self._draw, self._TFT, (50, 40), (180, 280), "OK", "green")

    def redraw(self):
        dx = 17     # X-Step
        x_start = 20
        y_start = 200
        # Clear scene
        self._draw.rectangle((0, 100, 240, y_start+2), "black")
        # Calc wf
        wf_max = max(self._wf)

        # Draw
        n = 0
        pts = []
        for i in self._wf:
            pts.append((x_start+n*dx, y_start - int(i/wf_max*80)))
            n = n+1

        n = 0
        for pt in pts:
            bound = [(pt[0]-2, pt[1]-2), (pt[0]+2, pt[1]+2)]
            self._draw.arc(bound, 0, 360, fill="yellow")
            if n == self._active_pt:
                marker = [(pt[0] - 1, pt[1] + 6), (pt[0] + 1, pt[1] - 6)]
                self._draw.rectangle(marker, "red")
            n = n + 1

        self._draw.line(pts, "white", 2)
        self._draw.line([(x_start, y_start), (12*dx+5, y_start)], "gray", 2)
        self._TFT.display()

    def inc_selected(self, dir):
        if dir == 1:
            self._active_pt = self._active_pt + 1
            if self._active_pt == 13:
                self._active_pt = 0
        if dir == -1:
            self._active_pt = self._active_pt - 1
            if self._active_pt < 0:
                self._active_pt = 12

    def start(self):
        print("Stroke adjustment start")
        TFT = self._TFT
        while self._running == 1:
            while not TFT.penDown():
                pass
            pos = TFT.penPosition()

            if self.prev_pt_btn.check_pos(pos) == 1:
                self.inc_selected(-1)
                self.redraw()
            if self.next_pt_btn.check_pos(pos) == 1:
                self.inc_selected(1)
                self.redraw()

            if self.adj_p_btn.check_pos(pos) == 1:
                self._wf[self._active_pt] = self._wf[self._active_pt] + 1
                self.redraw()
            if self.adj_n_btn.check_pos(pos) == 1:
                self._wf[self._active_pt] = self._wf[self._active_pt] - 1
                self.redraw()
            sleep(.1)
