---
num: 5
title: Operators and Expressions
tagline: Making the computer do the maths, correctly
learn: use the five arithmetic operators; master integer division and the modulus operator; predict the result of any expression using precedence and associativity; write compact code with compound assignment and increment operators; convert between types safely with static_cast; use the cmath library
---

## The bill that was wrong

:::story
Ruwan: Your program says 5 kilos of sugar shared between 2 customers is 2 kilos each. Where did the other kilo go?

Amaya: What? 5 divided by 2 is 2.5!

Nuwan: Not in C++. Not when both numbers are integers. Welcome to the most famous trap in beginner programming. Sit down, this chapter will save you a lot of embarrassment.
:::

## Expressions, operators and operands

An **expression** is anything that produces a value: `5`, `price`, `price * qty`, `(a + b) / 2`. An **operator** is a symbol that does something to values, and the values it works on are called **operands**.

In `price * qty`, the operator is `*` and the operands are `price` and `qty`.

## The five arithmetic operators

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | Addition | `7 + 2` | `9` |
| `-` | Subtraction | `7 - 2` | `5` |
| `*` | Multiplication | `7 * 2` | `14` |
| `/` | Division | `7 / 2` | `3` (both are ints!) |
| `%` | Remainder (modulus) | `7 % 2` | `1` |

The first three behave the way you expect. The last two need careful attention.

## The integer division trap

When **both** operands of `/` are integers, C++ performs **integer division**: it divides and then **throws away** the fractional part. It does not round. It truncates toward zero.

```cpp run title=int_division.cpp
#include <iostream>
using namespace std;

int main() {
    cout << 7 / 2 << endl;      //@ int / int gives int: 3
    cout << 7.0 / 2 << endl;    //@ double / int gives double: 3.5
    cout << 7 / 2.0 << endl;    //@ int / double gives double: 3.5
    cout << 1 / 3 << endl;      //@ 0, not 0.333...
    cout << -7 / 2 << endl;     //@ truncates toward zero: -3
    return 0;
}
```

```output
3
3.5
3.5
0
-3
```

The rule: **if either operand is a floating-point type, the division is done in floating point.** Only when both are integers do you get integer division.

:::watch
This line looks fine but contains a nasty bug:

```cpp check
int total = 487;
int count = 5;
double average = total / count;   // 97, not 97.4!
```

Storing the result in a `double` does **not** help. The division `total / count` is done first, as integer division, giving 97. Only **then** is 97 converted to 97.0 and stored. By the time the `double` gets involved, the decimal part is already gone.
:::

## Converting types: casting

To get a real division from two integers, convert one of them to `double` **before** dividing. This is called a **cast**.

```cpp run title=casting.cpp
#include <iostream>
using namespace std;

int main() {
    int total = 487, count = 5;
    double a = total / count;                          //@ wrong: 97
    double b = static_cast<double>(total) / count;     //@ right: 97.4
    double c = static_cast<double>(total / count);     //@ still wrong: cast happens too late
    double d = (double)total / count;                  //@ C-style cast: works, but older style
    cout << a << " " << b << " " << c << " " << d << endl;
    return 0;
}
```

```output
97 97.4 97 97.4
```

`static_cast<type>(value)` is the modern C++ way to convert a value. It is easy to search for in code and the compiler checks it more strictly. The older C-style cast `(double)total` works too, and you will see it in older code and exam papers.

:::brain
Look at line `c` again. The cast is there, so why is the answer still wrong? Think about **what** is being cast.
:::

### Automatic conversions

C++ also converts types on its own, which is called **implicit conversion**:

- In mixed arithmetic, the "smaller" type is **promoted**: `int + double` becomes `double + double`.
- When you store a value in a variable, it is converted to the variable's type. Storing a `double` in an `int` **truncates** it: `int x = 9.99;` makes `x` equal to 9.
- `char` and `bool` are promoted to `int` in arithmetic. `true` becomes 1, `false` becomes 0, and `'A' + 1` is 66.

:::nodumb
Q: Why does C++ do integer division at all? It seems like a trap.
A: Because it is genuinely useful. "How many full boxes of 12 can I fill with 100 eggs?" is `100 / 12`, which is 8. Integer division is fast and exact, and it is exactly what you need for counting whole things. The trap is only forgetting which kind you are getting.

Q: What happens if I divide by zero?
A: For integers, dividing by zero is **undefined behaviour**. Usually the program crashes immediately. For doubles, the IEEE 754 rules apply: `1.0 / 0.0` gives `inf` (infinity) and `0.0 / 0.0` gives `nan` (not a number). Either way, the answer is useless, so check that a divisor is not zero before you divide. You will learn how with `if` in Chapter 7.
:::

