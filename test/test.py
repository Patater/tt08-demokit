# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer
import math

@cocotb.test()
async def test_sine(dut):
    dut._log.info("Test sine behavior")
    sine = dut.user_project.waggle_demo.xsine

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    def sine_test(angle):
        sine_lut = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29,
            31, 33, 35, 37, 39, 41, 43, 45, 46, 48, 50, 52, 54, 56, 58, 60, 62,
            64, 66, 68, 70, 72, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 92, 94,
            96, 98, 100, 102, 104, 105, 107, 109, 111, 113, 115, 116, 118, 120,
            122, 124, 126, 127, 129, 131, 133, 135, 136, 138, 140, 142, 143,
            145, 147, 149, 150, 152, 154, 156, 157, 159, 161, 162, 164, 166,
            167, 169, 171, 172, 174, 176, 177, 179, 181, 182, 184, 185, 187,
            189, 190, 192, 193, 195, 196, 198, 199, 201, 203, 204, 206, 207,
            209, 210, 211, 213, 214, 216, 217, 219, 220, 222, 223, 224, 226,
            227, 229, 230, 231, 233, 234, 235, 237, 238, 239, 241, 242, 243,
            244, 246, 247, 248, 249, 251, 252, 253, 254, 255, 257, 258, 259,
            260, 261, 262, 263, 264, 266, 267, 268, 269, 270, 271, 272, 273,
            274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 284, 285,
            286, 287, 288, 289, 290, 290, 291, 292, 293, 294, 294, 295, 296,
            297, 297, 298, 299, 299, 300, 301, 301, 302, 303, 303, 304, 305,
            305, 306, 306, 307, 307, 308, 308, 309, 309, 310, 310, 311, 311,
            312, 312, 313, 313, 313, 314, 314, 314, 315, 315, 315, 316, 316,
            316, 317, 317, 317, 317, 318, 318, 318, 318, 318, 318, 319, 319,
            319, 319, 319, 319, 319, 319, 319, 319, 319, 319]
        return sine_lut[angle]

    async def sine_dut(angle):
        sine.x.value = angle
        # Wait a bit for the input value to be processed
        await ClockCycles(dut.clk, 2)
        return sine.xout.value.signed_integer

    expected = [sine_test(angle) for angle in range(0, 256)]
    actual = [await sine_dut(angle) for angle in range(0, 256)]

    for i,angle in enumerate(expected):
        #dut._log.info(f"Checking xsine({i}) is {angle}")
        #dut._log.info(f"\tGot {actual[i]}")
        assert actual[i] == angle

@cocotb.test()
async def test_palette(dut):
    dut._log.info("Test palette behavior")
    palette = dut.user_project.palette_inst

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    def color_to_rrggbb(color):
      if color >= 0 and color < 14:
          return 0b110000
      if color >= 14 and color < 28:
          return 0b110100
      if color >= 28 and color < 43:
          return 0b111000
      if color >= 43 and color < 57:
          return 0b111100
      if color >= 57 and color < 71:
          return 0b101100
      if color >= 71 and color < 85:
          return 0b011100
      if color >= 85 and color < 100:
          return 0b001100
      if color >= 100 and color < 114:
          return 0b001101
      if color >= 114 and color < 128:
          return 0b001110
      if color >= 128 and color < 142:
          return 0b001111
      if color >= 142 and color < 156:
          return 0b001011
      if color >= 156 and color < 171:
          return 0b000111
      if color >= 171 and color < 185:
          return 0b000011
      if color >= 185 and color < 199:
          return 0b010011
      if color >= 199 and color < 213:
          return 0b100011
      if color >= 213 and color < 228:
          return 0b110011
      if color >= 228 and color < 242:
          return 0b110010
      if color >= 242 and color < 256:
          return 0b110001

    async def color_to_rrggbb_dut(color):
        palette.color.value = color
        # Wait a bit for the input value to be processed
        await ClockCycles(dut.clk, 2)
        return palette.rrggbb.value

    expected = [color_to_rrggbb(x) for x in range(0, 256)]
    actual = [await color_to_rrggbb_dut(x) for x in range(0, 256)]

    for i,x in enumerate(expected):
        #dut._log.info(f"Checking color index {i} is {x}")
        assert actual[i] == x

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)

    dut._log.info("Check reset values")
    assert dut.uio_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Set the input values you want to test
    dut.ui_in.value = 0
    dut.uio_in.value = 0

    # Wait for some clock cycles to see the output values
    await ClockCycles(dut.clk, 200)

    assert dut.uo_out.value == 0b01000101
