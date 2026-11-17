---
num: 7
title: Making Decisions
tagline: if, else, switch, and programs that choose their own path
learn: write if, if-else and else-if ladders; nest decisions without getting lost; avoid the dangling else and the stray semicolon; use switch for menus and fixed choices; write compact choices with the conditional operator; validate input with guard clauses
---

## The program that always said yes

:::story
Dilshan: My program gives everyone a discount. Even people with no card. Even on public holidays. I checked the condition, it's right!

Nuwan: Show me.

Dilshan: `if (qualifies); cout << "Discount applied";`

Nuwan: See that little semicolon after the bracket? Your `if` is controlling an empty statement. The `cout` runs every time. Let's learn how `if` really works, so this never happens to you again.
:::

## The if statement

An `if` statement runs a block of code **only when a condition is true**:

```cpp nocheck
if (condition) {
    // runs only when condition is true
}
// the program continues here either way
```

```cpp run title=low_stock.cpp
#include <iostream>
using namespace std;

int main() {
    const int LOW_STOCK = 10;
    int stock;
    cout << "Stock of rice bags: ";
    cin >> stock;
    if (stock < LOW_STOCK) {
        cout << "Warning: stock is low. Order more!" << endl;
    }
    cout << "Stock check complete." << endl;
    return 0;
}
```

```output
Stock of rice bags: [[7]]
Warning: stock is low. Order more!
Stock check complete.
```

Run it again with 25, and only `Stock check complete.` is printed.

```flow
flowchart TD
  A[/Read stock/] --> B{stock < LOW_STOCK?}
  B -- Yes --> C[/Display warning/]
  B -- No --> D
  C --> D[/Display 'Stock check complete'/]
```

### Curly braces: technically optional, practically required

If the body of an `if` is a single statement, C++ lets you leave out the braces:

```cpp check
int stock = 5;
if (stock < 10)
    cout << "Low stock" << endl;
```

But this is a trap waiting to happen. Watch what occurs when someone adds a second line later:

```cpp check
int stock = 50;
if (stock < 10)
    cout << "Low stock" << endl;
    cout << "Ordering 100 more bags" << endl;   // NOT inside the if!
```

The indentation **lies**. Only the first statement belongs to the `if`. The second line runs every single time, so this shop orders 100 bags whatever the stock level.

:::watch
**Always use braces**, even for one line. Many professional style guides require it. In 2014, a real security bug in Apple's SSL code (nicknamed "goto fail") was caused by a duplicated line under an `if` without braces. The duplicated line always ran, and security checks were skipped.
:::

### The stray semicolon

This is Dilshan's bug:

```cpp check
bool qualifies = false;
if (qualifies);                        // the ; ends the if right here
{
    cout << "Discount applied" << endl;   // this block always runs
}
```

The semicolon is an **empty statement**. The `if` controls that empty statement, and the block underneath is just an ordinary block that always runs. g++ warns about this if you compile with `-Wall -Wextra` (*suggest braces around empty body*). Never put a semicolon directly after `if (...)`.

## if-else: one or the other

When you need to do one thing or another, use `else`:

```cpp run title=pass_fail.cpp
#include <iostream>
using namespace std;

int main() {
    int mark;
    cout << "Mark: ";
    cin >> mark;
    if (mark >= 50) {
        cout << "Pass" << endl;
    } else {
        cout << "Fail" << endl;
    }
    return 0;
}
```

```output
Mark: [[49]]
Fail
```

Exactly one of the two blocks runs. Never both, never neither.

## The else-if ladder: many choices

When there are more than two outcomes, chain `else if`:

```cpp run title=grade.cpp
#include <iostream>
using namespace std;

int main() {
    int mark;
    cout << "Mark (0-100): ";
    cin >> mark;

    if (mark >= 75) {
        cout << "Grade A" << endl;
    } else if (mark >= 65) {
        cout << "Grade B" << endl;
    } else if (mark >= 55) {
        cout << "Grade C" << endl;
    } else if (mark >= 35) {
        cout << "Grade S" << endl;
    } else {
        cout << "Grade F" << endl;
    }
    return 0;
}
```

```output
Mark (0-100): [[68]]
Grade B
```

C++ checks the conditions **from top to bottom** and runs **only the first** block whose condition is true. Then it skips the rest of the ladder.

That is why the second condition can simply be `mark >= 65`. We only reach it when `mark >= 75` was false, so we already know the mark is below 75. There is no need to write `mark >= 65 && mark < 75`.

