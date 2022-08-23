---
layout: post
title: CUDA and Nvidia GPUs
tags: gpu, cuda
published: true
---

GPU architectures are complex. People write PhD theses about how to use them optimally. This is an attempt to demystify them.

## Links

- https://cs.nyu.edu/manycores/cuda_many_cores.pdf
- https://www.youtube.com/watch?v=SrAMBi_8tIk&list=PLFtDTZgdIZy5n8LWmhTic07zTN3hJQVfy
- https://www.youtube.com/watch?v=lGefnd7Fmmo&list=PLFtDTZgdIZy5n8LWmhTic07zTN3hJQVfy&index=4
- https://nyu-cds.github.io/python-gpu/02-cuda/
- https://en.wikipedia.org/wiki/Thread_block_(CUDA_programming)
- https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/
- https://stackoverflow.com/a/10467342
- https://www3.nd.edu/~zxu2/acms60212-40212-S16/Lec-11-GPU.pdf
- http://15418.courses.cs.cmu.edu/spring2017/lecture/gpuarch/slide_004
- https://cvw.cac.cornell.edu/GPUarch/threadcore
- https://kdm.icm.edu.pl/Tutorials/GPU-intro/introduction.en/
    - I think this cheatsheet is best read after you understand a GPU's architecture and terminology.

## Terminology

- *CUDA* is Nvidia's proprietary API to execute code on their GPUs.
- *kernels* are CUDA programs that run on Nvidia GPUs.
- CPUs are *hosts*, GPUs are *devices*.
- Blocks contain threads. Threads in a block can have 1d, 2d, or 3d indexes.
- Grids contain blocks. Blocks in a grid can have 1d, 2d, or 3d indexes.
- Streaming multiprocessors (SM) are made up of cores.
- Streaming multiprocessor execute blocks. An entire block must be run on a single SM.
- Warps always have 32 threads. A block is executed as several warps.
- A warp consists of lanes (term doesn't seem to be used a lot though).
- The GPU is responsible for allocating thread blocks to SMs.
- Nvidia has changed the definition of "core" over time for marketing purposes.

## Concepts
- Programmer writes CUDA kernel. As part of writing kernel, they specify grid and block dimensions
  - How many blocks per grid? How many threads per block?
- The GPU will take these blocks, and allocate them across streaming multiprocessors
  - One block gets mapped to a single SM. No spreading threads in a block across SMs.
  - To execute a block, an SM will further divide threads in a block into warps. Warps are currently all of size 32 across all GPUs.
  - One thread is scheduled to run on a single core. So a warp requires 32 cores to run. Number of cores in an SM is a multiple of 32.
  - Depending on number of blocks, there could be several blocks allocated to a single SM. They are executed in sequence.
  - SM can context switch between active warps, say if a warp is waiting on a memory access to complete. It may schedule another warp that is ready to run.
  - Warp scheduling: https://www.cc.gatech.edu/fac/hyesoon/gputhread.pdf
- How to choose grid and block dimensions https://stackoverflow.com/a/9986748
  - > There are people writing PhD theses around the quantitative analysis of aspects of the problem
- `float` computation is much faster on GPUs than `double` computation. For some reason.

## GPU example
- I have an Nvidia GeForce GTX 1660 Ti.
- I learned this by running `nvidia-smi --query-gpu=name --format=csv`.
- Article on this particular GPU: https://www.nvidia.com/en-us/geforce/news/geforce-gtx-1660-ti-advanced-shaders-streaming-multiprocessor/
  - Turing architecture.
  - This GPU has 24 streaming multiprocessors and 1536 cores total (so 64 cores per SM).

## Code examples
- Vector addition: https://gist.github.com/vhxs/5bc0f4a00050ff277c43248a382e680f
- Matrix multiplication: https://github.com/vhxs/matrix-cuda
- More to come