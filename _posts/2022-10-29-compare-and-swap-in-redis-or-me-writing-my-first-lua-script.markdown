---
layout: post
title: Compare-and-swap in Redis or (me writing my first Lua script)
tags: cas, concurrency, lua, redis, atomicity, consensus, python
published: true
---

## What is compare-and-swap?

Compare-and-swap (or *CAS* for short) is an instruction that operates on a memory location to atomically
replace the value stored at that location with another value. It takes three arguments: (1) a memory address, (2) an expected value, and (3)
a replacement value, and succeeds only if the value in the given memory location is equal to the provided
expected value.

CAS has direct support at the hardware level, as `CMPXCHG` (compare and exchange) in the x86 instruction set,
or just as `CAS` in the ARM instruction set. Some programming languages (not Python) implement an interface for CAS,
such as `CompareAndSwap` in Go, or `__sync_bool_compare_and_swap` in C and C++.

There is a lot of published work on the theory of CAS, historically in SPAA, PPoPP, PODC, or DISC. CAS is a fundamental synchronization primitive
used in the design and implementation of concurrent data structures,
particularly because we can use CAS to take any object, and turn it into a thread-safe concurrent object with non-blocking methods
(or more precisely, depending on who you're talking to, a wait-free linearizable object). This is known in concurrent data
structures as *universality*, and in general, any object or instruction with infinite consensus number, like
CAS, is universal.

CAS is sometimes used in the implementation of lock-free data structures, in place of lock-based approaches which can
be prohibitive to use under high-contention workloads. Its most notable applications seem to be in the Linux kernel, probably since the kernel has to simultaneously juggle dozens of processes that all contend for the same resources. [This looks relevant](https://lwn.net/Articles/847973/), but I don't know a whole lot about concurrency as it relates to the Linux kernel.

## Consensus

One application of CAS is to decide which among several processes is first to access a shared resource. Suppose we initialize a
shared variable to a null value, and we have N processes all simultaneously calling CAS to update the variable with its own
unique process ID. Then since CAS is atomic, exactly one process $p_i$ will win out and update the variable so that it stores its ID $i$. After calling CAS, each process knows who the winner was.

This can be thought of as solving *consensus* among the processes.

## Can we do this in Redis?

My primary motivation for writing this post is exactly because I am building
a multiprocess Python application, and need to decide which among possibly several processes get to update a common document.

Python [does not](https://stackoverflow.com/questions/45802491/compare-and-swap-instruction-in-python) have a CAS implementation, probably because of the global interpreter. But the application I'm building does have access to a Redis server, which is an in-memory key-value
store (often used as middleware, such as a message broker). Redis exposes an interface where one stores a value for a given
key, sort of like RAM, so it is reasonable to think that Redis might support CAS operations.

Unfortunately, the main developer of Redis explicitly [wanted to exclude support for CAS](https://groups.google.com/g/redis-db/c/a4zK2k1Lefo/m/hOjM9iwDGhIJ), comparing it with the `Check-and-Set`
operation in memcached (a competitor technology) and what he didn't like about it. So Redis doesn't implement CAS.

Redis does have transactions though, and its [documentation claims](https://redis.io/docs/manual/transactions/) that Redis transactions can be used to implement CAS semantics.

### Attempt 1

So I went ahead and tried it out. This was my first attempt at implementing a CAS-like operation with
Redis:

```python
# Attempt 1 at implementing compare-and-swap (CAS) using Redis transactions.
# This attempt fails since pipeline.get can't be evaluated within the scope
# of a transaction. Its return value cannot be used within a transaction,
# so we cannot conditionally invoke pipeline.set based on what is returned by pipeline.get.
# Below, current_value isn't actually None, but a reference to a pipeline.get operation
# to be queued into the transaction.

import redis
from multiprocessing import Process
import time


def check_and_set(key, value):
    cache = redis.Redis(host="localhost", port=6379)
    txn = cache.pipeline()
    txn.watch(key)
    try:
        txn.multi()
        current_value = txn.get(key)
        if current_value is None:
            txn.set(key, value)
            print("success!")
        txn.execute()
    except redis.exceptions.WatchError:
        pass


if __name__ == "__main__":
    num_processes = 8
    key = f"key{time.time()}"

    processes = []
    for i in range(num_processes):
        p = Process(target=check_and_set, args=(key, i))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
```

Redis transactions are created as `pipeline` objects. Calling `pipeline.multi` denotes the beginning of a transaction and `pipeline.execute` ends and executes it. Before initializing a transaction, one uses `pipeline.watch` to define
a set of keys for which the transaction will abort if their values change during the transaction's execution.

In the above code, in `check_and_set` I defined a transaction that tries to `get` a given key's value. If the value is `None`, then the transaction writes (`set`s) a value at that key. `check_and_set` is called once by several that are started simultaneously, each trying to set the same key with a different value

The code above doesn't actually work, since inside a transaction block's definition, [one cannot](https://stackoverflow.com/questions/50309206/redis-atomic-get-and-conditional-set) actually instruct
the transaction to `get` a key's value to conditionally run `set`. Inside the transaction's definition, `get` and `set`
only append operations to the `pipeline` for deferred execution. The `None` check for `current_value` always fails, since `current_value` is just a handle to a `get` operation. So we never see `success!` printed to stdout.

### Attempt 2

So I tried to move the `get` outside of the transaction, in my second attempt:

```python

# Attempt 2 at implementing compare-and-swap (CAS) using Redis transactions
# This attempt fails since pulling pipeline.get our of the transaction results
# in the attempted CAS implementation being non-atomic.
# We end up with torn CASes and therefore races conditions.

import redis
from multiprocessing import Process
import time


def check_and_set(key, value):
    cache = redis.Redis(host="localhost", port=6379)
    txn = cache.pipeline()
    txn.watch(key)
    current_value = txn.get(key)
    if current_value is None:
        try:
            txn.multi()
            txn.set(key, value)
            txn.execute()
            print("success!")
        except redis.exceptions.WatchError:
            pass


if __name__ == "__main__":
    num_processes = 8
    key = f"key{time.time()}"

    processes = []
    for i in range(num_processes):
        p = Process(target=check_and_set, args=(key, i))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
```

The above code only runs `set` within a transaction. So two processes could both read `None`, and then sequentially execute their transactions so that neither process observes a change to the given key when its transaction is executed. Running this code usually results in `success!` being printed more than once, meaning that more than one process updated the key to its value. This is not the behavior we want.

From my understanding of why attempt 1 failed, it doesn't seem like one can conditionally execute a `set` operation based on the value of a `get` operation, within a single Redis transaction. This blog post goes into more detail about Redis tranasctions not being [full database transactions](https://stackexchange.github.io/StackExchange.Redis/Transactions.html)

### Attempt 3

As suggested by a few of the answers in the references above, Redis is capable of [running arbitrary Lua code](https://redis.io/docs/manual/programmability/eval-intro/) server side. Why Lua specifically is a mystery to me since it ranks [far down the list in popularity](https://spectrum.ieee.org/top-programming-languages-2022) or relevance by any metric. But importantly, Lua scripts sent to the Redis server are executed *atomically*, and can call `get` and `set` directly from within the script. So here's my third attempt at doing a CAS in Redis:

```python
# Attempt 3 at implementing compare-and-swap (CAS) using Lua scripts.
# This one was successful. This is because, for whatever reason, Redis supports
# the execution of arbitrary Lua scripts, and these scripts are executed *atomically*
# by the server. Since Lua script execution is atomic, we can group the necessary read
# and write transactions into the same script to execute a CAS.

import redis
from multiprocessing import Process
import time


def check_and_set(key, value):
    cache = redis.Redis(host="localhost", port=6379)
    success = cache.eval("""
        if redis.call('EXISTS', KEYS[1]) == 0 then
            redis.call('SET', KEYS[1], ARGV[1]);
            return 1;
            end;
        return 0;
    """, 1, key, value)
    if success:
        print("success!")


if __name__ == "__main__":
    num_processes = 8
    key = f"key{time.time()}"

    processes = []
    for i in range(num_processes):
        p = Process(target=check_and_set, args=(key, i))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
```

This time it works! When running this code, I only see `success!` printed once. What isn't clear to me is how this would impact performance under high contention or a heavy workload, since according to the documentation:

>  While executing the script, all server activities are blocked during its entire runtime

Such a script is probably acceptable to run atomically though since it's so short.