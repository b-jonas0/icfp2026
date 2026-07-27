#!python3

import sys, re, os;
def die(pat, *pla):
    msg = pat % pla
    raise RuntimeError(msg)
def warn(pat, *pla):
    msg = pat % pla
    print(msg, file = sys.stderr, flush = True)
os.chdir("/home/ambrus/a/verseny/icfp/2026")

"""
Sort using a sorting network made of minmax blocks that sort 2 inputs to 2 outputs.
"""

minmax_tpl = [
b"+-----+  ",
b"| >+>v|  ",
b"|>X+ v|  ",
b"|-+  s|>>",
b"|rW  W|  ",
b"| > ^ |  ",
b"|W    |  ",
b"|r   s|  ",
b"|^  @<|>>",
b"+-----+  ",
]
id_tpl = [
b"         ",
b"         ",
b"         ",
b">>>>>>>>>",
b"         ",
]

starttop_tpl = [
b"+-+       ",
b"|I|>v     ",
b"+-+ v     ",
b"+------+  ",
b"|>   sv|>>",
b"| v@< 9|  ",
b"| 7   M|  ",
b"|bM   1|  ",
b"|+9   {|  ",
b"|r*   {|  ",
b"|MM   M|  ",
b"|{1    |  ",
b"|^<    |  ",
]
start_tpl = [
b"|     m|  ",
b"|    vd|  ",
b"|    Wr|  ",
b"|    ss|>>",
b"|    M |  ",
]
startbot_tpl = [
b"|   ^<<|  ",
b"+------+  ",
]

endtop_tpl = [
b"  +-+",
b">>|O|",
b"^ +-+",
b"+---+",
b"|v@<|",
b"|r  |",
b"|b  |",
b"|   |",
b"|   |",
b"|   |",
b"|   |",
b"|   |",
b"|   |",
]
end_tpl = [
b"|   |",
b"|m  |",
b"|av |",
b"|rr |",
b"|s  |",
]
endbot_tpl = [
b"|>>^|",
b"+---+",
]

block_height, block_width = 5, 9
if block_height != len(id_tpl): die("id height")
if 2 * block_height != len(minmax_tpl): die("minmax height")
if block_height != len(start_tpl): die("start height")
if block_height != len(end_tpl): die("end height")
if len(starttop_tpl) != len(endtop_tpl): die("top height")
if len(startbot_tpl) != len(endbot_tpl): die("top height")
start_width = len(start_tpl[0])
end_width = len(end_tpl[0])
prog_mid = []
inputlen = 16
#inputlen = 6 # debug
for yo in range(inputlen):
    for tpl_row in id_tpl:
        if block_width != len(tpl_row): die("id width")
        row = bytearray(tpl_row * (inputlen * 2 - 3))
        prog_mid.append(row)
for xo in range(inputlen * 2 - 3):
    cnt_box = (min(1 + xo, inputlen * 2 - 3 - xo) + 1) // 2
    bot_box = inputlen - 2 - (xo % 2)
    x = xo * block_width
    for co in range(cnt_box):
        yo = bot_box - 2 * co
        for yi, tpl_row in enumerate(minmax_tpl):
            if block_width != len(tpl_row): die("minmax width")
            y = yo * block_height + yi
            prog_mid[y][x : x + block_width] = tpl_row
outputf = open("solve/s1e4-tmp.man", "wb")
for start_row, end_row in zip(starttop_tpl, endtop_tpl):
    if start_width != len(start_row): die("starttop width %r %r", start_width, start_row)
    if end_width != len(end_row): die("endtop width")
    outputf.write(start_row + start_row[-1 :] * len(prog_mid[0]) + end_row + b"\n")
for y, mid_row in enumerate(prog_mid):
    ym = y % block_height
    start_row = start_tpl[ym]
    if start_width != len(start_row): die("start width")
    end_row = end_tpl[ym]
    if end_width != len(end_row): die("end width")
    outputf.write(start_row + mid_row + end_row + b"\n")
outputf.flush()
for start_row, end_row in zip(startbot_tpl, endbot_tpl):
    if start_width != len(start_row): die("starttop width")
    if end_width != len(end_row): die("endtop width")
    outputf.write(start_row + b" " * len(prog_mid[0]) + end_row + b"\n")
outputf.close()






