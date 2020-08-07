#!/usr/bin/env python3

import bgb_link
from io import BufferedReader
from typing import List
hs: int
ack: int
menu: int
trade: int
colosseum: int
cancel: int
preamble: int
trade_data: int
done: int

# load program to run
fp: BufferedReader = open("./asm/hello/hello.bin", "rb")
program_str: bytes = fp.read()
fp.close()
program: List[int] = list(program_str)

hs, ack, menu, trade, colosseum, cancel, preamble, trade_data, done = list(
    range(9))
state: int = hs
counter = 0

data = []

# seed
data += [182, 147, 113, 81, 51, 23, 228, 205, 184, 165]

# preamble
data += [253, 253, 253, 253, 253, 253, 253, 253]

# party (bootstrap)
party = [248, 0, 54, 253, 1, 62, 88, 197, 195, 0xd6, 0xc5, 6, 21, 21, 21, 21, 21, 21, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227,
         227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 227, 206, 227, 227, 255, 33, 160, 195, 1, 136, 1, 62, 0, 205, 224, 54, 17, 24, 218, 33, 89, 196, 205, 85, 25, 195, 21, 218, 139, 142, 128, 131, 136, 141, 134, 232, 232, 232, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 64, 0, 0]
data += party

# preamble
data += [253, 253, 253, 253, 253]

# patchlist (196 bytes total)
patchlist: List[int] = [255, 255] + program + ([0] * 200)
patchlist: List[int] = patchlist[:196]
data += patchlist

party_and_patchlist: str = ", ".join(
    map(str, party + [253, 253, 253, 253, 253] + patchlist))
print("pokemonspoof.h contents...")
print("unsigned char DATA_BLOCK[619] = {" + party_and_patchlist + "};")


def cable_club(byte):
    global state, hs, ack, menu, trade, colosseum, cancel, trade_data

    if state == hs:
        if byte == 0x01:
            state = ack
            print("Connection established")
            return 0x02

    elif state == ack:
        if byte == 0x00:
            state = menu
            print("Menu")
            return 0x00

    elif state == menu:
        # 0xd0 trade
        # 0xd4 trade selected
        if byte == 0xd4:
            print("Trade Center")
            state = trade
            return byte
        else:
            return byte

    elif state == trade:
        if byte == 0xfd:
            state = preamble
        return byte

    elif state == preamble:
        if byte != 0xfd:
            print("Sending data...")
            state = trade_data
            return exchange_parties(byte)
        return byte

    elif state == trade_data:
        # 0xfd = Preamble byte for array
        # 0xfe = No data
        return exchange_parties(byte)

    return byte


def exchange_parties(byte):
    global counter, data, state, done
    if counter < len(data):
        ret = data[counter]
        counter += 1
        return ret
    else:
        state = done
        print("Done.")
    return byte


bgb_link.connect(8765, cable_club)
