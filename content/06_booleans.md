---
num: 6
title: True or False?
tagline: Booleans, comparisons and logic, the raw material of every decision
learn: compare values with the six relational operators; avoid the = versus == trap; compare doubles and strings correctly; combine conditions with AND, OR and NOT; use truth tables and De Morgan's laws; understand short-circuit evaluation and use it defensively
---

## Every decision starts with a question

:::story
Ruwan: I give a 10% discount to loyalty card holders, but only if they spend Rs. 2,000 or more. Pensioners get it on any amount. Except on public holidays, when nobody gets a discount because the shop is busy.

Amaya: Okay... that is a lot of "if"s.

Nuwan: Before you can write *if*, you need to write the *question*. Every question a computer asks has one of two answers: **true** or **false**. Today we learn how to ask good questions.
:::

In the next chapter you will write `if` statements that choose what to do. But an `if` is only as good as its **condition**. This chapter is about building conditions correctly, which is where most real-world logic bugs live.

## Relational operators

A **relational operator** compares two values and gives a `bool`: `true` or `false`.

| Operator | Meaning | Example (with `x = 7`) | Result |
|---|---|---|---|
| `==` | equal to | `x == 7` | `true` |
| `!=` | not equal to | `x != 7` | `false` |
| `<` | less than | `x < 10` | `true` |
| `>` | greater than | `x > 10` | `false` |
| `<=` | less than or equal to | `x <= 7` | `true` |
| `>=` | greater than or equal to | `x >= 8` | `false` |

You can store the result in a `bool` variable, or print it:

```cpp run title=compare.cpp
#include <iostream>
using namespace std;

int main() {
    double bill = 2350;
    int stock = 0;
    bool bigSpender = bill >= 2000;
    bool soldOut = stock == 0;
    cout << boolalpha;
    cout << "Big spender? " << bigSpender << endl;
    cout << "Sold out?    " << soldOut << endl;
    cout << "Bill under 1000? " << (bill < 1000) << endl;  //@ parentheses needed here
    return 0;
}
```

```output
Big spender? true
Sold out?    true
Bill under 1000? false
```

:::watch
In that last line, the parentheses around `bill < 1000` are required. Without them, `<<` has higher precedence than `<`, so the compiler tries to work out `cout << "..." << bill` first and then compare that to 1000, which does not compile. When you print a comparison, wrap it in parentheses.
:::

## The classic trap: = versus ==

- `=` is **assignment**: "store this value".
- `==` is **comparison**: "are these equal?"

Mixing them up is one of the most common bugs in C-family languages, because the wrong version often still compiles.

```cpp error title=trap.cpp
#include <iostream>
using namespace std;

int main() {
    int pin = 1234;
    bool unlocked = (pin = 9999);   //@ assigns 9999 to pin! Any non-zero value counts as true
    cout << unlocked << " " << pin << endl;
    return 0;
}
```

This prints `1 9999`. Instead of checking the PIN, the code **changed** it, and then treated 9999 as `true`, because in C++ any non-zero number converts to `true` and zero converts to `false`.

:::industry
Some programmers write comparisons "backwards", as in `9999 == pin`. If you accidentally write `9999 = pin`, it fails to compile, because you cannot assign to a literal. This style is called a **Yoda condition** ("if 9999 the pin is"). Most teams today rely on compiler warnings instead: `-Wall` warns you about assignments used as conditions.
:::

## Comparing decimals safely

You saw in Chapter 3 that doubles are approximations. That makes `==` dangerous:

```cpp run title=float_compare.cpp
#include <iostream>
#include <cmath>
using namespace std;

int main() {
    double a = 0.1 + 0.2;
    cout << boolalpha;
    cout << (a == 0.3) << endl;                         //@ false!
    const double EPSILON = 1e-9;
    cout << (fabs(a - 0.3) < EPSILON) << endl;          //@ "close enough": true
    return 0;
}
```

```output
false
true
```

The safe way is to check whether two numbers are **close enough**: their difference is smaller than a tiny tolerance, often called **epsilon**. `fabs` (from `<cmath>`) gives the absolute value of a double.