:::brain
What happens if you put the conditions in the opposite order, starting with `if (mark >= 35)`? Try a mark of 90 in your head.
---solution
A mark of 90 passes the **first** test, `mark >= 35`, so the program prints "Grade S" and skips everything else. In a ladder of `>=` tests, always start with the **highest** threshold. (With `<=` tests, start with the lowest.) The order of the conditions is part of the logic.
:::

:::watch
Each `else if` is really an `else` with an `if` inside it. A ladder of separate `if` statements (with no `else`) is **different**: every condition is checked, and several blocks can run.

```cpp check
int mark = 90;
if (mark >= 75) { cout << "A"; }
if (mark >= 65) { cout << "B"; }   // also true!
if (mark >= 55) { cout << "C"; }   // also true!
// prints ABC
```
:::

## Nested if statements

You can put an `if` inside another `if`. This is called **nesting**. It is useful when a second question only makes sense after the first one is answered.

```cpp run title=atm.cpp
#include <iostream>
using namespace std;

int main() {
    const int CORRECT_PIN = 4821;
    double balance = 15000;
    int pin;
    double amount;

    cout << "Enter PIN: ";
    cin >> pin;
    if (pin == CORRECT_PIN) {
        cout << "Amount to withdraw: ";
        cin >> amount;
        if (amount <= balance) {
            balance -= amount;
            cout << "Please take your cash. Balance: " << balance << endl;
        } else {
            cout << "Insufficient funds." << endl;
        }
    } else {
        cout << "Wrong PIN." << endl;
    }
    return 0;
}
```

```output
Enter PIN: [[4821]]
Amount to withdraw: [[20000]]
Insufficient funds.
```

### Nested if or a compound condition?

These two versions do the same job:

```cpp check
bool hasCard = true;
double bill = 3000;
// Nested
if (hasCard) {
    if (bill >= 2000) {
        cout << "Discount" << endl;
    }
}
// Compound
if (hasCard && bill >= 2000) {
    cout << "Discount" << endl;
}
```

Use a **compound condition** when both checks lead to one single action. Use **nesting** when the inner part does different things, or when you need to report **which** check failed (as the ATM does with "Wrong PIN" and "Insufficient funds").

### The dangling else

Which `if` does this `else` belong to?

```cpp check
bool hasCard = false;
double bill = 500;
if (hasCard)
    if (bill >= 2000)
        cout << "Discount" << endl;
else
    cout << "No card" << endl;
```

The indentation suggests the `else` belongs to `if (hasCard)`. But C++ has a fixed rule: **an `else` always belongs to the nearest unmatched `if` above it**. So it belongs to `if (bill >= 2000)`. For a customer **with** a card and a small bill, this prints "No card". For a customer without a card, it prints nothing at all.

The fix is the same as always: **use braces**, and the problem cannot happen.

## Guard clauses and input validation

A **guard clause** checks for a bad situation first and deals with it straight away. This keeps the main logic flat and readable.

```cpp run title=guard.cpp
#include <iostream>
using namespace std;

int main() {
    int qty;
    double unitPrice;
    cout << "Quantity: ";
    cin >> qty;
    if (!cin || qty <= 0) {                 //@ guard: bad input or impossible value
        cout << "Quantity must be a positive whole number." << endl;
        return 1;                           //@ stop with an error code
    }
    cout << "Unit price: ";
    cin >> unitPrice;
    if (!cin || unitPrice < 0) {
        cout << "Price cannot be negative." << endl;
        return 1;
    }
    cout << "Total: " << qty * unitPrice << endl;
    return 0;
}
```

```output
Quantity: [[-3]]
Quantity must be a positive whole number.
```

`!cin` is true when the last read failed (for example, the user typed letters). Writing `if (!cin)` is a common short form of `if (cin.fail())`.

`return 1;` inside `main` ends the program immediately and reports failure to the operating system. In Chapter 8 you will replace these early exits with a **loop** that asks again until the input is valid.

:::industry
Checking inputs at the start of a piece of code is called **defensive programming**. Banking apps, payment systems and medical software validate every value that comes in, because one unexpected value can cause wrong charges, crashes or security holes. A good habit: every time you write `cin >>`, ask yourself "what if the user types something silly here?"
:::

## switch: choosing from fixed options

When you compare **one** value against a list of **exact** values, a `switch` statement is often clearer than a long else-if ladder. Menus are the perfect example.

