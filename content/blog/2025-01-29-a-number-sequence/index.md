---
title: An OEIS Sequence
author: Vikram Saraph
date: "2025-01-29"
tags:
  - games
  - combinatorics
  - oeis
---

## What is OEIS?

The [On-Line Encyclopedia of Integer Sequences](https://oeis.org/) (OEIS) is exactly what it [sounds](https://oeis.org/listen.html) like: it’s a searchable database of interesting number sequences. It’s used by math researchers to discover sequences that they might encounter during their research, and it can help them find other relation sequences or relevant citations to published papers. Each entry in OEIS consists of several terms in the sequence, along with other associated data, like formulas or recurrence relations that define the sequence, programs that generate the sequence, and references to related OEIS sequences. [Here's the entry](https://oeis.org/A000045) for the Fibonacci sequence. You can read more about OEIS on their [FAQ page](https://oeis.org/FAQ.html).

OEIS has been around for nearly three decades (as of this writing), has over 300,000 sequences, and grows at a rate of a few dozen new sequences per day. Most interesting sequences have been found and added to OEIS by now, so it’s not something so remarkable to find a new one that you'd put on a résumé. Over the years I've looked up sequences on OEIS for both work and play, and have always found an entry with what I'm looking for. But recently, I accidentally came across a sequence in an unusual place while not even looking for one: I discovered it while chatting with an amateur mathematician (who will remain anonymous) in a gaming Discord server who was messing with tic-tac-toe-like grids and their arrangements. I was surprised it wasn't in OEIS. I was [nerd-sniped](https://xkcd.com/356/), so I submitted [the sequence](https://oeis.org/A378907), went through the peer review process, and got it accepted and published.

## The sequence

The inspiration for the following sequence came from a minigame in [Final Fantasy VIII](https://en.wikipedia.org/wiki/Final_Fantasy_VIII), called [Chocobo World](https://finalfantasy.fandom.com/wiki/Chocobo_World). In it, you control a character called Boko, a bird-like creature, and explore a world where go on a quest rescue a friend and fight enemies along the way. There’s a level-up mechanism where after each battle, a magic stone is randomly placed into a 3x3 grid that tracks your progress towards leveling up. Boko levels up when a row, column, or diagonal is completed, so if you’re lucky, you can level up him with as few as 3 stones, or if you’re unlucky, it takes as many as 7. Here's a video of a gamer [testing playing Chocobo World](https://www.youtube.com/watch?v=KIAbD7J2bRk&t=588s), leveling up Boko, and here's a screenshot from the game of what the 3x3 grid looks like with a complete diagonal of stones:

<div style="text-align: center;">
{{< figure src="ff8.png" caption="3 in a row on a diagonal" width="40%" >}}
</div>

The first question asked was how many ways there are place 6 stones into a 3x3 grid without leveling up. This isn't hard to reason about; there are only two ways to do this:

<div class="image-wrapper" style="display: flex; justify-content: space-evenly;">
  {{< figure src="diagonal.png" width="50%" >}}
  {{< figure src="anti.png" width="50%" >}}
</div>

Naturally, and especially if you’re a combinatorialist who likes to count things, the next question is then how many ways are there of doing this in the general \(n \times n\) case. That is, how many ways are there of placing the maximum (\(n^2 - n\)) number of stones (or abstractly, _items_) in an \(n \times n\) grid so that no row, column, or diagonal is complete? Let’s call this sequence \(A(n)\) for all integers \( n > 0 \).

When I'd first thought about this sequence, what came to mind were the [permutation matrices](https://en.wikipedia.org/wiki/Permutation_matrix). These are binary matrices that have exactly one 1 in each row and column. Here are two \(4 \times 4\) examples:

\[
\begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix} \qquad \begin{bmatrix}
1 & 0 & 0 & 0 \\
0 & 0 & 1 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}
\]

These matrices correspond exactly to arrangements of our \(n \times n\) with no complete row or diagonal, where 1s encode the _lack_ of a item placed in a slot, or "hole". That is, 1s correspond to white squares and 0s correspond to red. Permutation matrices are an incomplete characterization, though, since they don't account for the grid's diagonal or anti-diagonal. However they did give me a starting point to enumerate the sequence via code. This is the code I originally wrote to generate \(A(n)\) by enumerating over all permutation matrices:

```python
import numpy as np
from itertools import permutations

def count_permutation_matrices(n):
    count = 0

    # iterate over permutation matrices
    for perm in permutations(range(n)):
        matrix = np.zeros((n, n), dtype=int)
        for row, col in enumerate(perm):
            matrix[row, col] = 1

        # check both diagonals, reject those that aren't valid
        if not any(matrix[i, i] == 1 for i in range(n)):
            continue
        if not any(matrix[i, n - 1 - i] == 1 for i in range(n)):
            continue

        count += 1

    return count

n = 1
while True:
    print(count_permutation_matrices(n))
    n += 1
```

While this code is asympotically (\(O(n!)\)) very slow, that wasn't the point of it; it gave me enough terms to search OEIS for a sequence. It takes less than 5 seconds to obtain the sequence \(1, 0, 2, 10, 48, 270, 2004, 15406, 144656\). [Searching OEIS with these terms](https://oeis.org/search?q=1%2C+0%2C+2%2C+10%2C+48%2C+270%2C+2004%2C+15406%2C+144656&language=english&go=Search) previously yielded no search results, though now you'll get [A378907](https://oeis.org/A378907), which is the subject of this blog post.

I did try to find a closed-form expression or recurrence relation for \(A(n)\), but the best I could do in the limited time that I had was to count the number of grid arrangements with no complete row, column, or _single_ diagonal (disregarding the anti-diagonal). Let's call the number of such arrangements \(A'(n)\). These are the permutations that are also not [derangement](https://en.wikipedia.org/wiki/Derangement)s; a derangement \(\sigma\) is a permutation that has no [fixed point](<https://en.wikipedia.org/wiki/Fixed_point_(mathematics)>), so there is no \(i\) such that \(\sigma(i) = i\). If you look at the binary matrix representing a derangement \(\sigma\), the matrix could not have any elements on its diagonal, because if it did, then \(\sigma\) would fix the corresponding element and not be a derangement. Therefore \(A'(n)\) is exactly the number of permutations on \( n \) that are not derangements. The number of derangements \( D(n) \) for a given \( n \) is a well-studied sequence and is [on OEIS](https://oeis.org/A000166). The number of derangements on \( n \) is called the \(n\)th _subfactorial_, sometimes denoted \( ! n \). So \(A'(n) = n! - !n\).

If we defined an “anti-derangement” (this isn't standard terminology, I just made this up, don't quote me on it) as something complementary to a derangement, so that \( \sigma (i) \ne n + 1 - i \) for all \( 1 \le i \le n \), then by symmetry, the number of anti-derangements for a given \( n \) is exactly the number of derangements. An anti-derangement would correspond to a permutation matrix that doesn't have any 1s along its anti-diagonal. If we had a way of counting the number of permutations \( B(n) \) that are both derangements _and_ anti-derangements, then \( A(n) = n! - 2 \cdot !n + B(n) \) by the [inclusion-exclusion principle](https://en.wikipedia.org/wiki/Inclusion%E2%80%93exclusion_principle). But I wasn't sure how to compute \( B(n) \). Instead, another OEIS user pointed me to a sequence for \( B(n) \) after my submission for \( A(n) \).

## The submission process

At the encouragement of a [physics professor on Bluesky](https://bsky.app/profile/duetosymmetry.com/post/3lcutcw32js2p), I submitted the sequence to OEIS. The sequence was easy enough to describe, but not in OEIS yet, so I thought that it should belong in the database. Furthermore, by exposing this sequence to other mathematicians, I thought I might get a complete answer on an expression for \( A(n) \) from other mathematicians who actually know what they're doing. I was right about that.

The [submission process](https://oeis.org/wiki/Overview_of_the_contribution_process) was straightforward. The first step I had to take was [registering an account with OEIS](https://oeis.org/wiki/Special:RequestAccount), which was slightly more effort than I expected. When signing up, I had to send proof that I was who I was claiming to be before I got an account. I’d guess that this is to [limit the volume of submissions](https://oeis.org/wiki/Why_am_I_limited_to_3_submissions) they receieve every day. I ended up sending a few screenshots of my other online accounts to verify that it's really me.

OEIS treats each submission as mathematicians might a paper submission to a peer-reviewed journal, which is reasonable, since OEIS is a body of ever-growing mathematical knowledge in a very real sense. OEIS maintaining this level of integrity also means that they require authors to use their real names, and not pseudonyms, when registering an account, which unfortunately meant that I couldn’t directly credit the (anonymous) person I discovered this sequence with.

Once I had an account, I sent a draft submission. Doing this was quick since I already had a few terms from the Python program above. I came up with a one-sentence description of the sequence, found a few other related sequences (like the factorial and subfactorial sequences), cross-referenced them, and hit "send". It got added to the queue of all active submissions, which can be viewed [here](https://oeis.org/draft) without having to login to OEIS. I received feedback within just a few hours. Feedback on a submission happens via a comment chain on the submission, and other users can directly edit it while still in draft state. After revising it, this is the one-sentence description of the sequence:

> Number of permutations of [n] with at least one hit on both main diagonals.

Other users also came up with the formula \( A(n) = n! - 2 \cdot !n + B(n) \) like I did, except they also had a recurrence relation for \( B(n) \):


\[
B(n) =
\begin{cases}
(n-1) B(n-1) + 2(n-2) B(n-4), & \text{if } n \text{ is even} \\
(n-1) B(n-1) + 2(n-1) B(n-2), & \text{if } n \text{ is odd}
\end{cases}
\]

with initial conditions:


\[
B(0)= 1, \quad B(1) = 0, \quad B(2) = 0, \quad B(3) = 0.
\]

\( B(n) \) is also on OEIS as [A003471](https://oeis.org/A003471) and actually has an intuitive interpretation if you look at the comments on the entry:

> Suppose you have a group of married couples (plus perhaps one other person).
> You wish to organize a gift exchange so that:
> - each person gives and receives one gift.
> - no one gives himself a gift.
> - no one gives his/her spouse a gift.
>
> Then the sequence gives the number of ways that this can be done.

## _Et cetera_

Much like Wikipedia, OEIS operates on [donations](https://oeisf.org/donate/#DONORS) and volunteers' time. I donated a small amount after my submission was accepted, so my name will eventually appear on the foundation's list of donors.

If you want to search OEIS programmatically by running code, you can do this fairly easily [via GET requests](https://stackoverflow.com/a/6018539) and compute some interesting statistics about the database that way. Please use rate limiting though.

If you caught my pun in the very first sentence of this post, it's that OEIS has this cool feature where you can [listen to sequences](https://oeis.org/play.html). It turns the number sequence into a sequence of notes and lets you configure how you want to do this:

<div style="text-align: center;">
{{< figure src="oeis_play.png" caption="Knobs available to produce a MIDI file." width="50%" >}}
</div>

It lets you download music in [MIDI format](https://cecm.indiana.edu/361/midi.html), meaning you can open and edit it in music composition software like GarageBand or [Musescore](https://github.com/musescore/MuseScore). Here's a [MIDI](phi.midi) for [Euler's phi](https://en.wikipedia.org/wiki/Euler%27s_totient_function) function. It sounds really weird. Here's in an .mp3 of it so you can listen to it directly in the browser:

<div style="display: flex; justify-content: center;">
    <audio controls preload="auto">
        <source src="phi.mp3">
    </audio>
</div>