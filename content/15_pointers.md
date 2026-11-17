---
num: 15
title: Pointers and Memory
tagline: Looking under the hood at addresses, the stack and the heap
learn: find the address of a variable; declare, set and dereference pointers; compare pointers with references; use nullptr safely; reach struct members through a pointer with ->; understand how arrays and pointers are related; allocate and free memory on the heap; avoid leaks and dangling pointers; know why modern C++ prefers vectors and smart pointers
---

## Every box has an address

:::story
Amaya: You keep saying "arrays pass the address of the first element" and "a reference refers to the same memory". What is an address, really? Can I see one?

Nuwan: You can. Every variable lives somewhere in memory, and C++ lets you ask where. A variable that stores an address is called a **pointer**.

Dilshan: I heard pointers are the scary part of C++.

Nuwan: They are powerful, and you must be careful with them. But they are not magic. By the end of today you will see that you have been using the idea since Chapter 10.
:::

:::relax
Pointers take most people two or three passes to understand. That is completely normal. Read this chapter once for the big picture, type in the examples, then come back to it in a week. It will make much more sense the second time.
:::

## Addresses and the & operator

Memory is a long row of bytes, each with a numbered **address**. Put `&` in front of a variable to get its address:

```cpp run random title=address.cpp
#include <iostream>
using namespace std;

int main() {
    int stock = 42;
    double price = 230.5;
    cout << "stock is " << stock << " and lives at " << &stock << endl;
    cout << "price is " << price << " and lives at " << &price << endl;
    return 0;
}
```

```output
stock is 42 and lives at 0x7ffc9a3b5e2c
price is 230.5 and lives at 0x7ffc9a3b5e30
```

The addresses are printed in **hexadecimal** (base 16, starting with `0x`). Yours will be different, and they usually change every time you run the program, because modern operating systems deliberately place memory at unpredictable addresses for security.

:::watch
The `&` symbol has two different jobs in C++, depending on where it appears:

- In a **declaration**, it makes a **reference**: `int &r = stock;` (Chapter 10).
- In an **expression**, it means **"address of"**: `&stock`.

The same is true of `*`, as you are about to see. Context is everything.
:::

## Pointers

A **pointer** is a variable whose value is an **address**. You declare it with a `*` after the type it points to:

```cpp run title=pointer_basics.cpp
#include <iostream>
using namespace std;

int main() {
    int stock = 42;
    int *p = &stock;          //@ p is a pointer to int, holding stock's address

    cout << stock << endl;    //@ the value: 42
    cout << *p << endl;       //@ * in an expression: "the value at the address in p"

    *p = 50;                  //@ change stock THROUGH the pointer
    cout << stock << endl;

    int other = 7;
    p = &other;               //@ a pointer can be re-aimed at something else
    cout << *p << endl;
    return 0;
}
```

```output
42
42
50
7
```

Let's picture it. Suppose `stock` is stored at address `0x1000`:

| Variable | Address | Value |
|---|---|---|
| `stock` | `0x1000` | 42, then 50 |
| `p` | `0x2000` | `0x1000` (the address of `stock`) |

- `p` is the pointer itself: an address, `0x1000`.
- `*p` means "go to the address in `p` and use what is there". This is called **dereferencing**. `*p` **is** `stock`.
- `&stock` is `0x1000`.

| Expression | Meaning | Value |
|---|---|---|
| `stock` | the int | 50 |
| `&stock` | the address of the int | `0x1000` |
| `p` | the pointer's value, an address | `0x1000` |
| `*p` | the int that p points to | 50 |
| `&p` | the address of the pointer itself | `0x2000` |

:::nodumb
Q: Is it `int *p` or `int* p`?
A: Both mean the same thing, and programmers argue about it endlessly. Be careful with this line, though: `int* a, b;` makes `a` a pointer but `b` a plain `int`, because the `*` belongs to each name separately. Declare one pointer per line and the problem disappears.

Q: Why does a pointer need a type? An address is just a number.
A: The type tells C++ what is **at** the address: how many bytes to read and how to interpret them. An `int *` reads an int; a `double *` reads a double. Mixing them up would read the bytes completely wrongly, so C++ will not let you assign a `double *` to an `int *` without an explicit cast.
:::

## nullptr: a pointer to nothing

A pointer that does not point to anything valid should be set to **`nullptr`** (C++11). Always initialise pointers, just like any other variable.

```cpp run title=nullptr.cpp
#include <iostream>
using namespace std;

int main() {
    int *p = nullptr;                //@ points nowhere, on purpose
    if (p != nullptr) {              //@ always check before dereferencing
        cout << *p << endl;
    } else {
        cout << "No value yet." << endl;
    }
    return 0;
}
```