:::nodumb
Q: How small should epsilon be?
A: It depends on the size of your numbers and how much accuracy you need. For money in rupees, being within 0.001 is plenty. For scientific calculations you might need something much smaller, or a tolerance relative to the size of the numbers. `1e-9` (0.000000001) is a reasonable default for everyday values.

Q: Are `<` and `>` safe with doubles?
A: Mostly, yes. The danger is with exact equality. `price >= 2000.0` is fine for practical purposes, but remember that a value calculated as 1999.9999999 will not pass.
:::

## Comparing strings

You can compare `string` values with all six relational operators. `==` and `!=` work exactly as you would hope. `<` and `>` compare **alphabetically**, character by character, like a dictionary. This is called **lexicographic** order.

```cpp run title=string_compare.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string a = "apple", b = "Apple", c = "banana";
    cout << boolalpha;
    cout << (a == b) << endl;           //@ case matters: false
    cout << (a < c) << endl;            //@ 'a' comes before 'b': true
    cout << (b < a) << endl;            //@ 'A' (65) comes before 'a' (97): true
    cout << (string("10") < "9") << endl;  //@ '1' is before '9', so true!
    return 0;
}
```

```output
false
true
true
true
```

:::watch
String comparison uses **character codes**. All capital letters (65 to 90 in ASCII) come before all lowercase letters (97 to 122). So `"Zebra" < "apple"` is true. And numbers stored as text compare digit by digit, so `"10" < "9"`. If you need numeric order, convert the text to a number first (Chapter 12 shows how).
:::

## Combining conditions: logical operators

Real rules are rarely one comparison. Uncle Ruwan's discount needs several. **Logical operators** combine `bool` values:

| Operator | Name | True when... |
|---|---|---|
| `&&` | AND | **both** sides are true |
| `\|\|` | OR | **at least one** side is true |
| `!` | NOT | the value is false (it flips true and false) |

### Truth tables

A truth table lists every possible combination of inputs. Learn these three; you will use them every day.

| A | B | A && B | A \|\| B | !A |
|---|---|---|---|---|
| false | false | false | false | true |
| false | true | false | true | true |
| true | false | false | true | false |
| true | true | true | true | false |

In words:

- AND is strict: one false makes the whole thing false.
- OR is generous: one true makes the whole thing true.
- NOT flips.

:::watch
In everyday English, "or" sometimes means "one or the other, but not both". In C++, `||` is the **inclusive** OR: it is also true when **both** sides are true. A customer who is a pensioner **and** has a loyalty card passes `isPensioner || hasCard`.
:::

### Checking a range

To test whether `age` is between 18 and 60 inclusive, you need **two** comparisons joined with AND:

```cpp check
int age = 25;
bool workingAge = age >= 18 && age <= 60;
```

:::watch
Do **not** write it the way you would in maths:

```cpp error
bool workingAge = 18 <= age <= 60;   // compiles, but always true!
```

C++ evaluates this left to right: `18 <= age` becomes `true` or `false`, which is then converted to 1 or 0, and both 1 and 0 are `<= 60`. So the result is **always true**, even for an age of 75. g++ with `-Wall` warns: *comparisons like 'X<=Y<=Z' do not have their mathematical meaning*. This is another reason to always compile with warnings on.
:::

### Precedence of logical operators

From highest to lowest: `!`, then arithmetic, then relational (`<`, `>=`...), then equality (`==`, `!=`), then `&&`, then `||`.

So `a || b && c` means `a || (b && c)`, because `&&` binds more tightly than `||`, just as `*` binds more tightly than `+`.

The NOT operator binds very tightly, so `!x > 5` means `(!x) > 5`, which is almost never what you want. Write `!(x > 5)`, or better, `x <= 5`.

:::industry
Professional teams usually add parentheses whenever `&&` and `||` are mixed, even when precedence would give the right answer. `isPensioner || (hasCard && bill >= 2000)` is instantly clear. g++ even suggests it: *suggest parentheses around '&&' within '||'*.
:::

