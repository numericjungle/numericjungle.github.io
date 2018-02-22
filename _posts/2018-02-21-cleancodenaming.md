---
date: 2018-02-21 23:36:54.892960
layout: post
title: Notes on Clean Code Naming
description: "CleanCodeNaming"
tags: [Clean Code, book]
comments: true
---
Notes on Clean Code - A Handbook of Agile Software Craftsmanship

### Ch2: Meaningful Names
* Intention-Revealing names:
`   int elapsedTimeInDays; `
   `daysSinceCreation; `
   `daysSinceModification; `
   `fileAgeInDays`
* Avoid disinformation
  - Using inconsistent spellings is disinformation
  - Bad: `hp`, `aix`, `sco`, `XYZControllerForEfficientHandlingOfStrings`, `a = O1; l = o1`
* Meaningful distinctions
  - Bad: 
  `getActiveAccount()`
  `getActiveAccounts()`
  `getActiveAccountInfo()`
* Pronunceable names
* Searchable names
* Avoid encodings
  - Hungarian notation 
  - prefixes: bad example: `m_dsc`
* Class names
  - noun/ noun phrase: `Customer`, `AddressParser`
* Method names
  - verb/ verb phrase: `postPayment`, `deletePage`
* Matching with design patterns
  - e.g. AccountVistor <-> Visitor pattern