## The modulus operator: %

`%` gives the **remainder** after integer division. It only works with integer types.

| Expression | Integer division | Remainder (`%`) |
|---|---|---|
| `17 / 5` and `17 % 5` | 3 | 2 (because 17 = 3 × 5 + 2) |
| `20 / 4` and `20 % 4` | 5 | 0 |
| `3 / 8` and `3 % 8` | 0 | 3 |

It may look like a strange operator, but it is one of the most useful tools you have:

- **Even or odd?** `n % 2` is 0 for even numbers and 1 for odd positive numbers.
- **Divisible by k?** `n % k == 0`.
- **The last digit of a number:** `n % 10`. (`1234 % 10` is 4.)
- **Remove the last digit:** `n / 10`. (`1234 / 10` is 123.)
- **Wrap around:** `(day + 1) % 7` cycles 0, 1, 2, ..., 6, 0, 1, ...
- **Split units:** seconds into minutes and seconds, cents into rupees and cents.

```cpp run title=time_split.cpp
#include <iostream>
using namespace std;

int main() {
    int totalSeconds;
    cout << "Seconds: ";
    cin >> totalSeconds;
    int hours = totalSeconds / 3600;
    int minutes = (totalSeconds % 3600) / 60;
    int seconds = totalSeconds % 60;
    cout << hours << "h " << minutes << "m " << seconds << "s" << endl;
    return 0;
}
```

```output
Seconds: [[7385]]
2h 3m 5s
```

:::watch
With negative numbers, the result of `%` takes the **sign of the left operand** (the rule has been fixed since C++11). So `-7 % 3` is `-1`, and `7 % -3` is `1`. This means `n % 2 == 1` is **false** for negative odd numbers like -3, because `-3 % 2` is -1. To test for odd numbers safely, use `n % 2 != 0`.
:::

:::sharpen Digit detective
Without running it, work out what this prints when the user enters 4072.

```cpp run title=digits.cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int last = n % 10;
    int rest = n / 10;
    int secondLast = rest % 10;
    int sumOfLastTwo = last + secondLast;
    cout << last << " " << secondLast << " " << sumOfLastTwo << endl;
    return 0;
}
```
---solution
```output
[[4072]]
2 7 9
```
`4072 % 10` is 2. `4072 / 10` is 407, and `407 % 10` is 7. 2 + 7 is 9. Peeling digits off with `% 10` and `/ 10` is a classic technique. In Chapter 8 you will put it in a loop to add up **all** the digits of any number.
:::

## Who goes first? Precedence

What is `10 + 5 * 2 - 6 / 3`? You probably remember from school that multiplication and division come before addition and subtraction. C++ follows the same idea. Each operator has a **precedence** level, and higher precedence operators are evaluated first.

| Precedence (high to low) | Operators | Associativity |
|---|---|---|
| 1 | `()` parentheses | (innermost first) |
| 2 | `++` `--` (postfix) | left to right |
| 3 | `++` `--` (prefix), unary `-`, `!`, casts | right to left |
| 4 | `*` `/` `%` | left to right |
| 5 | `+` `-` | left to right |
| 6 | `<` `<=` `>` `>=` | left to right |
| 7 | `==` `!=` | left to right |
| 8 | `&&` | left to right |
| 9 | `\|\|` | left to right |
| 10 | `=` `+=` `-=` `*=` `/=` `%=` | right to left |

(This is a simplified version of the full table. Appendix A has the complete version for every operator in this book.)

Step by step:

```text
10 + 5 * 2 - 6 / 3
10 + 10    - 2        (* and / first, left to right)
20         - 2        (then + and -, left to right)
18
```

### Associativity: breaking ties

When two operators have the **same** precedence, **associativity** decides. Most arithmetic operators are **left to right**:

- `20 / 4 * 2` is `(20 / 4) * 2`, which is `5 * 2` = **10**, not `20 / 8`.
- `100 - 30 - 20` is `(100 - 30) - 20` = **50**, not `100 - 10`.

Assignment is **right to left**: `a = b = 0;` means `a = (b = 0);`, so both become 0.