```output
No value yet.
```

:::watch
Dereferencing a null pointer, or an uninitialised one, is **undefined behaviour**. With a null pointer, most systems crash immediately with a **segmentation fault**. With an uninitialised pointer, you might read or overwrite any random memory, which is even worse. Rule: every pointer is either `nullptr` or points to something valid, and you check before you dereference. Older code uses `NULL` or `0` instead of `nullptr`.
:::

## Pointers and references compared

You have seen both now. They are related: both let you reach another variable indirectly.

| | Reference `int &r = x;` | Pointer `int *p = &x;` |
|---|---|---|
| Must be initialised? | Yes | No (but you should, to `nullptr` at least) |
| Can be null? | No | Yes |
| Can be re-aimed at another variable? | No, it is bound for life | Yes |
| Syntax to reach the value | just `r` | `*p` |
| Main uses | function parameters, range-for loops | optional values, dynamic memory, arrays, data structures |

Here is the swap function from Chapter 10, written both ways:

```cpp run title=swap_both.cpp
#include <iostream>
using namespace std;

void swapRef(int &a, int &b) {
    int t = a; a = b; b = t;
}

void swapPtr(int *a, int *b) {       //@ receives two addresses
    int t = *a; *a = *b; *b = t;     //@ works on the values at those addresses
}

int main() {
    int x = 1, y = 2;
    swapRef(x, y);
    cout << x << " " << y << endl;
    swapPtr(&x, &y);                 //@ the caller must pass addresses explicitly
    cout << x << " " << y << endl;
    return 0;
}
```

```output
2 1
1 2
```

The pointer version makes the caller write `&x`, which at least makes it **visible** that `x` might change. In C++, references are usually preferred for parameters, because they are simpler and cannot be null. C code, which has no references, uses pointers for this everywhere.

## Pointers to structs: the -> operator

With a pointer to a struct, you could write `(*p).price`, but it is so common that C++ gives you a shortcut, the **arrow operator** `->`:

```cpp run title=arrow.cpp
#include <iostream>
#include <string>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

void discount(Product *p, double percent) {
    if (p == nullptr) return;               //@ guard against a null pointer
    p->price *= 1 - percent / 100;          //@ p->price means (*p).price
}

int main() {
    Product tea = {"Ceylon Tea 200g", 520, 4};
    Product *ptr = &tea;
    discount(ptr, 10);
    cout << ptr->name << " now Rs. " << ptr->price << endl;
    cout << tea.name << " now Rs. " << tea.price << endl;   //@ same product
    return 0;
}
```

```output
Ceylon Tea 200g now Rs. 468
Ceylon Tea 200g now Rs. 468
```

Use `.` with a struct **variable** (or a reference). Use `->` with a **pointer** to a struct.

## Pointers and arrays

The name of an array, used in an expression, turns into a pointer to its **first element**. This is called **array decay**, and it is why passing an array to a function passes an address (Chapter 11).

```cpp run title=pointer_arithmetic.cpp
#include <iostream>
using namespace std;

int main() {
    int stock[5] = {12, 40, 8, 25, 3};
    int *p = stock;                     //@ same as &stock[0]

    cout << *p << endl;                 //@ stock[0]
    cout << *(p + 1) << endl;           //@ stock[1]: p + 1 is the NEXT int, not the next byte
    cout << p[2] << endl;               //@ indexing works on pointers too
    p++;                                //@ move to the next element
    cout << *p << endl;

    for (int *q = stock; q < stock + 5; q++) {   //@ walk the array with a pointer
        cout << *q << " ";
    }
    cout << endl;
    return 0;
}
```

```output
12
40
8
40
12 40 8 25 3 
```

When you add 1 to an `int *`, it moves forward by `sizeof(int)` bytes (usually 4), to the next `int`. This is **pointer arithmetic**. In fact, C++ defines `arr[i]` to mean exactly `*(arr + i)`.

:::deep
Pointer arithmetic is how arrays really work underneath, and it is how iterators such as `v.begin()` and `v.end()` (Chapter 13) behave: `end` points **one past** the last element, so a loop runs while `q < stock + 5`. You are allowed to point one past the end, but never to dereference that position. Pointer arithmetic is also why out-of-bounds bugs are so easy in C and C++: nothing stops `p + 100`.
:::

## The stack and the heap

