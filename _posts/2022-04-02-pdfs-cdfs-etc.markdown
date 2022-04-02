---
layout: post
title: PDFs and CDFs via Measure Theory
tags: math, probability, measure theory
published: true
---

This post is redux of one of my few I posted on the first iteration of my blog. Writing this down helped me understand the vague way in which statisticians and applied mathematicians refer to probability distributions. Unedited, except to ensure that the embedded LaTeX renders.

&nbsp;

&nbsp;

&nbsp;

This post will be about Chapter 1 of Casella's Statistical Inference, with a particular focus on probability distributions, probability density functions, and cumulative distribution functions. The term "probability distribution function" has been (ambiguously) used to describe any of these functions, which can be confusing to readers. The goal of this blog post is to prove a more rigorous justification for why it is actually okay to use this term ambiguously.

Casella introduces the following definitions:

The measure-theoretic approach to define a probability space is used. Namely, a probability space is a sigma algebra $$B$$ over a set $$S$$, together with set function $$ P: B \to [0, 1]$$. The set $$ S$$ is the sample space, while elements of $$ B$$ are called events. The function $$ P$$ satisfies the usual requirements of a measure, with the additional constraint that $$ P(S) = 1$$. These requirements are called the Kolmogorov axioms. (If $$ S$$ is finite and $$ B$$ is the power set sigma algebra, then one can define $$ P$$ in terms of $$ P(s_i)$$ for each $$ s_i \in S$$, so long as they sum to $$ 1$$. The same is true of a countable sample space.)
A $$ T$$-valued random variable is a measurable function $$ X : S \to T$$, where $$ T$$ is a measurable space. In practice, it is usually the case that $$ X$$ is real-valued (with $$ \mathbb{R}$$ given the Borel algebra), so henceforth $$ X$$ is a measurable function $$ X: S \to \mathbb{R}$$. Measurability of $$ X$$ is a technicality and rarely ever discussed.

Given a random variable $$ X$$, we can define a new probability function on its range $$ \mathbb{R}$$. We are using the Borel algebra on $$ \mathbb{R}$$, so its events are simply Borel sets. The induced probability function (which I will abbreviate as IPF) $$ P_X$$ is defined as the pushforward measure of $$ P$$, or for Borel $$ A \subseteq \mathbb{R}$$:

$$ P_X(A) = P(X^{-1}(A))$$

One can verify that $$ P_X$$ satisfies the Kolmogorov axioms. Hence, in defining $$ X$$, we have implicitly defined a probability space on its range $$ \mathbb{R}$$. The cumulative distribution function (or CDF) $$ F_X : \mathbb{R} \to [0, 1]$$ is given by:

$$ F_X(t) = P_X(X \le t)$$

Note that this definition only makes sense because $$ \mathbb{R}$$ is ordered. Every random variable has a CDF defined as above, but why do we care about them? It turns out that $$ F_X$$ and $$ P_X$$ uniquely determine one another. The above equation defines $$ F_X$$ in terms of $$ P_X$$, but one can go the other way as well.

If we are given the CDF of a random variable $$ X$$, we can recover its IPF $$ P_X$$. To see how, one can interpret the CDF as defining the measure (or probability) of sets of the form $$ (- \infty, t]$$. These sets generate the Borel algebra, so the measure of any other Borel subset of $$ \mathbb{R}$$ is determined by the values $$ P_X$$ takes on the $$ (- \infty, t]$$. From this observation, we can extend $$ F_X$$, defined on subsets $$ (- \infty, t]$$, to $$ P_X$$ defined on all Borel subsets of $$ \mathbb{R}$$. Constructing the extension can be made rigorous using Caratheodory's extension theorem; see this document for a formal proof. In essence, the CDF and the IPF of a random variable give us the same information about that random variable.

We can take the identification of $$ F_X$$ with $$ P_X$$ one step further. Recall that, informally, a function is absolutely continuous if it has a derivative almost everywhere that satisfies the Fundamental Theorem of Calculus. A measure $$ \lambda$$ is absolutely continuous with respect to measure $$ \mu$$ if all $$ \mu$$-negligible sets are also $$ \lambda$$-negligible. Then $$ F_X$$ is absolutely continuous if and only if $$ P_X$$ is absolutely continuous with respect to the Borel measure. (This fact can be derived using linearity of integrals, the monotone converge theorem, and approximation of measurable sets by $$ G_\delta$$ sets). The Wikipedia article on absolute continuity mentions this relationship here.

When either CDF or IPF are absolutely continuous, we can define the probability density function (or PDF), $$ p_X$$, as the derivative of $$ F_X$$, which is equivalently the Radon-Nikodym derivative of $$ P_X$$ with respect to the Borel measure:

$$ p_X = \dfrac{dF_X}{dt} = \dfrac{dP_X}{d \mu}$$

As a derivative, the PDF is unique up to measure zero, so it can be treated as unique for all practical purposes. Given a PDF, the unique CDF defining it can be recovered by simply taking the appropriate antiderivative of the CDF. (A PDF is instead called a probability mass function if the range of the corresponding CDF is finite).

In summary: While people may use the word "distribution" liberally (e.g. $$ X$$ and $$ Y$$ have the same "distribution"), there is a solid mathematical justification in doing so. CDFs and IPFs contain the same information about a random variable, since each is uniquely determined by the other. PDFs (uniquely) exist when either CDF/IPF is absolutely continuous, and they determine the CDF/IPF.

Other tidbits from this chapter:

Bonferroni's inequality, which I had not come across before (at least by name) is given by $$ P(A \cap B) \ge P(A) + P(B) - 1$$, and can provide a lower bound on the probability of simultaneous events $$ A$$ and $$ B$$. It is easily derived from the Kolmogorov axioms.
Boole's inequality, also known as the union bound, states that the probability of a union of events is bounded by the sum of their probabilities. This inequality is essentially the countable sub-additivity axiom of the outer measure.