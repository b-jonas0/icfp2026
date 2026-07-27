#!python3

import sys, re, os;
os.chdir("/home/ambrus/a/verseny/icfp/2026")

"""
This program writes the main loop for the s1e2 Memory problem.
I'm writing the rest of the program in the organizers' editor.

The value of each memory cell ping-pongs on two pipes between two rooms.
We can't use just one room because pipes from a room to itself are forbidden in Littleman.
since we need two rooms, we might as well make use of both.
So the top room is responsible for memory writes and the bottom for reads.
For each read or write entry in the input, 
we run a full loop of both the write and read rooms,
sending each memory cell down and up.

The long write room gets an address from the right, which is -1 for a read instruction,
then it gets a data from the right but only for a write instruction.
The long read room gets an address from the right, then always writes data read to the right.

Within long rooms, the off-hand stores the data to write or the data read, 
and the backpack counts down to the address.
The row marked with s copies cells before the one we write;
the row marked with c copies cells after the one we write;
the row marked with r and w respectively does the read and write.
The row marked with i writes the initial zero values.

It should be possible to improve this solution by splitting the address space
and having a pair of long rooms for each chunk.
This would make the solution more square-shaped, 
but also faster because the men on the long rooms wouldn't have to do
an 800 cycle long full memory copy for each entry,
instead each man would be responsible for fewer memory cells.
However, it's a better use of my time to solve other tasks than to optimize this.

At one point the repeated instruction sequence said "sram".
I felt that was very appropriate for implementing RAM cells.
"""

tpl0 = [
b"   mmmm                 ",
b" +----------------+     ",
b"i|v s  0@<        |addr ",
b" |>    9M7*M1{Mr+v|<<<<<",
b"s| sarm      Mrab<|<<<<<",
b"w|  W             |data ",
b"c|^s<r         <  |write",
b" +----------------+     ",
b"    v^u                 ",
b"    v^                  ",
b" +----------------+     ",
b"s| asrm     M0b+r<|<<<<<",
b"r| W       >M1{M ^|addr ",
b"c|v<sr @<  ^*7M9 <|data ",
b" |>            Ws^|>>>>>",
b" +----------------+read ",
#b" |                |     ",
]

outputf = open("solve/s1e2-tmp.man", "wb")
repeat_col0, repeat_col1 = tpl0[0].index(b"m"), tpl0[0].rindex(b"m") + 1
repeat_cnt = 100
for tpl_row in tpl0[1 :]:
    rowb = bytearray(tpl_row[: repeat_col0])
    rowunit = tpl_row[repeat_col0 : repeat_col1]
    for repeat_ind in reversed(range(repeat_cnt)):
        rowb += rowunit.replace(b"u", bytes([ord("0") + repeat_ind // 10]) if 0 == repeat_ind % 10 else b" ")
    rowb += tpl_row[repeat_col1 :] + b"\n"
    outputf.write(rowb)
outputf.close()