```cpp run title=menu.cpp
#include <iostream>
using namespace std;

int main() {
    int choice;
    cout << "1. Add item\n2. Remove item\n3. Show stock\n4. Exit\n";
    cout << "Choose: ";
    cin >> choice;

    switch (choice) {
        case 1:
            cout << "Adding an item..." << endl;
            break;                          //@ jump out of the switch
        case 2:
            cout << "Removing an item..." << endl;
            break;
        case 3:
            cout << "Showing stock..." << endl;
            break;
        case 4:
            cout << "Goodbye!" << endl;
            break;
        default:                            //@ none of the cases matched
            cout << "Invalid choice." << endl;
    }
    return 0;
}
```

```output
1. Add item
2. Remove item
3. Show stock
4. Exit
Choose: [[3]]
Showing stock...
```

How `switch` works:

1. The value in brackets is evaluated once.
2. C++ jumps to the `case` with a matching value.
3. It runs statements from there **until it reaches `break`** (or the end of the switch).
4. If no case matches, it jumps to `default` (if there is one).

### Fall-through: the missing break

If you forget `break`, execution **falls through** into the next case:

```cpp run title=fallthrough.cpp
#include <iostream>
using namespace std;

int main() {
    int choice = 2;
    switch (choice) {
        case 1:
            cout << "One ";
        case 2:
            cout << "Two ";       //@ starts here...
        case 3:
            cout << "Three ";     //@ ...and keeps going, no break!
            break;
        default:
            cout << "Other";
    }
    cout << endl;
    return 0;
}
```

```output
Two Three 
```

Fall-through is usually a bug, and `-Wextra` warns about it. But it can be used on purpose to let several cases share code:

```cpp run title=grade_letters.cpp
#include <iostream>
using namespace std;

int main() {
    char grade;
    cout << "Grade letter: ";
    cin >> grade;
    switch (grade) {
        case 'A':
        case 'a':                    //@ both 'A' and 'a' arrive here
            cout << "Excellent" << endl;
            break;
        case 'B':
        case 'b':
            cout << "Good" << endl;
            break;
        case 'F':
        case 'f':
            cout << "Please see your lecturer" << endl;
            break;
        default:
            cout << "Unknown grade" << endl;
    }
    return 0;
}
```

```output
Grade letter: [[b]]
Good
```

### What switch can and cannot do

| switch can... | switch cannot... |
|---|---|
| test integers (`int`, `long`...) | test `double` or `float` values |
| test `char` values | test `string` values |
| test `enum` values (Chapter 14) | test ranges like `mark >= 75` |
| match several cases to one block | use variables as case labels (they must be constants) |

So use `switch` for menus, single-letter commands and fixed codes. Use `if`/`else if` for ranges, strings and complex conditions.

:::nodumb
Q: Is switch faster than if-else?
A: For a long list of exact integer values, the compiler can sometimes turn a `switch` into a **jump table**, which goes straight to the right case. Modern compilers are very good at optimising both forms, so choose whichever is **clearer**. Readability wins.

Q: Can I declare a variable inside a case?
A: Only inside its own braces: `case 1: { int x = 5; ... break; }`. Without braces, the compiler complains that the jump to a later case would skip the variable's initialisation.
:::

## The conditional operator: ? :

For a tiny either-or choice that produces a **value**, C++ has the **conditional operator** (often called the ternary operator, because it has three parts):

```cpp nocheck
condition ? valueIfTrue : valueIfFalse
```

```cpp run title=ternary.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int qty = 1;
    double bill = 2500;
    string word = (qty == 1) ? "item" : "items";
    double delivery = (bill >= 2000) ? 0 : 350;
    cout << qty << " " << word << ", delivery Rs. " << delivery << endl;
    return 0;
}
```

```output
1 item, delivery Rs. 0
```

It is perfect for small choices like plurals and simple fees. For anything more complex, use a normal `if`, because nested `? :` expressions quickly become unreadable.

## Variables live inside their block

A variable declared inside a block `{ }` exists **only** inside that block. This is called its **scope**.

```cpp error title=scope.cpp
#include <iostream>
using namespace std;

int main() {
    double bill = 2500;
    if (bill >= 2000) {
        double discount = bill * 0.1;   //@ discount is born here...
        cout << "Discount: " << discount << endl;
    }                                   //@ ...and dies here
    cout << discount << endl;           //@ error: 'discount' was not declared in this scope
    return 0;
}
```