:::brain
What is `9 / 2 * 2.0`? And `2.0 * 9 / 2`? Same numbers, same operators, different order. Work both out carefully, remembering integer division. Then check with a compiler.
---solution
`9 / 2 * 2.0` is `(9 / 2) * 2.0`. `9 / 2` is integer division, giving 4, so the result is **8**. `2.0 * 9 / 2` is `(2.0 * 9) / 2` = `18.0 / 2` = **9**. Order of evaluation changes whether integer division happens at all.
:::

### Use parentheses on purpose

Even when you know the precedence rules, **add parentheses when they make your intent clearer**. They cost nothing and prevent misunderstandings.

```cpp check
double price = 1000, discountRate = 0.1, vatRate = 0.18;
double a = price - price * discountRate + price * vatRate;          // legal but hard to read
double b = (price - price * discountRate) * (1 + vatRate);          // different formula!
double c = price - (price * discountRate) + (price * vatRate);      // same as a, but clearer
```

Notice that `a` and `b` are **different calculations**. `b` charges VAT on the discounted price; `a` charges it on the original price. Parentheses are how you tell the computer which one you mean.

:::sharpen Precedence puzzle
Evaluate each expression. Assume `int a = 6, b = 4;` and remember integer division.

1. `a + b * 2`
2. `(a + b) * 2`
3. `a / b * b`
4. `a % b + a / b`
5. `a - b - 1`
6. `2 + 3 * a % 4`
---solution
1. `a + b * 2` = 6 + 8 = **14**
2. `(a + b) * 2` = 10 × 2 = **20**
3. `a / b * b` = (6 / 4) × 4 = 1 × 4 = **4**. Integer division loses the remainder, so this is not 6.
4. `a % b + a / b` = 2 + 1 = **3**
5. `a - b - 1` = (6 − 4) − 1 = **1**
6. `2 + 3 * a % 4`: `*` and `%` have equal precedence, left to right, so (3 × 6) % 4 = 18 % 4 = 2, then 2 + 2 = **4**.
:::

## Assignment and compound assignment

`=` is the **assignment operator**. It is **not** "equals" in the maths sense. It means: *evaluate the right side, then store the result in the variable on the left.*

That is why this makes perfect sense in C++ but no sense in maths:

```cpp check
int stock = 40;
stock = stock - 3;   // take the current value (40), subtract 3, store 37
```

Updating a variable using its own value is so common that C++ has shortcuts, called **compound assignment operators**:

| Long form | Short form | Meaning |
|---|---|---|
| `x = x + 5;` | `x += 5;` | add 5 to x |
| `x = x - 5;` | `x -= 5;` | subtract 5 from x |
| `x = x * 5;` | `x *= 5;` | multiply x by 5 |
| `x = x / 5;` | `x /= 5;` | divide x by 5 |
| `x = x % 5;` | `x %= 5;` | replace x with x % 5 |

```cpp run title=compound.cpp
#include <iostream>
using namespace std;

int main() {
    double balance = 1000;
    balance += 250;      //@ deposit
    balance -= 100;      //@ withdraw
    balance *= 1.05;     //@ add 5% interest
    cout << balance << endl;
    return 0;
}
```

```output
1207.5
```

:::watch
`x =+ 5;` is **not** `x += 5;`. It is parsed as `x = +5;`, which simply sets x to 5. The compiler accepts it silently. Always write the operator first, then the `=`.
:::

## Increment and decrement: ++ and --

Adding or subtracting exactly 1 is so common that it has its own operators. `count++` adds 1 to `count`; `count--` subtracts 1.

They come in two forms, and the difference matters **only when you use the value in the same expression**:

- **Prefix** `++x`: increase x first, then use the **new** value.
- **Postfix** `x++`: use the **old** value, then increase x.

```cpp run title=increment.cpp
#include <iostream>
using namespace std;

int main() {
    int a = 5;
    int b = a++;    //@ b gets the old value 5, then a becomes 6
    cout << "a = " << a << ", b = " << b << endl;

    int c = 5;
    int d = ++c;    //@ c becomes 6 first, then d gets 6
    cout << "c = " << c << ", d = " << d << endl;
    return 0;
}
```

```output
a = 6, b = 5
c = 6, d = 6
```

On a line by itself, `count++;` and `++count;` do exactly the same thing. You will mostly use them in loops (Chapter 8).

:::watch
Never change the same variable more than once in one expression, as in `x = x++ + ++x;`. Some versions of this are **undefined behaviour**, some have rules so subtle that nobody remembers them, and all of them are impossible to read. If you see code like this in an exam question, the right answer is often "do not write code like this".
:::

## The math library: cmath

For anything beyond basic arithmetic, `#include <cmath>`:

| Function | What it does | Example | Result |
|---|---|---|---|
| `pow(x, y)` | x to the power y | `pow(2, 10)` | `1024` |
| `sqrt(x)` | square root | `sqrt(144)` | `12` |
| `abs(x)` | absolute value | `abs(-3.5)` | `3.5` |
| `round(x)` | nearest whole number (halves away from zero) | `round(2.5)` | `3` |
| `ceil(x)` | round up | `ceil(4.1)` | `5` |
| `floor(x)` | round down | `floor(4.9)` | `4` |
| `fmod(x, y)` | remainder for doubles | `fmod(7.5, 2)` | `1.5` |

These all return `double`. If you need an `int`, convert the result, for example `static_cast<int>(round(x))`.

:::watch
There is no `^` power operator in C++. `2 ^ 3` compiles, but `^` means **bitwise exclusive OR**, so `2 ^ 3` is 1, not 8. Use `pow(2, 3)`, or simply `2 * 2 * 2`.
:::

```cpp run title=geometry.cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    const double PI = 3.14159265358979;
    double radius;
    cout << "Radius of the cake (cm): ";
    cin >> radius;
    double area = PI * pow(radius, 2);
    double diagonalOfSquareBox = sqrt(2.0) * (2 * radius);
    cout << "Area: " << area << " cm^2" << endl;
    cout << "A square box must have a diagonal of at least "
         << ceil(diagonalOfSquareBox) << " cm" << endl;
    return 0;
}
```

```output
Radius of the cake (cm): [[10]]
Area: 314.159 cm^2
A square box must have a diagonal of at least 29 cm
```

## Worked example: the tuk-tuk fare estimator

Amaya's friend Dilshan drives a tuk-tuk on weekends. He charges a starting fee plus a rate per kilometre, plus a waiting charge per minute. He wants a program that estimates the fare and rounds it **up** to the next 10 rupees, because nobody carries small coins.

```cpp run title=fare.cpp
#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    const double BASE_FARE = 100.0;     // first kilometre included
    const double PER_KM = 80.0;         // for each km after the first
    const double PER_WAIT_MIN = 5.0;

    double km;
    int waitMinutes;
    cout << "Distance (km): ";
    cin >> km;
    cout << "Waiting time (minutes): ";
    cin >> waitMinutes;

    double extraKm = km - 1;            //@ the first km is in the base fare
    double fare = BASE_FARE + extraKm * PER_KM + waitMinutes * PER_WAIT_MIN;
    double rounded = ceil(fare / 10) * 10;   //@ round up to the next 10

    cout << fixed << setprecision(2);
    cout << "Exact fare:   Rs. " << fare << endl;
    cout << "Rounded fare: Rs. " << rounded << endl;
    return 0;
}
```

```output
Distance (km): [[6.3]]
Waiting time (minutes): [[7]]
Exact fare:   Rs. 559.00
Rounded fare: Rs. 560.00
```

The trick `ceil(fare / 10) * 10` is worth remembering: divide by 10, round up, multiply back by 10.

:::brain
What does this program charge for a trip of 0.5 km? Is that correct? What would you need to add to handle short trips properly? (You will be able to write the fix after Chapter 7.)
---solution
`extraKm` becomes −0.5, so the program **subtracts** Rs. 40 from the base fare and charges Rs. 60. That is a logic error: a trip shorter than 1 km should cost the full base fare. The fix is a decision: if `km` is less than 1, treat `extraKm` as 0. Testing with small, zero and unusual values is how you find bugs like this.
:::

:::compiler
Each line below is meant to calculate the average of three test marks `m1`, `m2` and `m3` (all `int`) as a `double`. Which ones are correct?

```cpp nocheck
double avgA = m1 + m2 + m3 / 3;
double avgB = (m1 + m2 + m3) / 3;
double avgC = (m1 + m2 + m3) / 3.0;
double avgD = static_cast<double>(m1 + m2 + m3) / 3;
double avgE = static_cast<double>((m1 + m2 + m3) / 3);
```
---solution
- **A** is wrong: precedence makes it `m1 + m2 + (m3 / 3)`.
- **B** is wrong: integer division, so the decimals are lost.
- **C** is correct: `3.0` is a double, so the division is done in floating point.
- **D** is correct: the sum is converted to double before dividing.
- **E** is wrong: the integer division happens first, and only the already-truncated result is converted.
:::

