---
num: 9
title: Functions
tagline: Break big problems into small, named, reusable pieces
learn: explain why functions make programs better; write, declare and call your own functions; understand parameters, arguments and return values; choose between void and value-returning functions; use default arguments and overloading; design functions that do one job well
---

## The 400-line main

:::story
Amaya: My checkout program is now 400 lines long. All in `main`. When I scroll down to fix the receipt, I forget what the top does. And I have copied the "read a valid number" loop six times.

Nuwan: And when you find a bug in that loop?

Amaya: I have to fix it in six places. I fixed it in five.

Nuwan: Then it is time for **functions**. Give each job a name, write it once, and use it anywhere.
:::

## What is a function?

A **function** is a named block of code that does one specific job. You have already used plenty of them: `sqrt(16)`, `pow(2, 10)`, `getline(cin, name)`. Someone else wrote those; now you will write your own.

Functions give you four big benefits:

1. **No repetition.** Write the code once, call it many times. Fix a bug in one place. Programmers call this the **DRY principle**: Don't Repeat Yourself.
2. **Readability.** `printReceipt(total);` says what happens. Forty lines of `cout` do not.
3. **Divide and conquer.** A big problem becomes several small problems, each easy to think about.
4. **Testing.** You can test each function on its own before putting the whole program together.

:::brain
Think about the Ruwan Stores checkout. List five separate jobs it does, and give each job a short name starting with a verb (like `readQuantity`). Those names are your first functions.
:::

## Anatomy of a function

```cpp fn title=anatomy
double calculateTotal(double unitPrice, int qty) {   //@ return type, name, parameters
    double total = unitPrice * qty;                  //@ the body
    return total;                                    //@ send the answer back
}
```

| Part | In the example | Meaning |
|---|---|---|
| **Return type** | `double` | The type of value the function gives back |
| **Name** | `calculateTotal` | How you call it. Use a verb: functions *do* things |
| **Parameter list** | `(double unitPrice, int qty)` | The inputs the function needs, each with a type |
| **Body** | `{ ... }` | The statements that do the work |
| **return statement** | `return total;` | Ends the function and sends a value back to the caller |

The first line, `double calculateTotal(double unitPrice, int qty)`, is called the function's **header** or **signature**.

## Calling a function

```cpp run title=call.cpp
#include <iostream>
using namespace std;

double calculateTotal(double unitPrice, int qty) {
    double total = unitPrice * qty;
    return total;
}

int main() {
    double rice = calculateTotal(230.50, 4);      //@ call 1
    double oil = calculateTotal(690, 2);          //@ call 2
    cout << "Rice: " << rice << endl;
    cout << "Oil:  " << oil << endl;
    cout << "Both: " << rice + oil << endl;
    cout << "Soap: " << calculateTotal(145, 3) << endl;  //@ use the result directly
    return 0;
}
```

```output
Rice: 922
Oil:  1380
Both: 2302
Soap: 435
```

When the program reaches `calculateTotal(230.50, 4)`:

1. `main` **pauses**.
2. The values `230.50` and `4` are **copied** into the parameters `unitPrice` and `qty`.
3. The function body runs.
4. `return total;` sends 922 back, and the function ends.
5. `main` **resumes**, and the call is replaced by its result: `double rice = 922;`.

```flow
flowchart LR
  M1["main: rice = calculateTotal(230.50, 4)"] -- "copies 230.50 and 4" --> F["calculateTotal runs<br>total = 922"]
  F -- "returns 922" --> M2["main continues: rice = 922"]
```

### Parameters and arguments

These two words are often mixed up:

- A **parameter** is the variable in the function's header: `unitPrice`, `qty`.
- An **argument** is the actual value passed in a call: `230.50`, `4`.

Arguments are matched to parameters **by position**, not by name. The first argument goes to the first parameter, and so on. The number and types must match (or be convertible).