## Building a compound condition, step by step

Let's turn Uncle Ruwan's rule into C++. Here is a method that works for any complicated rule:

1. **List the facts** as separate `bool` variables with clear names.
2. **Write each part of the rule** in plain English using AND, OR and NOT.
3. **Translate** to C++, adding parentheses around each group.
4. **Test** with a table of cases, including the edge cases.

**Step 1: facts.** `hasCard`, `isPensioner`, `isHoliday`, and the bill amount.

**Step 2: the rule in English.** A customer gets the discount if it is **not** a public holiday **and** (they are a pensioner **or** (they have a card **and** spend at least 2000)).

**Step 3: C++.**

```cpp run title=discount_rule.cpp
#include <iostream>
using namespace std;

int main() {
    bool hasCard = true;
    bool isPensioner = false;
    bool isHoliday = false;
    double bill = 2500;

    bool bigBill = bill >= 2000;
    bool qualifies = !isHoliday && (isPensioner || (hasCard && bigBill));

    cout << boolalpha << "Discount? " << qualifies << endl;
    return 0;
}
```

```output
Discount? true
```

Giving names to the parts (`bigBill`, `qualifies`) is a huge help. The final condition reads almost like the original sentence.

**Step 4: test.** Change the values and check that the program agrees with Uncle Ruwan in every case:

| hasCard | isPensioner | isHoliday | bill | Expected |
|---|---|---|---|---|
| true | false | false | 2500 | true |
| true | false | false | 1999 | false (bill too small) |
| true | false | false | 2000 | true (edge case: exactly 2000) |
| false | true | false | 300 | true (pensioners always qualify) |
| false | true | true | 300 | false (public holiday) |
| false | false | false | 9000 | false (no card, not a pensioner) |

:::brain
Suppose you forgot the outer parentheses and wrote `!isHoliday && isPensioner || hasCard && bigBill`. Which row of the test table would now give the wrong answer? Why?
---solution
`&&` binds more tightly than `||`, so it becomes `(!isHoliday && isPensioner) || (hasCard && bigBill)`. Now a card holder with a big bill gets the discount **even on a public holiday**. The test table does not contain that exact case, which shows something important: write a test for **every** rule, including "card holder, big bill, public holiday". Expected: false. Got: true.
:::

## De Morgan's laws: flipping conditions

Sometimes it is easier to describe when something is **not** allowed. Two rules from logic, named after the mathematician Augustus De Morgan, tell you how to flip a combined condition:

- `!(A && B)` is the same as `!A || !B`
- `!(A || B)` is the same as `!A && !B`

In words: when you push a NOT inside the brackets, **flip each part and swap AND with OR**.

Example: "the shop is open if it is not Sunday and not after 9pm":

```cpp check
int hour = 20;
bool isSunday = false;
bool open1 = !isSunday && !(hour >= 21);
bool open2 = !(isSunday || hour >= 21);   // De Morgan: the same thing
```

And a range check flipped: **not** between 18 and 60 is `!(age >= 18 && age <= 60)`, which De Morgan turns into `age < 18 || age > 60`.

:::sharpen De Morgan practice
Rewrite each condition **without** the outer `!`, using De Morgan's laws.

1. `!(x > 0 && y > 0)`
2. `!(isMember || total >= 5000)`
3. `!(day == 0 || day == 6)`
4. `!(score >= 50 && attendance >= 80)`
---solution
1. `x <= 0 || y <= 0`
2. `!isMember && total < 5000`
3. `day != 0 && day != 6`
4. `score < 50 || attendance < 80`

Notice that the opposite of `>` is `<=`, not `<`. Getting the boundary right is part of flipping a condition.
:::

## Short-circuit evaluation

C++ evaluates `&&` and `||` from **left to right**, and it **stops as soon as the answer is known**:

- For `A && B`: if `A` is false, the whole thing must be false, so `B` is **never evaluated**.
- For `A || B`: if `A` is true, the whole thing must be true, so `B` is **never evaluated**.

