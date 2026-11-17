---
num: 10
title: References, Scope and Recursion
tagline: Functions that change things, variables that know their place, and functions that call themselves
learn: pass arguments by reference to change the caller's variables; write the classic swap function; use const references for efficiency and safety; understand local, global and static variables; explain the call stack; write and trace recursive functions
---

## The swap that would not swap

:::story
Dilshan: I wrote a function to swap two prices. It prints the right thing inside the function, but back in main, nothing has changed. I've checked it ten times!

Nuwan: Your function is working perfectly. It is swapping its own **copies**. The originals never left main.

Dilshan: So how do I give a function the originals?

Nuwan: You pass them **by reference**.
:::

## The problem with copies

Here is Dilshan's function. Pass by value (Chapter 9) gives the function copies:

```cpp run title=swap_value.cpp
#include <iostream>
using namespace std;

void swapValues(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
    cout << "Inside:  a = " << a << ", b = " << b << endl;
}

int main() {
    int x = 10, y = 20;
    swapValues(x, y);
    cout << "In main: x = " << x << ", y = " << y << endl;
    return 0;
}
```

```output
Inside:  a = 20, b = 10
In main: x = 10, y = 20
```

The copies `a` and `b` were swapped, and then thrown away when the function ended.

## Pass by reference

Add an `&` after the parameter's type, and the parameter becomes a **reference**: another name for the caller's actual variable. No copy is made.

```cpp run title=swap_ref.cpp
#include <iostream>
using namespace std;

void swapValues(int &a, int &b) {     //@ & makes a and b aliases for the caller's variables
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    int x = 10, y = 20;
    swapValues(x, y);
    cout << "x = " << x << ", y = " << y << endl;
    return 0;
}
```

```output
x = 20, y = 10
```

Think of a reference as a **nickname**. If your friends call you "Amy", then "Amy" and "Amaya" are the same person. Anything that happens to Amy happens to Amaya. Inside `swapValues`, `a` is a nickname for `x` and `b` is a nickname for `y`.

### Tracing the swap

| Step | a (is x) | b (is y) | temp | x in main | y in main |
|---|---|---|---|---|---|
| call `swapValues(x, y)` | 10 | 20 | | 10 | 20 |
| `int temp = a;` | 10 | 20 | 10 | 10 | 20 |
| `a = b;` | 20 | 20 | 10 | **20** | 20 |
| `b = temp;` | 20 | 10 | 10 | 20 | **10** |
| return | | | | 20 | 10 |

The columns for `a` and `x` are always identical, because they are the **same memory**.

:::brain
Why do we need `temp` at all? What would happen if the function just did `a = b; b = a;`?
---solution
After `a = b;`, both hold 20. The original value of `a` (10) is gone, so `b = a;` copies 20 back into `b`. Both end up as 20. `temp` keeps a safe copy of the first value before it is overwritten. (The standard library also has `std::swap(x, y)` in `<utility>`, which does this for you.)
:::

### Rules for references

- The `&` goes in the **parameter list only**. The call looks completely normal: `swapValues(x, y);`.
- The argument must be a **variable** (something with a memory location). `swapValues(10, 20);` does not compile, because you cannot have a nickname for the number 10.
- The spacing does not matter: `int &a`, `int& a` and `int & a` all mean the same thing.

## Getting several results out of one function

A `return` statement gives back one value. Reference parameters can act as extra **output** channels:

```cpp run title=minmax.cpp
#include <iostream>
using namespace std;

void splitMinutes(int totalMinutes, int &hours, int &minutes) {
    hours = totalMinutes / 60;
    minutes = totalMinutes % 60;
}

int main() {
    int h, m;
    splitMinutes(135, h, m);
    cout << "135 minutes = " << h << "h " << m << "m" << endl;
    return 0;
}
```

```output
135 minutes = 2h 15m
```

`totalMinutes` is an **input** (passed by value). `hours` and `minutes` are **outputs** (passed by reference).

## const references: no copy, no changes

