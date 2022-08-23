---
layout: post
title: Messing with PyTorch weight initialization
tags: pytorch, machine learning, deep learning
published: true
---

See Jupyter notebook here[^1]: [notebook](https://github.com/vhxs/pytorch-playground/blob/master/pytorch_param_init.ipynb){:target="_blank"}

Lately I've been following along with Andrew Ng's deeplearning.ai coursera specialization to beef up my ML creds. Last I took his online course was in 2014, and it's changed quite a lot since then, probably driven by how popular the deep learning frameworks have become in industry (hype or otherwise). There's one particular thing though that caught my attention in Ng's video on Random Initialization in week 3 of Neural networks and deep learning.

Ng mentions that if you initialize a fully connected network's weights all to the same values, then all weights in a given layer will be equal at each timestep, which isn't very useful since the goal is for neurons in a layer to "learn" something different from one another. This didn't seem obvious to me at first, but since there's nothting breaking the symmetry among neurons, what else would there really be to distinguish among then (quirks in software/hardware implementation maybe)? It's a classic symmetry argument that mathematicians use all the time and isn't all that deep (pun not originally intended?) if you think about it just a bit.

But saying that something works in theory can be very different than actually observing it in practice. How about we try this out in pytorch and see whether we can see evidence of it?

I wrote some very unoriginal code in pytorch below to train a 2-layer fully connected network on MNIST. To observe what Ng said, we need to control how weights are initialized. We need them to not be random. But if you peek into `torch.nn.Linear`'s [source code](https://pytorch.org/docs/stable/_modules/torch/nn/modules/linear.html){:target="_blank"}, you can see that the layer's weights are initialized using some kind of uniform distribution called the Kaiming uniform distrbution[^2].

We need to scrap these weights and use our own. pytorch has these convenient functions `torch.nn.zeros_` and `torch.nn.ones_` that takes a tensor and sets all its elements to 0 or 1. I called these functions on `nn.Linear`'s weight and bias attributes, for each of the layers. Here's the code:

{% highlight python %}
import torch
import torch.nn as nn
import torchvision
import torch.optim as optim
import torchvision.transforms as transforms

class FullyConnected(torch.nn.Module):
    def __init__(self, const_init=True, activation_function="Tanh"):
        super().__init__()

        self.fc1 = nn.Linear(784, 100)
        self.fc2 = nn.Linear(100, 10)
        self.activation_function = getattr(torch.nn, activation_function)()

        # zero the parameters
        if const_init:
            nn.init.zeros_(self.fc1.weight)
            nn.init.zeros_(self.fc2.weight)
            nn.init.ones_(self.fc1.bias)
            nn.init.ones_(self.fc2.bias)

    def forward(self, x):
        x = self.fc1(x)
        x = self.activation_function(x)
        x = self.fc2(x)
        return x

def train_model(const_init=True, batch_size=60):
    train_data = torchvision.datasets.MNIST('.', download=True, transform=transforms.ToTensor())
    train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size)

    model = FullyConnected(const_init=const_init)

    optimizer = optim.SGD(model.parameters(), lr=0.01)

    criterion = nn.CrossEntropyLoss()

    model.train()
    for data, target in train_loader:
        
        optimizer.zero_grad()
        output = model(data.flatten(start_dim=1))
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

    return model
{% endhighlight %}

Each neuron's weights corresponds to a column in the matrix (rank 2 tensor) representing a layer. If we train the model for a single epoch (by calling train_model above) and print out the weights in the second layer, you can see with your own eyes that all columns are equal! (or, rows are all of the form $$(a, a, \ldots, a)$$)

{% highlight python %}
model = train_model()
print(model.fc2.weight)
{% endhighlight %}

(cutting terminal output short, see jupyter notebook if you want to see everything)
{% highlight terminal %}
Parameter containing:
tensor([[-0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005, -0.0005,
         -0.0005, -0.0005, -0.0005, -0.0005],
        [ 0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,  0.0009,
          0.0009,  0.0009,  0.0009,  0.0009],
          ...
{% endhighlight %}

Let's not just trust our eyes though, let's verify this programmatically by looking at the set of unique values in each row. Ideally this should be of size 1, for each row.

{% highlight python %}
for row in model.fc2.weight:
    val_set = set(row.tolist())
    print(val_set)
{% endhighlight %}

{% highlight terminal %}
{-0.0005255858995951712, -0.0005255864234641194, -0.0005255902651697397}
{0.0009435577085241675, 0.0009435573592782021, 0.0009435539250262082}
{0.00028612479218281806, 0.0002861249668058008, 0.00028612720780074596}
{0.0004142071702517569, 0.0004142068210057914, 0.0004142059769947082}
{-0.00015453004743903875, -0.00015452907246071845, -0.0001545274571981281}
{-0.0013299881247803569, -0.001329988008365035, -0.0013299871934577823}
{0.0002526552998460829, 0.0002526541065890342}
{0.0010613426566123962, 0.0010613424237817526}
{-0.0006094475975260139, -0.0006094477139413357, -0.0006094489945098758}
{-0.0003383587463758886, -0.00033835816429927945, -0.0003383552539162338}
{% endhighlight %}

So they're almost the same, but not quite? I don't know why this is, but since there's no apparent source of randomness (deterministic weight initialization, no shuffling of training dataset), we should be able to reproduce the above without having to seed with `manual_seed`. Let's compute a cryptographic hash of the model's parameters over several training runs, and see if they're the same each time.

{% highlight python %}
import hashlib

for i in range(5):
    m = hashlib.sha256()
    model = train_model()
    str_to_hash = ""
    for params in [model.fc1.weight, model.fc2.weight, model.fc1.bias, model.fc2.bias]:
        str_to_hash += "".join(map(str, params.flatten().tolist()))
    m.update(str_to_hash.encode('utf-8'))
    print(m.hexdigest())
{% endhighlight %}

{% highlight terminal %}
8fbece4fd14b2f4eba6783f4e08e4b6f2a8b64f277cc8abda6c2c09d94cc82a5
8fbece4fd14b2f4eba6783f4e08e4b6f2a8b64f277cc8abda6c2c09d94cc82a5
8fbece4fd14b2f4eba6783f4e08e4b6f2a8b64f277cc8abda6c2c09d94cc82a5
8fbece4fd14b2f4eba6783f4e08e4b6f2a8b64f277cc8abda6c2c09d94cc82a5
8fbece4fd14b2f4eba6783f4e08e4b6f2a8b64f277cc8abda6c2c09d94cc82a5
{% endhighlight %}

That's satisfying to see! So even if weights are almost equal, but not quite, at least they're off in the same kind of way each time. As a final sanity check, let's train the same model but let pytorch use its random initialization and see whether all weights are different.

{% highlight python %}
model = train_model(const_init=False)
for row in model.fc2.weight:
    val_set = set(row.tolist())
    print(len(val_set))
{% endhighlight %}

{% highlight terminal %}
100
100
100
100
100
100
100
100
100
100
{% endhighlight %}

Checks out. No idea what's up with weights being slightly off, but it's got to be because of some implementation quirk in pytorch. This is all evidence enough for me that confirms what Ng claimed about weight initialization.

[^1]: How can I automatically convert a rendered Jupyter notebook to something renderable by Jekyll?
[^2]: What is this exactly? I can't find much on this online. Will continue poking around.