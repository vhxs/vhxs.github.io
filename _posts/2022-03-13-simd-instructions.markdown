---
layout: post
title: SIMD instructions
tags: simd, hardware, rpi, perf
published: true
---

SIMD stands for single instruction, multiple data. This is a way of implementing parallelism by issuing one instruction to multiple points of data, for example adding one vector to another (with the addition instruction being common across multiple vector elements). Modern x86 processors (like those sold by Intel) support SIMD instructions like SSE, AVX2, and AVX512. These instructions require some kind of hardware support. For processors that support such instructions, it call be a useful way for extracting parallelism from it, especially when the task to be executed on the processor is easily parallelizable, such as convolution operators found in CNNs. It's easy to discuss and understand in theory, but how do you actually *use* it in practice?

Stackoverflow tech blog post about SIMD instructions: [link](https://stackoverflow.blog/2020/07/08/improving-performance-with-simd-intrinsics-in-three-use-cases/)

Raspberry Pis are cheap devices that have most of the functionality of personal computers. They're used a lot for educational purposes. But they have a different architecture (they're ARM, not x86) than Intel processors, so they have a different instruction sets as well. This includes what SIMD instructions there are made available by the hardware and microarchitecture.

ARM's tutorial on how to utilize SIMD:
[link](https://developer.arm.com/documentation/102467/0100)

Intended audience:
> Low-level software engineers, library writers, and other developers wanting to use Advanced SIMD technology will find this guide useful.

Challenge accepted

It looks like ARM Neon is the name of the architecture extensions that provide SIMD on certain ARM processors including those on RPis. Let's see if we can find the relevant header file on my RPi.

```
pi@raspberrypi:~ $ mlocate arm_neon.h
/usr/lib/gcc/aarch64-linux-gnu/8/include/arm_neon.h
```

So `arm_neon.h` exists as a header file on my RPi. AArch64 is (more or less, don't take my word for it) synonymous with ARM64, and `arm_neon.h` is C header file through which Neon intrinsics are accessible.

```
#include "arm_neon.h"

int main(void) {
    return 0;
}
```

This program compiles successfully with `gcc`, so the header file was probably included successfully?

ARM's developer page linked above provides a couple of example functions that use Neon SIMD extensions in order to vectorize them. One of them takes an array of interleaved RGB values as illustrated on ARM's page:

![RGB](https://documentation-service.arm.com/static/606449625f0ba621d5d587b4?token=)

and uses SIMD instructions as shown below to de-interleave the array:

```
void rgb_deinterleave_neon(uint8_t *r, uint8_t *g, uint8_t *b, uint8_t *rgb, int len_color) {
    /*
     * Take the elements of "rgb" and store the individual colors "r", "g", and "b"
     */
    int num8x16 = len_color / 16;
    uint8x16x3_t intlv_rgb;
    for (int i=0; i < num8x16; i++) {
        intlv_rgb = vld3q_u8(rgb+3*16*i);
        vst1q_u8(r+16*i, intlv_rgb.val[0]);
        vst1q_u8(g+16*i, intlv_rgb.val[1]);
        vst1q_u8(b+16*i, intlv_rgb.val[2]);
    }
}
```

Above, it looks to me like `vld3q_u8` loads three, 16-wide registers from a C array in memory (`v` for vector, `ld` for load, `3q` for 3 quad, and `u8` being type `uint8_t`). Similary, I think that `vst1q_u8` stores data from a single 16-wide register into a C array (`st` for store).

Here, the "single instruction"s being applied to "multiple data" are load and store operations being applied to 16 elements simultaneously.

The point of SIMD instructions and architectures are as another way of achieving parallelism through hardware that supports it, and so one would hope that they would observe some kind of speedup after vectorizing a function with SIMD. I took the example code from the ARM developer page, added a few time measurements (see code snippet [here](https://gist.github.com/vhxs/14526f782dc80f34158b79dd7cec738e) compiled with `gcc -o3 rgb.c -o exe_rgb_o3`), and checked whether I saw any speedup. On 500 RGB arrays each of size 3 x 65536, I get the following timing results:

```
pi@raspberrypi:~ $ ./exe_rgb_o3 500 65536
Without SIMD: 0.593816
With SIMD: 0.180591
```

So the SIMD implementation is a bit over 3x faster. Does this change at all if we remove the `O3` compiler optimization flag?

```
pi@raspberrypi:~ $ gcc rgb.c -o exe_rgb
pi@raspberrypi:~ $ ./exe_rgb 500 65536
Without SIMD: 0.577297
With SIMD: 0.182808
```

Not really.

How does this speedup vary as we vary the length of the RGB array? Using this script, let's try executing this code ranging over arrays of size 1 through 1048576, in powers of 2, and see what we get:

```
import subprocess
import matplotlib.pyplot as plt

sizes = [2**n for n in range(17)]
speedups = []
for s in sizes:
    output = subprocess.run(["./exe_rgb_o3", "500", f"{s}"], capture_output=True)
    lines = output.stdout.decode("utf-8").split('\n')
    no_simd = float(lines[0].split()[2])
    with_simd = float(lines[1].split()[2])
    speedups.append(no_simd / with_simd)

plt.plot(sizes, speedups)
plt.xscale("log")
plt.xlabel("Array size")
plt.ylabel("Speedup")
plt.title("Speedup obtained from SIMD")
plt.savefig("speedups.png")
```

![SIMD speedup](/assets/images/simd_speedups.png)

Seems clear to me that the maximum speedup we could possibly get from running this code is 16x, since we're using vector registers of length 16. In most cases it looks like we get a speedup somewhere between 3x and 4x. I have to wonder what's goin on with array size 8 though, why is the speedup (~6x) so much higher? What if we regenerate the same plot, except with array sizes [*4, 5, 6, 7,* __8__, *9, 10, 11, 12*]?

![SIMD speedup 2](/assets/images/simd_speedups2.png)

Interesting, so speedup keeps increasing past an array size of 8! What if we zoom out a bit more, how high does it go and when does speedup drop off again?

![SIMD speedup 3](/assets/images/simd_speedups3.png)

So speedup reaches a bit over 10x, then drops off when the array size is 16. Moreover, speedup increases linearly until about an array size of 32, then falls again. This doesn't seem like a coincidence, considering peaks seem to occur around multiples of 16, which is the size of our vector registers. Each time we cross a multiple of 16, we need to use one more vector operation to process the entire array, though I don't know whether I have an explanation for why speedup drops all the way to 3-4x when this happens. I'm sure a computer architect would be able to provide a much more complete answer.

In the above example, it's load and store operations that are vectorized, but there are also SIMD operations that vectorize arithimetic operations like addition. The second example on ARM's page is on [matrix multiplication](https://developer.arm.com/documentation/102467/0100/Matrix-multiplication-example). Vectorized matrix multiplication looks like it uses `vfmaq_laneq_f32`, where `fma` stands for fused multiply-add, or any operation that can be written as $$a + (b \times c)$$. Dot products are multiplications followed by additions, so FMAs are convenient for implementing linear algebra functions. Libraries like `numpy` use vectorized FMA and other operations, as can be seen explicitly by looking at its source code here: [github code pointer](https://github.com/numpy/numpy/blob/623bc1fae1d47df24e7f1e29321d0c0ba2771ce0/numpy/core/src/common/simd/neon/arithmetic.h#L244).

If I have time to return to screw around with more SIMD operations, it would be interesting to collect some performance numbers on SIMD'ized matrix multiplication and see whether they reflect what we saw with vectorized deinterleaving.