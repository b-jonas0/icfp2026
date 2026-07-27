#!python3

import sys, re, os;
def die(pat, *pla):
    msg = pat % pla
    raise RuntimeError(msg)
def warn(pat, *pla):
    msg = pat % pla
    print(msg, file = sys.stderr, flush = True)
os.chdir("/home/ambrus/a/verseny/icfp/2026")

output_s = open("pubtest/s2e1-o0-lit.txt", "rb").read()
re.fullmatch(b"[ -~]+", output_s)
instr_seq_m = bytearray(b"@")
for c in output_s:
    cs = c - 27
    ch, cl = divmod(cs, 10)
    if not (0 <= ch <= 9 and 0 <= cl <= 9): die("out of bounds")
    instr_seq_m += bytes([ord("0")+ch, ord("s"), ord("0")+cl, ord("s")])
instr_seq_m += b"H"
instr_seq = bytes(instr_seq_m)
instr_len = len(instr_seq)
instr_seq_s = instr_seq.decode()
warn("instr: %s:::%s %s", instr_seq_s[: 20], instr_seq_s[-20 :], len(instr_seq))

min_diam, best_netwd, best_netht = 9e9999, None, None
for netwd in range(50, 200):
    grosswd = netwd + 4
    netht = -((instr_len - 2) // -netwd)
    grossht = netht + 6
    diam = max(grossht, grosswd)
    if diam <= min_diam: 
        min_diam, best_netwd, best_netht = diam, netwd, netht
warn("paginate: %s %s %s %s %s", best_netwd, best_netht, best_netwd*best_netht, instr_len, min_diam)

ind, parity = 0, False
sys.stdout.flush()
outputf = open("solve/s2e1-tmp.man", "wb")
outputf.write(b"+" + b"-" * (best_netwd + 2) + b"+\n")
while ind < instr_len:
    instr_chunk = instr_seq[ind : ind + best_netwd]
    ind += best_netwd
    prog_row = None
    if not parity: 
        prog_row = b"|>" + instr_chunk.ljust(best_netwd) + b"v|\n"
    else:
        prog_row = b"|v" + instr_chunk[::-1].rjust(best_netwd) + b"<|\n"
    outputf.write(prog_row)
    parity = not parity
outputf.flush()
outputf.write(b"+" + b"-" * (best_netwd + 2) + b"+\n")
prog_tail = [
b"    v+-----------+",
b"+-+ >|>@5M+Mr*Mrv|",
b"|O|<<|^s+++W9M +<|",
b"+-+  +-----------+",
]
for prog_row in prog_tail:
    outputf.write(prog_row + b"\n")
outputf.flush()

warn("all done;")
