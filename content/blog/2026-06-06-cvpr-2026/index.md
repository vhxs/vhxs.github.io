---
title: My experience at CVPR 2026
author: Vikram Saraph
date: "2026-06-06"
tags:
  - cvpr
  - conference
  - machine learning
  - computer vision
---

I attended [CVPR 2026](https://cvpr.thecvf.com/Conferences/2026) in Denver, CO -- my second machine learning conference after ICML in 2023, and my second conference of the year after [JMM 2026](https://meetings.ams.org/math/jmm2026/meetingapp.cgi/Home/0) in Washington, DC (where I was an [invited speaker](https://meetings.ams.org/math/jmm2026/meetingapp.cgi/Paper/54386)). I wanted to write about that experience. That ship has sailed, but I thought I'd write about this one!

With [ICCV](https://en.wikipedia.org/wiki/International_Conference_on_Computer_Vision) and [ECCV](https://en.wikipedia.org/wiki/European_Conference_on_Computer_Vision), [CVPR](https://en.wikipedia.org/wiki/Conference_on_Computer_Vision_and_Pattern_Recognition) is considered one of the top three venues for computer vision research. This year there were [16,000+ paper submissions](https://cvpr.thecvf.com/Conferences/2026/News/Technical_Program), 4089 accepted papers, and 10,000+ attendees, so there's a *lot* going on at these conferences. My original research background is *not* in machine learning and I do not claim expertise in frontier AI/ML research, as excited as I get being surrounded by this stuff (especially by the mathematics of it). So this is just my perspective, but I'm always happy to receive feedback and corrections if something is misstated or misrepresented (email me!).

During the course of the conference I took notes scattered across [Obsidian](https://obsidian.md/), Signal notes-to-self, and pictures of slides and posters. It's obviously hard to capture *everything* I experienced in a blog post, but I'm going to try writing down what I found most interesting or memorable (and not necessarily just going for what's trendy).

## Conference Structure

As I mentioned, there's a lot that happens here, so I'll start with a bird's-eye view (you can skip this if you already know how these work). CVPR ran from Wednesday, June 3 to Sunday, June 7. The first two days are for workshops and tutorials, and the remaining three days are for the main conference. Workshops each focus on specific topics and are organized by a small group of researchers. Each has their own submission process where the organizers decide which submissions are accepted for oral presentation. Workshop proposals must themselves be submitted and accepted to CVPR for them to be held. Depending on the physical venue (I find that most convention centers are the same though), workshops happen in breakout-style rooms with maybe attendance by 200-500 people at a time. To me, they feel much more community-oriented than oral presentations at the main conference. I didn't attend any tutorials so I'm not going to comment on those.

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="https://assets.simpleviewinc.com/simpleview/image/upload/c_fill,f_jpg,h_752,q_65,w_1920/v1/clients/denver/20130701_ccc_213_7e69cef3-04c1-4191-b46c-c19843cdff3c.jpg" width="80%" caption="The Denver Convention Center. Yes that is a [blue bear](https://en.wikipedia.org/wiki/I_See_What_You_Mean_(Argent)) outside the convention center.">}}
</div>

Then there are the main conference days. These mainly consist of oral presentations, poster sessions, and keynotes (though there are a few other various activities that happen as well). At this conference there were about two poster sessions and two oral sessions of oral presentations, happening at non-overlapping times. Each oral session consists of four concurrently running tracks, each track with a particular theme (for example, "multimodal vision" or "generative diffusion modeling"). The poster sessions happen in a big, open space in an exhibit hall, a few hundred out at a time. I really like these sessions because as an attendee you're free to walk around, pick out what interests you, and actually engage and have a conversation with the author(s) about their work (and maybe even connect afterwards!). By contrast, oral sessions happen in auditorium-sized rooms with capacity in the 1000s. Each talk is 10-15 minutes in length and there's time for about one question after each. It makes sense that this is the format, since oral submissions are much more selective. But it does make the format feel performative.

There are about 4-8 keynote talks that happen during the main conference. These talks are typically targeted towards a broad audience and don't get into too much technical detail (and they're not necessarily related to computer vision), so they tend to be interesting. For example, this year there was a talk on the state of quantum computing.

