---
num: 2
title: Hello, C++
tagline: Meet the language, the compiler, and your very first program
learn: know where C++ came from and where it is used today; understand the difference between compiled and interpreted languages; follow the journey from source code to a running program; write, compile and run your first program; read compiler error messages without panic
---

## Amaya meets the compiler

:::story
Amaya: Okay, I have VS Code open. I typed some C++ code. Now what? I pressed "Run" and it said "g++ is not recognized".

Nuwan: Your editor is just a fancy notepad. It does not understand C++. You need a **compiler** to translate your code into something the computer can run.

Amaya: Translate? Into what?

Nuwan: Into machine code. Remember the 1s and 0s from last week? Let me show you how it works, and then we will write your first real program.
:::

## Where C++ came from

C++ was created by **Bjarne Stroustrup**, a Danish computer scientist working at Bell Labs in the United States. In 1979 he started work on a language he called "C with Classes". He wanted the speed and low-level control of the C language, plus better tools for organising large programs.

The language was renamed **C++** in 1983. The name is a programmer's joke: in C, `++` means "add one", so C++ means "one step beyond C". The first commercial release came in 1985.

To make sure every compiler understands the language the same way, C++ is defined by an international standard published by ISO (the International Organization for Standardization). A new version arrives roughly every three years:

| Standard | Year | Highlights |
|---|---|---|
| C++98 / C++03 | 1998 / 2003 | The first official standard, including the Standard Template Library (STL) |
| C++11 | 2011 | The start of "Modern C++": `auto`, range-based `for` loops, smart pointers, lambdas |
| C++14 | 2014 | Smaller improvements to C++11 |
| C++17 | 2017 | Structured bindings, `std::optional`, the filesystem library |
| C++20 | 2020 | Concepts, modules, ranges, coroutines |
| C++23 | 2024 (published) | Many library improvements |
| C++26 | Next | The next standard, currently on its way through the ISO process |

This book uses **C++17**. It is supported by every modern compiler and covers everything a beginner needs. Everything you learn here still works in the newer standards.

:::relax
You do not need to memorise this table. It is here so you understand why tutorials online sometimes say "this needs C++11" or "this is a C++20 feature". Newer versions add things; they very rarely break old code.
:::

## Where C++ is used today

Is a language from the 1980s still worth learning? Absolutely. C++ is consistently ranked among the most popular programming languages in the world, and it powers software that other software depends on:

- **Games and game engines.** Unreal Engine, used by many big-budget games, is written in C++.
- **Web browsers.** The engines inside Chrome and Firefox are written largely in C++.
- **Databases.** MySQL and MongoDB are built mostly in C++.
- **Finance.** High-speed trading systems, where a few microseconds matter, are commonly written in C++.
- **Artificial intelligence.** Libraries such as PyTorch and TensorFlow are used from Python, but their heavy number-crunching parts are written in C++.
- **Embedded systems.** Cars, medical devices and microcontrollers often run C or C++. If you have programmed an Arduino board, you have already written a form of C++.

:::industry
Very few people build websites in C++. But a huge amount of the software running underneath websites, phones, banks and games is C++. Learning it well teaches you how computers actually work: memory, speed and efficiency. Those ideas transfer to every other language you will ever learn.
:::

## Compiled vs interpreted languages

There are two main ways to turn source code into something a computer can run.

A **compiled** language, like C++, is translated **completely, before it runs**. A program called a **compiler** reads your whole source code, checks it, and produces an **executable file** of machine code. You can then run that file as many times as you like, without the compiler.

An **interpreted** language, like Python or JavaScript, is translated **while it runs**. A program called an **interpreter** reads your code and carries it out step by step, every time you run it.

| | Compiled (C++) | Interpreted (Python) |
|---|---|---|
| When is it translated? | Once, before running | Every time it runs |
| Speed when running | Usually very fast | Usually slower |
| When are many errors found? | At compile time, before running | Often only when that line runs |
| What do you share? | The executable (for one type of system) | The source code (and the user needs the interpreter) |

:::deep
The line between the two is blurrier than this table suggests. Java compiles your code into an in-between form called **bytecode**, which the Java Virtual Machine then runs, often compiling the busiest parts into machine code while the program is running. Modern JavaScript engines do something similar. C++ is about as "compiled" as a language gets, which is a big part of why it is fast.
:::

