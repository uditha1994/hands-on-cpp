---
num:
kind: front
slug: start
title: How to Use This Book
tagline: Read this first. It will save you time later.
---

## Your brain on code

Let's be honest. Your brain is not built to remember things just because you read them once. It is built to remember things that feel **important**, **surprising** or **useful right now**. A tiger in the jungle? Your brain remembers. A table of data types on page 47? Your brain politely ignores it.

So this book does not just *tell* you things. It makes you **think**, **predict**, **type**, **break** and **fix**. That is how real programmers learn, and it is how you will learn too.

Here is what you will see on almost every page:

| You will see | What it means | What you should do |
|---|---|---|
| **Brain Power** | A question to think about | Stop and think for a minute before reading on. Really. |
| **Sharpen your pencil** | A short exercise | Do it on paper or in your editor. Then check the solution. |
| **Code Magnets** | A program cut into pieces | Put the pieces back in the right order. |
| **Be the Compiler** | Code with mistakes in it | Find what the compiler would complain about. |
| **Watch it!** | A common trap | Read it twice. These are the mistakes everyone makes. |
| **There are no Dumb Questions** | Questions students really ask | Read them, even if you think you know the answer. |
| **Under the hood** | What the computer is really doing | Optional on the first read, gold on the second. |
| **From the real world** | How professionals use this | Shows you why the topic matters in a real job. |
| **Quick Check** | A few multiple choice questions | Answer before you look. Wrong answers teach you the most. |
| **Lab** | A bigger hands-on task | Do it at the computer. This is where the learning sticks. |
| **Bullet Points** | The chapter in a nutshell | Use these for revision before exams. |

:::brain
Why do you think this book asks you to *predict the output* of a program before showing it? What happens in your head when your prediction turns out to be wrong?
:::

## The rules of this book

1. **Type the code yourself.** Do not copy and paste. Your fingers learn the syntax faster than your eyes do.
2. **Run every program.** Every complete program in this book has been compiled and tested with a real C++ compiler (g++, using the C++17 standard). If your output is different, that is a clue, not a disaster.
3. **Break things on purpose.** Delete a semicolon. Change `<` to `<=`. See what happens. Error messages become your friends when you meet them often.
4. **Do the exercises before you look at the answers.** In the web version, solutions are hidden behind a button. In the PDF, they are at the back of the book.
5. **Take breaks.** Your brain keeps working on a problem even after you stop. Many bugs are solved in the shower.
6. **Talk about it.** Explain a concept to a friend. If you cannot explain it simply, read that part again.

:::watch
In the terminal outputs in this book, anything the **user types** is shown <span class="typed">like this</span>. Everything else was printed by the program.
:::

## What you need

You need a computer and a C++ compiler. That is all. Here are three good options:

- **On your own computer:** install a compiler such as **g++** (part of GCC) or **clang++**, plus a code editor such as **Visual Studio Code**. On Windows, many students use the MinGW-w64 build of GCC, or Code::Blocks, which comes with a compiler. On macOS, installing the Xcode Command Line Tools gives you `clang++`. On Linux, `g++` is usually one command away from your package manager.
- **In your browser:** online compilers let you write and run C++ without installing anything. They are great for quick tests, though you cannot always work with files on them.
- **In the lab:** use whatever your lecturer has set up. The code in this book is standard C++, so it runs the same everywhere.

When you compile from a terminal, this is the command used throughout the book:

```text
g++ -std=c++17 -Wall program.cpp -o program
```

`-std=c++17` tells the compiler which version of C++ to use. `-Wall` turns on helpful warnings. `-o program` names the finished program. Chapter 2 explains each part.

## Who this book is for

This book is for you if:

- you have **never programmed before**, or you tried once and got lost,
- you are studying C++ in a diploma, foundation or first-year degree course,
- you want to understand **why** code works, not just copy it.

It starts from zero. By the last chapter you will be building a complete console application that stores its data in files, uses functions, arrays, vectors and structs, and is split across multiple source files the way professional projects are.

## Meet the cast

Learning is easier with people. This book follows a small group of characters through one big project.

<div class="cast">
<div class="cast-card"><span class="avatar" style="background:var(--accent);color:#111">A</span><h4>Amaya</h4><p>A first-year computing student. Curious, determined, and new to programming. She promised her uncle she would build software for his shop. She has no idea how yet.</p></div>
<div class="cast-card"><span class="avatar" style="background:#5B6B7A;color:#fff">R</span><h4>Uncle Ruwan</h4><p>Amaya's uncle. He runs <b>Ruwan Stores</b>, a busy little grocery shop in Kandy. He keeps everything in a thick exercise book and is tired of losing track of stock and money.</p></div>
<div class="cast-card"><span class="avatar">N</span><h4>Nuwan</h4><p>Amaya's cousin, a software engineer. He visits on weekends, answers questions with more questions, and has strong opinions about curly braces.</p></div>
<div class="cast-card"><span class="avatar" style="background:#2F7D6D;color:#fff">D</span><h4>Dilshan</h4><p>Amaya's classmate. He makes the mistakes so you do not have to, and he asks the questions everyone else is too shy to ask.</p></div>
</div>

Every chapter adds a piece to **the Ruwan Stores system**. In the final chapter, all the pieces come together into one working application.

:::story
Ruwan: Amaya, you study computers, no? Can you make a program for the shop? Something that remembers my stock, adds up bills, tells me what is running low...

Amaya: Of course, Uncle! How hard can it be?

Nuwan: *(laughing)* Famous last words. But yes, she can do it. One step at a time.
:::

## How the book is organised

The book is in four parts.

- **Part 1, Foundations (Chapters 1 to 5):** how to think like a programmer, the shape of a C++ program, variables, input and output, and operators.
- **Part 2, Control flow (Chapters 6 to 8):** making decisions and repeating actions. This is where programs start to feel alive.
- **Part 3, Organising code and data (Chapters 9 to 15):** functions, arrays, vectors, strings, searching and sorting, structs and pointers.
- **Part 4, Real programs (Chapters 16 and 17):** files, multi-file projects, debugging and the final capstone project.

The appendices at the end give you quick-reference cheat sheets, a guide to common compiler errors, and a glossary.

:::relax
You do not have to understand everything the first time. Some ideas, like references and pointers, take two or three passes before they click. That is completely normal. Keep going, and come back later.
:::