So far, every variable you have created was **automatic**: it lives on the **stack** (Chapter 10's call stack) and disappears when its function or block ends. That is fast and safe, but it has limits:

- Stack memory is fairly small (often a few megabytes).
- Variables vanish when their function returns.
- Their sizes are fixed when you write the code.

The **heap** (also called the free store) is a large pool of memory you can request **while the program runs**. Memory you get from the heap stays allocated until **you** give it back.

| | Stack | Heap |
|---|---|---|
| How you get it | declare a variable | `new` |
| How you free it | automatically, at the end of the block | `delete`, which you must call yourself |
| Size | small | large |
| Lifetime | until the block ends | until you delete it |
| Speed | very fast | slower |

### new and delete

```cpp run title=new_delete.cpp
#include <iostream>
using namespace std;

int main() {
    int *p = new int(25);            //@ one int on the heap, set to 25
    cout << *p << endl;
    delete p;                        //@ give the memory back
    p = nullptr;                     //@ good habit: no dangling pointer

    int n;
    cout << "How many days? ";
    cin >> n;
    double *sales = new double[n];   //@ an array whose size is chosen at runtime
    for (int i = 0; i < n; i++) sales[i] = 1000.0 * (i + 1);
    double total = 0;
    for (int i = 0; i < n; i++) total += sales[i];
    cout << "Total: " << total << endl;
    delete[] sales;                  //@ arrays from new[] need delete[]
    sales = nullptr;
    return 0;
}
```

```output
25
How many days? [[4]]
Total: 10000
```

### What can go wrong

Managing heap memory by hand is where many serious C++ bugs come from:

| Bug | What happens | Example |
|---|---|---|
| **Memory leak** | you never `delete`, so the memory stays used until the program ends | `new` inside a loop with no `delete` |
| **Dangling pointer** | you use a pointer after the memory was deleted | `delete p; cout << *p;` |
| **Double delete** | you delete the same memory twice | `delete p; delete p;` (undefined behaviour) |
| **Wrong delete** | `delete` on memory from `new[]`, or the other way round | `delete sales;` instead of `delete[] sales;` |

:::watch
Never return a pointer (or reference) to a **local** variable:

```cpp fn nowarn
int *badIdea() {
    int total = 100;
    return &total;     // total is destroyed when the function returns!
}
```

The address points to stack memory that is reused by the next function call. Using it is undefined behaviour. g++ warns: *address of local variable 'total' returned*.
:::

## Modern C++: let something else do the deleting

Because manual `new` and `delete` are so error-prone, modern C++ strongly prefers tools that clean up **automatically**:

- For a **collection** of values whose size is decided at runtime: **`std::vector`**. It uses the heap internally, and frees the memory when the vector goes out of scope. The dynamic array example above is simply `vector<double> sales(n);`.
- For a **single object** on the heap: a **smart pointer**, such as `std::unique_ptr` from `<memory>`.

```cpp run title=smart_pointer.cpp
#include <iostream>
#include <memory>
#include <string>
using namespace std;

struct Product {
    string name;
    double price;
};

int main() {
    unique_ptr<Product> p = make_unique<Product>();   //@ C++14: allocate on the heap
    p->name = "Dhal 500g";
    p->price = 320;
    cout << p->name << ": Rs. " << p->price << endl;
    return 0;
}                                                     //@ the Product is deleted automatically here
```

```output
Dhal 500g: Rs. 320
```

A `unique_ptr` **owns** its object. When the `unique_ptr` is destroyed, at the end of its scope, it deletes the object for you. You cannot forget, and you cannot delete twice. This idea, tying a resource's lifetime to an object's scope, is called **RAII** (Resource Acquisition Is Initialization), and it is one of the most important ideas in modern C++. `vector`, `string`, `ifstream` and smart pointers all follow it.

:::industry
In professional modern C++ code, a raw `new` or `delete` is rare, and code reviewers will ask why it is there. You still need to **understand** pointers, because they appear in older code, in C libraries, in embedded systems, in data structures such as linked lists and trees, and in every job interview about C++. But in your own new code, reach for `vector`, `string`, references and smart pointers first.
:::

:::compiler
Predict what each snippet does. Which ones are bugs?

```cpp nocheck
// A
int x = 5;
int *p = &x;
*p += 3;
cout << x;

// B
int *q;
*q = 10;

// C
int *r = new int(7);
r = new int(8);
delete r;

// D
int arr[3] = {1, 2, 3};
int *s = arr;
cout << *(s + 3);

// E
double *d = new double[10];
delete d;
```
---solution
- **A** prints `8`. `*p` is `x`, so adding 3 through the pointer changes `x`. Correct code.
- **B** is undefined behaviour: `q` is uninitialised, so `*q = 10` writes to a random address. Initialise pointers (`int *q = nullptr;`) and only dereference valid ones.
- **C** leaks memory. The first `new int(7)` is never deleted, because `r` was re-aimed before anyone freed it. Nothing points to it any more, so it can never be freed.
- **D** reads `arr[3]`, one past the end. Undefined behaviour.
- **E** uses `delete` on memory from `new[]`. It must be `delete[] d;`. Better: use `vector<double> d(10);` and no delete at all.
:::

:::quiz
? If `int x = 9; int *p = &x;`, what is `*p`?
- The address of x
* 9
- The address of p
- 0
> Dereferencing p gives the int it points to.

? What does `p->stock` mean?
- p minus stock
* (*p).stock
- &p.stock
- p.stock
> The arrow operator dereferences a pointer and selects a member.

? If p points to stock[0] in an int array, what does p + 2 point to?
- 2 bytes after stock[0]
* stock[2]
- The value stock[0] + 2
- Nothing; it does not compile
> Pointer arithmetic moves in whole elements.

? Which correctly frees `int *a = new int[50];`?
- delete a;
* delete[] a;
- free(a[50]);
- Nothing, it is automatic
> Memory from new[] must be released with delete[].

? Why does modern C++ prefer vector and unique_ptr over raw new and delete?
- They are always faster
* They free their memory automatically, preventing leaks and double deletes
- Raw pointers are not allowed any more
- They use the stack instead of the heap
> This is the RAII idea: cleanup happens when the owner goes out of scope.
:::

:::lab Pointer workout
1. Write `void minMaxPtr(const int *arr, int n, int *minOut, int *maxOut)` that finds the smallest and largest elements using **pointer arithmetic only** (no `[ ]`). Return the results through the two output pointers.
2. Write `int *findValue(int *arr, int n, int target)` that returns a pointer to the first element equal to `target`, or `nullptr` if there is none. In `main`, use the returned pointer to **change** that element to 0.
3. Ask the user how many prices they have, create a `vector<double>` of that size, fill it, and print the total. (Notice how much simpler this is than `new[]` and `delete[]`.)
---solution
```cpp run title=pointer_lab.cpp
#include <iostream>
#include <vector>
using namespace std;

void minMaxPtr(const int *arr, int n, int *minOut, int *maxOut) {
    *minOut = *arr;
    *maxOut = *arr;
    for (const int *p = arr + 1; p < arr + n; p++) {
        if (*p < *minOut) *minOut = *p;
        if (*p > *maxOut) *maxOut = *p;
    }
}

int *findValue(int *arr, int n, int target) {
    for (int *p = arr; p < arr + n; p++) {
        if (*p == target) return p;
    }
    return nullptr;
}

int main() {
    int stock[6] = {12, 40, 8, 25, 3, 40};
    int lo, hi;
    minMaxPtr(stock, 6, &lo, &hi);
    cout << "Min " << lo << ", max " << hi << endl;

    int *hit = findValue(stock, 6, 25);
    if (hit != nullptr) *hit = 0;
    for (int s : stock) cout << s << " ";
    cout << endl;

    int n;
    cout << "How many prices? ";
    cin >> n;
    vector<double> prices(n);
    double total = 0;
    for (double &p : prices) {
        cin >> p;
        total += p;
    }
    cout << "Total: " << total << endl;
    return 0;
}
```

```output
Min 3, max 40
12 40 8 0 3 40 
How many prices? [[3]]
[[230.5 690 145]]
Total: 1065.5
```
Note that `minMaxPtr` assumes `n` is at least 1. A safer version checks `n <= 0` first, because reading `*arr` from an empty array is undefined behaviour.
:::

:::bullets
- `&x` gives the **address** of `x`. A **pointer** (`int *p`) stores an address. `*p` **dereferences** it to reach the value.
- `&` and `*` mean different things in declarations and in expressions.
- Initialise every pointer. Use **`nullptr`** for "points to nothing", and check before dereferencing.
- References are simpler and cannot be null; pointers can be null and re-aimed. Prefer references for parameters.
- `p->member` is shorthand for `(*p).member`.
- An array name decays to a pointer to its first element. `p + 1` moves to the next **element**, and `arr[i]` means `*(arr + i)`.
- Stack memory is automatic; **heap** memory comes from `new` and must be released with `delete` (or `delete[]` for arrays).
- Watch for **leaks**, **dangling pointers** and **double deletes**.
- Modern C++ prefers **`vector`** and **smart pointers** (`unique_ptr`), which clean up automatically (**RAII**).
:::
