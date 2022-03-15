---
layout: post
title: My Adventures in Android Engineering
tags: android, software
published: true
---

This is a post I'll periodically update as I learn more.

Software is a fast moving target because computer systems are relatively easy to spin up, modify, and tear down, compared with aerospace (planes) or automotive (cars) systems that probably take years or decades to design, change, and deploy. It's automation that software enables that just makes stuff move fast.

I've found this to be especially so with Android. The whole Android ecosystem is still so rapidly changing, so developing and maintaining a stable Android application requires *a lot* of time and attention, moreso than your typical software project. Suggested architectures and frameworks change as frequently as a few times a year. Frequenting the r/androiddev I've read many posts from developers sharing their frustration with the unstable platform and environment.

Until my recent involvement on an Android project, I hadn't had much of anything to do with Android, so I have learned all of this in the process. What follows are rough notes on what I've learned, and what I hope will be future-proof suggestions on how to tackle learning about Android.

### What and how to learn

If you already know Java then you're already at a huge advantage, since Android application code is typically written in either Java or Kotlin, and built to target a Google-modified [JVM](https://source.android.com/devices/tech/dalvik) called the Android Runtime (ART) (years ago known as Dalvik). In 2019, Google announced that Android development will increasingly be Kotlin-first, so it's best to learn Kotlin if you don't know it already. Kotlin is similar enough to Java for this to not be much of a challenge.

StackOverflow and Google are the most obvious places to go to search for how to do this or that in code. But because of how quickly Android has evolved, I've found that top search results more often than not provide wrong answers, since they're too dated. If I Google anything about Android, I make sure I restrict my searching to the last 1-2 years, and this usually works well enough.

This blog on all things Android looks like a fantastic way to keep up with all the changes the Android constantly undergoes: [blog](https://commonsware.com/blog/archive.html)

I've found it really helpful to just sequentially go through the Associate Android Developers Certification course material. Google started releasing this material sometime in 2020, though the content is still being updated. Browsing r/androiddev subreddit, even glancing at just the headlines, has also helped me mentally reinforce which frameworks/packages/architectures are relevant today, and which are considered dated.

### Development environment

Use Android Studio (and avoid Eclipse). It's a free JetBrains product. JetBrains has some amazing, intuitive, shallow-learn-curve IDEs and this is absolutely one of them. It sets up a lot of boilerplate code, XML configurations, build files, etc for you.

Android projects are built using the Gradle build system. Gradle build scripts can themselves be written in Groovy, Java, or Kotlin, though in my experience it's only worthwhile to learn what you need about Gradle, since the build system itself seems to be very complex.

In contrast with developing an application to be deployed on a server, you don't really have a dev server on which you can build or test your application. Android Studio comes with an emulator. But if you're like me and need the satisfcation of seeing your application run on a real device, I would suggest getting a [Samsung Tab A7 Lite](https://www.samsung.com/us/mobile/tablets/buy/?modelCode=SM-T220NZAAXAR), I got one for only $120. People online only complain about application performance, but in my opinion this doesn't matter a whole lot if you're developing only to learn. You can connect your device to your dev server over USB.

Gaining root access can be dicey. You *can* root your device, but by doing so you're probably going to void the warranty of whatever device you have, since you usually need to exploit a known vulnerability. Many devices don't seem to have official support for gaining root access, there isn't any `sudo` or `dsenableroot`. There are probably security reasons for this that I don't know much about.

[//]: # Comment

Debugging an Android application can also be much slower than debugging any other kind of app. You can displays alerts (called Toasts) on the device, but it's sometimes not as effective as `print` statements. For virtual devices, Android Studio has this tool called Logcat. There's also the `adb` CLI that you can use to interface with either virtual or physical devices.

React Native seems to be a popular alternative to developing Android apps in Kotlin, but with the rise of WebAssembly and the industry trend to move

### A small subset of core concepts

Definitely a nonexhaustive list:

- Top-level properties of an Android app are defined in its manifest file, which is just an XML file. Includes stuff like that app's name, permissions to interact with the internet or other apps, etc.
- An app's layout and design is specified in XML files, under the `res` (for "resources") direcory. This includes defining how text, buttons, and other views are laid out relative to one another. This is also where navigation between different screens is defined. Android Studio has a graphical interface for working with layouts, though you can choose to just modify the XML directly.
- You should understand the application lifecycle. The building blocks of an app are Activities and Fragments, and have asynchronous callbacks (like `onCreate`, `onDestory`) for each part in their lifecycles.
- Follow Google's recommended software architecture: https://developer.android.com/jetpack/guide. This means using `ViewModel` to store and separate state for UI logic that is executed in Fragments and Activities. `LiveData` implements the observable design pattern, and is a good way for your UI to subscribe to state stored in a `ViewModel` object.
- As with server applications, Android applications support concurrency and multi-threading. Kotlin makes it really easy to spawn a new thread with `thread { ... }`, though corountines seem to be the recommended approach to handling concurrency. 
- Persist state using Room. You don't have full control of your device, and can't just install Postgres or MongoDB. Setting up a Room database requires a lot of boilerplate code and is not as simple as using a driver like `psycopg2` for Python or `pgx` for Golang. Handling data migration when updating the database schema is done with versioning.
- Inter-application communication is via Intents. It's not as easy as using shared memory, or a TCP or Unix domain socket. Your application also has to be given permission to interact with other apps, probably for security reasons.
- Jetpack Compose, officially released by Google a few months ago, seems to be the latest recommended toolkit to write applications.

### Bottom Line

Android engineering is a full-time job and getting started properly requires a massive upfront time investment. This is because (1) Android is a relatively new technology, so its ecosystem is rapidly changing and has yet to stabilize and (2) compared with other software projects, Android development requires a very high amount of cognitive overhead to getting even the most minimal of applications off the ground. A "hello world" application can be implemented in almost any language in just one line, but an Android application is several hundreds of lines long because of the sheer amount of boilerplate code.

I wouldn't call Android development hard, but it definitely requires a much higher level of time commitment to keep up with than other technologies.