:::watch
Getting the order of arguments wrong is a logic error the compiler may not catch. `calculateTotal(4, 230.50)` compiles, because 4 converts to a double and 230.50 converts to an int (becoming 230, possibly with a warning). The result is 920 instead of 922. Read function headers carefully.
:::

## void functions: doing without returning

Some functions perform an action but have no answer to give back. Their return type is `void`:

```cpp run title=void_demo.cpp
#include <iostream>
#include <string>
using namespace std;

void printLine(int width) {
    for (int i = 0; i < width; i++) {
        cout << "=";
    }
    cout << endl;
}

void printHeader(string shopName) {
    printLine(30);                     //@ functions can call other functions
    cout << "  " << shopName << endl;
    printLine(30);
}

int main() {
    printHeader("RUWAN STORES, KANDY");
    cout << "Thank you for shopping!" << endl;
    printLine(30);
    return 0;
}
```

```output
==============================
  RUWAN STORES, KANDY
==============================
Thank you for shopping!
==============================
```

A `void` function can use `return;` (with no value) to finish early, but it does not have to.

:::watch
You cannot use the result of a `void` function, because there is none. `int x = printLine(30);` is a compile error. And a function that promises a value must return one on **every** path. If a non-void function reaches its closing brace without a `return`, it is undefined behaviour. `-Wall` warns: *control reaches end of non-void function*.
:::

### Which kind should I write?

| Ask yourself | Write |
|---|---|
| Does the caller need an answer back? (a total, a grade, true/false) | a **value-returning** function |
| Does it just do something? (print, save, beep) | a **void** function |

A good rule: functions that **calculate** should usually **return** the result and let the caller decide whether to print it. A function that both calculates and prints is harder to reuse. What if next time you want to save the total to a file instead?

## Declare before use: prototypes

C++ reads your file from top to bottom. If `main` calls a function that is defined **below** it, the compiler has not seen it yet:

```cpp error title=order.cpp
#include <iostream>
using namespace std;

int main() {
    cout << square(5) << endl;     //@ error: 'square' was not declared in this scope
    return 0;
}

int square(int n) {
    return n * n;
}
```

You can fix this in two ways. Either define every function **above** `main`, or put a **prototype** (a declaration) at the top. A prototype is the function's header followed by a semicolon:

```cpp run title=prototype.cpp
#include <iostream>
using namespace std;

int square(int n);                 //@ prototype: "this function exists, trust me"

int main() {
    cout << square(5) << endl;
    return 0;
}

int square(int n) {                //@ definition: the actual code
    return n * n;
}
```

```output
25
```

Many programmers like this layout: prototypes at the top as a "table of contents", then `main`, then the details. In Chapter 17, prototypes move into **header files**, and this is exactly how large projects are organised.

:::nodumb
Q: Do parameter names in the prototype have to match the definition?
A: No. The compiler only cares about the types, so `int square(int);` is a legal prototype. But including good names makes the prototype more useful as documentation.

Q: Can a function return two values?
A: A `return` statement returns one value. To get more than one result out of a function, you can use reference parameters (Chapter 10) or return a struct that bundles several values together (Chapter 14).
:::

## Pass by value: functions get copies

By default, C++ passes arguments **by value**: the parameter is a **copy** of the argument. Changing the copy inside the function does not touch the original.

```cpp run title=by_value.cpp
#include <iostream>
using namespace std;

void addBonus(int points) {
    points += 100;                                     //@ changes the copy only
    cout << "Inside the function: " << points << endl;
}

int main() {
    int myPoints = 250;
    addBonus(myPoints);
    cout << "Back in main:        " << myPoints << endl;   //@ still 250
    return 0;
}
```

```output
Inside the function: 350
Back in main:        250
```

This is usually exactly what you want, because a function cannot accidentally change your data. When you **do** want a function to change the caller's variable, you need pass by reference, which is the main topic of Chapter 10.

## Local variables

