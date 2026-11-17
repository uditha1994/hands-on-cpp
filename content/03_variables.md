---
num: 3
title: Variables, Data Types and Constants
tagline: Giving your data a home in memory
learn: understand what a variable really is inside memory; declare and initialise variables safely; choose the right data type for each job; know the limits of int, double and char; use const for values that must never change; name things like a professional
---

## Uncle Ruwan's memory problem

:::story
Ruwan: Rice is Rs. 230 a kilo this week. Last week it was 220. Next week, who knows. How will your program remember that?

Amaya: It needs a place to keep the price... a box with a label on it?

Nuwan: That is exactly what a **variable** is. A labelled box in the computer's memory. The label stays the same. What is inside the box can change.
:::

## What is a variable, really?

Your computer's memory (RAM) is like a huge set of numbered storage lockers. Each locker holds one **byte**, which is 8 **bits** (8 tiny on/off switches). Every byte has an **address**, a number that says where it is.

Working with raw addresses would be horrible. So C++ lets you give a chunk of memory a **name** and a **type**:

```cpp check
int quantity = 3;
```

This one line asks the compiler to:

1. reserve enough memory to hold a whole number (on most systems today, 4 bytes),
2. remember that this memory is called `quantity`,
3. store the value 3 in it.

| Name | Type | Value | Address (example) |
|---|---|---|---|
| `quantity` | `int` | 3 | `0x7ffd5e8c` |

You will never need to know the exact address. The compiler handles that. You just use the name. (In Chapter 15 you will peek at real addresses using pointers.)

:::brain
A variable has a **name**, a **type**, a **value** and an **address**. Which of these can change while the program runs? Which ones are fixed once the variable exists?
:::

## Declaring and initialising

**Declaring** a variable tells the compiler it exists and what type it has. **Initialising** it gives it its first value. You can do both at once, and you usually should.

```cpp check
int age;              //@ declared, but holds no meaningful value yet
age = 20;             //@ assigned a value later
int marks = 85;       //@ declared and initialised in one line
double price = 230.50;
char grade = 'A';
bool inStock = true;
string customer = "Fathima";  //@ needs <string>
```

You can declare several variables of the same type on one line:

```cpp check
int apples = 10, oranges = 5, mangoes = 0;
```

### Three ways to initialise

C++ has a few spellings for giving a starting value. You will see all of them in other people's code:

```cpp check
int a = 5;     //@ copy initialisation: the classic style
int b(5);      //@ direct initialisation
int c{5};      //@ brace initialisation (C++11 and later)
```

Brace initialisation has one big advantage: it refuses to silently lose data.

```cpp error title=narrowing.cpp
#include <iostream>
using namespace std;

int main() {
    int x = 7.9;    //@ compiles: x quietly becomes 7
    int y{7.9};     //@ error: narrowing conversion from double to int
    cout << x << " " << y << endl;
    return 0;
}
```

With `=`, the decimal part is thrown away without complaint. (g++ only warns if you also turn on `-Wconversion`.) With `{}`, g++ refuses to compile, because turning 7.9 into 7 loses information. That kind of protection is why many modern style guides prefer braces.

:::watch
**Never use a variable before giving it a value.** A local variable that is declared but not initialised contains whatever bits happened to be in that memory before. Using it is **undefined behaviour**, which means the C++ standard makes no promise at all about what happens. In practice you get a random-looking number, and your program gives different answers on different days.

```cpp error
int total;            // no value!
total = total + 230;  // total + 230 = ??? + 230
```

The fix is simple: `int total = 0;`. Make "initialise on declaration" a habit from today.
:::

## The fundamental data types

C++ is a **statically typed** language. Every variable has a type that is fixed when you write the code. The type tells the compiler how much memory to use and which operations make sense.

| Type | What it stores | Typical size | Example |
|---|---|---|---|
| `int` | Whole numbers | 4 bytes | `int qty = 12;` |
| `short` | Smaller whole numbers | 2 bytes | `short year = 2026;` |
| `long` | Larger whole numbers | 4 or 8 bytes (see below) | `long views = 3000000L;` |
| `long long` | Very large whole numbers | 8 bytes | `long long population = 22000000LL;` |
| `float` | Decimal numbers, about 7 significant digits | 4 bytes | `float weight = 2.5f;` |
| `double` | Decimal numbers, about 15 to 16 significant digits | 8 bytes | `double price = 230.50;` |
| `char` | One character | 1 byte | `char size = 'M';` |
| `bool` | `true` or `false` | 1 byte | `bool paid = false;` |
| `string` | Text (from the standard library) | varies | `string item = "Dhal";` |