## The journey from source code to a running program

When you type `g++ hello.cpp -o hello`, it looks like one step. Really, four things happen:

```flow
flowchart LR
  A["hello.cpp<br>(your code)"] --> B[Preprocessor]
  B --> C[Compiler]
  C --> D["hello.o<br>(object code)"]
  D --> E[Linker]
  L["Library code<br>(iostream, ...)"] --> E
  E --> F["hello<br>(executable)"]
```

1. **Preprocessing.** Lines that start with `#`, such as `#include <iostream>`, are handled first. The preprocessor pastes the contents of the header file into your code.
2. **Compiling.** The compiler checks your code against the rules of C++ and translates it into low-level instructions. Most error messages you see come from here.
3. **Assembling.** Those instructions become **object code**: machine code that is not yet a complete program.
4. **Linking.** The **linker** joins your object code with the library code you used (for example, the code that actually makes `cout` work) and produces the final executable.

:::nodumb
Q: Why should I care about the linker?
A: Because some errors come from it, and they look different. If you see `undefined reference to ...`, the compiler was happy, but the linker could not find a piece of code you used. A classic beginner cause is misspelling `main`, for example `int Main()`. C++ is case sensitive, so the linker finds no `main` and gives up.

Q: Do I have to run these four steps myself?
A: No. `g++` runs all of them for you. In Chapter 17, when your project has several `.cpp` files, you will see why being able to compile them separately and link them later is so useful.
:::

## Your first C++ program

Type this into a file called `hello.cpp`. Type it, do not paste it.

```cpp title=hello.cpp
#include <iostream>       //@ pull in the input/output library
using namespace std;      //@ let us write cout instead of std::cout

int main() {              //@ every program starts running here
    cout << "Hello, World!" << endl;  //@ print a line of text
    return 0;             //@ tell the operating system: all good
}                         //@ end of main
```

Now compile it and run it. In a terminal:

```output shell
$ [[g++ -std=c++17 -Wall hello.cpp -o hello]]
$ [[./hello]]
Hello, World!
```

On Windows the second command is usually `hello.exe` or `.\hello`. If you are using an IDE such as Code::Blocks or an online compiler, a Run or Build button does both steps for you.

:::watch
The terminal output above shows the commands you type at the `$` prompt. In most of this book, the terminal boxes only show what the **program** prints, with the keyboard input that the user types shown <span class="typed">like this</span>.
:::

You just wrote a program. Five lines, and every one of them matters. Let's take it apart.

## Inside the program, line by line

### #include: borrowing a library

```cpp nocheck
#include <iostream>
```

The `#` means this line is for the **preprocessor**. `#include` says "copy the contents of this file in here". `<iostream>` is a **header file** from the C++ Standard Library. It contains the declarations for `cout` (console output), `cin` (console input) and friends.

Angle brackets, `<iostream>`, mean "look in the standard library's folders". Quotes, `"shop.h"`, mean "look in my project folder first". You will write your own header files in Chapter 17.

### using namespace std: skipping the long names

Everything in the C++ Standard Library lives inside a **namespace** called `std`. A namespace is like a surname. There could be many people called Kasun, but "Kasun Perera" is clearer. Without the `using` line, you must write the full name:

```cpp run title=no_using.cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
```

```output
Hello, World!
```

The `::` is called the **scope resolution operator**. `std::cout` means "the `cout` that lives in `std`".

:::industry
In large professional projects, many teams avoid `using namespace std;`, especially in header files, because it pulls hundreds of names into your code and can cause clashes. They write `std::` every time. This book uses `using namespace std;` in small programs to keep things readable while you learn. When you join a team, follow their style guide.
:::

### main(): where everything starts

Every C++ program must have exactly one function called `main`. When you run the program, the operating system calls `main`, and the statements inside it run from top to bottom.

`int` before `main` means `main` gives back a whole number when it finishes. `return 0;` sends back 0, which by convention means "success". Any other value means something went wrong. Scripts and other programs check this number.

:::deep
For `main` only, C++ lets you leave out `return 0;`. If you do, the program behaves as if you wrote it. Every other function that promises to return a value must actually return one. In this book we always write `return 0;` in `main` so the intention is obvious.
:::

### Statements, semicolons and blocks

