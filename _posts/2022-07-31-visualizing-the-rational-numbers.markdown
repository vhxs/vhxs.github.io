---
layout: post
title: Visualizing Rational and Algebraic Numbers
date: 2022-07-31
tags: polynomials, algebraics, opengl, graphics, visualization
published: true
---

The rational numbers $$\mathbb{Q}$$ are those of the form $$a / b$$ for $$a, b \ne 0 \in \mathbb{N}$$, and are a dense subset of $$\mathbb{R}$$. This is to say that the closure of $$\mathbb{Q}$$ is $$\mathbb{R}$$, or that any real number can be approximated with arbitrary precision by a sequence of rational numbers.

Because the rationals are dense, visualizing them by plotting all of them on the real line would just cover the entire line, if each rational point is given the same, nonzero volume. However, the rational numbers *can* be [covered by an open set of finite volume](https://math.stackexchange.com/questions/195313/open-cover-rationals-proper-subset-of-r) if, for example, we enumerate the rationals $$\mathbb{q}_0, \mathbb{q}_1, \mathbb{q}_2, \ldots$$, and cover each $$q_i$$ by an open set $$\mathcal{O}_i$$ of volume $$\mu(\mathcal{O}_i) = 2^{-i}$$. By countable subadditivity, the volume of all the $$\mathcal{O}_i$$ is bounded by $$1 + \frac{1}{2} + \frac{1}{4} + \ldots = 2$$. In general, you can choose $$\mathcal{O}_i$$ so that the sum of their volumes converges.

To turn this observation into a visualization of the rational numbers, I focused just on the unit square $$[0, 1] \times [0, 1]$$, since all of $$\mathbb{R}$$ is infinite and I can't draw something infinite. For each rational point $$(i / k, j / k)$$ in the unit square, I drew a square of side length proportional to $$k^{-1.6}$$. If you do the math for each $$k$$, the squares have a total volume proportional to $$k^2 / k^{3.2} = k^{-1.2}$$, which is a convergent series if you sum over $$1 \le k < \infty$$.

Here's [Python code](https://gist.github.com/vhxs/4cf0e7def3f287268b8978ca6a9f879e) (using Tkinter) I used to draw such a visualization, for $$k$$ up to $$75$$, and here's the result:

![very green](/assets/images/rationals.png)

The smaller the square, the darker it's colored.

My attempt to visualize the rational numbers was actually inspired by this visualization of the *algebraic* numbers I saw on wikipedia (I did *not* make this):

![bright lights](https://upload.wikimedia.org/wikipedia/commons/d/d1/Algebraicszoom.png)

I'd found partial C and OpenGL source code, posted by the author here way back in 2011: [link](https://en.wikipedia.org/wiki/User:Stephen_J._Brooks/algebraics/src). This code was missing dependencies and was written in an older version of OpenGL, so I couldn't just compile it and run it off the shelf. So I rewrote it in Go, and used Go's bindings for the latest version of OpenGL. This wasn't easy since I didn't know OpenGL, and OpenGL's programming model has changed substantially since the original code was written. 

My source code here: [link](https://github.com/vhxs/algebraics-viz/blob/master/cmd/algebraics/main.go). This is the closest I got (I made this):

![almost bright lights](/assets/images/algebraics.png)

Not too bad! They almost look the same. The only things I'm missing here are correct texturing and the right zoom level.

The algebraic numbers are dense in $$\mathbb{C}$$, and the algebraic closure of $$\mathbb{Q}$$ in $$\mathbb{C}$$ when regarded as fields. More specifically, the algebraics are all those that are roots of some polynomial with integer coefficients. For example, $$\sqrt{2}$$ is [not rational](https://proofwiki.org/wiki/Square_Root_of_2_is_Irrational#:~:text=2%E2%88%96q2%E2%9F%B9,%E2%88%9A2%20cannot%20be%20rational.), but it is algebraic since it's a root of $$x^2 - 2$$. So is $$i$$ which is a root of $$x^2 + 1$$. But [we don't even know](https://math.stackexchange.com/questions/159350/why-is-it-hard-to-prove-whether-pie-is-an-irrational-number) whether $$\pi + e$$ is algebraic, or even whether it's rational.

As complex numbers, the algebraics have real and imaginary parts, so can be drawn in a plane. To generate the points in the visualization above, we first enumerate all integer polynomials by their *length*. The [length of a polynomial](https://en.wikipedia.org/wiki/Height_function#Height_of_a_polynomial) is the sum of the absolute value of its coefficients. Given a length $$L > 0$$, there are finitely many integer polynomials with length $$L$$. Then using Newton's method, we can factor the polynomial, find all its roots, and plot these roots on the complex plane as above.

This is how the visualization above is created. The size of the point is inversely proportional to the length of the polynomial it's a root of, and the color is determined by the degree of the polynomial. I drew roots for polynomials up to height $$12$$.

[Vulkan](https://www.vulkan.org/) is the apparent successor to OpenGL and it seems like the consensus online now is to learn Vulkan if you want to get into computer graphics. It would be interesting to try rewriting this using Vulkan and see how far I get.

Things that helped me do this:
- [OpenGL book](https://learnopengl.com/book/book_pdf.pdf)
- [Hello triangle in Golang](https://github.com/cstegel/opengl-samples-golang/blob/master/hello-triangle/hello_triangle.go) (Hello triangle is like the Hello world of graphics)
- [Drawing circles using triangle fans](https://stackoverflow.com/questions/59468388/how-to-use-gl-triangle-fan-to-draw-a-circle-in-opengl)
- [Coloring vertex array objects (VAOs) using shaders](https://mathweb.ucsd.edu/~sbuss/MathCG2/OpenGLsoft/SimpleDrawModern/explainSDM.html)