These days, CVPR and similar-tier conference use mobile apps to help their attendees network and connect with one another. This year CVPR used [Cvent](https://www.cvent.com/). Their people search was good, but I didn't find their user experience to otherwise be very good. A colleague of mine who also attended pointed me to this [webapp](https://cvprworkshopradar.vercel.app/) that someone built ([source code](https://github.com/Gabrysse/cvprworkshopradar)). It let you keyword search over workshops and tutorials. I [forked it](https://github.com/vhxs/cvprworkshopradar) and used Claude Code to add a semantic search feature.

To keep it brief, I'll mainly go through some of the workshops I attended, since I had more energy to take notes on them as they were earlier in the conference. For the main conference I focused more on the poster sessions (for reasons mentioned above).

## Workshops

One of the first workshops I attended was on [embedded vision](https://embeddedvisionworkshop.wordpress.com/), which is all about running vision and image processing algorithms on embedded devices that have low size, weight, or power constraints. I listened in on most of the session, but these were a few presentations that I noted down:

- [EventGuard: Sparsity-Aware In-Sensor Denoising for Frame-Based Event Vision Sensors](https://openaccess.thecvf.com/content/CVPR2026W/EVW/papers/So_EventGuard_Sparsity-Aware_In-Sensor_Denoising_for_Frame-Based_Event_Vision_Sensors_CVPRW_2026_paper.pdf). From this talk I learned about [event cameras](https://en.wikipedia.org/wiki/Event_camera), which aren't everyday cameras in that individual pixel data is captured independently from one another, and asynchronously only when changes are detected. These cameras can be sensitive to background noise. I'd also learned of spiking neural networks (I would need to read more about these to explain any further) and binary neural networks (where weights and activations can only be \( \pm 1 \)). One thing that stuck with me during the presentation is their neural networks reduced to mostly XNORs and [popcount](https://vaibhavsagar.com/blog/2019/09/08/popcount/) operations.

- [BlankSkip: Early-exit Object Detection onboard Nano-drones](https://arxiv.org/abs/2603.28149): Seemed interesting because it tries to accelerate inference by using an [early-exit](https://dl.acm.org/doi/epdf/10.1145/3698767) architecture, where "early exit" means only doing a partial inference if nothing of interest is found in frame. Their architecture is some hybrid of a [MobileNet](https://arxiv.org/pdf/1704.04861) and [SSD](https://arxiv.org/abs/1512.02325). YOLO architectures are mentioned in a related work section (also, in reading about SSD, or Single Shot Detectors, their architecture is named "SSD", but the paper also refers to YOLO as an example of a Single Shot Detector, which is very confusing terminology). As mentioned in the paper, apparently YOLO architectures generally trade latency for accuracy compared with MobileNet.

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="early_exit.png" width="80%" caption="Early-exit with MobileNet extractor and SSD head.">}}
</div>

- [TinyDEVO: Deep Event-based Visual Odometry on Ultra-low-power Multi-core Microcontrollers](https://arxiv.org/pdf/2604.08060): Visual odometry is all about all about determining the position and orientation of an object (in this case, applied to drones) from camera images. This one proposed an architecture for doing so on (low-power) microcontrollers. Average trajectory error is mentioned as an evaluation metric.

I sat in the [XAI4CV](https://xai4cv.github.io/) (Explainable AI for Computer Vision) workshop and listened to:

- [FaCT: Faithful Concept Traces for Explaining Neural Networks](https://arxiv.org/pdf/2510.25512). I don't know a whole lot about explainable AI, so from this talk I tried to understand what, concretely or mathematically, explainability means. I'm sure there are many different definitions of this, but one key thing I learned of was the B-cos transform, which is meant to replace linear layers with an "explainable" equivalent. The below excerpt from [this paper](https://arxiv.org/pdf/2205.10268) explains it well:

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="b_cos_explain.png" width="50%" caption="The B-cos transform explained">}}
</div>

They use these together with sparse encoders to propose a new model called FaCT, which they claim performs better than SoTA on interpretability metrics for certain image classification tasks.

I spent quite a bit of time at the Humans of Generative AI workshop, the content of which I found to be uniquely different among the other papers at this conference. It originally caught my attention because of [this post](https://bsky.app/profile/lucyq.bsky.social/post/3mgv2zu3kns2z). Some of it was related to computer vision, some not, but it drew a lot of interest from security and privacy researchers.

- [Juliana Castro Varón](https://julianacastro.co/) of the [New York Times' AI Initiatives](https://www.nytco.com/press/introducing-the-a-i-initiatives-team/) gave a talk (using all hand-drawn slides) on how NYT uses AI to improve user experience in searching for and ranking news articles. Surprisingly relevant to some large-scale document search problems that I myself have worked on.

- [Caught in a Mafia Romance: How Users Explore Intimate Narratives with Chatbots](https://arxiv.org/pdf/2603.01319): Analyzes usage of [character.ai](https://character.ai/) personas and related discussion on relevant subreddits. 

- Structured Listening: Codifying Human-Meaningful Voice Signals to Ground Generative AI Reasoning, which doesn't have a link, but was about one of Modulate AI's models (doesn't have a corresponding paper online as far as I can tell). This one was interesting to listen to because I found out later that it was presented by the CTO of my academic sibling's employer, [Modulate AI](https://www.modulate.ai/). They're building in-house ensemble models for advanced audio processing, taking paralinguistic aspects into consideration, and building products using these models.

The [Synthetic Data for Computer Vision](https://syndata4cv.github.io/) workshop had a lot of interesting stuff.

- There was a talk given by [Jia Deng](https://www.cs.princeton.edu/~jiadeng/) of [Princeton's Vision and Learning Lab](https://pvl.cs.princeton.edu/) titled "Can We Train AI (from scratch) without Collecting Any Data?". Roughly, the talk was about how one can get quite far with just procedurally-generated data, specifically for 3D vision anyways. He mentioned the [Infinigen](https://infinigen.org/) product built by their lab ([open source](https://github.com/princeton-vl/infinigen)) as well as their [ProcFunc](https://github.com/princeton-vl/procfunc) Python library that "transpiles" Blender node workflows into Python code.

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="https://raw.githubusercontent.com/princeton-vl/infinigen/refs/heads/main/docs/images/hello_room/ocmesh_base.png" width="80%" caption="Infinigen render from their [hello world example](https://github.com/princeton-vl/infinigen/blob/main/docs/HelloRoom.md) outside the convention center.">}}
</div>

- [Georgia Gkioxari](https://georgiagkioxari.com/) of Caltech gave a talk on [SAM 3D](https://ai.meta.com/research/sam3d/), Meta's new 3D segmentation model capable of reconstructing 3D object from 2D images (she was also on the panel for [Women in Computer Vision](https://cvpr.thecvf.com/virtual/2025/workshop/32375) which I attended). She began the talk by explaining how one of Meta's older models had struggled with the relative depth of different objects within a scene. This talk got theoretical very quickly, which I do like, but sometimes don't have the background to follow. It had mentioned the term "flow matching" (which I'll discuss later).

There was a [Maritime Computer Vision Workshop](https://macvi.org/workshop/cvpr) that I briefly sat in but didn't get much from.

Of the oral sessions, the most memorable one I'd attended was on visual security, which had several talks on [watermarking](https://en.wikipedia.org/wiki/AI_content_watermarking). Of those, [this one](https://openaccess.thecvf.com/content/CVPR2026/papers/Vargas_NOWA_Null-space_Optical_Watermark_for_Invisible_Capture_Fingerprinting_and_Tamper_CVPR_2026_paper.pdf) was the most memorable since it seemed like it assumed a pretty aggressive threat model.

## Things I want to learn more about

There was a lot of information to take in during this conference, including lots of exciting math. These are just the first three things that came to mind and is definitely non-exhaustive:

### Flow matching

Flow matching was mentioned on several posters. This conference was the first time I'd heard of it. I had asked one of the poster presenters to explain the concept to me, which I feel like I got something from. I did a little reading about it afterwards and discovered that the technique was introduced in [this paper](https://arxiv.org/pdf/2210.02747) by Meta AI.

As far as I understand, flow matching is a new generative AI technique that lets one sample from complicated distributions by sampling from noise and transforming the result in a continuous manner. There are some [blog](https://mlg.eng.cam.ac.uk/blog/2024/01/20/flow-matching.html) [posts](https://peterroelants.github.io/posts/flow_matching_intro/) out there that explain it. It borrows the concept of a [flow](https://en.wikipedia.org/wiki/Flow_(mathematics)) used in geometry. The first thing I thought of when reading about these is of homotopies. If restricting to a finite interval, flows are technically homotopies, but they obviously carry much more structure than _just_ topology.

### Quantum computing (in general)

This one was a wildcard, but there was a [great keynote talk](https://cvpr.thecvf.com/virtual/2026/invited-talk/40398) by IBM's CTO for quantum computing on the general state of the field. I was chatting with Claude while sitting in this talk trying to understand the basic concepts. This is what I'd gotten while doing this:

- A qubit is a unit vector in \( \mathbb{C}^2 \)
- \( n \) qubits are represented by an element from a tensor product of \( n \) copies of \( \mathbb{C}^2 \), or \( \mathbb{C}^2 \otimes \cdots \otimes \mathbb{C}^2 = \mathbb{C}^{2^n}\)
- Like in traditional computing, we use gates to implement quantum circuits. Except for some reason these circuits must be reversible (or invertible). Mathematically, they must be represented by [unitary matrices](https://en.wikipedia.org/wiki/Unitary_matrix).
- Like in traditional computing, where [NAND](https://en.wikipedia.org/wiki/NAND_logic) and [NOR](https://en.wikipedia.org/wiki/NOR_logic) are universal, the [Toffoli gate](https://en.wikipedia.org/wiki/Toffoli_gate) is universal. And as with traditional computing, where you wouldn't use NANDs or NORs like this in practice, you wouldn't use Toffoli gates in practice either. Finding efficient quantum circuits is a challenge.
- [Qiskit](https://www.ibm.com/quantum/qiskit) is a Python library developed by IBM to simulate quantum circuits.
- [Quantum compilers](https://www.quera.com/glossary/quantum-compiler) turn high-level code like Qiskit into circuits.

This talk reminded me of my peer's [attempt](https://shortexactsplit.super.site/quantum-computing) at understanding quantum computing. I was also reminded of the fact that the startup, [Quantiuum](https://www.quantinuum.com/), [IPO'd recently](https://finance.yahoo.com/quote/QNT/).

### Contrastive loss and learning

Now this one's been around for a long time. It is by no means new, I haven't had a good reason to learn what it is exactly, but I saw it around CVPR enough for me to want to understand what it is. "Contrastive" is literally the C in [CLIP](https://en.wikipedia.org/wiki/Contrastive_Language%E2%80%93Image_Pre-training), a very popular image/text embedding model released by [OpenAI](https://openai.com/index/clip/). Constrative learning is the process of learning a model by pushing together similar samples' representation in a vector space, and pushing apart dissimilar ones (samples are _contrasted_ with one another). Encord has a good blog post on [contrastive learning](https://encord.com/blog/guide-to-contrastive-learning/). 

### VLAs and World Models

I'm lumping these two together, even though they are different, since they both help us (broadly speaking) comprehend the 3D world around us. I've seen both of these kinds of models mentioned by the self-driving car companies (the biggest sponsors of CVPR this year). 

[VLA](https://en.wikipedia.org/wiki/Vision%E2%80%93language%E2%80%93action_model) stands for vision-language-action models, and like VLMs, consume image and text as input. But instead of outputing text, a VLA outputs a predicted sequence of actions for, say, a robot or autonomous vehicle to take. There are different ways of modeling actions in a world. GM recently published a [blog post](https://engineering.gm.com/home.detail.html/Pages/news/us/en/engineering/2026/mar/0310-training-driver-ai.html) on how they're using VLAs for making sense of vehicle trajectories in autonomous driving, for example.

<div class="image-wrapper" style="display: flex; justify-content: space-evenly; align-items: flex-end;">
  {{< figure src="https://upload.wikimedia.org/wikipedia/commons/4/4c/General_architecture_of_a_vision-language-action_model.png" width="80%" caption="Simple block diagram from the Wikipedia page on VLAs.">}}
</div>

There's been a lot of [buzz](https://trends.google.com/explore?q=world%2520model&date=2016-01-01%202026-06-01&geo=US) around [world models](https://en.wikipedia.org/wiki/World_model_(artificial_intelligence)) recently (eg, I tried to go to a workshop on world models, but the room was packed and overflowing, so I didn't bother). Yann LeCun has been a [major proponent](https://awxlong.github.io/assets/pdf/autonomous-ml-lecunnpdf.pdf) of world models lately (apparently giving a [lecture at Brown](https://drive.google.com/file/d/1zTbQDIDOiRDiN790iPWzShMPux0z8o7z/view) recently). When at Meta, his lab had introduced [variants](https://arxiv.org/pdf/2506.09985) of the JEPA architecture. Fei Fei Li (founder of [World Labs](https://www.worldlabs.ai/)) wrote a [blog post](https://drfeifei.substack.com/p/a-functional-taxonomy-of-world-models) recently disambiguating the ways in which the term "world model" is used.

## Fun things

That's enough writing -- this blog post is getting pretty long and I don't want to deliberate too much longer. The cool thing about going to conferences is that you get to travel.

This was the second time I'd been to Denver (first time in 2019, just for fun, between grad school and starting my first job). There's a lot to do in Denver. I went to the [Museum of Illusions](https://moidenver.com/), which was fun, but short and gimmicky. I also went to [Meow Wolf's Convergence Station](https://meowwolf.com/visit/denver). I don't really know what to call it other than an immersive exhibit. You should read about its history: it was started by an anarchist artist collective but is now incorporated and has multiple locations, including in [Santa Fe](https://meowwolf.com/visit/santa-fe) and [Las Vegas](https://meowwolf.com/visit/las-vegas).

If you didn't know, Denver is also close to the mountains. I'd already been up [Pikes Peak](https://en.wikipedia.org/wiki/Pikes_Peak) in the Rocky Mountains during my last trip. This time I took a short trip to Boulder. It's really easy to get there from Denver by bus, and both the station and buses are pretty nice. The bus takes you very close to [CU Boulder](https://www.colorado.edu/), and from there, [Chautauqua Park](https://bouldercolorado.gov/locations/chautauqua-park) is walking distance. There are hiking trails of varying intensity levels that all starts there.

## Ending thoughts

After my trip to ICML in 2023, I didn't think the opportunity to go to a premier machine learning conference would come around again, but I was wrong! I'm grateful for my employer funding myself and a few of my colleagues to attend and learn. My attendance was also another reminder that these conferences are big and this world is small -- more than once, I ran into former peers of mine while wandering around the conference venue.

If you get the chance to attend one of these conferences, you should jump at it. Conference proceedings are always made available afterwards, but it's hard to replace the experience of directly being able to engage with researchers at the frontier of machine learning.