If you need a value after the `if`, declare the variable **before** it:

```cpp check
double bill = 2500;
double discount = 0;          // declared outside, with a sensible default
if (bill >= 2000) {
    discount = bill * 0.1;    // only assigned inside
}
cout << "Pay: " << bill - discount << endl;
```

You will study scope properly in Chapter 10.

## Worked example: the Ruwan Stores checkout

Time to put Chapter 6 and this chapter together. Here is the full discount rule from the start of Chapter 6, with input validation and a receipt.

```cpp run title=checkout.cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    const double CARD_DISCOUNT = 0.10;
    const double MIN_FOR_CARD = 2000;
    double bill;
    char card, pensioner, holiday;

    cout << "Bill amount (Rs.): ";
    cin >> bill;
    if (!cin || bill <= 0) {
        cout << "Invalid bill amount." << endl;
        return 1;
    }
    cout << "Loyalty card? (y/n): ";
    cin >> card;
    cout << "Pensioner? (y/n): ";
    cin >> pensioner;
    cout << "Public holiday? (y/n): ";
    cin >> holiday;

    bool hasCard = (card == 'y' || card == 'Y');
    bool isPensioner = (pensioner == 'y' || pensioner == 'Y');
    bool isHoliday = (holiday == 'y' || holiday == 'Y');

    double discount = 0;
    string reason;
    if (isHoliday) {
        reason = "No discounts on public holidays";
    } else if (isPensioner) {
        discount = bill * CARD_DISCOUNT;
        reason = "Pensioner discount";
    } else if (hasCard && bill >= MIN_FOR_CARD) {
        discount = bill * CARD_DISCOUNT;
        reason = "Loyalty card discount";
    } else if (hasCard) {
        reason = "Spend Rs. 2000 or more to use your card";
    } else {
        reason = "No discount";
    }

    cout << fixed << setprecision(2);
    cout << "\nBill:     Rs. " << setw(10) << bill << endl;
    cout << "Discount: Rs. " << setw(10) << discount << "  (" << reason << ")" << endl;
    cout << "To pay:   Rs. " << setw(10) << bill - discount << endl;
    return 0;
}
```

```output
Bill amount (Rs.): [[1850]]
Loyalty card? (y/n): [[y]]
Pensioner? (y/n): [[n]]
Public holiday? (y/n): [[n]]

Bill:     Rs.    1850.00
Discount: Rs.       0.00  (Spend Rs. 2000 or more to use your card)
To pay:   Rs.    1850.00
```

Notice how the ladder handles the **most decisive rule first** (a public holiday beats everything), and how each branch also sets a `reason`. Explaining **why** is a small touch that makes users trust a program.

:::compiler
This program should print "Child" for ages under 13, "Teen" for 13 to 19, and "Adult" otherwise. Find all the bugs.

```cpp error
#include <iostream>
using namespace std;

int main() {
    int age;
    cin >> age;
    if (age < 13);
        cout << "Child" << endl;
    else if (age >= 13 || age <= 19)
        cout << "Teen" << endl;
    else
        cout << "Adult" << endl;
    return 0;
}
```
---solution
1. `if (age < 13);` has a stray semicolon. This also causes a compile error, because the `else` no longer has an `if` to belong to.
2. `age >= 13 || age <= 19` is true for every age. It should use `&&`. Better still, because the ladder already knows the age is at least 13 at that point, simply write `else if (age <= 19)`.
3. Not an error, but missing braces make the code fragile. Here is the fixed version:

```cpp run title=age_fixed.cpp
#include <iostream>
using namespace std;

int main() {
    int age;
    cin >> age;
    if (age < 13) {
        cout << "Child" << endl;
    } else if (age <= 19) {
        cout << "Teen" << endl;
    } else {
        cout << "Adult" << endl;
    }
    return 0;
}
```

```output
[[16]]
Teen
```
:::

:::magnets
Rebuild a program that reads a number and prints whether it is positive, negative or zero.
~~~
#include <iostream>
using namespace std;
int main() {
int n;
cin >> n;
if (n > 0) {
cout << "Positive" << endl;
} else if (n < 0) {
cout << "Negative" << endl;
} else {
cout << "Zero" << endl;
}
return 0;
}
~~~
:::

:::fireside if-else ladder|switch
1: I can do everything you can do. Ranges, strings, complex conditions, the lot.

2: True. But when someone builds a menu with ten options, you become a wall of `else if (choice == 7)` lines. I just line the cases up neatly.

