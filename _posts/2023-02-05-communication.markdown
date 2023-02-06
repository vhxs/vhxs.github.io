---
layout: post
title: Communication in the abstract
tags: distributed, blockchain, simplicial complex, phd, logic
published: true
---

My PhD in computer science was nominally and technically on a topic in distributed computing, but the *methodology* was much closer to combinatorics and [algebraic topology](https://mathworld.wolfram.com/AlgebraicTopology.html), and results I derived were computability[^4]-theoretic; these are all fields in *pure* mathematics. I therefore find it difficult to explain to others that my dissertation *substantially* diverges from what is considered classical distributed computing, so this post is meant to shed some light on what it is that I studied as a graduate student, and how it fits into the broader context of distributed computing as an academic discipline.

I'd like to pick a few concepts I spent years thinking about, from my [dissertation](https://cs.brown.edu/research/pubs/theses/phd/2019/saraph.vikram.pdf), and explain them in detail, since the connections between [distributed computability](https://dl.acm.org/doi/abs/10.1145/2421096.2421118) and algebraic topology are not really obvious at all. But they do run deep. I will refer to concurrent and distributed systems interchangeably since at a high enough level of abstraction, they are the same. *Processes* are abstract agents that communicate with one another, and could represent nodes communicating over a computer network, carrier pigeons delivering letters point-to-point, or people communicating over instant messaging.

### Registers and read/write memory

In concurrent programming, one way processes communicate is via shared memory. To reason about shared memory, shared memory is mathematically modeled in various ways, but the simplest way is as a set of abstract registers that processes can individually write to and read from. Reads and writes can happen concurrently since processes can execute these operations concurrently. A register is called [*safe*](https://en.wikipedia.org/wiki/Safe_semantics) if:
- A read not concurrent with any write returns the value written by the latest write.
- A read that is concurrent with a write may return any value within the register's allowed range of values.

Whether safe registers actually exist in hardware seems to be more of a [philosophical](https://cstheory.stackexchange.com/questions/29069/in-what-sense-does-a-safe-register-exist) [point](https://stackoverflow.com/questions/25728948/programming-safe-regular-atomic-registers-with-java) rather than a practical one:

Safety is really the minimal guarantee you should expect any register to have. It's not asking much of a register. But from safe registers, one can mathematically construct registers with much stronger properties. A register is called [*atomic*](https://en.wikipedia.org/wiki/Atomic_semantics) if any sequence of reads and writes can be *linearized*, or if they appear to happen in a sequential order ([linearizability](https://cs.brown.edu/~mph/HerlihyW90/p463-herlihy.pdf) is a entire subject on its own that I won't discuss here). The construction of atomic registers from safe registers can be found in Leslie Lamport's seminal paper [*On Interprocess Communication*](https://courses.cs.washington.edu/courses/cse452/22wi/papers/lamport-on-interprocess-communication.pdf).

The closest analogue of atomic registers that I can think of in a programming language is the [`AtomicInteger`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/atomic/AtomicInteger.html) in Java. Its `get` and `set` operations are atomic reads and writes, respectively.

### Atomic snapshots

If we assume that the number of processes is known beforehand, say $$N$$ of them, then we can construct yet more idealized models of shared memory. In the *atomic snapshot* model, $$N$$ processes share access to an array of registers, all initialized to a null value, and processes can execute two operations on this array:
- Process $$p_i$$ can write to its assigned register $$i$$
- Any process can take a *snapshot* of the entire array

As the name suggests, both writes and snapshots are atomic. Atomic snapshots we introduced in [*Atomic Snapshots of Shared Memory*](https://people.csail.mit.edu/shanir/publications/AADGMS.pdf) and can be constructed from atomic registers.

This is a good time to restate that these are all *idealized* versions of shared memory, used primarily to prove impossibility and computability results in the theory of concurrency and distributed computing. Implementing atomic snapshots is *provably* hard in practice. There are all kinds of [complexity-theoretic](https://en.wikipedia.org/wiki/Computational_complexity) results out there on their implementations, including impossibility results on lower bounds of round complexities, attempts to make them probabilistic with randomized algorithms, etc, though these results falls outside of the scope of my dissertation. Theoretical advances on these topics are typically published in [PODC](https://www.podc.org/), [DISC](http://www.disc-conference.org/wp/), or [OPODIS](https://www.opodis.net/).

From atomic snapshots, we can go one step further and define the *immediate* atomic snapshot, or just immediate snapshot. As with atomic snapshots, processes share access to a register array, but the write and snapshot operations are combined into one. When a process executes an immediate snapshot on the shared array, it writes a value to its assigned register, then takes a snapshot right after. At best, if another process writes its value after the first one, but before the first returns its snapshot, then both processes are guaranteed to return the same snapshot; the second one cannot observe more than the first. Letting $$S_i$$ be the snapshot of process $$p_i$$, this property is formalized in the following way:
- Self-containment: $$\forall i: i \in S_i$$
- Atomicity: $$\forall i, j: S_i \subseteq S_j \vee S_j \subseteq S_i$$
- Immediacy: $$\forall i, j: i \in S_j \rightarrow S_i \subseteq S_j$$

Each immediate snapshot array is *one-shot*, or usable only once per process. To enable processes to take more than one snapshot, we simply use more than one immediate snapshot array, as many as needed to implement a hypothetical algorithm. Immediate snapshots are probably among the strictest, structured, and well-behaved models of shared memory, and that allows one to more easily reason about them in proofs. [*Immediate Atomic Snapshots and Fast Renaming*](https://dl.acm.org/doi/pdf/10.1145/164051.164056) is the first paper to introduce this model and also its construction from atomic snapshots.

The main takeaway here is this: since we can theoretically construct immediate snapshots from safe registers, these two models of shared memory (and every one in between) are computationally equivalent. Any concurrent algorithm that is *computable* (that is, disregarding any notion of complexity) from immediate snaphots is also computable from safe registers.

### Simplicial complexes and distributed system states

As I'll discuss in the next section, immediate snapshots give rise to interesting topological and combinatorial structures called *simplicial complexes*. A simplicial complex is a kind of higher dimensional generalization of a graph [^1], where more than two nodes in a graph can be connected together by what's called a simplex. Edges connecting two nodes are $$1$$-simplexes, triangles connecting three nodes are $$2$$-simplexes, and in general, $$n+1$$ nodes are connected together by $$n$$-simplexes. You could go to [Wikipedia](https://en.wikipedia.org/wiki/Simplicial_complex) to find an example of a simplicial complex, but here's one I drew myself:

<center><img src="https://user-images.githubusercontent.com/93892166/216788942-aa0c8245-9ac2-4ab0-bc7e-f1b42fc01d77.png" width="400"></center>

*Chromatic* simplicial complexes, or complexes whose vertices are labeled with colors, can be used to model and reason about abstract multi-agent systems. Specifically, consider a system with $$n$$ agents, with each agent having a unique *color*. Then create a node for each possible state that an agent can be in, with the node colored by the agent's color. This set of nodes is a 0-dimensional simplicial complex. Next, add 1-simplexes, or edges, between pairs of nodes whose states they represent are possible simultaneously. Clearly we cannot connect nodes of the same color, since an agent can only be in one state at a given time. Now we have a graph. Continue this process by adding 2-simplexes among node triples whose states are possible simultaneously. Continuing this construction all the way to $$n$$, we end up with an $$n$$-dimensional simplicial complex. Each $$n$$-simplex represents one among many possible global states within the system.

As an example, suppose Alice, Bob, and Carole want to see a movie. Alice doesn't want to go alone, but Bob and Carole don't like each other, so that one doesn't go if the other one does. In this system, each of Alice, Bob, and Carole either go to a movie, or they do not, so there are six different individual states. Let's draw them:

<center><img src="https://user-images.githubusercontent.com/93892166/216788869-eb111201-3726-4f23-bda5-4e9dcd676bfe.png" width="400"></center>

In the above, <span style="color:red">Alice is red</span>, <span style="color:yellow; background-color:black">Bob is yellow</span>, and <span style="color:green">Carole is green</span>; a shaded vertex indicates that the person is a No :heavy_multiplication_x: to going, and non-shaded vertices are Yes :heavy_check_mark:. Next, we can draw edges between nodes of different colors whose states are compatible together:

<center><img src="https://user-images.githubusercontent.com/93892166/216788874-ebd3073e-2b0b-4fbd-9f99-82906e527dea.png" width="400"></center>

Notice how there's no edge connecting the non-shaded yellow and green circles. That's because Bob and Carole don't like each other.

<center><img src="https://user-images.githubusercontent.com/93892166/216788882-56f6388b-9992-40bf-ae24-1e42323b14b0.png" width="400"></center>

Next, we fill in all triangles (or $$2$$-simplexes) that capture the combinations in which three go to (or don't go to) see the move. The triangle that looks like is missing corresponds to the case where Alice would go see a movie alone.

### Connections with other areas of math

Based on the example above, if it seems like there is a relationship between chromatic simplicial complexes and the concept of *possible worlds* in epistemic logic, that's because there is. Each maximal simplex can be thought of as a possible world in a distributed system. Both Herlihy's book on [Distributed Computing through Combinatorial Topology](https://www.sciencedirect.com/book/9780124045781/distributed-computing-through-combinatorial-topology) and Fagin's book on [Reasoning about Knowledge](https://www.cs.rice.edu/~vardi/papers/book.pdf) begin with the [muddy children puzzle](https://plato.stanford.edu/entries/dynamic-epistemic/appendix-B-solutions.html#muddy), which is a toy problem that illustrates the combinatorial complexity of reasoning about possible states even within a small system. In the past few years, there have been [a few](https://personal.cis.strath.ac.uk/jeremy.ledent/assets/pdf/STACS22.pdf) [papers](https://link.springer.com/chapter/10.1007/978-3-030-88853-4_3) published formalizing the correspondence between simplicial complexes and epsitemic logic, [including one](https://strathprints.strath.ac.uk/73836/1/Goubault_etal_IAC_2020_A_simplicial_complex_model_for_dynamic_epistemic_logic.pdf) that establishes an equivalence of categories between chromatic simplicial complexes and Kripke frames when these two are formalized as categories.

Simplicial complexes are a mathematical construct that originally arose from the study of algebraic topology, and they play a crucial role in the computation of [homology groups](https://en.wikipedia.org/wiki/Simplicial_homology). [This video](https://www.youtube.com/watch?v=sgzPex6FIbA) does a great job at explaining their relevance to the field. They generalize to CW-complexes, for which there is a wealth of historical literature. CW-complexes are a nice sweet spot between simplicial complexes and the [wild west](https://mathoverflow.net/a/74877) that are [arbitrary](https://njwildberger.com/2015/12/02/the-alexander-horned-sphere-is-it-nonsense/) [topological](https://blogs.scientificamerican.com/roots-of-unity/a-few-of-my-favorite-spaces-antoines-necklace/) [spaces](https://math.ucr.edu/~res/math205C/longline.pdf)[^2]. Simplicial complexes are fundamentally combinatorial objects whose properties are captured purely as sets, though at the same time, they can be treated and reasoned about as topological objects. Some of the related theorems are readily transferable to simplicial complexes, including the [cellular approximation theorem](https://en.wikipedia.org/wiki/Cellular_approximation_theorem). A good introduction to algebraic topology is [Allen Hatcher's book](https://pi.math.cornell.edu/~hatcher/AT/AT.pdf) which is free online.

### Immediate snapshots revisited

Let's revisit the immediate atomic snapshot and look at the simplicial complex that it gives rise to. Imagine a system of $$n$$ processes that all execute an immediate snapshot on a shared array. If each process $$p_i$$ has exactly one possible value it can write to the array, say its ID $$i$$, then the processes' starting states are represented by a single $$n$$-simplex. With three processes, this would just look like a triangle, corresponding to a single possible global state:

<center><img src="https://user-images.githubusercontent.com/93892166/216788850-f243c09e-7e87-4548-af94-2d2b592cb8e6.png" width="400"></center>

Now consider all possible global states of the system after the processes execute an immediate snapshot. After executing an immediate snapshot, each process observed some subset of other processes; if it was first, then it would have observed no other processes and its snapshot would only contain its ID. If a process is last to execute its snapshot, it observes every single other ID in the array. If, in the case of three processes, we draw all possible states and link them together with simplexes, we get this:

<center><img src="https://user-images.githubusercontent.com/93892166/216788860-6e3ecc53-e556-4b30-9615-3c268f13baf8.png" width="400"></center>

This looks a lot like the original single triangle we started with, but subdivided many ways. The resulting complex we obtain is called the [*standard chromatic subdivision*](https://arxiv.org/abs/1506.03944) of the original complex[^3]. If the three processes execute *another* immediate snapshot, using the snapshots obtained from the first round as their respective states, then we get an *even more subdivided* triangle:

<center><img src="https://user-images.githubusercontent.com/93892166/216788865-bbc33bd9-dc9b-434c-82ac-886c986b1478.png" width="400"></center>

The processes can repeat this procedure arbitrarily many times, with the resulting possible global states being represented by an ever more deeply subdivided triangle. The important takeaways here are (1) immediate snapshots (and therefore read/write memory in general) cannot alter the topological structure of the distributed system (immediate snapshots only subdivide the space) and (2) the number of possible states in a distributed system grows combinatorially as processes communicate with one another. In this particular case, there are $$13^n$$ possible global states among three processes that execute $$n$$ immediate atomic snapshots; this is a perfect illustration of why [*correctness in concurrency is hard*](https://concurrencyfreaks.blogspot.com/2021/12/the-importance-of-correctness-in.html), since one has to verify the correctness of *every possible interleaving* of a concurrent algorithm. 

In the example above, we considered a system where each process has a single possible starting state (i.e. one possible global state). In cases where processes have more than one possible starting state (as in the movie example from the previous section), executing an immediate snapshot results in each simplex being separately subdivided; this works out since the standard chromatic subdivision is consistently defined along boundaries. Consider for example a system in which processes' starting states are represented by a hexagon. Then after one immediate snapshot, we'd get the following simplicial complex:

<center><img src="https://user-images.githubusercontent.com/93892166/216789894-c6904fb4-841e-445d-9e89-d8d62806893d.png" width="400"></center>

Again, notice that we now have a subdivided hexagon; that is, the immediate snapshot has not fundamentally altered the topological structure of the processes' initial states.

### Synchronization primitives and consensus

The [*consensus problem*](https://en.wikipedia.org/wiki/Consensus_(computer_science)) is one that is central to the theory of distributed systems (it is [*universal*](https://dl.acm.org/doi/10.1145/99164.99185) among concurrency problems in a very specific sense). The problem is typically stated as follows. Given $$n$$ processes each with an input value $$v_i$$, a solution to the consensus problem is a distributed algorithm that satisifies the following three properties:
- Termination: Eventually, every non-faulty process returns a value.
- Agreement: All non-faulty processes return the same value.
- Validity: The value returned by non-faulty processes must have been the input of *some* process.

The fact that immediate snapshots cannot change the topology of a distributed system's state space is related to the [FLP impossibility theorem](https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf) (named after its authors), which roughly states that there is no distributed algorithm implementable from only read/write memory, that solves consensus, when even one process may fail-stop. The corresponding impossibility theorem in topology land is the [No-retraction theorem](https://en.wikipedia.org/wiki/Retraction_(topology)#No-retraction_theorem), which states that there is no continuous function mapping an $$n$$-dimensional ball to its boundary (which is a sphere). It turns out that for a distributed algorithm to solve consensus among processes, it would be forced to tear holes in the processes' complex. But an algorithm implemented only from read/write memory cannot do this, since tearing holes is an operation that changes the topology of a space. Tearing holes in a space is *not* a [homeomorphism](https://www.youtube.com/watch?v=Bu7P1qzmP78).

To solve consensus, one needs to use communication primitives stronger than read/write memory. There are many different synchronization primitives out there, some implemented in hardware and software, including [mutex locks](https://en.wikipedia.org/wiki/Lock_(computer_science)), [barriers](https://en.wikipedia.org/wiki/Barrier_(computer_science)), and [semaphores](https://en.wikipedia.org/wiki/Semaphore_(programming)), among many others. Lower level primitives include [test-and-set](https://en.wikipedia.org/wiki/Test-and-set) and [compare-and-swap](https://en.wikipedia.org/wiki/Compare-and-swap) (the latter which I brifely wrote about in another post). Synchronization primitives enable one to control the way in which processes may interleave, thus restricting their possible outcomes and hence the realizable simplexes in system's complex. Controlling their concurrency in the right way *can* therefore tear holes in the system's state space.

Compare-and-swap (or CAS), in particular, can solve consensus among arbitrarily many process (or CAS has [infinite consensus number](https://www.cs.yale.edu/homes/aspnes/pinewiki/WaitFreeHierarchy.html)). The algorithm is quite straightforward to write in pseudocode; if processes have access to a shared atomic variable that can be CAS'd, then we can implement a `decide` function as follows

```python
def decide(input_value):
    # decision is shared and initialized to None
    compare_and_swap(decision, None, input_value)

    # the final value of decision is the processes' consensus value
    return decision
```

It turns out that solving consensus among processes completely rips apart the processes' state space into maximally disconnected components.


### Tearing holes

As a more visual example of how synchronization primitives alter the topology of the system's space, consider the *delayed* immediate snapshot, which I myself introduced in [Asynchronous Computability Theorems for t-Resilient Systems](https://link.springer.com/chapter/10.1007/978-3-662-53426-7_31). It is a variation on a two-round immediate snapshot protocol, where a synchronization barrier is applied between the two rounds. Its purpose is, informally, to only allow process interleavings where every process observes at least a certain number of other processes (this number controllable by a parameter $$t$$). This is what the pseudocode for it looks like:

```python
# mem0 and mem1 are shared arrays of length n+1
# done is a shared boolean variable
done = False
def delayed_snapshot(_id):
    immediate:
        mem0[_id] = _id
        snap0 = snapshot(mem0)
    if |snap0| <= n - t:
        while not done:
            pass
    immediate:
        mem1[_id] := snap0
        snap1 := snapshot(mem1)
    done = True
    return snap1
```

In English, a process first executes and captures an initial snapshot. If, in this snapshot, it observes enough other processes above a threshold, then it proceeds with the second snapshot. If, on the other hand, it observes too few others, it waits on any other process to set the boolean `done` flag, indicating the threshold has been reached. Once this flag is set, only then does it proceed with the second snapshot.

Decreasing the number $$t$$ strips more from the simplexes' boundaries. Starting with the hexagonal complex as before, this is what the $$1$$-resilient delayed snapshot does:

<center><img src="https://user-images.githubusercontent.com/93892166/216789673-6818a288-bc5d-444f-993e-3995908e6cdf.png" width="400"></center>

Applying the delayed snapshot has clearly altered the topology of the original hexagon, since the resulting space (call it $$\mathcal{K}_1$$) is no longer [simply connected](https://en.wikipedia.org/wiki/Simply_connected_space). Its [fundamental group](https://en.wikipedia.org/wiki/Fundamental_group) is no longer trivial; instead, $$\pi_1(\mathcal{K}_1) = \mathbb{Z}$$.

If we look at the effect of the $$0$$-resilient delayed snapshot, we get this:

<center><img src="https://user-images.githubusercontent.com/93892166/216789668-8cf36250-59e9-4cc0-860a-6079c04f78df.png" width="400"></center>

This space (call it $$\mathcal{K}_0$$) isn't even connected anymore; it has been completely torn apart. CAS does this too, if we were to visualize its effect on a system's possible state space.

In higher dimensions (or with more processes), the degree of a space's connectedness is characterized by its [higher homotopy groups](https://en.wikipedia.org/wiki/Homotopy_group), which are *very* hard to compute in general. We don't even know what the [homotopy groups of spheres](https://en.wikipedia.org/wiki/Homotopy_groups_of_spheres#Table_of_homotopy_groups) look like.

### Ending thoughts

"Distributed computing" can mean many different things depending on the context. This is probably in part due to the sheer number of the different kinds of distributed systems that are out there. Almost anything can be described as a distributed system: nodes in computer networks, people in social networks, [cars in a traffic network](https://www.reddit.com/r/pics/comments/6qulze/traffic_deadlock/), parts moving through supply chains, etc. And there are all kind of mathematical models ([actor model](https://en.wikipedia.org/wiki/Actor_model), [Petri nets](https://en.wikipedia.org/wiki/Petri_net)) that researchers have developed to describe distributed systems[^5]. The model described in this post was primarily developed to study the *computability-theoretic* aspects of distributed systems, and is therefore an extremely idealized model, with little by way of direct applications other than extending the frontier of human knowledge.

Blockchains are a particular kind of distributed system that have garnered lots of interest over the [past decade](https://trends.google.com/trends/explore?date=all&geo=US&q=blockchain), mainly due to the cryptocurrency and NFT hype. While most problems solvable by a blockchain can be solved by some variation of a distributed database, there are lots of interesting *research* questions that emerge from the dynamics that are unique to blockchains. Take for example [A Knowledge-Based Analysis of the Blockchain Protocol](https://arxiv.org/pdf/1707.08751.pdf), or [Atomic Cross-Chain swaps](https://arxiv.org/pdf/1801.09515.pdf). However, decentralized systems, which blockchains are an instance of, have been around for a while.

Since studying social media and social networks, I have wondered about the potential for modeling their various aspects using simplicial complexes. In chat applications like Discord and Slack, users can create communication channels that selectively include certains sets of people. Sending a message to a channel looks a lot like an [atomic broadcast](https://en.wikipedia.org/wiki/Atomic_broadcast) to that channel. Contrast this with communication over direct messages only. Communication via broadcasts to a set of $$n$$ could be modeled as an $$n-1$$ simplex, with DM-only communication represented by the complex obtained from taking the $$1$$-[skeleton](https://en.wikipedia.org/wiki/N-skeleton) of this simplex.

Since finishing my PhD, I have gained a lot of hands-on experience with software technologies, like MongoDB, Elasticsearch, Kubernetes, Kafka, and Redis, that incorporate quintessential concepts from distributed systems when deployed at scale. Examples include:
- The [Paxos consensus protocol](https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf), and its more [comprehensible](https://types.pl/@wilcoxjay/109799400461121947) alternative [Raft](https://raft.github.io/), are both used a lot in real-world distributed systems for solving problems like [leader election](https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/) and [log replication](https://martinfowler.com/articles/patterns-of-distributed-systems/replicated-log.html). [etcd](https://etcd.io/), a Kubernetes dependency for maintaining cluster state, uses Raft.
- ZooKeeper is a dependency is of Kafka, and implements [Zab](https://marcoserafini.github.io/papers/zab.pdf), an atomic broadcast protocol.
- In practice, linearizability is a very strong and expensive condition to guarantee. NoSQL databases sacrifice this level of consistency for [weaker forms](https://jepsen.io/consistency), like [causal consistency](https://jepsen.io/consistency/models/causal). MongoDB's consistency guarantees are configured by varying its [write concern](https://www.mongodb.com/docs/manual/reference/write-concern/).

If you want to learn more about the practice of distributed systems today, you probably don't need to learn that much more beyond some of the main theoretical results in distribured computing. [Designing data intensive applications](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781491903063/) distills some of the core concepts and terminology into a single book. [Awesome distributed systems](https://github.com/theanalyst/awesome-distributed-systems) is a GitHub repository which aggregates a ton of useful resources to learn.

[^1]: Hypergraphs are actually more general. This difference is that simplicial complexes are required to be [downward closed](https://en.wikipedia.org/wiki/Upper_set).
[^2]: [*Counterexamples in Topology*](https://www.amazon.com/Counterexamples-Topology-Dover-Books-Mathematics/dp/048668735X) is full of wild topological spaces. As with all Dover books it's cheap. Buy it.
[^3]: This is closely related to the more common [barycentric subdivision](https://en.wikipedia.org/wiki/Barycentric_subdivision).
[^4]: Or [*recursion*-theoretic](https://en.wikipedia.org/wiki/Talk:Computability_theory), if you're from the west coast and not the [midwest](https://math.uchicago.edu/~drh/mcs/Jointseminar.html).
[^5]: This is in contrast with traditional computing, where the Turing machine (and its equivalent variants) have been long established as *the* way to abstractly model computers.