A **statement** is one complete instruction. In C++, most statements end with a **semicolon** `;`. The semicolon is how the compiler knows where one instruction stops and the next starts. Forgetting it is the most common error you will ever make. Everyone does it.

A **block** is a group of statements inside curly braces `{ }`. The braces after `int main()` mark the start and end of the main function.

C++ does not care about line breaks or extra spaces between parts of a statement. This is legal:

```cpp check
cout <<
    "Hello"
    << endl;
```

But just because it is legal does not mean it is a good idea. Use indentation (usually 4 spaces) inside every block, so that the structure of your program is visible at a glance.

:::watch
C++ is **case sensitive**. `cout`, `Cout` and `COUT` are three different names. Only `cout` exists in the standard library. The same goes for `main` and `Main`, `int` and `Int`.
:::

### Comments: notes for humans

The compiler ignores comments. They are for people, including you in six months.

```cpp check
// This is a single-line comment. Everything after // is ignored.

/* This is a multi-line comment.
   It can run across
   several lines. */

int items = 3;  // a comment can also sit at the end of a line
```

Good comments explain **why**, not **what**. The code already says what it does.

```cpp check
int count = 0;
count = count + 1;   // add 1 to count   (useless: the code already says this)
count = count + 1;   // the first customer is always free, so start at 1  (useful: explains a reason)
```

## Printing with cout

`cout` is pronounced "see-out" and stands for **console output**. The `<<` arrows are the **insertion operator**: they push whatever is on the right into the output stream. You can chain as many as you like:

```cpp run title=receipt_header.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Ruwan Stores" << endl;
    cout << "No. 12, Peradeniya Road, Kandy" << endl;
    cout << "Items: " << 3 << ", Total: Rs. " << 1450 << endl;
    return 0;
}
```

```output
Ruwan Stores
No. 12, Peradeniya Road, Kandy
Items: 3, Total: Rs. 1450
```

Text inside double quotes is called a **string literal**. It is printed exactly as written. Numbers without quotes are printed as numbers.

### Going to a new line: endl or \n

`endl` ends the line and moves the cursor to the start of the next one. The special character `\n` (backslash n) does the same thing inside a string:

```cpp run title=newlines.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Line one\nLine two\n";
    cout << "Line three" << endl;
    return 0;
}
```

```output
Line one
Line two
Line three
```

:::nodumb
Q: So what is the difference between endl and \n?
A: Both give you a new line. `endl` also **flushes** the output, which means it forces everything waiting in the output buffer to be sent to the screen immediately. Flushing takes a little time. In a loop that prints thousands of lines, using `\n` is noticeably faster. For small programs, use whichever you find clearer.
:::

### Escape sequences

`\n` is an **escape sequence**: a backslash followed by a character that has a special meaning. Here are the ones you will use most:

| Escape sequence | Meaning | Example output |
|---|---|---|
| `\n` | New line | moves to the next line |
| `\t` | Tab | jumps to the next tab stop |
| `\"` | A double quote character | `He said "hi"` |
| `\'` | A single quote character | `It's` (needed inside `' '`) |
| `\\` | A backslash character | `C:\Users` |

```cpp run title=escapes.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Item\tQty\tPrice\n";
    cout << "Rice\t2\t460\n";
    cout << "Uncle Ruwan says \"Thank you, come again!\"\n";
    cout << "Saved to C:\\shop\\bills\n";
    return 0;
}
```

```output
Item	Qty	Price
Rice	2	460
Uncle Ruwan says "Thank you, come again!"
Saved to C:\shop\bills
```

:::sharpen What does it print?
Predict the exact output, including line breaks, before you check.

```cpp run title=predict.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "A" << "B" << endl << "C";
    cout << "D\n\nE" << endl;
    return 0;
}
```
---solution
```output
AB
CD

E
```
`endl` ends the first line after `AB`. `C` and `D` have no line break between them, so they print together as `CD`. Then `\n\n` gives **two** line breaks, which creates the empty line before `E`.
:::

## When things go wrong: three kinds of errors

Every programmer meets three kinds of errors. Knowing which kind you have is half the fix.

| Kind | When it shows up | Example | Who catches it |
|---|---|---|---|
| **Compile-time error** (syntax error) | When you compile | Missing semicolon, misspelled name | The compiler, which refuses to build |
| **Runtime error** | While the program runs | Dividing an integer by zero, reading a missing file | Sometimes nobody: the program crashes or misbehaves |
| **Logic error** | When you check the results | Using `+` instead of `*`, wrong formula | Only you, by testing |