This is called **short-circuit evaluation**, and it is not just a speed trick. You can use it to protect your program.

```cpp run title=short_circuit.cpp
#include <iostream>
using namespace std;

int main() {
    int itemsSold = 0;
    double revenue = 0;
    //@ if itemsSold is 0, the division is never attempted
    bool goodAverage = itemsSold != 0 && revenue / itemsSold > 500;
    cout << boolalpha << goodAverage << endl;
    return 0;
}
```

```output
false
```

Because `itemsSold != 0` is false, C++ never evaluates `revenue / itemsSold`. If you swap the two halves, the division is attempted first, and with integer operands it would be a division by zero.

:::industry
This pattern is called a **guard**: put the safety check on the left of `&&`, and the risky operation on the right. You will use it with arrays ("is the index valid **and** is the element positive?"), with files ("is the file open **and** does it contain data?") and with pointers ("is the pointer not null **and** does it point to a valid value?"). Order matters.
:::

## The ! operator and bool variables

Because a `bool` variable already holds true or false, you do not need to compare it to `true`:

```cpp check
bool isPaid = false;
bool a = isPaid == true;    // works, but clumsy
bool b = isPaid;            // better
bool c = isPaid == false;   // works, but clumsy
bool d = !isPaid;           // better: read it as "not paid"
```

Name bool variables as yes/no questions (`isPaid`, `hasStock`, `canDeliver`) and the conditions will read like English.

## Worked example: the loan eligibility checker

A microfinance society lends to small business owners who meet these rules:

- age between 21 and 60 inclusive, **and**
- monthly income of at least Rs. 75,000, **or** a guarantor,
- **and** no existing unpaid loan.

```cpp run title=loan.cpp
#include <iostream>
using namespace std;

int main() {
    int age;
    double income;
    char guarantorAnswer, unpaidAnswer;

    cout << "Age: ";
    cin >> age;
    cout << "Monthly income (Rs.): ";
    cin >> income;
    cout << "Has a guarantor? (y/n): ";
    cin >> guarantorAnswer;
    cout << "Has an unpaid loan? (y/n): ";
    cin >> unpaidAnswer;

    bool ageOk = age >= 21 && age <= 60;
    bool hasGuarantor = guarantorAnswer == 'y' || guarantorAnswer == 'Y';
    bool incomeOk = income >= 75000 || hasGuarantor;
    bool noDebt = !(unpaidAnswer == 'y' || unpaidAnswer == 'Y');

    bool eligible = ageOk && incomeOk && noDebt;
    cout << boolalpha << "Eligible: " << eligible << endl;
    return 0;
}
```

```output
Age: [[34]]
Monthly income (Rs.): [[60000]]
Has a guarantor? (y/n): [[Y]]
Has an unpaid loan? (y/n): [[n]]
Eligible: true
```

Notice how the program accepts both `'y'` and `'Y'`. Users do not care about your capital letters, so your conditions should not either.

:::compiler
Each condition below has a bug. Find it and fix it.

1. A teenager is someone aged 13 to 19: `age > 13 && age < 19`
2. A weekend is Saturday (6) or Sunday (0): `day == 6 || 0`
3. The answer is yes: `answer == 'y' || answer == "Y"`
4. A valid mark is 0 to 100: `mark >= 0 || mark <= 100`
5. Check the average only if count is not zero: `total / count > 50 && count != 0`
---solution
1. The ends are excluded. It should be `age >= 13 && age <= 19`.
2. `|| 0` compares nothing; 0 is just false. It should be `day == 6 || day == 0`.
3. `"Y"` is a string literal, not a char. Use `'Y'` in single quotes.
4. `||` makes it true for every number (every number is either at least 0 or at most 100). Use `&&`.
5. The guard is on the wrong side. Write `count != 0 && total / count > 50`, so the division never happens when count is 0.
:::

:::quiz
? What is the value of `!(5 > 3 && 2 > 4)`?
* true
- false
- 1 > 0
- It does not compile
> 5 > 3 is true and 2 > 4 is false, so the AND is false, and NOT false is true.