Copying an `int` is cheap. Copying a long `string`, or the big collections you will meet in later chapters, costs time and memory. A **const reference** gives the function direct access without copying, and promises not to change the original:

```cpp run title=const_ref.cpp
#include <iostream>
#include <string>
using namespace std;

void printLabel(const string &name, double price) {
    cout << "[" << name << " - Rs. " << price << "]" << endl;
    // name = "x";   would not compile: name is read-only here
}

int main() {
    string item = "Basmati Rice 5kg Family Pack";
    printLabel(item, 2450);
    printLabel("Salt 1kg", 120);      //@ const references can bind to temporary values too
    return 0;
}
```

```output
[Basmati Rice 5kg Family Pack - Rs. 2450]
[Salt 1kg - Rs. 120]
```

### Choosing how to pass

| How | Syntax | Copy? | Can change the original? | Use it for |
|---|---|---|---|---|
| By value | `int qty` | Yes | No | Small types: `int`, `double`, `char`, `bool` |
| By reference | `int &qty` | No | **Yes** | When the function must change the caller's variable |
| By const reference | `const string &s` | No | No | Large types you only need to read: `string`, `vector`, structs |

:::industry
In professional C++ code, `const &` is everywhere: `void print(const vector<Product> &items)`. Reviewers will often ask "why is this string passed by value?" Build the habit now: **small types by value, big types by const reference, and plain references only when the function's job is to change something**.
:::

:::watch
A reference parameter can change the caller's data in ways that surprise people reading the call. `updateStock(qty);` gives no visual hint that `qty` might change. Use reference parameters deliberately, and choose function names that make the change obvious, such as `addToStock` or `resetCounter`.
:::

## Scope: where a variable lives

The **scope** of a variable is the part of the program where its name can be used.

### Local scope

A variable declared inside a block `{ }` is **local** to that block. It is created when execution reaches its declaration and destroyed at the closing brace. Function parameters are local to their function.

```cpp check
int total = 0;
for (int i = 0; i < 3; i++) {     // i exists only in the loop
    int square = i * i;           // square is re-created on every iteration
    total += square;
}
// i and square do not exist here; total does
```

### Global scope

A variable declared **outside all functions** is **global**. Every function in the file can see and change it.

```cpp run title=global.cpp
#include <iostream>
using namespace std;

int salesToday = 0;                 //@ global: visible everywhere below this line

void recordSale() {
    salesToday++;
}

int main() {
    recordSale();
    recordSale();
    recordSale();
    cout << "Sales today: " << salesToday << endl;
    return 0;
}
```

```output
Sales today: 3
```

It looks convenient. So why do experienced programmers avoid global variables?

- **Any function can change them**, so when the value is wrong, the bug could be anywhere in the program.
- **Functions become hard to reuse and test**, because they secretly depend on outside data that is not in their parameter list.
- **Names can clash** with local variables, as you will see next.

:::industry
Global **constants** are fine and common: `const double VAT_RATE = 0.18;` at the top of a file cannot be changed by anyone, so it causes none of the problems above. Global **variables** are a code smell. Pass data in through parameters and back out through return values or references.
:::

### Shadowing

A local variable with the same name as a global one **hides** (shadows) it:

```cpp run title=shadow.cpp
#include <iostream>
using namespace std;

int count = 100;          //@ global

int main() {
    int count = 5;        //@ local: shadows the global
    cout << count << endl;      //@ the local one
    cout << ::count << endl;    //@ :: with no name in front means "the global one"
    return 0;
}
```

```output
5
100
```

Shadowing is legal, but it confuses readers. Avoid reusing names this way.

### static local variables: a local that remembers

Normally a local variable is destroyed when its function returns. A **`static` local** variable is created only **once** and keeps its value between calls, but it is still only visible inside its function:

```cpp run title=static_local.cpp
#include <iostream>
using namespace std;

int nextReceiptNumber() {
    static int number = 1000;    //@ initialised only the first time
    number++;
    return number;
}

int main() {
    cout << nextReceiptNumber() << endl;
    cout << nextReceiptNumber() << endl;
    cout << nextReceiptNumber() << endl;
    return 0;
}
```

