---
num: B
kind: appendix
title: Compiler Error Decoder
tagline: What g++ is really trying to tell you
---

## How to read any error

Every g++ message has the same shape:

```output noterm
file.cpp:12:5: error: 'total' was not declared in this scope
```

**File** `file.cpp`, **line** 12, **column** 5, **kind** `error` (the program was not built) or `warning` (it was built, but something looks wrong), and then the **message**.

Four golden rules:

1. Fix the **first** error first, then recompile. Later errors are often caused by the first one.
2. If the line looks fine, check the line **above** it.
3. Read the whole message slowly. g++ often suggests the fix (`did you mean 'total'?`).
4. Treat warnings as bugs that have not happened yet.

The messages below are real g++ 13 messages, sometimes shortened. Other compilers (clang, Visual C++) word them differently, but the meaning is the same.

## Errors

| Message | Usual cause | Fix |
|---|---|---|
| `expected ';' before 'return'` (or `expected ',' or ';' before ...`) | missing semicolon at the end of the previous statement | add the `;` on the line **before** the one reported |
| `'total' was not declared in this scope` | misspelt name, wrong capitalisation, variable used outside its block, or used before it was declared | check spelling and case; declare the variable earlier or in an outer block |
| `'cout' was not declared in this scope` | missing `#include <iostream>` or missing `using namespace std;` | add the include, or write `std::cout` |
| `expected '}' at end of input` | a `{` was never closed | count your braces; fix indentation to find the gap |
| `missing terminating " character` | a string with no closing quote | add the closing `"` |
| `'else' without a previous 'if'` | a stray `;` after `if (...)`, or braces in the wrong place | remove the semicolon; add braces |
| `no match for 'operator<<' (operand types are 'std::istream' ...)` | `cin << x` instead of `cin >> x` (or printing something cout cannot print, such as a struct) | use `>>` with `cin`; print struct members one by one |
| `conversion from 'double' to non-scalar type 'std::string' requested` | assigning a number to a string | use `to_string(x)` |
| `invalid conversion from 'const char*' to 'int'` | assigning text such as `"5"` to an int | use `5`, or `stoi("5")` |
| `too few arguments to function 'int add(int, int)'` | a call with the wrong number of arguments | match the call to the parameter list |
| `assignment of read-only variable 'MAX'` | changing a `const` | do not change constants; use a normal variable if it must change |
| `cannot bind non-const lvalue reference of type 'int&' to an rvalue of type 'int'` | passing a literal such as `5` to an `int &` parameter | pass a variable, or make the parameter `const int &` or plain `int` |
| `redeclaration of 'int x'` | declaring the same variable twice in one scope | remove the type from the second line: `x = 2;` |
| `expected ';' after struct definition` | missing `;` after the closing `}` of a struct | write `};` |
| `'struct P' has no member named 'b'` | misspelt member name | check the struct definition |
| `invalid array assignment` | `b = a;` with plain arrays | copy with a loop, or use `vector` |
| `jump to case label` | declaring a variable inside a `case` without braces | wrap the case body in `{ }` |
| `void value not ignored as it ought to be` | using the result of a `void` function | make the function return a value, or do not use its result |
| `cannot convert 'double*' to 'int*' in initialization` | pointer of the wrong type | make the types match |
| `narrowing conversion of '7.9000000000000004e+0' from 'double' to 'int'` | brace initialisation that would lose data, such as `int x{7.9};` | use the right type, or convert deliberately with `static_cast` |
| `'string' was not declared in this scope` | missing `#include <string>` or `std::` | add the include |

## Linker errors

These appear **after** compiling succeeded, when the linker joins everything.

| Message | Usual cause | Fix |
|---|---|---|
| `undefined reference to 'main'` | no `main` function, or a misspelt one such as `Main` | name it `int main()` |
| `undefined reference to 'readInt(...)'` | the function was declared but never defined, or its `.cpp` file is missing from the build | add the definition, or add the `.cpp` file to the g++ command |
| `multiple definition of 'helper()'` | a function body in a header included by several `.cpp` files | move the body into one `.cpp` file, and keep only the prototype in the header |
| `ld returned 1 exit status` | the summary line after any linker error | read the lines above it |

## Warnings worth fixing

| Warning | What it means |
|---|---|
| `'x' is used uninitialized` | you read a variable before giving it a value |
| `unused variable 'x'` | you declared something you never use: a typo or leftover code |
| `suggest parentheses around assignment used as truth value` | probably `=` where you meant `==` |
| `comparisons like 'X<=Y<=Z' do not have their mathematical meaning` | write `X <= Y && Y <= Z` |
| `control reaches end of non-void function` | some path through a function has no `return` |
| `comparison of integer expressions of different signedness` | an `int` compared with `v.size()`; use `size_t` or a range-based loop |
| `this statement may fall through` | a `case` without `break` (enabled by `-Wextra`) |
| `this 'if' clause does not guard...` | indentation suggests a line is inside an `if`, but without braces it is not |
| `suggest explicit braces to avoid ambiguous 'else'` | a dangling else: add braces |
| `address of local variable 'x' returned` | returning a pointer or reference to a local variable |

## Runtime problems (no error message at all)

| Symptom | Common causes |
|---|---|
| The program prints a strange huge or negative number | uninitialised variable; integer overflow; reading past the end of an array |
| `Segmentation fault` (or the program just crashes) | dereferencing a null or invalid pointer; going far out of array bounds; infinite recursion |
| The program never stops | a loop whose condition never becomes false; `while (...);` with a stray semicolon; `cin` stuck in a fail state |
| The program skips an input | the getline trap: `getline` after `cin >>` without `cin.ignore` |
| The last line of a file is processed twice | looping on `eof()` instead of on the read |
| The answer is a little wrong | integer division; `==` on doubles; operator precedence |
| A saved file is empty or missing | the stream was never checked after opening; wrong working directory; file opened in overwrite mode |
| `terminate called after throwing an instance of 'std::out_of_range'` | `.at()` or `substr` with an index that is too large |
| `terminate called after throwing an instance of 'std::invalid_argument'` | `stoi` or `stod` on text that is not a number |