:::watch
The C++ standard only guarantees **minimum** sizes. For example, an `int` must be at least 16 bits. The sizes in the table are what you will see on almost every modern desktop. One real difference: `long` is **8 bytes** on 64-bit Linux and macOS, but **4 bytes** on 64-bit Windows. If you need a guaranteed size, use `long long` (at least 64 bits) or the fixed-width types such as `int32_t` from `<cstdint>`.
:::

You can ask your own compiler with `sizeof`:

```cpp run title=sizes.cpp
#include <iostream>
using namespace std;

int main() {
    cout << "char:      " << sizeof(char) << " byte" << endl;
    cout << "bool:      " << sizeof(bool) << " byte" << endl;
    cout << "int:       " << sizeof(int) << " bytes" << endl;
    cout << "long long: " << sizeof(long long) << " bytes" << endl;
    cout << "double:    " << sizeof(double) << " bytes" << endl;
    return 0;
}
```

```output
char:      1 byte
bool:      1 byte
int:       4 bytes
long long: 8 bytes
double:    8 bytes
```

### Choosing a type: the quick guide

- Counting things (items, students, loops)? **`int`**
- Money, measurements, anything with decimals? **`double`**
- A single letter or symbol? **`char`**
- A yes/no answer? **`bool`**
- Names, words, sentences? **`string`**
- Really huge whole numbers, like phone numbers stored as numbers or world population? **`long long`**

:::nodumb
Q: Why not just use double for everything? It can hold whole numbers too.
A: Three reasons. Whole numbers in an `int` are always **exact**, while doubles can have tiny rounding errors (you will see this in a moment). Some operations, such as `%` (remainder) and array indexes, only work with integer types. And using `int` tells readers "this is a count", which makes the code easier to understand.

Q: Should a phone number be an int?
A: No. A phone number like `0771234567` starts with 0, which an `int` would drop, and you never do arithmetic on phone numbers. Store it as a `string`. The rule of thumb: if you would never add or multiply it, it is probably text. The same goes for NIC numbers and postal codes.
:::

## Whole numbers have limits

An `int` uses 32 bits, so it can only hold about four billion different values. Half are negative. The exact limits are in `<climits>`:

```cpp run title=limits.cpp
#include <iostream>
#include <climits>
using namespace std;

int main() {
    cout << "Smallest int: " << INT_MIN << endl;
    cout << "Largest int:  " << INT_MAX << endl;
    return 0;
}
```

```output
Smallest int: -2147483648
Largest int:  2147483647
```

What happens if you go past the largest value? This is called **overflow**.

:::watch
For **signed** types like `int`, overflow is **undefined behaviour** in C++. On most machines the value "wraps around" to a large negative number, but the compiler is allowed to assume overflow never happens, which can lead to strange results. Do not rely on it. If your values might get big, use `long long`.

For **unsigned** types, wrapping around is defined and guaranteed. `unsigned int` values cannot be negative. Taking 1 away from an unsigned 0 gives the largest unsigned value, 4294967295 on a typical system. That surprises people, so only use unsigned types when you have a clear reason.
:::

:::industry
Overflow bugs are not just exam questions. In 2014, the YouTube view counter for "Gangnam Style" approached the limit of a 32-bit signed integer, 2,147,483,647, and YouTube upgraded the counter to a 64-bit integer. Engineers think about the range of every number they store.
:::

## Decimal numbers are approximations

`float` and `double` store numbers in binary using a format called **floating point** (standardised as IEEE 754). Many decimal fractions cannot be represented exactly in binary, just as 1/3 cannot be written exactly in decimal (0.3333...). So the computer stores the closest value it can.

```cpp run title=precision.cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    float f = 0.1f;
    double d = 0.1;
    cout << setprecision(20);    //@ show 20 significant digits
    cout << "float:  " << f << endl;
    cout << "double: " << d << endl;
    return 0;
}
```

```output
float:  0.10000000149011611938
double: 0.10000000000000000555
```

