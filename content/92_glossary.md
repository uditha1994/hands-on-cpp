---
num: C
kind: appendix
title: Glossary
tagline: The words programmers use, in plain English
---

## A to D

| Term | Meaning | Chapter |
|---|---|---|
| **Accumulator** | A variable that builds up a running total inside a loop | 8 |
| **Algorithm** | A finite, ordered set of clear steps that solves a problem | 1 |
| **Argument** | The actual value passed to a function in a call | 9 |
| **Array** | A fixed-size collection of elements of the same type, accessed by index | 11 |
| **ASCII** | A standard that gives each common character a number, such as 'A' = 65 | 3 |
| **Assignment** | Storing a value in a variable with `=` | 5 |
| **Associativity** | The rule for the order of operators with the same precedence | 5 |
| **Base case** | The condition that stops a recursive function | 10 |
| **Big-O notation** | A way to describe how the work an algorithm does grows with the input size | 8, 13 |
| **Binary search** | Searching sorted data by repeatedly halving the range, O(log n) | 13 |
| **Block** | A group of statements inside `{ }` | 2 |
| **bool** | A type that holds `true` or `false` | 3, 6 |
| **Breakpoint** | A place where a debugger pauses your program | 17 |
| **Buffer** | A temporary storage area, such as the input buffer that holds what the user types | 4 |
| **Bug** | A mistake that makes a program behave wrongly | 1, 2 |
| **Call stack** | The stack of function calls currently running, each with its own frame | 10 |
| **Cast** | An explicit type conversion, such as `static_cast<double>(x)` | 5 |
| **Compiler** | The program that translates source code into machine code | 2 |
| **Compound assignment** | Shortcuts such as `+=` and `*=` | 5 |
| **Concatenation** | Joining strings together | 12 |
| **const** | A keyword that makes a variable read-only | 3 |
| **CSV** | Comma-separated values: a simple text format for tables | 16 |
| **Dangling pointer** | A pointer to memory that has already been freed | 15 |
| **Debugger** | A tool that runs a program step by step and shows variable values | 17 |
| **Declaration** | Telling the compiler that something exists and what type it has | 3, 9 |
| **Definition** | Providing the actual content: a variable's storage or a function's body | 9, 17 |
| **De Morgan's laws** | Rules for flipping combined conditions: `!(A && B)` is `!A \|\| !B` | 6 |
| **Dereference** | Using `*p` to reach the value a pointer points to | 15 |

## E to L

| Term | Meaning | Chapter |
|---|---|---|
| **Edge case** | An unusual input at the limits of what a program handles, such as 0 or an empty list | 1 |
| **Element** | One value stored in an array or vector | 11 |
| **enum class** | A type with a fixed list of named values | 14 |
| **Escape sequence** | A backslash code inside a string, such as `\n` or `\t` | 2 |
| **Exception** | An error object thrown when something goes wrong, which can be caught with `try` / `catch` | 12, 17 |
| **Executable** | The finished program file that the computer can run | 2 |
| **Expression** | Anything that produces a value, such as `price * qty` | 5 |
| **Fail state** | The state `cin` enters after a failed read; it must be cleared | 4 |
| **Flowchart** | A diagram of an algorithm using standard shapes | 1 |
| **Function** | A named, reusable block of code that does one job | 9 |
| **Global variable** | A variable declared outside all functions, visible everywhere | 10 |
| **Guard clause** | An early check that rejects bad input or situations | 7 |
| **Header file** | A file (`.h`) of declarations that other files include | 2, 17 |
| **Heap** | Memory requested at runtime with `new` (or managed by vectors and smart pointers) | 15 |
| **IDE** | Integrated Development Environment: an editor, compiler and debugger in one | 2 |
| **Include guard** | `#ifndef`, `#define`, `#endif` lines that stop a header being read twice | 17 |
| **Index** | The position of an element in an array, vector or string, starting at 0 | 11 |
| **Infinite loop** | A loop whose condition never becomes false | 8 |
| **Initialisation** | Giving a variable its first value | 3 |
| **IPO model** | Input, Process, Output: a simple way to design a program | 1 |
| **Iteration** | One repetition of a loop; also the general idea of repeating | 1, 8 |
| **Iterator** | An object that marks a position in a container, such as `v.begin()` | 13 |
| **Lambda** | A small unnamed function written inline, such as `[](int a, int b) { return a < b; }` | 14 |
| **Linear search** | Checking every element in turn, O(n) | 13 |
| **Linker** | The program that joins object files and libraries into an executable | 2, 17 |
| **Local variable** | A variable that exists only inside its block or function | 9, 10 |
| **Logic error** | A mistake that makes a program give wrong results without crashing | 2 |

