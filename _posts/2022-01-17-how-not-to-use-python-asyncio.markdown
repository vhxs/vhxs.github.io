---
layout: post
title: How not to use Python Asyncio
tags: python, concurrency, failure
published: true
---

I'm not sure how many people write about their failures, but I think there's value in doing so if you learned something in the process of failing. In this case, I tried to use Python's `asyncio` library to do something that would never work, but I also learned *why* it wouldn't work.

`asyncio` is a Python library used to write concurrent code, and just like JavaScript, uses the `async/await` syntax. Also as with JavaScript, node.js, and v8, `asyncio` runs code in a single thread. This might seem confusing at first if you've written multithreaded code, because what does concurrency mean in the context of a single thread?

This is where it's useful to distinguish between concurrency and parallelsim. *Parallelism* is where we have one or more tasks, and many workers, and we want to divide tasks among workers. Division of labor can be either easy or hard depending on how inherently divisble the tasks are: for example, sorting is hard to parallelize, but counting words in documents is easy to parallelize. *Concurrency* refers to the idea of a single worker working on many tasks simultaneously by switching between them, and is one way for multiple workers to achieve parallelism. An operating system juggles many applications concurrently by (context) switching between them. There's a lot of writing on this topic, by people smarter than me, which goes into more depth explaining concurrency vs parallelism.[^1] [^2]

So concurrency is a meaningful concept even when you have one worker, like the single thread used in JavaScript's event loop or in `asyncio`. That single thread might want to switch from one task that's waiting on the response from an HTTP request, to another task that has all the necessary data dependencies readily available in memory.

I tried to use `asyncio` to implement two "workers", or in this case, Alice and Bob, participating in Diffie-Hellman key exchange that I wrote about here. I originally wrote Alice's code and Bob's code as two separate tasks, and since they need communicate, I tried to use a TCP connection for this, with Alice being the client that opens a connection with Bob's server. Minimally, this is what my code looked like:

{% highlight python %}
import asyncio
import socket

async def alice():
    print("started alice")
    # alice's task starts: she attempts to connect to Bob's server
    while True:
        try:
            # this is where we try to connect to bob's server
            # if the server hasn't started, we try again
            # but we never reach the point of being able to try again (see bob's code)
            conn = socket.create_connection(('127.0.0.1', 1337))
        except Exception as e:
            print(f"got exception {e}, retrying...")
            await asyncio.sleep(1)

    # proceed with diffie-hellman, using conn to communicate with bob
    print("alice never reaches this point")

async def bob():
    print("started bob")
    # bob's task starts: he spins up a server and listens for incoming connections
    sock = socket.create_server(('127.0.0.1', 1337))

    # this is a blocking call, which halts execution of the asyncio event loop
    print("waiting for connections...")
    conn, _ = sock.accept()

    # this is where we would proceed with diffie-hellman, if we ever got to this point
    print("bob never reaches this point")

async def main():
    # create tasks
    run_alice = asyncio.create_task(alice())
    run_bob = asyncio.create_task(bob())

    # run them concurrently
    await asyncio.gather(run_alice, run_bob)

if __name__ == '__main__':
    asyncio.run(main())

{% endhighlight %}

When I run this code, I see the following output:

{% highlight shell %}
started alice
got exception [Errno 61] Connection refused, retrying...
started bob
waiting for connections...
{% endhighlight %}

And the program stalls. The problem here is when Bob calls `sock.accept`. This function call is *blocking*, meaning that program execution does not proceed until a client requests to open a connection. However, by blocking at `sock.accept`, it blocks *the entire `asyncio` event loop*, including the code that Alice would execute the open a connection with Bob's server. So `sock.accept` deadlocks the entire program.

The lesson here is avoid using blocking function calls in a single-threaded event loop like what's used in `asyncio`. `asyncio` has its own bindings for creating TCP connections and servers, though I haven't looked that deeply into it. Instead, to implement Diffie-Hellman key exchange, I opted to use Python's `threading` library, which supports honest-to-goodness multithreading. Alice and Bob run their code in their own respective threads.

[^1]: It's [this](https://justinpombrio.net/2020/01/25/concurrency.html) that really made me think about the utility of distinguishing between concurrency and parallelism: 
[^2]: [Talk](https://go.dev/blog/waza-talk) by Rob Pike, one of the creators of golang, on concurrency.