:::magnets
Arrange the magnets into a program that reads a number of eggs and prints how many full trays of 30 can be filled and how many eggs are left over.
~~~
#include <iostream>
using namespace std;
int main() {
int eggs;
cin >> eggs;
cout << "Trays: " << eggs / 30 << endl;
cout << "Left over: " << eggs % 30 << endl;
return 0;
}
~~~
:::

:::quiz
? What is the value of `17 / 4`?
- 4.25
* 4
- 5
- 1
> Both operands are integers, so the fraction is discarded.

? What is the value of `17 % 4`?
- 4
- 4.25
* 1
- 0
> 17 = 4 × 4 + 1, so the remainder is 1.

? After `int x = 10; int y = x++ * 2;` what are x and y?
- x = 11, y = 22
* x = 11, y = 20
- x = 10, y = 20
- x = 10, y = 22
> Postfix ++ uses the old value (10) in the expression, then increments x.

? Which expression gives 2.5?
- `5 / 2`
- `static_cast<double>(5 / 2)`
* `static_cast<double>(5) / 2`
- `int(5.0 / 2)`
> The cast must happen before the division.

? What does `20 - 10 - 5` evaluate to?
* 5
- 15
- 25
- It depends on the compiler
> Subtraction is left to right: (20 − 10) − 5 = 5.

? What does `2 ^ 3` evaluate to in C++?
- 8
- 6
* 1
- It does not compile
> ^ is bitwise XOR, not a power operator. Use pow(2, 3).
:::

:::lab Ruwan Stores bill splitter and change maker
**Part A.** Three friends buy groceries and want to split the bill equally. Read the bill total (a double) and print what each person pays, rounded **up** to the nearest rupee using `ceil`, and how much extra the shop receives because of the rounding.

**Part B.** Uncle Ruwan gives change using Rs. 1000, 500, 100, 50, 20 and 10 notes and coins. Read an amount of change (a whole number of rupees, a multiple of 10) and print how many of each note or coin to give, using as few as possible. Use only `/` and `%`. (No `if` statements needed!)
---solution
**Part A**

```cpp run title=split.cpp
#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

int main() {
    const int PEOPLE = 3;
    double bill;
    cout << "Bill total (Rs.): ";
    cin >> bill;
    double each = ceil(bill / PEOPLE);
    double extra = each * PEOPLE - bill;
    cout << fixed << setprecision(2);
    cout << "Each person pays: Rs. " << each << endl;
    cout << "Rounding extra:   Rs. " << extra << endl;
    return 0;
}
```

```output
Bill total (Rs.): [[2459.75]]
Each person pays: Rs. 820.00
Rounding extra:   Rs. 0.25
```

**Part B**

```cpp run title=change.cpp
#include <iostream>
using namespace std;

int main() {
    int change;
    cout << "Change to give (Rs.): ";
    cin >> change;

    int n1000 = change / 1000;  change %= 1000;
    int n500  = change / 500;   change %= 500;
    int n100  = change / 100;   change %= 100;
    int n50   = change / 50;    change %= 50;
    int n20   = change / 20;    change %= 20;
    int n10   = change / 10;    change %= 10;

    cout << "1000 x " << n1000 << endl;
    cout << " 500 x " << n500 << endl;
    cout << " 100 x " << n100 << endl;
    cout << "  50 x " << n50 << endl;
    cout << "  20 x " << n20 << endl;
    cout << "  10 x " << n10 << endl;
    return 0;
}
```

```output
Change to give (Rs.): [[1780]]
1000 x 1
 500 x 1
 100 x 2
  50 x 1
  20 x 1
  10 x 1
```
Each step takes as many of the current note as fit (`/`), then keeps only what is left (`%=`). Choosing the biggest note first is called a **greedy** strategy. It gives the fewest notes for this set of values, although for some unusual coin systems a greedy choice is not always the best.
:::

:::bullets
- `int / int` is **integer division**: the fractional part is thrown away (truncated toward zero).
- If **either** operand is a double, division is done in floating point.
- Cast **before** dividing: `static_cast<double>(total) / count`.
- `%` gives the remainder and works only with integers. Use it for even/odd tests, digits, wrap-around and splitting units.
- **Precedence**: `* / %` before `+ -`. **Associativity** breaks ties, mostly left to right; assignment is right to left.
- Use **parentheses** to make your intent obvious.
- `x += 5` means `x = x + 5`. `x++` uses the old value then adds 1; `++x` adds 1 then uses the new value.
- `<cmath>` gives you `pow`, `sqrt`, `abs`, `round`, `ceil` and `floor`. There is no `^` power operator.
:::