```output
1001
1002
1003
```

This gives you the memory of a global without letting the whole program touch it.

## The call stack

How does the computer keep track of which function is running, where to return to, and whose local variables are whose? It uses the **call stack**.

Every time a function is called, a **stack frame** is pushed onto the stack. The frame holds that call's parameters, local variables and the place to return to. When the function returns, its frame is popped off and its local variables vanish.

```cpp run title=stack.cpp
#include <iostream>
using namespace std;

int square(int n) {
    return n * n;                       //@ frame: square(n = 4)
}

int sumOfSquares(int a, int b) {
    return square(a) + square(b);       //@ frame: sumOfSquares(a = 3, b = 4)
}

int main() {
    cout << sumOfSquares(3, 4) << endl; //@ frame: main
    return 0;
}
```

```output
25
```

While `square(4)` is running, the stack looks like this, with the newest frame on top:

| Call stack (top is running now) |
|---|
| `square` : n = 4 |
| `sumOfSquares` : a = 3, b = 4 (waiting for square to return) |
| `main` (waiting for sumOfSquares to return) |

When you use a debugger later, the "call stack" window shows exactly this picture. It is the first place to look when a program crashes.

## Recursion: functions that call themselves

A **recursive** function calls **itself** to solve a smaller version of the same problem. It sounds like a magic trick, but you have already seen the idea in everyday life: "to climb 10 steps, climb 1 step, then climb the remaining 9 steps."

Every recursive function needs two parts:

1. A **base case**: a version of the problem so small that you can answer it directly, without recursion.
2. A **recursive case**: a step that makes the problem smaller and calls the function again.

### Factorial

The factorial of n, written n!, is n × (n − 1) × ... × 1. So 5! = 120. Notice that 5! = 5 × 4!. That is a recursive definition:

- 0! = 1 (base case)
- n! = n × (n − 1)! (recursive case)

```cpp run title=factorial.cpp
#include <iostream>
using namespace std;

long long factorial(int n) {
    if (n <= 1) {                  //@ base case: stop here
        return 1;
    }
    return n * factorial(n - 1);   //@ recursive case: a smaller problem
}

int main() {
    for (int i = 0; i <= 5; i++) {
        cout << i << "! = " << factorial(i) << endl;
    }
    cout << "20! = " << factorial(20) << endl;
    return 0;
}
```

```output
0! = 1
1! = 1
2! = 2
3! = 6
4! = 24
5! = 120
20! = 2432902008176640000
```

### Tracing recursion

Here is how `factorial(4)` unfolds. Each call waits for the one below it:

```text
factorial(4) = 4 * factorial(3)
                   factorial(3) = 3 * factorial(2)
                                      factorial(2) = 2 * factorial(1)
                                                         factorial(1) = 1   <- base case
                                      factorial(2) = 2 * 1 = 2
                   factorial(3) = 3 * 2 = 6
factorial(4) = 4 * 6 = 24
```

The calls go **down** until they hit the base case, then the answers come back **up**, one stack frame at a time.

