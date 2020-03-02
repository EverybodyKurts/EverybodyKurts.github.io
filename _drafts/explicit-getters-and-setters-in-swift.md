---
layout: post
title:  Swift bindings with explicit getters and setters
date:   2020-02-28 12:00:00 -0500
tags: [swift, swiftui]
---

Apple's [SwiftUI tutorials](https://developer.apple.com/tutorials/swiftui/tutorials) do a great job of introducing developers to the fundamental concepts of SwiftUI, including the `@Binding` property wrapper. However, the tutorial doesn't demonstrate how to initialize a `Binding` with an explicit getter and setter via [`init(get:set:)`](https://developer.apple.com/documentation/swiftui/binding/3363053-init). 