Neither is exactly 0.1. The `double` is much closer, which is why **`double` is the default choice** for decimals. `float` is mainly used where memory is tight, such as in graphics and on small devices.

:::watch
Because of these tiny errors, **do not compare decimals with `==`**. For example, `0.1 + 0.2 == 0.3` is **false** in C++. Chapter 6 shows you the safe way to compare floating-point numbers.
:::

:::deep
Should a shop store money in `double`? For learning and small programs, yes. Real banking and accounting systems usually avoid floating point for money. A common trick is to store amounts in the smallest unit as an integer, for example **cents** in a `long long`, so Rs. 230.50 becomes 23050. Integers are exact, so the books always balance.
:::

## Characters are secretly numbers

A `char` holds one character, written in **single quotes**: `'A'`, `'7'`, `'?'`. Inside the computer, each character is stored as a small number. The common mapping is **ASCII**, where `'A'` is 65, `'B'` is 66, `'a'` is 97 and `'0'` is 48.

```cpp run title=chars.cpp
#include <iostream>
using namespace std;

int main() {
    char grade = 'A';
    cout << grade << endl;            //@ prints the character
    cout << int(grade) << endl;       //@ prints its code: 65
    char next = grade + 1;
    cout << next << endl;             //@ 66 is 'B'
    return 0;
}
```

```output
A
65
B
```

:::watch
`'A'` (single quotes) is a `char`. `"A"` (double quotes) is a string literal containing one character. They are different types. Writing `char c = "A";` is an error.
:::

## Booleans: true or false

A `bool` holds one of two values, `true` or `false`. You will use them constantly once you start making decisions in Chapter 6. By default, `cout` prints them as `1` and `0`. The `boolalpha` manipulator prints words instead:

```cpp run title=bools.cpp
#include <iostream>
using namespace std;

int main() {
    bool inStock = true;
    bool isClosed = false;
    cout << inStock << " " << isClosed << endl;
    cout << boolalpha << inStock << " " << isClosed << endl;
    return 0;
}
```

```output
1 0
true false
```

## Strings: text

`string` is not built into the core language the way `int` is. It comes from the C++ Standard Library, so include `<string>`. (Some compilers let you get away without it, because `<iostream>` happens to include it. Do not rely on that.)

```cpp run title=strings_intro.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string shop = "Ruwan Stores";
    string town = "Kandy";
    string sign = shop + ", " + town;   //@ + joins strings together
    cout << sign << endl;
    cout << "Length: " << sign.length() << endl;
    return 0;
}
```

```output
Ruwan Stores, Kandy
Length: 19
```

Strings can do a lot more. Chapter 12 is all about them.

## Constants: values that must not change

Some values should never change while the program runs: the number of days in a week, a tax rate, a shop's maximum discount. Mark them with `const`:

```cpp error title=const_demo.cpp
#include <iostream>
using namespace std;

int main() {
    const double VAT_RATE = 0.18;   //@ fixed for the whole program
    const int MAX_ITEMS = 50;
    VAT_RATE = 0.20;                //@ error: assignment of read-only variable
    cout << MAX_ITEMS << endl;
    return 0;
}
```

If any line tries to change a `const`, the compiler stops you. A bug that would have been silent becomes a compile-time error, which is exactly where you want it.

A `const` must be initialised when it is declared, because you cannot assign it later.

:::nodumb
Q: Is 0.18 the real VAT rate in Sri Lanka?
A: Tax rates change with government policy, so never trust a number in a textbook for real business use. That is actually the best argument for constants: when the rate changes, you update **one line**, not every place the number appears in your code.

Q: What about #define? I saw `#define PI 3.14` in a tutorial.
A: That is the old C way. `#define` is a blind text replacement done by the preprocessor, with no type and no scope. Modern C++ prefers `const` (or `constexpr`, a stronger version for values known at compile time). They are type-checked and safer.
:::

:::deep
`constexpr` means "this value is known at **compile time**". `constexpr double PI = 3.14159265358979;` lets the compiler calculate with it while compiling. For now, think of `constexpr` as a stricter `const` for fixed numbers. Both are good choices for your constants.
:::

## Let the compiler work out the type: auto

C++11 added `auto`, which tells the compiler to work out the type from the starting value:

```cpp check
auto count = 10;        // int
auto price = 230.50;    // double
auto letter = 'Z';      // char
auto ok = true;         // bool
```

`auto` is handy with long type names, which you will meet later with vectors. For simple variables, writing the type yourself is clearer while you are learning.

:::watch
`auto` must have an initial value, because the compiler needs something to look at. `auto total;` is an error. Also note that `auto name = "Amaya";` gives you a C-style character pointer, **not** a `string`. Write `string name = "Amaya";` when you want a string.
:::

## Naming variables like a professional

C++ has a few hard rules for names (identifiers):

- They may contain **letters, digits and underscores** only.
- They must **not start with a digit**. `2ndItem` is illegal, `item2` is fine.
- No spaces. `unit price` is illegal, `unitPrice` is fine.
- They must not be a **keyword**, such as `int`, `return`, `if`, `while` or `class`.
- They are **case sensitive**. `total`, `Total` and `TOTAL` are three different variables.

:::watch
Avoid names that start with an underscore followed by a capital letter, such as `_Total`, and names containing two underscores in a row, such as `my__var`. The C++ standard reserves those for the compiler and library writers.
:::

Beyond the rules, follow these **conventions**:

| Kind of name | Convention | Examples |
|---|---|---|
| Variables | `camelCase`: first word lowercase, then capitals | `unitPrice`, `itemCount`, `isMember` |
| Constants | `ALL_CAPS` with underscores | `MAX_ITEMS`, `VAT_RATE` |
| Loop counters | Short names are fine | `i`, `j`, `k` |
| Booleans | Read like a yes/no question | `isPaid`, `hasStock`, `canDeliver` |

Good names are the cheapest documentation in the world. Compare these:

```cpp nocheck
double t = p * q * 1.18;                        // what is t? p? q?
double totalWithVat = unitPrice * quantity * 1.18;  // obvious at a glance
```

:::sharpen Legal or not?
Which of these variable names are legal in C++? For the legal ones, are they **good** names?

`totalPrice`, `2price`, `total price`, `_count`, `int`, `customerName`, `x`, `discount%`, `MAX_DISCOUNT`, `itemCount2`
---solution
| Name | Legal? | Comment |
|---|---|---|
| `totalPrice` | Yes | Good camelCase name |
| `2price` | No | Starts with a digit |
| `total price` | No | Contains a space |
| `_count` | Yes | Legal, but leading underscores are best avoided |
| `int` | No | It is a keyword |
| `customerName` | Yes | Good name |
| `x` | Yes | Legal, but meaningless unless it really is an x coordinate |
| `discount%` | No | `%` is not allowed in names |
| `MAX_DISCOUNT` | Yes | Good name for a constant |
| `itemCount2` | Yes | Legal; digits are fine after the first character |
:::

## Putting it together: Ruwan Stores' product card

Amaya's first useful program stores one product's details in variables and prints a product card.

```cpp run title=product_card.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    const string SHOP_NAME = "Ruwan Stores";
    string itemName = "Red Rice (1 kg)";
    char category = 'G';          //@ G for groceries
    int stockLevel = 42;
    double unitPrice = 230.50;
    bool onPromotion = false;

    cout << "---- " << SHOP_NAME << " ----" << endl;
    cout << "Item:      " << itemName << endl;
    cout << "Category:  " << category << endl;
    cout << "In stock:  " << stockLevel << endl;
    cout << "Price:     Rs. " << unitPrice << endl;
    cout << "Promotion: " << boolalpha << onPromotion << endl;
    return 0;
}
```

```output
---- Ruwan Stores ----
Item:      Red Rice (1 kg)
Category:  G
In stock:  42
Price:     Rs. 230.5
Promotion: false
```

Notice that `230.50` printed as `230.5`. By default, `cout` drops trailing zeros. In the next chapter you will learn to print money properly, with exactly two decimal places.

:::compiler
Find every error in this program. There are five.

```cpp error
#include <iostream>
using namespace std;

int main() {
    int items = 5
    double price = 99.99;
    const int MAX = 10;
    string name = 'Kasun';
    MAX = 20;
    cout << Items * price << endl;
    return 0;
}
```
---solution
1. Line 5: `int items = 5` is missing its semicolon.
2. Line 8: `'Kasun'` uses single quotes. Strings need double quotes: `"Kasun"`.
3. Line 8 also uses `string` without `#include <string>`. Some compilers accept it, but you should include the header.
4. Line 9: `MAX = 20;` tries to change a `const`. The compiler reports an assignment of a read-only variable.
5. Line 10: `Items` has a capital I, but the variable is called `items`. C++ is case sensitive.
:::