Logic errors are the sneakiest. The program compiles and runs perfectly. It just gives the wrong answer.

:::fireside The Compiler|A Logic Error
1: People call me strict. I call myself helpful. If you forget a semicolon, I tell you the file, the line and even the column. Within seconds.

2: You are very loud about it. I prefer to stay quiet. I let the program compile, run, and print a beautiful, confident, completely wrong total.

1: That is exactly why programmers should thank me. I catch problems *before* the program reaches a customer.

2: And I am why they write tests. Nobody catches me except a human who checks the answer with a calculator.

1: Fine. Let's agree on one thing. Students should read my messages carefully, and test their programs with real data.

2: Agreed. But I am still not telling them where I am hiding.
:::

### Reading a g++ error message

Let's make a mistake on purpose. Here is a program with a missing semicolon:

```cpp error title=shop.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Welcome to Ruwan Stores!" << endl  //@ the semicolon is missing here
    return 0;
}
```

This is what g++ says:

```output noterm
shop.cpp: In function 'int main()':
shop.cpp:5:47: error: expected ';' before 'return'
    5 |     cout << "Welcome to Ruwan Stores!" << endl
      |                                               ^
      |                                               ;
    6 |     return 0;
      |     ~~~~~~
```

Read it like this:

- `shop.cpp:5:47` means **file** `shop.cpp`, **line 5**, **column 47**.
- `error:` tells you it is an error, not a warning. The program was **not** built.
- `expected ';' before 'return'` is the actual problem. The compiler even draws the missing `;` for you.

:::watch
The compiler reports where it **noticed** the problem, which is sometimes a line **after** the real mistake. Here it complains about the `return` on line 6 even though the semicolon is missing from line 5. When an error does not make sense on the line shown, look at the line above.
:::

### Common first-timer errors

| You wrote | g++ says (shortened) | The fix |
|---|---|---|
| Forgot `;` | `expected ';' before ...` | Add the semicolon at the end of the previous statement |
| `Cout << "Hi";` | `'Cout' was not declared in this scope` | C++ is case sensitive. Use `cout` |
| Forgot `#include <iostream>` | `'cout' was not declared in this scope` | Add the include at the top |
| `cout << totl;` with a variable called `total` | `'totl' was not declared in this scope; did you mean 'total'?` | Fix the spelling. g++ often suggests the right name |
| `int Main()` | `undefined reference to 'main'` (from the linker) | The function must be called `main`, all lowercase |
| Missing closing `}` | `expected '}' at end of input` | Count your braces. Good indentation makes this easy to spot |
| `cout << "Hello;` | `missing terminating " character` | Close the string with a matching `"` |

:::nodumb
Q: I fixed one error and now there are five new ones. What happened?
A: Usually nothing bad. One mistake, like a missing brace, can confuse the compiler about everything that follows. The general rule is: **fix the first error first**, recompile, and repeat. Many of the later errors disappear on their own.

Q: What are warnings?
A: Warnings mean "this is legal C++, but it looks suspicious". The program still compiles. Treat warnings as early bug reports. The `-Wall` option turns most of the useful ones on. Professional teams often compile with warnings treated as errors.
:::

### A simple debugging routine

When your program does not work, panic is optional. Follow these steps:

1. **Read the first error message slowly.** Note the line number.
2. **Look at that line and the line above it.** Check semicolons, braces, quotes and spelling.
3. **Fix one thing, then recompile.** Do not change five things at once.
4. **If it compiles but gives wrong results,** add temporary `cout` lines that print the values of your variables, so you can see where things start to go wrong.
5. **Explain your code out loud, line by line.** Programmers call this **rubber duck debugging**, because you can explain it to a rubber duck on your desk. You will often hear yourself say the mistake.

:::compiler
Each of these programs is meant to print `Ruwan Stores is open`. Pretend you are the compiler. Which ones will compile? Fix the broken ones.

**A**

```cpp error
#include <iostream>
using namespace std;
int main() {
    cout << "Ruwan Stores is open" << endl;
    return 0;
```

**B**