Variables declared inside a function, including its parameters, are **local** to that function. They are created when the function is called and destroyed when it returns. Two functions can each have a variable called `total`, and they are completely separate.

```cpp run title=locals.cpp
#include <iostream>
using namespace std;

int doubleIt(int x) {
    int result = x * 2;        //@ this result belongs to doubleIt
    return result;
}

int main() {
    int result = 7;            //@ a different variable that happens to share the name
    cout << doubleIt(result) << " " << result << endl;
    return 0;
}
```

```output
14 7
```

## Functions that answer questions: returning bool

Functions that return `bool` make conditions read like English. Name them as questions:

```cpp run title=bool_functions.cpp
#include <iostream>
using namespace std;

bool isLeapYear(int year) {
    return (year % 4 == 0 && year % 100 != 0) || year % 400 == 0;
}

bool isValidMark(int mark) {
    return mark >= 0 && mark <= 100;
}

int main() {
    for (int y = 2023; y <= 2028; y++) {
        if (isLeapYear(y)) {
            cout << y << " is a leap year" << endl;
        }
    }
    cout << boolalpha << isValidMark(105) << endl;
    return 0;
}
```

```output
2024 is a leap year
2028 is a leap year
false
```

Notice `return condition;` instead of `if (condition) return true; else return false;`. The condition already **is** a bool.

### Returning early

A function can have several `return` statements. The first one that runs ends the function. This is great for guard clauses:

```cpp fn
char gradeFor(int mark) {
    if (mark < 0 || mark > 100) return '?';    // guard
    if (mark >= 75) return 'A';
    if (mark >= 65) return 'B';
    if (mark >= 55) return 'C';
    if (mark >= 35) return 'S';
    return 'F';
}
```

No `else` is needed: once a `return` runs, nothing after it in the function happens.

## Default arguments

You can give parameters **default values**. If the caller leaves that argument out, the default is used:

```cpp run title=defaults.cpp
#include <iostream>
using namespace std;

void printLine(int width = 30, char symbol = '=') {
    for (int i = 0; i < width; i++) cout << symbol;
    cout << endl;
}

int main() {
    printLine();            //@ width 30, symbol '='
    printLine(10);          //@ width 10, symbol '='
    printLine(10, '-');     //@ width 10, symbol '-'
    return 0;
}
```

```output
==============================
==========
----------
```

:::watch
Default parameters must come **at the end** of the parameter list. `void f(int a = 1, int b);` is an error. Also, if you use a prototype, put the defaults in the **prototype only**, not in the definition as well.
:::

## Overloading: same name, different parameters

C++ lets several functions share a name as long as their **parameter lists differ** (in number or types). This is called **function overloading**. The compiler chooses the right one from the arguments you pass.

```cpp run title=overload.cpp
#include <iostream>
#include <string>
using namespace std;

double area(double side) {                  //@ a square
    return side * side;
}
double area(double width, double height) {  //@ a rectangle
    return width * height;
}
void show(int n)    { cout << "int: " << n << endl; }
void show(double d) { cout << "double: " << d << endl; }
void show(string s) { cout << "string: " << s << endl; }

int main() {
    cout << area(4) << " " << area(4, 2.5) << endl;
    show(7);
    show(7.5);
    show(string("seven"));
    return 0;
}
```

```output
16 10
int: 7
double: 7.5
string: seven
```

:::watch
You **cannot** overload on return type alone. `int read();` and `double read();` cannot both exist, because a call like `read();` gives the compiler no way to choose. The parameter lists must be different.
:::

## Worked example: the grade report, refactored

Here is a program that reads marks for several students and prints a report. Look at how `main` reads almost like a summary of the program, because the details live in functions.