1: And when they forget a `break`, you run three cases at once.

2: That is called fall-through, and it is sometimes useful! Besides, compilers warn about it now.

1: You cannot even compare a `string`. Or a `double`.

2: Fair. So here is the deal: I take the menus, the single characters, and the fixed codes. You take everything with ranges and logic.

1: Deal. And they should both use braces.

2: Always.
:::

:::quiz
? How many blocks of an if / else-if / else ladder can run in one pass?
- All of them
- Zero or more
* Exactly one
- It depends on the compiler
> The first true condition's block runs, or the else block if none is true.

? What does this print when x is 5? `if (x > 10); cout << "Big";`
- Nothing
* Big
- A compile error
- 5
> The semicolon ends the if. The cout is a separate statement that always runs.

? In a switch, what happens if a case has no break?
- A compile error
- The switch ends
* Execution falls through into the next case
- The default case runs
> Without break, statements of the following cases run too.

? Which of these can NOT be used directly in a switch?
- int
- char
* string
- an enum
> switch only works with integer-like types. Use if-else for strings.

? An else belongs to...
- the first if in the function
* the nearest unmatched if above it
- whichever if it is indented under
- the if with the most conditions
> Indentation means nothing to the compiler. Use braces to make it clear.

? What is the value of `(7 % 2 == 0) ? "even" : "odd"`?
- "even"
* "odd"
- 1
- true
> 7 % 2 is 1, so the condition is false and the second value is chosen.
:::

:::lab The electricity bill calculator
A simplified block tariff (invented for this exercise; real tariffs change often) charges per unit:

| Units used in the month | Rate per unit |
|---|---|
| first 60 units | Rs. 10 |
| next 30 units (61 to 90) | Rs. 15 |
| every unit above 90 | Rs. 40 |

There is also a fixed charge: Rs. 150 if the total units are 60 or fewer, otherwise Rs. 400.

1. Read the number of units. Reject negative values with a guard clause.
2. Calculate the energy charge using the blocks above. (For 100 units: 60 × 10 + 30 × 15 + 10 × 40.)
3. Add the fixed charge and print an itemised bill with two decimal places.
4. Test with 0, 45, 60, 61, 90, 100 and 250 units. Write the expected answers **before** running the program.
5. **Extension:** add a menu using `switch`: 1 for domestic (the tariff above), 2 for religious places (a flat Rs. 8 per unit, no fixed charge).
---solution
```cpp run title=electricity.cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int units;
    cout << "Units used: ";
    cin >> units;
    if (!cin || units < 0) {
        cout << "Units must be zero or more." << endl;
        return 1;
    }

    double energy = 0;
    if (units <= 60) {
        energy = units * 10.0;
    } else if (units <= 90) {
        energy = 60 * 10.0 + (units - 60) * 15.0;
    } else {
        energy = 60 * 10.0 + 30 * 15.0 + (units - 90) * 40.0;
    }
    double fixedCharge = (units <= 60) ? 150 : 400;

    cout << fixed << setprecision(2);
    cout << "Energy charge: Rs. " << setw(9) << energy << endl;
    cout << "Fixed charge:  Rs. " << setw(9) << fixedCharge << endl;
    cout << "Total:         Rs. " << setw(9) << energy + fixedCharge << endl;
    return 0;
}
```

```output
Units used: [[100]]
Energy charge: Rs.   1450.00
Fixed charge:  Rs.    400.00
Total:         Rs.   1850.00
```
Expected totals: 0 units gives 150.00; 45 gives 600.00; 60 gives 750.00; 61 gives 1015.00; 90 gives 1450.00; 100 gives 1850.00; 250 gives 7850.00. The tests at 60, 61 and 90 are **boundary tests**. Bugs love boundaries.
:::

:::bullets
- `if (condition) { ... }` runs its block only when the condition is true.
- **Always use braces.** Never put a semicolon straight after `if (...)`.
- `if ... else` runs exactly one of two blocks. An **else-if ladder** runs the **first** matching block only, so order the conditions carefully.
- An `else` belongs to the **nearest unmatched `if`**, whatever the indentation says.
- Use **guard clauses** to reject bad input early: `if (!cin || qty <= 0) { ... }`.
- `switch` compares one integer, char or enum value against constant cases. Remember `break`; missing breaks cause **fall-through**.
- `condition ? a : b` chooses between two values. Keep it for small choices.
- A variable declared inside a block exists only inside that block.
:::