:::quiz
? Which type is the best choice for storing a customer's mobile number such as 0771234567?
- int
- double
* string
- long
> Phone numbers can start with 0 and are never used in arithmetic, so they are text.

? What is printed by `cout << int('A');`?
- A
* 65
- 1
- It does not compile
> Characters are stored as numbers. In ASCII, 'A' is 65.

? What is wrong with `int total; total = total + 10;`?
- Nothing
- int cannot hold 10
* total was never initialised, so its starting value is unpredictable
- You must use double
> Reading an uninitialised local variable is undefined behaviour. Write `int total = 0;`.

? Which statement does NOT compile?
- `int a = 7.9;`
* `int b{7.9};`
- `double c = 7;`
- `int d(7);`
> Brace initialisation refuses narrowing conversions, such as double to int.

? Why is `double` usually preferred over `float`?
- It uses less memory
* It is much more precise
- It stores text as well
- It cannot be negative
> A double gives about 15 to 16 significant digits, against about 7 for a float.
:::

:::lab Your shop's product cards
1. Write a program that stores the details of **three** Ruwan Stores products (name, category letter, stock level, price, whether it is on promotion) in well-named variables, and prints a neat card for each.
2. Add a constant `LOW_STOCK_LIMIT` with the value 10. For now, just print it at the bottom: `Reorder when stock falls below 10`.
3. Use `sizeof` to print how many bytes each of your variables uses.
4. **Challenge:** store one price in a `float` and the same price in a `double`, then print both with `setprecision(20)` (from `<iomanip>`). What do you notice?
---solution
Here is one possible answer for parts 1 and 2. Your product names and values can be different.

```cpp run title=three_cards.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    const int LOW_STOCK_LIMIT = 10;

    string item1 = "Red Rice (1 kg)";
    char cat1 = 'G';
    int stock1 = 42;
    double price1 = 230.50;

    string item2 = "Coconut Oil (750 ml)";
    char cat2 = 'G';
    int stock2 = 8;
    double price2 = 690.00;

    string item3 = "Soap Bar";
    char cat3 = 'H';
    int stock3 = 25;
    double price3 = 145.00;

    cout << item1 << " [" << cat1 << "] stock " << stock1 << ", Rs. " << price1 << endl;
    cout << item2 << " [" << cat2 << "] stock " << stock2 << ", Rs. " << price2 << endl;
    cout << item3 << " [" << cat3 << "] stock " << stock3 << ", Rs. " << price3 << endl;
    cout << "Reorder when stock falls below " << LOW_STOCK_LIMIT << endl;
    return 0;
}
```

```output
Red Rice (1 kg) [G] stock 42, Rs. 230.5
Coconut Oil (750 ml) [G] stock 8, Rs. 690
Soap Bar [H] stock 25, Rs. 145
Reorder when stock falls below 10
```
Notice the repetition: three sets of nearly identical variables. That is a warning sign. In Chapters 11 and 14 you will learn **arrays** and **structs**, which store many products without copying the same lines again and again.

For part 4, the `float` value usually shows an error in the 7th or 8th significant digit, while the `double` stays accurate much further.
:::

:::bullets
- A **variable** is a named, typed piece of memory. Its value can change; its name and type cannot.
- **Always initialise** variables. Reading an uninitialised variable is undefined behaviour.
- Use `int` for counts, `double` for decimals, `char` for single characters, `bool` for yes/no and `string` for text.
- Sizes are **typical, not guaranteed**. Check with `sizeof`. `long` differs between Windows and Linux.
- Integers have **limits** (`INT_MAX` is 2147483647). Signed overflow is undefined behaviour.
- Floating-point numbers are **approximations**. Prefer `double`, and never compare decimals with `==`.
- `const` makes a value read-only, and the compiler enforces it. Name constants in `ALL_CAPS`.
- Brace initialisation `int x{5};` prevents silent narrowing.
- Use **meaningful camelCase names**. Names are documentation.
:::
