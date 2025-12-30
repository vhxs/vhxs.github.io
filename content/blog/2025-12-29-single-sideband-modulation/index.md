---
title: The Math of Single-sideband Modulation
author: Vikram Saraph
date: "2025-12-29"
tags:
  - fourier transform
  - signal processing
  - analysis
  - amateur radio
---

I wrote this post as I learned about signal modulation while studying for getting a [Technician amateur radio license](https://www.arrl.org/getting-your-technician-license). [Single-sideband modulation](https://www.hamradioschool.com/post/understanding-single-sideband-ssb) (SSB for short) is just one of a handful of [modes](https://en.wikipedia.org/wiki/List_of_amateur_radio_modes) of transmitting information by amateur radio, though I initially found the math of it to be confusing.

So did some digging around on the Internet to resolve my confusion. This blog post is the result of that digging. **As a disclaimer**: neither my professional nor educational background is in RF or electrical engineering. But I've always had an interest in electronics and I do have the math background to understand some of the nuances to write about it. If there is anything misstated here, please feel free to reach out over any one of my many social media accounts, and I will correct any mistakes.

## What is signal modulation? Why use it?

Signal modulation is a technique in signal processing used to encode information in a radio wave in order to transmit that information. Typically, a lower-frequency wave is encoded in a higher-frequency one (called the [_carrier wave_](https://en.wikipedia.org/wiki/Carrier_wave)), by varying the amplitude, frequency, or phase of the carrier wave. It'd be like using a laser pointer (our carrier wave) to transmit Morse code (information to send) by turning it on and off. The process of varying the carrier wave is called _modulation_, and a carrier wave that has been varied to encode information is said to be _modulated_.

Why not just transmit low-frequency signals directly? We can’t do this due to physical limitations of the antennas that transmit RF. The exact math and physics of these limitations would warrant its own blog post, but in simple terms, the longer the wavelength of the signal to be transmitted, the longer antenna you would need to do that. And with signals in the range of voice frequency, which is [300 Hz to 3400 Hz](https://en.wikipedia.org/wiki/Voice_frequency), if using a [half-wave dipole antenna](https://www.youtube.com/watch?v=PPKEpJEt_cM) (for example), you would need an antenna of length between 40 km and 475 km to match such a signal's resonant frequency. That is completely unreasonable to do. So we have to transmit information using higher frequencies instead. That’s where modulation of high-frequency signals comes into the picture.

<div style="text-align: center;">
{{< figure src="https://lowpowerlab.com/wp-content/uploads/2017/04/image22.jpg" caption="A picture of a half-wave dipole antenna I found on the Internet" width="50%" >}}
</div>

## Amplitude modulation

_Amplitude modulation_ is modulation of the carrier wave by varying its amplitude. How this works is best illustrated by simple example. Suppose we start with a plain sine wave. This wave carries no information (beyond its frequency and amplitude) since it’s just a plain sine wave. Indeed, if we take the Fourier transform of the unmodulated carrier wave, we get a single impulse corresponding to the single frequency in the wave.

Hypothetically, what if we could control the amplitude of this wave, say between two values, 1 and 0.5? Then we could transmit bits using this convention: in a given time interval, any time we see an amplitude of 1, interpret it as a 1, and 0.5 for 0. Then we could transmit bits and hence information over the signal. Here's an example signal I made in [Grapher](https://en.wikipedia.org/wiki/Grapher), where peak amplitudes are 3 and 1, respectively ([source file](https://github.com/vhxs/vhxs.github.io/blob/main/content/blog/2025-12-29-single-sideband-modulation/binary_am.gcx)).

<div style="text-align: center;">
{{< figure src="binary_am.png" caption="An amplitude-modulated (AM) signal to transmit bits. Exact equation shown in figure" width="80%" >}}
</div>

This particular method of modulation is very similar to [on-off keying](https://www.open.edu/openlearn/digital-computing/exploring-communications-technology/content-section-1.4) (OOK), where in on-off keying, the lower amplitude is 0. OOK is used in digital signal modulation. Amplitude modulation is conceptually similar, but instead of varying the amplitude between two discrete values, we continuously vary the amplitude so that we can represent continuous signals.

Here's a 10 Hz signal modulated by a 1 Hz signal. The purple curve shows 1 Hz pattern is called the modulated signal's _envelop_.

<div style="text-align: center;">
{{< figure src="simple_am_with_envelop.png" caption="A 10 Hz signal amplitude-modulated with a 1 Hz signal. Envelop in purple." width="80%" >}}
</div>

An amplitude-modulated wave supposedly contains redundant information. This is what I learned anyways as I studied for the amateur radio exam. I wanted to understand why this was and what this meant exactly, but the [Wikipedia page on SSB](https://en.wikipedia.org/wiki/Single-sideband_modulation) felt too unapproacheable for me as someone lacking any RF background. So I went to YouTube looking for videos on SSB, and found [this one](https://www.youtube.com/watch?v=sv1xzlBut1I) to be helpful in explaining what SSB is and what it does. It explains SSB in terms of an amplitude-modulated signal's two _sidebands_. And to understand what sidebands are, we need to review the Fourier transform.

### Fourier transform and the spectrum of a signal 

Here's Wikipedia's first sentence on the Fourier transforms, which I think does a decent job at explaining what it is in just a single sentence:

> The Fourier transform is an integral transform that takes a function as input, and outputs another function that describes the extent to which various frequencies are present in the original function.

The Fourier transform maps functions to other functions. In RF, an input function \( s \) to the Fourier transform is a signal in the _time domain_, whose graph's x axis is time and y axis is amplitude. The Fourier tranform maps a signal \( s \) represented in the time domain to its representation \( \hat{s} \) in the _frequency domain_, where the x axis is instead _frequency_, not time. \( \hat{s}(x) \) is generally complex-valued, so to visualize it, we'll plot \( |\hat{s}(x)| \). This is sometimes also called the _spectrum_ of \( s \).

Here's the definition of the Fourier transform:

$$ \hat{s}(\xi) = \displaystyle\int_{-\infty}^{\infty} s(x) e^{-i 2 \pi \xi x} dx $$

The Fourier transform of a pure sine wave (here, a 5 Hz wave) is a single impulse ([Dirac delta](https://en.wikipedia.org/wiki/Dirac_delta_function)) in the frequency domain, as below:

<div style="text-align: center;">
{{< figure src="sine_wave_fourier.png" caption="A 5 Hz wave and its Fourier transform" width="80%" >}}
</div>

I _did_ say above that we'd see a single impulse, but there are actually _two_ impulses. What gives?

If \( s \) is real-valued (which we're assuming), then \( \hat{f} \) is a Hermitian function. In math-speak, that means:

$$ \hat{s}(-\xi) = \overline{\hat{s} (\xi)} $$

The proof of this is straightforward and can be written on a single line. This property of \( \hat{s} \) implies that \( | \hat{s} (-\xi) | = | \hat{s} (\xi) | \), or that \( |\hat{s}| \) is an even function, which gives us the symmetry about the y axis that we're seeing. It's usually only the positive spectrum that's plotted since, for real-valued fuctions, the negative spectrum is just the  mirror image of the positive spectrum (and it's unclear to me anyways whether [negative frequencies have a physical meaning](https://dsp.stackexchange.com/questions/431/what-is-the-physical-significance-of-negative-frequencies)). Here we've shown the full spectrum.

### Sidebands

Let's now look at the spectrum (both positive and negative frequencies) of an amplitude-modulated signal. Generally, given a message signal \( m(t) \) with \( |m(t)| \le 1 \), and a carrier wave whose frequency is \( f \) and amplitude \( A \), the signal obtained by amplitude-modulating the carrier by \( m \) is given by the following equation:

$$ s(t) = A (1 + \mu m(t)) \cos (2 \pi f t) $$

where \( 0 < \mu \le 1 \). Choosing \( A = 1 \), \( f = 40 \), and \( m(t) = \cos (2 \pi t) \), we get:

<div style="text-align: center;">
{{< figure src="am_fourier.png" caption="40 Hz wave modulated by 1 Hz wave using AM" width="80%" >}}
</div>

There's still the symmetry about the y axis as expected, but each carrier impulse now also has two impulses on either side of it, at 39 Hz and at 41 Hz. We can see where these additional symmetries come from by taking the Fourier transform of the modulated signal \( s(t) \):

$$ \hat{s}(\xi) = \frac{A}{2} (\delta(\xi - f) + \delta(\xi + f)) + \frac{A}{2} (\hat{m}(\xi - f) + \hat{m}(\xi + f)) $$

I won't go over the details here, but \( \hat{s} \) can be computed by using linearity of the Fourier transform, and identity 115 [in this table of common transforms](https://en.wikipedia.org/wiki/Fourier_transform#Tables_of_important_Fourier_transforms). The lefthand summand are the carrier wave impulses, and the righthand summand the _four_ impulses from the message signal \( m(t) \), whose Fourier transform is \( \hat{m} (\xi) = \delta(\xi - 1) + \delta(\xi + 1) \)

From the equation above we can see the symmetry of \( \hat{s} \) about the frequency \( f \), regardless of whatever signal \( m \) we're given. Let's try another more messy signal. 

<div style="text-align: center;">
{{< figure src="noisy_am_fourier.png" caption="40 Hz wave modulated by a baseband given on the lefthand side" width="90%" >}}
</div>

In signal processing, the message signal \( m \) is also called the _baseband_. A  (frequency) _band_ just refers to the interval of frequencies \( [f_{low}, f_{high} ] \) in the frequency domain, and its _bandwidth_ is \( f_{high} - f_{low} \).

The symmetry across positive and negative impluses is still obviously there. The band to the left of the carrier impulse is called the _lower sideband_, while band to the right is the _upper sideband_. The upper and lower sidebands are mirror images of one another, so in theory, we could send just one of them and reconstruct the original modulated signal from it. We could also cut out the carrier wave's impulse because it doesn't actually contain any information.

This is exactly what single-sideband modulation does: only one sideband is transmitted. 

## Single-sideband modulation

In SSB, one of the sidebands is dropped since both sidebands have the same information. What does this mean in practice, though; how do we define a modulated signal whose Fourier transform is only one of the sidebands?

One other thing I'd also found confusing with SSB modulation is it being described as "removing the carrier". I found this language to be confusing because I thought that the use of a high-frequency carrier to transmit information was the whole point of modulation, so then wouldn't "removing the carrier" (whatever that meant) defeat the purpose of modulation? Reading [this answer](https://ham.stackexchange.com/questions/9761/why-are-carrier-waves-necessary) on the Amateur Radio Stack Exchange cleared up this confusion: in SSB, we remove the _frequency_ of the carrier wave, but that frequency is still used to push the baseband into RF range so that it can be transmitted at RF wavelengths.

For SSB, let's first visualize the spectrum we _want_ our modulated signal to have. Below, we've already removed the carrier impulse, the lower sideband is colored blue, and the upper sideband is colored red. We want SSB to produce a spectrum with the red curve _only_. 

<div style="text-align: center;">
{{< figure src="ssb_spectrum_red_blue.png" caption="40 Hz wave modulated by a baseband given on the lefthand side" width="70%" >}}
</div>

So why not just compute the inverse Fourier transform of the upper sideband directly? The Fourier transform is an invertible linear operator (in fact, it's [unitary](https://math.stackexchange.com/questions/1429086/prove-the-fourier-transform-is-a-unitary-linear-operator) [for](https://en.wikipedia.org/wiki/Unitary_operator) [\( L^2 \) functions](https://en.wikipedia.org/wiki/Square-integrable_function)). And we know the inverse will be real-valued because the red curve is symmetric about the y axis. There's nothing actually stopping us from doing this, so let's do it.

From what I have read online, this is not conventionally how SSB is derived. I had a [long conversation with ChatGPT](https://chatgpt.com/share/694a0bb3-de60-8000-b287-048d638c1082) to formulate my thoughts and figure out how precisely to do it this way. It seems like a correct approach to me. The conversation also mentions the [Hilbert transform](https://en.wikipedia.org/wiki/Hilbert_transform). More on that later.

## The derivation

Let's assume an amplitude of \( 1 \) for simplicity. Let's also start with \( \hat{m}(\xi - f) \) since it is the upper and lower sidebands (sans the carrier impulse) in the positive spectrum of \( m \). We only want to reason about one sideband though. Let's pick the upper sideband. In the positive spectrum, this is \( \hat{m}(\xi - f)u(\xi -f ) \) where \( u \) is the [Heaviside step function](https://en.wikipedia.org/wiki/Heaviside_step_function). The step function is used to isolate only the sideband that we want.

To ensure the inverse transform is real-valued, we need the function we're inverting to be even. Let's call the function we want to invert \( \hat{s}_{ssb} \). Then following definition is forced, since we want \( s_{ssb} \) to be real-valued (so \( \hat{s}_{ssb} \) is Hermitian):

$$ \hat{s}_{ssb}(\xi) = \hat{m}(\xi - f)u(\xi - f ) + \overline{\hat{m}(-\xi - f)}u(- \xi -f ) $$

This is because we need \( \hat{s}_{ssb}(\xi) = -\overline{\hat{s}_{ssb}(-\xi)} \) to hold. For convenience let's just call \( A(\xi) = \hat{m}(\xi - f)u(\xi -f ) \). The inverse Fourier transform of \( \hat{s}_{ssb}(\xi) \) is given by:

$$ s_{ssb}(t) = \dfrac{1}{2 \pi} \int_{-\infty}^\infty \left [ A(\xi) + \overline{A(-\xi)} \right ] e^{i \xi t} d \xi = \dfrac{1}{2 \pi} \int_{-\infty}^\infty A(\xi) e^{i \xi t} d \xi + \dfrac{1}{2 \pi} \int_{-\infty}^\infty \overline{A(-\xi)} e^{i \xi t} d \xi $$

Call the lefthand term above \( x(t) \). Making the subsitution \( \omega = -\xi \), the righthand term above can be rewritten:

$$ \dfrac{1}{2 \pi} \int_{-\infty}^\infty \overline{A(-\xi)} e^{i \xi t} d \xi = \dfrac{1}{2 \pi} \int_{\infty}^{-\infty} - \overline{A(\omega)} e^{-i \omega t} d \omega = \dfrac{1}{2 \pi} \overline{ \int_{-\infty}^{\infty} A(\omega) e^{i \omega t} d \omega } = \overline{ x(t) }$$

So:

$$ s_{ssb}(t) = x(t) + \overline{ x(t) } = 2 \Re (x(t))$$

where [\( \Re \)](https://mathworld.wolfram.com/RealPart.html) is the real part of a complex number.

### The analytic signal

The next step is to define the _analytic spectrum_ of \( m \), which we'll denote as \( M_a \):

$$ M_a(\xi) = 2 u(\xi)M(\xi) $$

By applying a step function, \( M_a \) kills off all negative frequencies of \( m \). So the inverse transform of \( M_a \), the signal \( m_a \) called the _analytic signal_ of \( m \) has a spectrum will no negative frequencies, but it is complex-valued. If you've taken courses in complex analysis like I have, you might recognize the term "analytic" as in a [complex analytic (or holomorphic) function](https://en.wikipedia.org/wiki/Holomorphic_function) and wonder _why_ \( m_a \) is called the _analytic_ signal. There is apparently a [relationship between the analytic signal and holomorphic functions](https://dsp.stackexchange.com/a/89572/90141), but I won't explore it in this blog post.

Let's compute \( m_a \) by applying the definition of the inverse Fourier transform:

$$ m_a(t) = \dfrac{1}{2 \pi} \int_{-\infty}^\infty M_a(\xi) e^{i \xi t} d \xi = \dfrac{1}{2 \pi} \int_{0}^\infty 2 \hat{m}(\xi) e^{i \xi t} d \xi = \dfrac{1}{\pi} \int_{0}^\infty \hat{m}(\xi) e^{i \xi t} d \xi $$

Now let's rewrite \( x(t) \) so that it is expressible in terms of \( m_a (t) \), making the substitution \( \omega = \xi - f \):

$$ x(t)
= \frac{1}{2\pi} \int_{-\infty}^{\infty}
\hat{m}(\xi - f)\, u(\xi - f)\, e^{i \xi t}\, d\xi
= \frac{1}{2\pi} \int_{f}^{\infty}
\hat{m}(\xi - f)\, e^{i \xi t}\, d\xi
= \dfrac{1}{2\pi} e^{ift} \int_0^\infty \hat{m}(\xi) e^{i\xi t} d \xi
= \dfrac{1}{2} m_a(t) e^{ift} $$

Therefore:

$$ s_{ssb}(t) = \Re (m_a(t) e^{ift}) $$

### The Hilbert transform

Since \( 2u(\xi) = 1 + \text{sgn}(\xi) \), we can write \( m_a \) as follows:

$$ m_a(t) = \dfrac{1}{2 \pi} \int_{-\infty}^\infty (1 + \text{sgn}(\xi)) \hat{m}(\xi) e^{i\xi t} d \xi = m(t) + \dfrac{1}{2 \pi} \int_{-\infty}^\infty \text{sgn}(\xi) \hat{m}(\xi) e^{i \xi t} d \xi $$

The term in square brackets is called the _Hilbert transform_ of \( m \), though this is not typically the expression used to define it. We'll derive the typical definition from this.

Notice the expression \( \dfrac{1}{2 \pi} \int_{-\infty}^\infty \text{sgn}(\xi) \hat{m}(\xi) e^{i \xi t} d \xi \) is the inverse transform \( \mathcal{F}^{-1} (\text{sgn} \cdot \hat{m}) \). [The inverse transform of a product is the convolution of inverse transforms](https://en.wikipedia.org/wiki/Convolution_theorem), so this is \( \mathcal{F}^{-1} (\text{sgn}) * \mathcal{F}^{-1} (\hat{m}) = \mathcal{F}^{-1} (\text{sgn}) * m \).

We won't compute \( \mathcal{F}^{-1} (\text{sgn}) \) since it requires complex analyis that is a bit out of scope here. ChatGPT is able to generate a correct [proof of its derivation](https://chatgpt.com/share/6950b342-5ffc-8000-9c2c-95ffe583ad5f). It requires an understanding of [tempered distributions](https://en.wikipedia.org/wiki/Distribution_(mathematical_analysis)#Tempered_distribution) (of which the Dirac delta function is one) and [Cauchy principal values](https://en.wikipedia.org/wiki/Cauchy_principal_value). We'll refer to [this table](https://en.wikipedia.org/wiki/Fourier_transform#Distributions,_one-dimensional) for determining \( \mathcal{F}^{-1} (\text{sgn}) \); it is \( \dfrac{i}{\pi} \text{PV} \left( \dfrac{1}{t} \right ) \), where PV refers to the Cauchy principal value. Convolving with \( m \), and unraveling the definition of the convolution:

$$ (\mathcal{F}^{-1} (\text{sgn}) * m)(t) = \dfrac{i}{\pi} \text{PV} \left( \dfrac{1}{t} * m \right ) 
= \dfrac{i}{\pi} \text{PV} \left( \int_{-\infty}^\infty \dfrac{m(\tau)}{t - \tau} d\tau \right)
= i \left [ \dfrac{1}{\pi} \text{PV} \left( \int_{-\infty}^\infty \dfrac{m(\tau)}{t - \tau} d\tau \right) \right ] $$

The expression in the square brackets is how the Hilbert transform \( \mathcal{H}(m) \) is defined. So returning to the expression for \( m_a \), we've got:

$$ m_a(t) = m(t) + i\mathcal{H}(m)(t) $$

So then:

$$ s_{ssb}(t) = \Re ( \left [ m(t) + i\mathcal{H}(m)(t) \right ] e^{ift} ) $$

Finally, using [Euler's formula](https://mathworld.wolfram.com/EulerFormula.html):

$$ s_{ssb}(t) = \Re ( \left [ m(t) + i\mathcal{H}(m)(t) \right ] \cdot [\cos(ft) + i\sin(ft)] ) = m(t)\cos(ft) - \mathcal{H}(m)(t)\sin(ft) $$

This is general expression for a carrier wave of frequency \( f \) modulated with single-sideband modulation. The Wikipedia article on the Hilbert transform has a [table of common transformations](https://en.wikipedia.org/wiki/Hilbert_transform#Table_of_selected_Hilbert_transforms).

### Can we simplify this derivation?

Most of the content I found online about SSB either wasn't self-contained enough to explain the full derivation of SSB, or wasn't mathematically rigorous enough for my liking. Furthermore, I felt that the analytic signal and Hilbert transform were introduced as concepts without motivating _why_ we care about them.

In the proof I've written here, I started with computing the inverse Fourier transform of the desired spectrum from the outset, and then defined the analytic signal and the Hilbert transform as they appeared naturally in the computation of the inverse transform. In my opinion, the proof can be further shortened if we don't really care about mentioning these two concepts. But I wanted to do it this way since it helped me better understand a few important topics that appear in signal processing. I've outlined all the steps you need here for a complete and accurate proof, while also mentioning the analytic signal and the Hilbert transform, but I unfortunately think the proof is a lot of algebraic and symbolic manipulation without much intuition. If I find opportunity to add intuition to the proof itself, I'll update this post.

This all being said, I liked [this document](https://www.comm.utoronto.ca/~frank/notes/hilbert.pdf) on the Hilbert transform which also defines and derives the expression for SSB.

## _Et cetera_ (including use of AI)

This post covers only the mathematics of single-sideband modulation. It does not cover how it's _implemented_ in circuitry. I'd probably have to get into the physics and electronics of modulation, which I'm not qualified to do (yet anyways). From what I've read so far though, [mixers](https://en.wikipedia.org/wiki/Frequency_mixer) are used in signal modulation.

Generally speaking, using AI (ChatGPT) helped me understand SSB. It generated Python scipts, helped explain intuition, and wrote some proofs. It still made mistakes with proofs, often times making subtle errors or weird assumptions. That's why I still tried to manually verify each detail and write up my own proof.

I wrote several Python scripts to create the matplotlib figures in this post. I didn't include them in this post because I think their source code is mostly a distraction, but in the interest of open-sourcing things that I do, I uploaded them all [here](https://github.com/vhxs/vhxs.github.io/tree/main/content/blog/2025-12-29-single-sideband-modulation) along with this post's source. I used single-shot prompting with ChatGPT to do this, but I did try to read the generated code, mainly ensuring that I know what each one is doing. In the process of doing this (though I ended up not using), I also learned of the [scipy.signals](https://docs.scipy.org/doc/scipy/tutorial/signal.html) package. SciPy has lots of cool applied math stuff.

These Python scripts used the [fast Fourier transform (FFT) from NumPy](https://numpy.org/doc/stable/reference/routines.fft.html). [FFT algorithms](https://en.wikipedia.org/wiki/Fast_Fourier_transform) are fast implementations of the [discrete Fourier transform](https://en.wikipedia.org/wiki/Discrete_Fourier_transform) (DFT), which is like a discrete version of the Fourier transform that operates on finite sequences. Obviously, when making plots, we can't actually work with continuous functions, we can only sample points from them. The DFT lets us work with discrete sets of points, which is okay, since the DFT does [converge](https://en.wikipedia.org/wiki/Convergence_of_Fourier_series) to the Fourier transform in some sense.

Single-sideband modulation is [just one](https://en.wikipedia.org/wiki/Signal_modulation#/media/File:Modulation_categorization.svg) of many approaches to signal modulation. It's used in amateur radio to transmit analog data over an analog signal, but it's also used by WiFi (for example) to transmit digital data over an analog signal. [Quadrature amplitude modulation](https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation) (QAM) is used to transmit data over WiFi signals. ["Modem"](https://en.wikipedia.org/wiki/Modem) stands for modulator-demodulator, because one of the functions of a modem is literally to modulate and demodulate signals. Who knew. There's a lot of other interesting math (and visuals) in QAM that I'd like to explore in another blog post. 

You probably don't need all these mathematical details to get even an [amateur extra license](https://www.arrl.org/upgrading-to-an-extra-license), the most advanced of amateur radio licenses. I'm just shooting for an technician's for the time being. There's a nice website, [hamstudy.org](https://hamstudy.org/), that gives you free access to practice exams. And their mobile app is only $4. I've signed up for an exam in early 2026; wish me luck.