? What does `18 <= age <= 60` evaluate to when age is 75?
- false
* true
- 75
- A compile error
> 18 <= 75 gives true (1), and 1 <= 60 is true. Always write age >= 18 && age <= 60.

? In `b != 0 && a / b > 2`, what happens when b is 0?
- The program crashes
* The division is never evaluated and the result is false
- The result is true
- It is undefined behaviour
> Short-circuit evaluation stops after the left side is false.

? Which is equivalent to `!(x < 5 || y == 3)`?
- `x > 5 && y != 3`
* `x >= 5 && y != 3`
- `x >= 5 || y != 3`
- `x < 5 && y == 3`
> Flip each part and swap OR for AND. The opposite of < is >=.

? Which comparison is true?
- `string("apple") == string("Apple")`
* `string("Zebra") < string("apple")`
- `string("9") < string("10")`
- `0.1 + 0.2 == 0.3`
> Capital letters have smaller codes than lowercase ones, so "Zebra" sorts first.
:::

:::lab Eligibility checks for Ruwan Stores
Write one program that reads the information it needs and prints `true` or `false` for each of these questions:

1. **Free delivery:** the order is at least Rs. 5,000 **and** the distance is at most 5 km.
2. **Leap year:** a year is a leap year if it is divisible by 4 **and** not divisible by 100, **or** if it is divisible by 400. (Test with 2024, 1900, 2000 and 2026.)
3. **Valid time:** the hour is from 0 to 23 **and** the minute is from 0 to 59.
4. **Shop open:** the shop opens from 7 to 21 (hours), and is closed on public holidays.

For each one, write a small test table first, then the code.
---solution
```cpp run title=checks.cpp
#include <iostream>
using namespace std;

int main() {
    double order, distance;
    int year, hour, minute;
    char holiday;

    cout << "Order value and distance (km): ";
    cin >> order >> distance;
    cout << "Year: ";
    cin >> year;
    cout << "Hour and minute: ";
    cin >> hour >> minute;
    cout << "Public holiday? (y/n): ";
    cin >> holiday;

    bool freeDelivery = order >= 5000 && distance <= 5;
    bool leap = (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
    bool validTime = hour >= 0 && hour <= 23 && minute >= 0 && minute <= 59;
    bool isHoliday = holiday == 'y' || holiday == 'Y';
    bool open = validTime && hour >= 7 && hour < 21 && !isHoliday;

    cout << boolalpha;
    cout << "Free delivery: " << freeDelivery << endl;
    cout << "Leap year:     " << leap << endl;
    cout << "Valid time:    " << validTime << endl;
    cout << "Shop open:     " << open << endl;
    return 0;
}
```

```output
Order value and distance (km): [[5200 3.5]]
Year: [[1900]]
Hour and minute: [[20 45]]
Public holiday? (y/n): [[n]]
Free delivery: true
Leap year:     false
Valid time:    true
Shop open:     true
```
For the leap year rule: 2024 is true, 1900 is false (divisible by 100 but not 400), 2000 is true (divisible by 400), and 2026 is false. Notice the shop rule uses `hour < 21`: at 21:00 the shop has just closed. Deciding whether a boundary is included is a question to ask the user, not to guess.
:::

:::bullets
- Relational operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) produce `bool` values.
- `=` assigns; `==` compares. Mixing them up is a classic bug. Compile with `-Wall`.
- Never test doubles with `==`. Check `fabs(a - b) < EPSILON` instead.
- Strings compare in dictionary order **by character code**, so capitals come before lowercase.
- `&&` needs both sides true; `||` needs at least one; `!` flips.
- A range check needs two comparisons: `x >= lo && x <= hi`. Never write `lo <= x <= hi`.
- `&&` binds more tightly than `||`. Add parentheses when mixing them.
- De Morgan: `!(A && B)` is `!A || !B`, and `!(A || B)` is `!A && !B`.
- **Short-circuit evaluation** stops early. Put guards on the **left** of `&&`.
:::