```cpp run title=grade_report.cpp
#include <iostream>
#include <iomanip>
#include <limits>
using namespace std;

int readMark(int studentNo);
char gradeFor(int mark);
void printRow(int studentNo, int mark);

int main() {
    const int STUDENTS = 3;
    int total = 0;
    cout << "No.  Mark  Grade" << endl;
    for (int s = 1; s <= STUDENTS; s++) {
        int mark = readMark(s);
        printRow(s, mark);
        total += mark;
    }
    cout << fixed << setprecision(1);
    cout << "Class average: " << static_cast<double>(total) / STUDENTS << endl;
    return 0;
}

// Ask until a whole number from 0 to 100 is entered.
int readMark(int studentNo) {
    int mark;
    while (true) {
        cout << "Mark for student " << studentNo << ": ";
        cin >> mark;
        if (!cin) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        } else if (mark >= 0 && mark <= 100) {
            return mark;                   //@ return also leaves the loop
        }
        cout << "Please enter 0 to 100." << endl;
    }
}

char gradeFor(int mark) {
    if (mark >= 75) return 'A';
    if (mark >= 65) return 'B';
    if (mark >= 55) return 'C';
    if (mark >= 35) return 'S';
    return 'F';
}

void printRow(int studentNo, int mark) {
    cout << setw(3) << studentNo << setw(6) << mark << setw(7) << gradeFor(mark) << endl;
}
```

```output
No.  Mark  Grade
Mark for student 1: [[82]]
  1    82      A
Mark for student 2: [[105]]
Please enter 0 to 100.
Mark for student 2: [[47]]
  2    47      S
Mark for student 3: [[66]]
  3    66      B
Class average: 65.0
```

The validation loop that was copied six times in Amaya's old program now lives in **one** place: `readMark`.

## Designing good functions

:::industry
Professional developers follow a few simple guidelines:

- **Single responsibility.** A function should do **one** job. If you need the word "and" to describe it ("reads the price **and** calculates tax **and** prints the bill"), split it up.
- **Short.** If a function does not fit on one screen, it is probably doing too much.
- **Verb names.** `calculateTax`, `printReceipt`, `isValidPin`. A reader should guess what it does without looking inside.
- **Few parameters.** More than four or five parameters is a warning sign. Chapter 14 shows how to group related data into a struct.
- **No surprises.** A function called `calculateTotal` should not secretly print things or change global data.
:::

A short comment above a function, saying **what** it does (not how), what it expects and what it returns, helps everyone who uses it:

```cpp fn
// Returns the delivery charge in rupees for an order.
// Orders of Rs. 5000 or more are delivered free within 5 km.
// distanceKm must not be negative.
double deliveryCharge(double orderValue, double distanceKm) {
    if (orderValue >= 5000 && distanceKm <= 5) return 0;
    return 150 + distanceKm * 40;
}
```

:::compiler
Find the problems in these functions.

```cpp error
int addTax(double amount) {
    double taxed = amount * 1.18;
    return taxed;
}

void greet(string name) {
    return "Hello, " + name;
}

int maxOf(int a, int b) {
    if (a > b) {
        return a;
    }
}

double average(int a, int b);
double average(int x, int y) { return (x + y) / 2; }
```
---solution
1. `addTax` returns `int`, so the double result is **truncated**: 100 becomes 118, but 99.99 becomes 117 instead of 117.99. The return type should be `double`.
2. `greet` is `void`, so it cannot return a value. Either make it return `string`, or print the greeting inside.
3. `maxOf` has no `return` when `a <= b`. That is undefined behaviour; add `return b;` at the end.
4. `average` compiles (parameter names may differ between prototype and definition), but `(x + y) / 2` is **integer division**. It should be `(x + y) / 2.0`.
:::

:::magnets
Rebuild this program, which uses a function to find the cube of a number.
~~~
#include <iostream>
using namespace std;
int cube(int n) {
return n * n * n;
}
int main() {
int x;
cin >> x;
cout << cube(x) << endl;
return 0;
}
~~~
:::

:::quiz
? In `double area(double w, double h)`, what are w and h?
- Arguments
* Parameters
- Return values
- Prototypes
> Parameters are the variables in the header. Arguments are the values passed in a call.

