# Contributing to Hands-On C++

Thank you for helping to improve the book.

## Workflow

1. Create a branch from `main`, named for the change: `fix/ch08-off-by-one`, `content/ch12-more-exercises`, `tooling/faster-pdf`.
2. Make your change and run `make verify`.
3. Open a pull request into `main` and complete the checklist. CI must pass before merging.

Commit messages follow the [Conventional Commits](https://www.conventionalcommits.org/) style, for example `fix(ch08): correct loop trace table` or `feat(content): add string exercises`.

## Writing style

- Plain, friendly English. Short sentences. Speak to the reader as "you".
- No em dashes.
- Every claim about C++ must be correct for C++17. When behaviour depends on the platform or compiler, say so.
- Numbers that are invented for an exercise (prices, tariffs, tax rates) must be described as examples.

## Chapter source format

Each chapter in `content/` starts with front matter:

```
---
num: 7
title: Making Decisions
tagline: if, else, switch, and programs that choose their own path
learn: first goal; second goal; third goal
---
```

`##` headings become numbered sections. Special blocks use `:::name` and end with `:::` on its own line:

| Block | Purpose |
|---|---|
| `:::story` | Dialogue. Each paragraph starts with `Amaya:`, `Nuwan:`, `Ruwan:`, `Dilshan:` or `Compiler:` |
| `:::brain` | A question to think about |
| `:::sharpen Title` | An exercise. Put the answer after a `---solution` line |
| `:::compiler` | A "Be the Compiler" exercise with `---solution` |
| `:::lab Title` | A larger practical task with `---solution` |
| `:::project Title` | An open-ended project |
| `:::watch` | A common mistake |
| `:::nodumb` | Questions and answers, written as `Q:` and `A:` lines |
| `:::deep` | "Under the hood" background |
| `:::industry` | How professionals use the idea |
| `:::relax` | Reassurance |
| `:::fireside A\|B` | A conversation between two concepts, lines starting `1:` and `2:` |
| `:::quiz` | Multiple choice: `? question`, `- wrong`, `* correct`, `> explanation` |
| `:::magnets` | Code magnets: the correct program between two `~~~` lines |
| `:::bullets` | The chapter summary |

## Code blocks

The tag after ` ```cpp ` tells the verifier what to do:

| Tag | Meaning |
|---|---|
| (none) | A complete program: it must compile without errors |
| `run` | Compile, run, and compare with the next ` ```output ` block |
| `check` | A snippet: wrap it in `main` and compile it |
| `fn` | Function definitions: compile them with an empty `main` |
| `error` | Deliberately broken code: not compiled |
| `nocheck` | Not compiled (fragments, pseudo-code) |
| `random` | Output varies between runs: compile and run, but do not compare |
| `title=name.cpp` | Show a file name above the code |
| `group=x file=y` | Part of a multi-file program; all files in group `x` are compiled together |
| `expectfile=name` | Compare the file the program writes with a following ` ```file name result ` block |

Inside ` ```output ` blocks, wrap anything the user types in `[[double brackets]]`. The verifier feeds that text to the program as keyboard input. A ` ```file name seed ` block creates a data file that later programs in the chapter can read.

Add a handwritten-style margin note to any code line with `//@ note text`.