## M to R

| Term | Meaning | Chapter |
|---|---|---|
| **Machine code** | The binary instructions a processor runs directly | 1, 2 |
| **Member** | A variable or function inside a struct or class | 14 |
| **Memory leak** | Heap memory that is never freed | 15 |
| **Modulus** | The `%` operator, which gives the remainder of integer division | 5 |
| **Namespace** | A named container for identifiers, such as `std` | 2 |
| **Nested loop** | A loop inside another loop | 8 |
| **npos** | The value `find` returns when nothing was found | 12 |
| **nullptr** | The value for a pointer that points to nothing | 15 |
| **Object file** | Compiled code (`.o`) that is not yet linked into a program | 17 |
| **Off-by-one error** | A loop that runs one time too many or too few | 8 |
| **Operand** | A value that an operator works on | 5 |
| **Overflow** | A value too large for its type | 3 |
| **Overloading** | Several functions with the same name but different parameters | 9 |
| **Parameter** | A variable in a function's header that receives an argument | 9 |
| **Pass by reference** | Giving a function direct access to the caller's variable (`int &x`) | 10 |
| **Pass by value** | Giving a function a copy of the argument | 9 |
| **PDLC** | Program development life cycle: define, design, code, test, document, maintain | 1 |
| **Pointer** | A variable that stores a memory address | 15 |
| **Precedence** | Which operators are evaluated first | 5 |
| **Preprocessor** | The stage that handles `#` lines, such as `#include`, before compiling | 2 |
| **Prototype** | A function declaration: its header followed by `;` | 9 |
| **Pseudocode** | An algorithm written in structured plain English | 1 |
| **RAII** | Resource Acquisition Is Initialization: resources are released automatically when their owner goes out of scope | 15 |
| **Recursion** | A function calling itself to solve a smaller version of the problem | 10 |
| **Reference** | Another name (alias) for an existing variable | 10 |
| **Runtime error** | An error that happens while the program is running | 2 |

## S to Z

| Term | Meaning | Chapter |
|---|---|---|
| **Scope** | The part of the program where a name can be used | 7, 10 |
| **Sentinel** | A special input value that means "stop" | 8 |
| **Short-circuit evaluation** | `&&` and `\|\|` stop as soon as the result is known | 6 |
| **Smart pointer** | A pointer object, such as `unique_ptr`, that deletes its object automatically | 15 |
| **Source code** | The human-readable program you write | 2 |
| **Stack** | The memory area for function calls and local variables | 10, 15 |
| **Stack overflow** | Running out of stack space, often from recursion without a base case | 10 |
| **Statement** | One complete instruction, usually ending with `;` | 2 |
| **static (local)** | A local variable that keeps its value between calls | 10 |
| **Stream** | A flow of characters in or out of a program, such as `cin`, `cout` or a file | 4, 16 |
| **String** | A sequence of characters | 3, 12 |
| **Struct** | A user-defined type that groups related members | 14 |
| **Syntax error** | Code that breaks the grammar rules of the language | 2 |
| **Trace table** | A table used to run an algorithm by hand, step by step | 1 |
| **Truth table** | A table of the results of a logical expression for every input | 6 |
| **Undefined behaviour** | Code whose result the C++ standard does not define; anything may happen | 3, 11, 15 |
| **Variable** | A named, typed piece of memory whose value can change | 3 |
| **Vector** | A resizable array from the standard library (`std::vector`) | 11 |
| **void** | The return type of a function that returns nothing | 9 |
| **Warning** | A message about code that is legal but suspicious | 2 |