? What is printed? `void f(int x) { x = 10; }` ... `int a = 5; f(a); cout << a;`
* 5
- 10
- 0
- It does not compile
> Pass by value gives f a copy. The original a is unchanged.

? Which is a valid prototype for `int maxOf(int a, int b) { ... }`?
- `maxOf(int a, int b);`
* `int maxOf(int, int);`
- `int maxOf(a, b);`
- `int maxOf(int a, int b)`
> A prototype needs the return type, name and parameter types, ending with a semicolon.

? Which pair of functions can NOT be overloaded?
- `void p(int)` and `void p(double)`
- `void p(int)` and `void p(int, int)`
* `int p(int)` and `double p(int)`
- `void p(string)` and `void p(char)`
> Functions cannot differ only in their return type.

? What does `printLine(5)` use for symbol, given `void printLine(int width = 30, char symbol = '*')`?
- Nothing; it is an error
* '*'
- '5'
- '='
> Only width was supplied, so symbol takes its default.
:::

:::lab Ruwan Stores toolkit
Write these functions, then a `main` that tests each one with at least three calls, including edge cases:

1. `double applyDiscount(double amount, double percent)` returns the amount after the discount.
2. `bool isValidPrice(double price)` returns true for prices greater than 0 and at most 1,000,000.
3. `double readPositiveDouble(string prompt)` keeps asking (using the prompt) until the user types a positive number, then returns it.
4. `void printMoneyRow(string label, double amount)` prints the label left-aligned in 15 characters and the amount right-aligned in 12 characters, with two decimal places.
5. Use them all in a program that reads one bill amount and a discount percentage and prints a neat summary.
---solution
```cpp run title=toolkit.cpp
#include <iostream>
#include <iomanip>
#include <string>
#include <limits>
using namespace std;

double applyDiscount(double amount, double percent) {
    return amount - amount * percent / 100.0;
}

bool isValidPrice(double price) {
    return price > 0 && price <= 1000000;
}

double readPositiveDouble(string prompt) {
    double value;
    while (true) {
        cout << prompt;
        cin >> value;
        if (!cin) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        } else if (value > 0) {
            return value;
        }
        cout << "Please enter a positive number." << endl;
    }
}

void printMoneyRow(string label, double amount) {
    cout << fixed << setprecision(2);
    cout << left << setw(15) << label << right << setw(12) << amount << endl;
}

int main() {
    double bill = readPositiveDouble("Bill amount: ");
    if (!isValidPrice(bill)) {
        cout << "That bill looks wrong." << endl;
        return 1;
    }
    double pct = readPositiveDouble("Discount %: ");
    double pay = applyDiscount(bill, pct);
    printMoneyRow("Bill", bill);
    printMoneyRow("Discount", bill - pay);
    printMoneyRow("To pay", pay);
    return 0;
}
```

```output
Bill amount: [[-50]]
Please enter a positive number.
Bill amount: [[4500]]
Discount %: [[10]]
Bill                4500.00
Discount             450.00
To pay              4050.00
```
Good test cases for `applyDiscount`: 0%, 100%, and 12.5%. For `isValidPrice`: 0, 0.01, 1000000 and 1000000.01. Testing just around each limit is called **boundary value testing**.
:::

:::bullets
- A **function** is a named, reusable block that does one job. Functions remove repetition (DRY) and make code readable.
- A function has a **return type, name, parameter list and body**. Use verb names.
- **Parameters** are the variables in the header; **arguments** are the values passed in the call. They match by position.
- `return value;` ends the function and sends the value back. A `void` function returns nothing.
- Define functions above `main`, or declare them first with a **prototype** ending in `;`.
- By default, arguments are **passed by value**: the function works on a copy.
- Local variables exist only while their function runs.
- **Default arguments** go at the end of the parameter list. **Overloaded** functions share a name but differ in their parameters.
- Give each function a **single responsibility**. Prefer returning results over printing them.
:::
