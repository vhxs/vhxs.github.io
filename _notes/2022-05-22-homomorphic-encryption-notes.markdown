---
layout: post
title: Homomorphic encryption notes
tags: cryptography, rings, encryption
published: true
---

Homomorphic encryption is a kind of encryption that allows you to do arithmetic (here, specifically, addition and multiplication, or, *ring operations*) on encrypted data. Roughly speaking, this is because encryption and decryption are ring homomorphisms. Functions composed of addition and multiplication of elements from a ring are polynomials. Arithmetic circuits are a *specific way* of evaluating a polynomial, sort of like how Boolean circuits compute Boolean functions (truth tables).

Various homomorphic encryption schemes had been around for a while, but none of them permitted arbitrary numbers of addition or multiplication operations. You can only compute arithmetic circuits of certain bounds or sizes with these schemes (partially, somewhat, etc). However, Craig Gentry showed in his PhD thesis around 2009 (also work published in [STOC](https://dl.acm.org/doi/10.1145/1536414.1536440), *the* premier venue on [theoretical computer science](http://acm-stoc.org/)) that *fully* homomorphic encryption is possible. He proved the existence of such a scheme, introducing the novel idea of *bootstrapping*, which reduces the *noise* generated when performing arithmetic (called *homomorphic* in the literature, but the algebraist in me considers that an abuse of terminology) operations. Bootstrapping involves evaluation of the decryption and encryption functions, *as arithmetic circuits themselves*. It seems like a very meta idea.

The plaintext spaces and ciphertext spaces generally look like the quotient ring $$\mathbb{Z}_t[x] / (p(x))$$, which are weird beasts since these things are finite rings that aren't always fields, depending on the context. These being the world in which homomorphic encryption takes places invites the application of all kinds of known results from classical (the Italian school of) algebraic geometry.[^2]

Homomorphic encryption is considered secure because if you can crack it, then you can crack ring learning with errors (using a polynomial reduction), and that's a theoretically hard problem in the sense of computational complexity.

Gentry only proved the *existence* of such a scheme. Proving existence or non-existence of an algorithm is the very first step in any kind of basic research. Existence of an algorithm means that it is *theoretically possible* to do a certain thing, though the asymptotic complexity of such an algorithm may be high.[^1] Since Gentry's thesis, there have been several attempts at making homomorphic encryption faster, by throwing hardware acceleration, approximations, and fancier parallelization approaches at it, since it's still considered slow.

There are tons or papers and several homomorphic encryption libraries out there now.

Homomorphic encryption can be applied to problems wherever privacy is a concern, since it allows a third party to perform computation on data without knowing what that data is (though it alone cannot ensure authenticity, just confidentiality). Possible application domains are in health care and cloud computing.

### Papers
BFV, BGV, and CKKS are the major encryption schemes. Good starting point though the papers can be dense. These are all just authors' names. Cryptographers use IACR instead of arXiv for preprints.
- BFV: https://eprint.iacr.org/2012/144
- BGV: https://eprint.iacr.org/2011/277
- CKKS: https://eprint.iacr.org/2016/421.pdf

Other stuff
- SIMD'izing homomorphic encryption https://eprint.iacr.org/2011/133.pdf

This list will grow as I come across more stuff.

### Libraries
- Microsoft SEAL: https://www.microsoft.com/en-us/research/project/microsoft-seal/
- Concrete: https://github.com/zama-ai/concrete
- NuFHE: https://github.com/nucypher/nufhe
- Palisade: https://palisade-crypto.org/software-library/ (unlike the others this isn't hosted on github for some reason)
- TenSeal: https://github.com/OpenMined/TenSEAL 

### Misc
- https://fhe.org/
- https://homomorphicencryption.org/
- Crypto stackexchange has a wealth of information on homomorphic encryption: https://crypto.stackexchange.com/questions/tagged/homomorphic-encryption
- https://github.com/jonaschn/awesome-he

[^1]: Sort of like how it is theoretically possible to take any data structure with a sequential specification, and turn that into a wait-free linearizable data structure that can be concurrently accessed. But wait-free data structures are rarely used in practice since they're slow.

[^2]: Grothendieck's algebraic geometry is probably a bit much to study, even if you want to go deep into the theoretical weeds of how homomorphic encryption works. You probably don't need to open Hartshorne to understand it.