```cpp error
#include <iostream>
using namespace std;
int main() {
    cout << "Ruwan Stores is open" << endl
    return 0;
}
```

**C**

```cpp
#include <iostream>
using namespace std;
int main() {
cout<<"Ruwan Stores is open"<<endl;
return 0;
}
```

**D**

```cpp error
#include <iostream>
using namespace std;
int main() {
    cout << "Ruwan Stores is open << endl;
    return 0;
}
```
---solution
- **A** does not compile. The closing `}` of `main` is missing. g++ reports `expected '}' at end of input`.
- **B** does not compile. The semicolon after `endl` is missing.
- **C** compiles and runs correctly. It is badly formatted (no spaces, no indentation), but the compiler does not care about layout. People do, though, so please do not write code like this.
- **D** does not compile. The string is never closed, because the `"` before `<< endl` is missing. g++ reports `missing terminating " character`.
:::

:::magnets
Put the magnets in order to make a program that prints the two lines `Ruwan Stores` and `Open 7am to 9pm`.
~~~
#include <iostream>
using namespace std;
int main() {
cout << "Ruwan Stores" << endl;
cout << "Open 7am to 9pm" << endl;
return 0;
}
~~~
:::

:::quiz
? What does the preprocessor do with `#include <iostream>`?
- Downloads the iostream library from the internet
* Copies the contents of the iostream header into your code before compiling
- Runs the program
- Checks your spelling
> Lines starting with `#` are preprocessor directives. `#include` pastes the named file into your source code.

? Which stage combines your object code with library code to make the final executable?
- The preprocessor
- The compiler
* The linker
- The editor
> The linker joins object files and libraries. Errors that mention `undefined reference` usually come from it.

? What does `return 0;` at the end of `main` mean?
- The program printed nothing
* The program finished successfully
- The program should restart
- The program had zero errors at compile time
> By convention, 0 tells the operating system that the program completed successfully.

? Which of these is a logic error?
- Forgetting a semicolon
- Writing `Cout` instead of `cout`
* Calculating a total with `price + qty` instead of `price * qty`
- Forgetting `#include <iostream>`
> The program compiles and runs, but the answer is wrong. Only testing finds logic errors.

? What does `\t` print?
- The letter t
- A new line
* A tab
- A backslash
> `\t` is the escape sequence for a horizontal tab.
:::

:::lab Your first Ruwan Stores program
Write a program called `welcome.cpp` that prints exactly this:

```text
=============================
   RUWAN STORES, KANDY
   "Fresh. Fair. Friendly."
=============================
Open: Mon to Sat, 7am to 9pm
```

Then try these experiments, one at a time, and note what the compiler says:

1. Remove one semicolon.
2. Change `main` to `Main`.
3. Remove the `#include` line.
4. Remove one `"` from a string.
---solution
```cpp run title=welcome.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "=============================" << endl;
    cout << "   RUWAN STORES, KANDY" << endl;
    cout << "   \"Fresh. Fair. Friendly.\"" << endl;
    cout << "=============================" << endl;
    cout << "Open: Mon to Sat, 7am to 9pm" << endl;
    return 0;
}
```

```output
=============================
   RUWAN STORES, KANDY
   "Fresh. Fair. Friendly."
=============================
Open: Mon to Sat, 7am to 9pm
```
The quotes around the slogan need the escape sequence `\"`. For the experiments: (1) `expected ';' before ...`; (2) a linker error, `undefined reference to 'main'`; (3) `'cout' was not declared in this scope` together with a note suggesting `#include <iostream>`; (4) `missing terminating " character`.
:::

:::bullets
- C++ was created by **Bjarne Stroustrup** (work began in 1979, named C++ in 1983) and is defined by an **ISO standard**. This book uses **C++17**.
- C++ is a **compiled** language: the whole program is translated to machine code before it runs, which makes it fast.
- Building a program means **preprocessing, compiling, assembling and linking**. `g++` does all four.
- Every program needs exactly one `main()` function. `return 0;` means success.
- Most statements end with a **semicolon**. Blocks use **curly braces**. C++ is **case sensitive**.
- `cout << ...` prints. `endl` and `\n` both start a new line. Escape sequences such as `\t` and `\"` print special characters.
- There are **compile-time**, **runtime** and **logic** errors. Read error messages from the **first** one, and check the line above the one reported.
:::