:::watch
**A recursive function without a reachable base case never stops.** Each call adds a frame to the call stack until the stack runs out of space and the program crashes with a **stack overflow** (yes, that is where the famous website's name comes from). Always check: does every recursive call move closer to the base case?
:::

### More recursion

```cpp run title=recursion_more.cpp
#include <iostream>
using namespace std;

void countdown(int n) {
    if (n == 0) {
        cout << "Liftoff!" << endl;
        return;
    }
    cout << n << " ";
    countdown(n - 1);
}

int digitSum(int n) {
    if (n < 10) return n;                  //@ one digit: the sum is itself
    return n % 10 + digitSum(n / 10);
}

double power(double base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}

int main() {
    countdown(5);
    cout << digitSum(40721) << endl;
    cout << power(2, 10) << endl;
    return 0;
}
```

```output
5 4 3 2 1 Liftoff!
14
1024
```

:::nodumb
Q: Is recursion better than a loop?
A: Neither is always better. Anything you can do with recursion, you can do with a loop, and the loop version is often faster and uses less memory (no stack frames). Recursion shines when the problem is naturally recursive: exploring folders inside folders, family trees, mazes, and many sorting and searching algorithms such as **merge sort** and **quicksort**. You will meet those in later modules on data structures and algorithms.

Q: Why is the famous Fibonacci example slow?
A: The naive recursive version, `fib(n) = fib(n-1) + fib(n-2)`, calculates the same values again and again. `fib(40)` makes over 300 million calls. A simple loop computes it in 40 steps. Recursion is elegant, but you must think about how much work it does.
:::

:::sharpen Trace the mystery
What does `mystery(5)` return? Trace it with a table before you run it.

```cpp run title=mystery.cpp
#include <iostream>
using namespace std;

int mystery(int n) {
    if (n == 0) return 0;
    return n + mystery(n - 1);
}

int main() {
    cout << mystery(5) << endl;
    return 0;
}
```
---solution
```output
15
```
`mystery(5)` = 5 + mystery(4) = 5 + 4 + mystery(3) = ... = 5 + 4 + 3 + 2 + 1 + 0 = **15**. It adds the numbers from 1 to n. What happens if you call `mystery(-1)`? The base case `n == 0` is never reached, so it recurses until the stack overflows. A safer base case is `if (n <= 0) return 0;`.
:::

## Worked example: the mini banking simulator

Let's use pass by reference to build a small bank account program. `balance` lives in `main`, and the functions change it through references.

```cpp run title=bank.cpp
#include <iostream>
#include <iomanip>
using namespace std;

void deposit(double &balance, double amount) {
    balance += amount;
}

bool withdraw(double &balance, double amount) {
    if (amount > balance) {
        return false;                      //@ refuse: balance is left unchanged
    }
    balance -= amount;
    return true;
}

void showBalance(const double &balance) {
    cout << fixed << setprecision(2) << "Balance: Rs. " << balance << endl;
}

int main() {
    double balance = 5000;
    int choice;
    do {
        cout << "\n1. Deposit  2. Withdraw  3. Balance  0. Exit\nChoice: ";
        cin >> choice;
        double amount;
        switch (choice) {
            case 1:
                cout << "Amount: ";
                cin >> amount;
                deposit(balance, amount);
                showBalance(balance);
                break;
            case 2:
                cout << "Amount: ";
                cin >> amount;
                if (!withdraw(balance, amount)) {
                    cout << "Insufficient funds." << endl;
                }
                showBalance(balance);
                break;
            case 3:
                showBalance(balance);
                break;
            case 0:
                cout << "Goodbye." << endl;
                break;
            default:
                cout << "Invalid choice." << endl;
        }
    } while (choice != 0);
    return 0;
}
```

```output

1. Deposit  2. Withdraw  3. Balance  0. Exit
Choice: [[1]]
Amount: [[2500]]
Balance: Rs. 7500.00

1. Deposit  2. Withdraw  3. Balance  0. Exit
Choice: [[2]]
Amount: [[9000]]
Insufficient funds.
Balance: Rs. 7500.00

1. Deposit  2. Withdraw  3. Balance  0. Exit
Choice: [[0]]
Goodbye.
```

Notice `withdraw`: it **changes** the balance through a reference **and** returns a `bool` to say whether it worked. This "do it and report success" pattern is very common.

:::compiler
What does each program print? One of them does not compile.

**A**

```cpp run title=quizA.cpp
#include <iostream>
using namespace std;
void f(int &n) { n = n * 2; }
int main() {
    int a = 4;
    f(a);
    f(a);
    cout << a << endl;
    return 0;
}
```

**B**

```cpp error title=quizB.cpp
#include <iostream>
using namespace std;
void f(int &n) { n = n * 2; }
int main() {
    f(4);
    return 0;
}
```

**C**

```cpp run title=quizC.cpp
#include <iostream>
using namespace std;
int x = 1;
void g() { int x = 50; x++; }
int main() {
    g();
    cout << x << endl;
    return 0;
}
```
---solution
**A** prints `16`. `f` doubles the real `a` twice: 4, 8, 16.

```output
16
```

**B** does not compile. A non-const reference cannot bind to the literal 4, because there is no variable to change.

**C** prints `1`. Inside `g`, the local `x` shadows the global one, so only the local is changed.

```output
1
```
:::

:::quiz
? What does the & mean in `void update(int &stock)`?
- The address of stock is printed
* stock is a reference to the caller's variable
- stock is a constant
- stock is optional
> The parameter becomes another name for the argument; no copy is made.

? Which is the best way to pass a long string that a function only needs to read?
- string s
- string &s
* const string &s
- string *s
> A const reference avoids the copy and prevents accidental changes.

? What happens to a normal local variable when its function returns?
* It is destroyed
- It keeps its value for next time
- It becomes global
- It is saved to disk
> Local variables live in the function's stack frame, which is removed on return.

? What makes a `static` local variable different?
- It cannot be changed
- It is visible in every function
* It keeps its value between calls
- It is stored in a file
> It is initialised once and lives for the whole program, but its name is still local.

? Every recursive function needs...
- a loop
- a global variable
* a base case that stops the recursion
- at least two parameters
> Without a reachable base case, recursion continues until the stack overflows.
:::

:::lab The stock adjuster
1. Write `void addStock(int &stock, int amount)` and `bool removeStock(int &stock, int amount)`. `removeStock` must refuse (return false and leave the stock unchanged) if there is not enough stock, or if the amount is not positive.
2. Write `void stats(int a, int b, int c, int &smallest, int &largest, double &average)` that calculates all three results for three stock levels.
3. Write a recursive function `int countDigits(int n)` that returns how many digits a positive number has (`countDigits(4072)` is 4).
4. Test everything from `main`, including the refusal cases.
---solution
```cpp run title=stock_tools.cpp
#include <iostream>
using namespace std;

void addStock(int &stock, int amount) {
    if (amount > 0) stock += amount;
}

bool removeStock(int &stock, int amount) {
    if (amount <= 0 || amount > stock) return false;
    stock -= amount;
    return true;
}

void stats(int a, int b, int c, int &smallest, int &largest, double &average) {
    smallest = a;
    if (b < smallest) smallest = b;
    if (c < smallest) smallest = c;
    largest = a;
    if (b > largest) largest = b;
    if (c > largest) largest = c;
    average = (a + b + c) / 3.0;
}

int countDigits(int n) {
    if (n < 10) return 1;
    return 1 + countDigits(n / 10);
}

int main() {
    int rice = 20;
    addStock(rice, 15);
    cout << "Rice: " << rice << endl;
    cout << boolalpha << removeStock(rice, 50) << " " << rice << endl;
    cout << removeStock(rice, 5) << " " << rice << endl;

    int lo, hi;
    double avg;
    stats(12, 40, 8, lo, hi, avg);
    cout << lo << " " << hi << " " << avg << endl;

    cout << countDigits(4072) << " " << countDigits(7) << endl;
    return 0;
}
```

```output
Rice: 35
false 35
true 30
8 40 20
4 1
```
:::

:::bullets
- **Pass by value** copies the argument. **Pass by reference** (`int &x`) makes the parameter an alias for the caller's variable, so changes are visible outside.
- Use reference parameters for **swap** and for returning several results.
- Use **const references** (`const string &s`) to pass big objects cheaply and safely.
- **Local** variables live inside their block. **Global** variables are visible everywhere and are best avoided (global constants are fine).
- A local variable with the same name as a global one **shadows** it. `::name` reaches the global.
- A **static local** variable keeps its value between calls.
- Each function call gets a **stack frame** on the **call stack**.
- **Recursion** needs a **base case** and a recursive case that moves towards it. Missing base cases cause **stack overflow**.
:::
