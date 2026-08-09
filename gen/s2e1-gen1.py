#!python3

import sys, re, os, itertools
def die(pat, *pla):
    msg = pat % pla
    raise RuntimeError(msg)
def warn(pat, *pla):
    msg = pat % pla
    print(msg, file = sys.stderr, flush = True)
os.chdir("/home/ambrus/a/verseny/icfp/2026")

output_s = open("pubtest/s2e1-o0-lit.txt", "rb").read()
re.fullmatch(b"[ -~]+", output_s)
src_v = []
oind, ochunk_len = 0, 4
while oind < len(output_s):
    ochunk = output_s[oind : oind + ochunk_len]
    ochunk += b" " * (ochunk_len - len(ochunk))
    src_num = 0
    for oc in reversed(ochunk):
        if not 32 <= oc < 131:
            die("output byte out of range %d", oc)
        src_num = src_num * 99 + oc - 32
    if not 0 <= src_num < 10**8:
        die("source numeric literal out of range")
    src_chunk = b"`%08d`s" % src_num
    if 11 != len(src_chunk):
        die("source code chunk length wrong: %d %r", len(src_chunk), src_chunk)
    src_v.append(src_chunk)
    oind += ochunk_len
src_len = len(src_v)
warn("src chunk count: %d", src_len)

min_diam, best_netwd, best_netht = 9e9999, None, None
for netwd in range(1, 20):
    grosswd = 11 * netwd + 5
    netht = -(src_len // -netwd)
    grossht = netht + 6
    diam = max(grossht, grosswd)
    if diam <= min_diam: 
        min_diam, best_netwd, best_netht = diam, netwd, netht
warn("paginate: %s %s %s %s %s", best_netwd, best_netht, best_netwd*best_netht, src_len, min_diam)

sys.stdout.flush()
outputf = open("solve/s2e1-tmp.man", "wb")
outputf.write(b"+" + b"-" * (11 * best_netwd + 3) + b"+\n")
prog_v = []
ind, parity = 0, False
while ind < src_len:
    src_chunk = src_v[ind : ind + best_netwd]
    prog_row_mid = (b" " if 0 < ind else b"@") + b"".join(src_chunk).ljust(11 * best_netwd)
    prog_row = None
    if not parity: 
        prog_row = b"|>" + prog_row_mid + b"v|\n"
    else:
        prog_row = b"|v" + prog_row_mid[::-1] + b"<|\n"
    ind += best_netwd
    if src_len <= ind:
        prog_row = bytearray(prog_row)
        if parity:
            prog_row[1 : 2] = b"H"
        else:
            prog_row[len(prog_row) - 3 : len(prog_row) - 2] = b"H"
    parity = not parity
    outputf.write(prog_row)
outputf.flush()
outputf.write(b"+" + b"-" * (11 * best_netwd + 3) + b"+\n")
prog_tail = [
b"+-+<----------<+------+ v+----------------------+             ",
b"|O|+--------+  |v@<s+<| >|v        sW/WrsW/WrsW<|  +---------+",
b"+-+|@5M1{>s<|>>|>rW r^|<<|>@r         WrW/WsrW/^|<<|@9M*++>s<|",
b"   +--------+  +------+  +----------------------+  +---------+",
]
for prog_row in prog_tail:
    outputf.write(prog_row + b"\n")
outputf.flush()

warn("all done;")
