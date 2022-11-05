---
layout: post
title: Review of Deeplearning.ai specialization
tags: deep learning, review
published: true
---

I recently completed the deeplearning.ai specialization offered by coursera. The specialization consists of 5 courses, each one being divided into 4 "weeks", though they realistically can be completed in a few hours. Each week has a multiple choioce assignment and a few coding labs. The coding labs mostly walk you through Jupyter notebooks where you build different neural network layers from scratch (both training them and using them for inference), and then applying them to toy problems to illustrate the concepts you just learned.

This is a very rough breakdown of the specialization:

 - neural networks and deep learning, which covers what are neural networks, gradient descent, backpropagation, training, inference, and other basic concepts as a starting point.
 - improving deep neural networks, which is very self explanatory: it covers general guidelines and rules of thumb for how to improve performance of deployed neural networks. This includes basic hyperparameter optimization techniques (grid search), what is regularization and how to mitigate overfitting with regularization, different optimizers (Adam, Adagrad), what their differences are, how to choose a learning rate, etc.
 - structuring machine learning projects, which covers the "operational" aspects of applying deep learning. This one is different from the other four, in that the assignments consist of case studies. You're given a real-world-ish scenario where you have to deal with real world constraints (not enough data, poorly informed stakeholders, deadlines) and have to select an action given a problem situation.
 - convolutional neural networks, which begins with what a convolutional layer is, how they are composed together with pooling operations to form different architectures, and various problems you can solve with them. This includes image classification, object detection, image segmentation, facial recognition, and one-shot learning. It also covers historically popular or novel architectures like LeNet, AlexNet, VGG, YOLO, U-Net, mobilenet, among others that I'm probably missing here. 
 - sequence models. Covers the concept of recurrent neural networks, then LSTMs and GRUs, and various tasks that can be solved with sequence models, like machine translation and keyword detection. It also covers transformers, which is a monstrously complex architecture but is trendy to use these days.

In my opinion, many MOOCs don't have much value since the material covered is usually at a superficial level, not comparable to what one might learn in a real university course, and not representative of applied knowledge that you'd pick up with experience in industry. While I think these ring true of the deeplearning.ai specialization, it's less so.

I think you have know all the content in the specialization if you ever claim that you *know* deep learning. In that sense I think this course is a bare minimim baseline for entry into the field, if you know nothing at all about it going in. At the very least it introduces you to basic concepts and terminology used in the field, but it certainly won't make you an ML researcher or engineer overnight.

Topics I can think of that aren't covered by the specialization are:
- Generative Adversarial Networks
- Neural recommender systems
- Neural anomaly detection
- Graph learning/GCNs/GNNs
- Deep reinforcement learning
- [Diffusion models, which seems to be the latest trend](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)

Deep learning is a massive and rapidly changing field though, so any kind of course on it will miss lots of topics.

What a random user on [Blind](https://www.teamblind.com/post/Deeplearningai-HYVXAbrP) has to say that I would agree with (as of 2020):
- Its a good course if you have 0 knowledge of DL. I think it lays down the foundational concepts well. How valueable it will be to you will depend on your prior knowledge of the DL field.

Similarly from [r/datascience, 2019](https://www.reddit.com/r/datascience/comments/axzkw7/your_thoughts_on_courseras_deep_learning/ehxky48/)