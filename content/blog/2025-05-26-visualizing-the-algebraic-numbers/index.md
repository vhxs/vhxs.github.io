---
title: Visualizing the Algebraic Numbers
author: Vikram Saraph
date: "2025-04-12"
tags:
  - numbers
  - algebra
  - combinatorics
  - visualization
---

## What are the Algebraic Numbers?

The [algebraic numbers](https://mathworld.wolfram.com/AlgebraicNumber.html) are complex numbers that are solutions of polynomial equations with integer coefficients. For example, \(\sqrt{2} \) is algebraic because it satisfies \( x^2 - 2 = 0 \), while the number \( \pi \) is not algebraic (it's [transcendental](https://en.wikipedia.org/wiki/Transcendental_number)) since it's not a root of any integer polynomial you can imagine. They form a subfield of the complex numbers, so they're closed under addition, subtraction, multiplication, and division. Furthermore, the rational numbers are a subfield of the algebraic numbers, since the rational number \( a / b \) is a root of the linear integer polynomial \( bx - a = 0 \).

You'd probably learn about the algebraic numbers when taking an advanced undergraduate course in abstract algebra. That's when I learned about them, and I was particularly fascinated by them after seeing [this cool visualization of them on Wikipedia](https://en.wikipedia.org/wiki/Algebraic_number#/media/File:Algebraicszoom.png). Generally speaking, there isn't a straightfoward way to visualize them; for example, if you drew a dot at each algebraic number on the complex plane, you'd fill up
the whole plane, since algebraic numbers are [_dense_](https://en.wikipedia.org/wiki/Dense_set) in the complex numbers. And that wouldn't make for a very interesting visualization, would it?

[Stephen J. Brooks](https://en.wikipedia.org/wiki/User:Stephen_J._Brooks), the Wikipedia user who developed this visualization, decided to do something much more creative instead. A snippet of the C and OpenGL source code used to create the visualization is included in the image's [metadata](https://en.wikipedia.org/wiki/User:Stephen_J._Brooks/algebraics/src), though it's not self-contained enough to just copy, compile, and run, and it's light on details of what the code is doing or how it works.

This blog post is my attempt at demystifying the original visualization by rewriting the code in Python, and explaining here the math involved and how the math is translated into code. The code I wrote which I'll reference in this post is [here](https://github.com/vhxs/algebraics-viz).

<div style="text-align: center;">
{{< figure src="example.png" caption="Example output from my application. Continue on to read more about what this is." width="80%" >}}
</div>

## Elsewhere on the Internet (Related Work)

I'm not the first one to visualize the algebraic numbers or even attempt to reverse engineer Brooks' visualization, so I'm including a related work section with content I found (sort of like how one would do with a peer-reviwed publication) while scouring the depths of the Internet for what else is online.

Brooks' original code snippet is [here](https://en.wikipedia.org/wiki/User:Stephen_J._Brooks/algebraics/src). In 2013, his visualization was the [subject of _Visual Insights_](https://blogs.ams.org/visualinsight/2013/09/01/algebraic-numbers/), a now-defunct (as of 2021) [blog series](https://blogs.ams.org/visualinsight/about-visual-insight/) published on [The American Mathematical Society's website](https://blogs.ams.org/) and edited by mathematician [John Baez](https://math.ucr.edu/home/baez/). In his post, he describes what's in the visualization and also cites another blogger's code, [David Moore](https://www.mathandcode.com/), who'd taken Brooks' original code and turned it into a desktop application written in C. Moore's code is [available on Sourceforge](https://sourceforge.net/projects/algebraicnumbers/), though it wasn't self-contained enough for me to quickly determine how to build it without investing more time.

If you look up "algebraic number visualization" in a search engine, you'll also find this set of visualizations [posted on _Illustrating Mathematics_](https://im.icerm.brown.edu/portfolio/visualizing-algebraic-numbers/), a [blog on ICERM's website](https://im.icerm.brown.edu/) with lots of neat mathematical art and visuals. They look similar to Brooks' visualization, though unfortunately there isn't source code obviously posted anywhere online for these ones.

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="https://upload.wikimedia.org/wikipedia/commons/d/d1/Algebraicszoom.png" width="100%" caption="Brooks' visualization of the algebraic numbers on Wikipedia">}}
  {{< figure src="https://i0.wp.com/im.icerm.brown.edu/wp-content/uploads/2019/12/image4-3.png?w=1727&ssl=1" width="70%" caption="A visualizations of the algebraic numbers on ICERM's blog" >}}
</div>

I myself have known about Brooks' visualization since learning about the algebraic numbers in 2011, and in summer of 2022 when I had ample free time but less focused of a career direction, I decided to recreate the visualization in [Go](https://go.dev/) as reason to learn a new language. In the process, I also learned the minimum amount of [OpenGL](https://www.opengl.org/) I needed to know to (mostly) successfully rewrite it. Looking back, the code isn't very well structued, but it works. I left the Go code I wrote intact on a separate branch of my Python project [here](https://github.com/vhxs/algebraics-viz/tree/original-go-implementation); as of this writing, this branch is also self-contained enough to just clone and run.

## Generating and Visualizing Algebraic Numbers

Brooks' code to generate his visualization takes place in roughly three steps:
1. Generate a set of integer polynomials
2. Find roots of all the polynomials
3. Draw them on a 2d plane

(2) is thoroughly studied and root finding is a solved problem, the most well-known algorithm being [Newton's method](https://en.wikipedia.org/wiki/Newton%27s_method). Brooks' code has an implementation of Newton's method, and he uses this together with [polynomial long division](https://en.wikipedia.org/wiki/Polynomial_long_division) to find all roots of a given polynomial. For completeness, I translated that section of code [into Python](https://github.com/vhxs/algebraics-viz/blob/main/algebraics/polynomial/polynomial.py#L18) and use the same approach to find polynomial roots, though one could just use [`numpy.roots`](https://numpy.org/doc/2.2/reference/generated/numpy.roots.html) to find roots more efficiently.

(1) is the most mathematically interesting among these. One needs to be able to enumerate all integer polynomials to generate a set of them, and it isn't entirely obvious how one would do this. I'll first describe how I enumerated them, and compare it with how Brooks did it in his code; they're slightly different approaches but conceptually very similar.

### Enumerating Polynomials

Any integer polynomial of degree \( d \) is representable by the tuple:

\[ (a_0, \ldots, a_d) \]

where \( a_i \in \mathbb{Z} \) is the coefficient for term \(x^i\) in the polynomial. So for _all_ positive integers \( d \), we need to list of _all_ tuples \( (a_0, \ldots, a_d) \). We'll enumerate polynomials by their [_length_](https://en.wikipedia.org/wiki/Height_function#Height_of_a_polynomial). [^1] According to Wikipedia, the length of a polynomial \(p(x) = a_0 + a_1 x + \cdots a_d x^d\) is given by the sum of absolute value of its coefficients:

\[ \displaystyle L(p) = \sum _{i = 0} ^{d} | a_i | \]

If we fix both the degree \( d \) and the length \( \ell \) of a polynomial, then there are only finitely many such polynomials. That is, there only finitely many integer tuples \( (a_0, \ldots, a_d) \) that satisfy the equation:

\[ |a_0| + \cdots + |a_d| = \ell \]

So if we could enumerate all integer tuples \( (a_i) \) that satisfy the above for given \(\ell \) and \( d \), then we could hypothetically enumerate all integer polynomials with the following pseudocode: 

```
for length in range(1, max_length):
    for degree in range(1, max_degree):
        enumerate_polynomials(length, degree)
```

Here's the [snippet](https://github.com/vhxs/algebraics-viz/blob/main/algebraics/polynomial/polynomial.py#L120-L133) from my Python code that does exactly this:

```python
def enumerate_polynomials(
    max_length: int, max_degree: int
) -> Generator[ComplexPolynomial]:
    for length in range(max_length + 1):
        for degree in range(2, max_degree + 1):
            for partition in enumerate_partitions(length + degree + 1, degree + 1):
                coefficients = [x - 1 for x in partition]
                if coefficients and coefficients[-1] != 0:
                    yield from map(
                        lambda coefs: ComplexPolynomial(
                            coefficients=[complex(x, 0) for x in coefs], length=length
                        ),
                        generate_signs(coefficients),
                    )
```

We can simplify finding all solutions to \( |a_0| + \cdots + |a_d| = \ell \) by finding all _non-negative_ tuples \( (a_i) \) that satisfy the equation, then iterate over all sign tuples \( (\pm 1, \ldots, \pm 1) \) and multiply each sign with each solution \( a_i \). So we would only need to find all positive integer solutions to:

\[ a_0 + \cdots + a_d = \ell \]

Solving such an equation is a variation of solving the well-known problem of finding [integer partitions](https://en.wikipedia.org/wiki/Integer_partition). There's one more requirement not explicitly discussed yet, which is that \( a_d > 0 \) since the assumption is that the degree of \( p \) is \( d \); all other \( a_ i \) are permitted to be \( 0 \).

Here's the [snippet](https://github.com/vhxs/algebraics-viz/blob/main/algebraics/polynomial/partition.py#L5-L16) from my code that enumerates partitions of `n` with `length` many terms in the sum. There are standard implementations out there for how to enumerate integer partitions, this one being recursive:

```python
def enumerate_partitions(n: int, length: int) -> Generator[list[int]]:
    def enumerate_partitions_recursive(n: int, current_partition: list[int]) -> Generator[list[int]]:
        if len(current_partition) == length:
            if n == 0:
                yield list(current_partition)
            return
        for i in range(1, n + 1):
            current_partition.append(i)
            yield from enumerate_partitions_recursive(n - i, current_partition)
            current_partition.pop()

    yield from enumerate_partitions_recursive(n, [])
```

This is how I enumerate polynomials in my code. Now let's compare it to Brooks' C code. These are the relevant for loops I'd like to highlight from his code for polynomial enumeration:

```C
for (h=2;h<=maxh;h++) // maxh is the maximum possible length
{
  // ...
  for (i=(1<<(h-1))-1;i>=0;i-=2) // i is an integer whose binary representation encodes polynomial coefficients
  {
    t[0]=0;
    for (j=h-2,k=0;j>=0;j--)
      if ((i>>j)&1) t[k]++; else {k++; t[k]=0;}
    // ...
    for (j=(1<<(nz-1))-1;j>=0;j--) // j is an integer whose binary representation encodes signs
    // ...
```

The outermost loop with index `h` looks like it's enumerating over a maximum possible polynomial length `maxh`. The next loop, indexed by `i`, starts with `i` being equal to \(2^{h-1} - 1 \) and decrements down to `0`. Such a number `i` is representable by \( h - 1 \) bits, and reading the body of this for loop, each run of `1`s of length \( r \) in this bit sequence encodes the coefficient \( r \). `0`s in the bit sequence separate the encoded coefficients. To make this more concrete, here's an example bit sequence:

\[ 1111001011101 \]

and this is the polynomial it represents:

\[ 4 + x^2 + 3x^3 + x^4 \]

Another way of thinking about this encoding is that each coefficient is represented in [unary](https://en.wikipedia.org/wiki/Unary_numeral_system), and each coefficient's unary representation is separated by a `0`.

In this way, the maximum possible length of polynomial coefficients encodes like this is \( h - 1 \). This is approach is similar to how I've enumerated all integer polynomials, but with each iteration of the outermost loop, we aren't actually enumerating every single polynomial of length up to `maxh`; this variable just sets an upper bound. However, any polynomial \( p \) is representable by the bit encoding above, so for large enough `h` (a large enough iteration of the for loop), \( p \)'s bit representation would be enumerated. So Brooks' enumeration does exhaustively enumerate all integer polynomials.

The bottommost for loop above iterates over sign bits in the same way my code does, but using another integer `j` to encode a bit sequence representing the sign of each coefficient.

Whichever way one chooses to enumerate the polynomials, this concludes step (1), and after root finding in step (2), one ends up with a set of complex numbers to visualize.

### Visualizing the Roots

We want to visualize these roots on the 2d plane. Each root is a complex number with real and imaginary parts, which are the (x, y) coordinates of a point on the 2d plane. We could just draw a black dot at each such point, but that wouldn't be fun. Instead, Brooks' visualization draws a circle at (x, y), with a radius and color that varies based on the length and degree of its corresponding polynomial, respectively. If the root \( z \) is a root of polynomial \( p \) with degree \( d \) and length \( \ell \), then the radius of the drawn circle is inversely proportional to \( \ell + d \); more specifically, the radius is \( \dfrac{1}{2^{\ell + d + 1}} \). The degree \( d \) determines the color of the circle, so that all circles of a given degree are colored the same.

Consider the case where we want to visualize all polynomials up to degree \( 3 \) and length \( 2 \). Brooks' visualization excludes polynomials of degree \( 1 \), so we'll only consider \( 2 \) and \( 3 \). Then these set of polynomials capture all the roots we want to plot:

- \( x^2 \)
- \( x^2 + 1 \)
- \( x^2 - 1 \)
- \( x^3 + 1 \)
- \( x^3 - 1 \)

There are other polynomials not listed here, such as \( -x^2 + 1 \) that differ only in sign from one of the above, and thus have the same roots, or \(x^3 - x^2 \) whose roots are otherwise captured by some combination of the above. This set of polynomials has the following roots: \( 0, \pm 1, \pm i\) which are roots of polynomials of degree \( 2 \) and \( 3 \), and \( \pm \frac{1}{2} \pm i \frac{\sqrt{3}}{2} \) which are roots of polynomials of degree 3. If a complex number is a root of polynomials of different degrees, multiple circles are drawn, and overlapping circles are drawn such that their colors blend together.

Below, degree \( 2 \) roots (\( 0, \pm 1, \pm i\)) are red and the degree \( 3 \) roots (\( \pm \frac{1}{2} \pm i \frac{\sqrt{3}}{2} \)) are green. The red circles are purely real or imaginary (they falls on the axes), while the green circles are not.

<div style="text-align: center;">
{{< figure src="length_2_degree_3.png" caption="Red circles are of degree 2, green circles are of degree 3" width="50%" >}}
</div>

## Building an Application

In 2022, I had originally translated Brooks' code into Go. This time in 2025, I was more explicit with my goals: I wanted to (1) make my code easily useable and reproducible, and (2) wanted to write code of reasonably good quality (eg, not research-quality code written to meet a paper deadline). So I picked a language that I'm much more familiar with: Python. By now, I've written and rewritten multiple Python applications and am a fairly competent Python developer knowledgeable in modern libraries and tools, so I thought that this would also be a good way to put my skills into practice working on a thing that I love spending time thinking about: visualizing math.

The code is on [GitHub](https://github.com/vhxs/algebraics-viz). I used Astral's [uv](https://docs.astral.sh/uv/) for dependency management, [Pydantic](https://docs.pydantic.dev/latest/) to manage data associated with polynomials and their roots (along with some validation logic), and [Dynaconf](https://www.dynaconf.com/) for basic configuration management. I used [pytest](https://docs.pytest.org/en/stable/) to write a test for my root-finding implementation. I installed the [mypy](https://mypy-lang.org/) VSCode extension, so that it would get mad at me if I've got bad type hints somewhere, and added [Ruff](https://docs.astral.sh/ruff/) as a GitHub Action to repository to enforce good formatting. Also on GitHub is an Action to run `pytest`, and also an Action to publish a release of the application as a standalone executable, targeted for Ubuntu (and built with [pyinstaller](https://pyinstaller.org/en/stable/)) though not thoroughly tested.

I used [PyQt6](https://pypi.org/project/PyQt6/) to add a GUI to the code and make it a desktop application, though this was the first time I've used PyQt and a long time since I've built any GUIs in Python (I've built some GUIs in [Tkinter](https://docs.python.org/3/library/tkinter.html) a long, long time ago). So the GUI code is a bit messier than I like, but getting that part correct was less important to me.

Here's a screenshot of the application when initially launched on macOS:

<div style="text-align: center;">
{{< figure src="app_screenshot.png" caption="The desktop application" width="70%" >}}
</div>

There's a lot that could be done to improve this application. For example, the `pytest` suite could be expanded to include tests for the polynomial enumeration algorithms. I implemented Brooks' algorithm for polynomial enumeration, but it's not currently usable through the GUI. The application could also use tooltips and generally better explain what each UI widget controls.

However, I think there are just enough good practices employed in the development of this application for it to be extensible by others. Part of the focus on code quality is to enable others to easily build off of it. I believe that any source code used to develop mathematical visualizations like this should be accessible and easy to use, so that it might inspire other mathematicians or software engineers to do innovative and cool visualization stuff with math. Brooks' original code is license under a [Creative Commons ShareAlike license](https://creativecommons.org/licenses/by-sa/4.0/deed.en). I've license my code under an [MIT license](https://opensource.org/license/mit).

## Use of AI

ChatGPT was generally a force multiplier in the development of this code, provided that I was using it effectively. Here are a few examples of how it helped me:

- Researching Python GUI frameworks that were compatible with [PyOpenGL](https://pyopengl.sourceforge.net/). GUI frameworks recommended by ChatGPT included [PyGame](https://www.pygame.org/news), [Dear PyGui](https://dearpygui.readthedocs.io/en/latest/), and [PyQt](https://wiki.python.org/moin/PyQt). I went with PyQt6, though ChatGPT 4o was giving me PyQt5 code snippets until I explicitly asked it to use version 6.
- Searching PyQt6 documentation. I'm not that experienced of a UI developer, but ChatGPT was able to take vague descriptions of what features I wanted to add to the GUI, and recommend the relevant PyQt6 functions that I should use.
- Writing basic PyQt6 widgets. ChatGPT (o3) was less good at this, but it still pointed me in the right direction.
- Translating my Go code into Python. It was pretty good at this, but I'll also take some credit here since I'd already done the hard work of traslating the original C code into Go. However, ChatGPT o3 seems to do a decent job at [comprehending the C code](https://chatgpt.com/share/6834e900-e8e0-8000-a499-67774f2c4ca2).
- Turning my vague description of what I thought should be a mathematical theorem, and [suggesting](https://chatgpt.com/c/67ec5d82-ded0-8000-9a42-0ee1902fe6af) an actual theorem that formally states what I had in mind. I learned of Cauchy's root bound for the first time via ChatGPT 4o.

The one instance I used ChatGPT for writing this post was to [ask it for a succinct description of the algebraic numbers](https://chatgpt.com/share/6834eb50-7dd8-8000-89dd-d7e36906f48a) for my target audience. It gave me something that wasn't technically accurate enough for me to include; namely, it suggested that all algebraic numbers are expressible by radicals, which is [not true](https://www.quora.com/Can-a-number-be-algebraic-but-not-expressible-by-means-of-radicals). Nothing else about this blog post is AI-generated.

## _Et Cetera_

As I was thinking about visualizing the algebraic numbers, and enumerating polynomials by degree \( d \) and length \( \ell \), I was wondering what constrained algebraic numbers to be "close" to the origin. What prevents roots of these polynomials to be way far out there? As we see, the roots cluster around the origin, so some mathmetical property must be forcing this. [Cauchy's root bound](https://en.wikipedia.org/wiki/Geometrical_properties_of_polynomial_roots#Lagrange's_and_Cauchy's_bounds) is a theorem I learned when writing about this post. It's a bound on the absolute value of a polynomial's roots, in terms of \( d \) and \( \ell \). Here's one version of the bound:

\[ 1 + \max \left\{ \dfrac{a_{n-1}}{a_n}, \dfrac{a_{n-2}}{a_n}, \ldots, \dfrac{a_{0}}{a_n} \right\} \]

John Baez's blog post includes a citation of [Roth's Theorem](https://en.wikipedia.org/wiki/Roth%27s_theorem). As quoted from the Wikipedia page:

> It is of a qualitative type, stating that algebraic numbers cannot have many rational approximations that are 'very good'.

The blog post suggests that this observation could be turned into other interesting ideas for visualizing the algebraic numbers.

The real algebraic numbers are [countable](https://en.wikipedia.org/wiki/Countable_set) and dense in the real numbers, and that's one motivation for devising creative ways to visualize them. This is also true of the rational numbers \( \mathbb{Q} \): they're also countable and dense in \( \mathbb{R} \). Similarly, mathematicians have explored ways of [visualizing the rational numbers](https://risingentropy.com/visualizing-the-rationals/). In writing this post, I was wondering whether there are creative ways of visualizing the real [computable numbers](https://en.wikipedia.org/wiki/Computable_number), since they're also countable, dense, and form a subfield of \( \mathbb{R} \). In fact, they're also a [real closed field](https://en.wikipedia.org/wiki/Real_closed_field) like the real algebraic numbers. The main challenge here is determining a natural way to map computable numbers onto the 2d plane; this is much more obvious to do with both the rational and algebraic numbers. Also, the [computable numbers aren't computably enumerable](https://math.stackexchange.com/questions/76374/properties-of-computable-numbers#comment181525_76374).

<!-- A polynomial is [solvable by radicals](https://math.stackexchange.com/questions/720630/what-does-it-mean-for-a-polynomial-to-be-solvable-by-radicals) if all its roots can be expressed with arithmetic operations and radicals. -->

[^1]: It's unclear to me where "length" is standard terminology here. It's mentioned on Wikipedia, but has no explicit reference, and neither can I find good references for it online. However, the "height" of a polynomial is standard terminology.