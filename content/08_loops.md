---
num: 8
title: Loops
tagline: Doing things again and again, without writing them again and again
learn: repeat code with while, do-while and for; choose the right loop for the job; use counters, accumulators and sentinel values; control loops with break and continue; write nested loops; validate input properly; make random numbers for games; get a first feel for Big-O efficiency
---

## A thousand bills a week

:::story
Ruwan: Your checkout program is very nice. But it does one bill and then it stops. I have two hundred customers on a Saturday! Must I run it two hundred times?

Amaya: I could copy the code two hundred times...

Nuwan: *(choking on his tea)* Please don't. Computers are very good at one thing above all: repetition. Let me show you **loops**.
:::

A **loop** repeats a block of code. Each repetition is called an **iteration**. Every loop needs three ingredients:

1. **A starting point**, such as a counter set to 1.
2. **A condition** that decides whether to go round again.
3. **Progress**: something inside the loop must change, so that the condition eventually becomes false.

Forget the third ingredient and you get an **infinite loop**.

## The while loop

A `while` loop checks its condition **before** each iteration. If the condition is true, the body runs, and then the condition is checked again.

```cpp nocheck
while (condition) {
    // body: runs again and again while condition is true
}
```

```cpp run title=countdown.cpp
#include <iostream>
using namespace std;

int main() {
    int count = 5;              //@ 1. start
    while (count > 0) {         //@ 2. condition
        cout << count << "... ";
        count--;                //@ 3. progress
    }
    cout << "Shop is open!" << endl;
    return 0;
}
```

```output
5... 4... 3... 2... 1... Shop is open!
```

```flow
flowchart TD
  A[count = 5] --> B{count > 0?}
  B -- Yes --> C[/Display count/]
  C --> D[count = count - 1]
  D --> B
  B -- No --> E[/Display 'Shop is open!'/]
```

Let's trace it:

| Iteration | count before | `count > 0`? | Printed | count after |
|---|---|---|---|---|
| 1 | 5 | true | `5...` | 4 |
| 2 | 4 | true | `4...` | 3 |
| 3 | 3 | true | `3...` | 2 |
| 4 | 2 | true | `2...` | 1 |
| 5 | 1 | true | `1...` | 0 |
| (check) | 0 | **false** | loop ends | |

If the condition is false from the very start, the body runs **zero** times. That is a key feature of `while`.

### The infinite loop

```cpp nocheck
int count = 5;
while (count > 0) {
    cout << count << endl;
    // forgot count--
}
```

`count` stays 5 forever, the condition is always true, and the program prints 5 until you stop it. In a terminal, press **Ctrl + C** to stop a runaway program.

:::watch
Two classic causes of infinite loops:

1. **No progress:** forgetting to update the loop variable.
2. **A stray semicolon:** `while (count > 0);` The semicolon makes an empty body, so the loop spins forever doing nothing, and the block below it is never reached.
:::

## Counters and accumulators

Two patterns appear inside loops again and again:

- A **counter** counts how many times something happens: `count++`.
- An **accumulator** builds up a running total: `total += value`.

Both must be **initialised before the loop** (usually to 0).

## The sentinel loop: Ruwan Stores' running bill

Remember the flowchart from Chapter 1, where the cashier types prices and enters 0 to finish? Now you can write it. The value 0 is the **sentinel**: a special value that means "stop".

```cpp run title=running_bill.cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double price;
    double total = 0;       //@ accumulator
    int items = 0;          //@ counter

    cout << "Enter prices (0 to finish):" << endl;
    cout << "Price: ";
    cin >> price;                   //@ read the first value before the loop
    while (price != 0) {
        total += price;
        items++;
        cout << "Price: ";
        cin >> price;               //@ read the next value at the end
    }

    cout << fixed << setprecision(2);
    cout << items << " items, total Rs. " << total << endl;
    return 0;
}
```

```output
Enter prices (0 to finish):
Price: [[230.50]]
Price: [[690]]
Price: [[145]]
Price: [[0]]
3 items, total Rs. 1065.50
```

This shape is called the **priming read** pattern: read once before the loop, then read again at the **end** of each iteration. That way the sentinel is checked before it can be added to the total.

:::brain
What would go wrong if you moved the `cin >> price;` to the **top** of the loop body and removed the read before the loop?
---solution
`price` would be **uninitialised** when the condition `price != 0` is first checked, which is undefined behaviour. And the sentinel 0 would be **added to the total and counted as an item** before the condition gets a chance to stop the loop. Adding 0 to the total happens to do no harm, but the item count would be one too high. The priming read avoids both problems.
:::

## The do-while loop: always at least once

A `do-while` loop checks its condition **after** the body. So the body always runs **at least once**.

```cpp nocheck
do {
    // body: runs at least once
} while (condition);    // note the semicolon here!
```

That makes it perfect when you must do something before you can decide whether to repeat it, like asking for a PIN:

```cpp run title=pin_retry.cpp
#include <iostream>
using namespace std;

int main() {
    const int CORRECT_PIN = 4821;
    const int MAX_TRIES = 3;
    int pin;
    int tries = 0;

    do {
        cout << "Enter PIN: ";
        cin >> pin;
        tries++;
    } while (pin != CORRECT_PIN && tries < MAX_TRIES);

    if (pin == CORRECT_PIN) {
        cout << "Welcome!" << endl;
    } else {
        cout << "Card blocked after " << MAX_TRIES << " attempts." << endl;
    }
    return 0;
}
```

```output
Enter PIN: [[1111]]
Enter PIN: [[4812]]
Enter PIN: [[4821]]
Welcome!
```

:::watch
The `while (...)` at the end of a do-while **needs a semicolon**. A `while` loop at the top must **not** have one. Mixing them up is a common source of compile errors and infinite loops.
:::

## The for loop: counting made neat

When you know how many times to repeat, or you are counting through a range, the `for` loop puts all three ingredients on one line:

```cpp nocheck
for (initialisation; condition; update) {
    // body
}
```

```cpp run title=for_basic.cpp
#include <iostream>
using namespace std;

int main() {
    for (int day = 1; day <= 7; day++) {
        cout << "Day " << day << " ";
    }
    cout << endl;
    return 0;
}
```

```output
Day 1 Day 2 Day 3 Day 4 Day 5 Day 6 Day 7 
```

The exact order of events:

1. **Initialisation** (`int day = 1`) runs **once**, at the very start.
2. **Condition** (`day <= 7`) is checked. If false, the loop ends.
3. **Body** runs.
4. **Update** (`day++`) runs.
5. Go back to step 2.

A `for` loop is really a tidy `while` loop. These two are equivalent:

```cpp check
for (int i = 0; i < 3; i++) {
    cout << i;
}

int j = 0;
while (j < 3) {
    cout << j;
    j++;
}
```

### for loop variations

```cpp run title=for_variations.cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 10; i >= 0; i -= 2) cout << i << " ";    //@ counting down in steps of 2
    cout << endl;
    for (int i = 1; i <= 1000; i *= 10) cout << i << " ";  //@ multiplying
    cout << endl;
    int sum = 0;
    for (int i = 1; i <= 100; i++) sum += i;               //@ add 1 to 100
    cout << "Sum 1..100 = " << sum << endl;
    return 0;
}
```

```output
10 8 6 4 2 0 
1 10 100 1000 
Sum 1..100 = 5050
```

:::watch
**Off-by-one errors** are the most common loop bug. Does your loop run 9 times or 10 times? Ask: what is the **first** value, what is the **last** value, and is the condition `<` or `<=`?

- `for (int i = 0; i < 10; i++)` runs 10 times: i = 0, 1, ..., 9.
- `for (int i = 1; i <= 10; i++)` runs 10 times: i = 1, 2, ..., 10.
- `for (int i = 0; i <= 10; i++)` runs **11** times. Often a bug.

Programmers usually count from 0 with `<`, because that is exactly what arrays need (Chapter 11).
:::

:::nodumb
Q: Can I use the loop variable after the for loop ends?
A: Not if you declared it in the `for` line. `for (int i = 0; ...)` creates `i` inside the loop's scope, and it disappears when the loop ends. If you need the final value, declare `i` before the loop.

Q: Why is the counter always called i?
A: Tradition, going back to early mathematics and the Fortran language. `i`, `j` and `k` are accepted names for short loop counters. For anything longer or more meaningful, use a real name such as `day` or `customer`.
:::

## Choosing the right loop

| Situation | Best loop | Why |
|---|---|---|
| You know the number of repetitions (or a range to count through) | `for` | Start, condition and update are together on one line |
| Repeat until something happens, which might be immediately | `while` | It can run zero times |
| The body must run at least once (menus, input prompts, PIN entry) | `do-while` | It checks after the body |

All three can do each other's jobs. Choosing the natural one makes your code easier to read.

:::fireside while loop|do-while loop
1: I am the careful one. I look before I leap. If the condition is false, I do nothing at all.

2: And I am the brave one. I leap first and look afterwards. Somebody has to show the menu before the user can choose "Exit".

1: Being brave is how you divide by zero.

2: Being careful is how you write the same `cout` and `cin` twice, once before the loop and once inside it.

1: Fine. Menus and input prompts are yours.

2: And anything that might need to happen zero times is yours. Also, people keep forgetting my semicolon.

1: Mine they keep adding where it does not belong.
:::

## break and continue

Two statements give you finer control inside any loop:

- `break` **leaves the loop immediately**. Execution continues after the loop.
- `continue` **skips the rest of this iteration** and jumps to the next one. (In a `for` loop, the update still runs.)

```cpp run title=break_continue.cpp
#include <iostream>
using namespace std;

int main() {
    // continue: skip the multiples of 3
    for (int i = 1; i <= 10; i++) {
        if (i % 3 == 0) {
            continue;
        }
        cout << i << " ";
    }
    cout << endl;

    // break: stop at the first number divisible by 7
    for (int n = 50; n <= 100; n++) {
        if (n % 7 == 0) {
            cout << "First multiple of 7 from 50: " << n << endl;
            break;
        }
    }
    return 0;
}
```

```output
1 2 4 5 7 8 10 
First multiple of 7 from 50: 56
```

:::watch
Use `break` and `continue` to make code clearer, not to escape from loops you designed badly. If a loop has three `break` statements scattered through it, it is usually a sign that the condition should be rewritten. Also note that `break` only leaves the **innermost** loop (or switch) it is in.
:::

## The input validation loop

In Chapter 7, a guard clause stopped the program when the input was bad. A better program **asks again**. This is the loop that professional console programs use:

```cpp run title=validate.cpp
#include <iostream>
#include <limits>
using namespace std;

int main() {
    int qty;
    while (true) {
        cout << "Quantity (1-100): ";
        cin >> qty;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Please type a whole number." << endl;
        } else if (qty < 1 || qty > 100) {
            cout << "Quantity must be between 1 and 100." << endl;
        } else {
            break;                                  //@ valid: leave the loop
        }
    }
    cout << "OK, " << qty << " items." << endl;
    return 0;
}
```

```output
Quantity (1-100): [[ten]]
Please type a whole number.
Quantity (1-100): [[500]]
Quantity must be between 1 and 100.
Quantity (1-100): [[12]]
OK, 12 items.
```

`while (true)` looks like an infinite loop, and it would be, except that the `break` gives it one clearly marked exit. This "loop and a half" pattern is common and perfectly respectable for input loops.

:::deep
If the input stream reaches **end of file** (for example, the user presses Ctrl + D on Linux or Ctrl + Z then Enter on Windows), `cin.fail()` becomes true and stays true, because there is nothing left to read. A truly robust program also checks `cin.eof()` and gives up gracefully instead of looping forever. For classroom programs, the version above is enough.
:::

## Nested loops

A loop inside a loop is a **nested loop**. For **each** iteration of the outer loop, the inner loop runs **completely**.

```cpp run title=times_table.cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    for (int row = 1; row <= 5; row++) {          //@ outer: 5 rows
        for (int col = 1; col <= 5; col++) {      //@ inner: 5 columns per row
            cout << setw(4) << row * col;
        }
        cout << endl;                             //@ end of each row
    }
    return 0;
}
```

```output
   1   2   3   4   5
   2   4   6   8  10
   3   6   9  12  15
   4   8  12  16  20
   5  10  15  20  25
```

The inner body ran 5 × 5 = **25** times.

### Pattern printing

Pattern problems are excellent nested loop practice. The trick is to work out how the inner loop depends on the outer one.

```cpp run title=triangle.cpp
#include <iostream>
using namespace std;

int main() {
    int rows = 4;
    for (int r = 1; r <= rows; r++) {
        for (int s = 1; s <= rows - r; s++) cout << " ";       //@ leading spaces
        for (int k = 1; k <= 2 * r - 1; k++) cout << "*";      //@ stars: 1, 3, 5, 7
        cout << endl;
    }
    return 0;
}
```

```output
   *
  ***
 *****
*******
```

:::sharpen Pattern prediction
What does this print?

```cpp run title=pattern2.cpp
#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 4; i++) {
        for (int j = 1; j <= i; j++) {
            cout << j;
        }
        cout << endl;
    }
    return 0;
}
```
---solution
```output
1
12
123
1234
```
The inner loop runs `i` times, printing 1 up to `i`. Row 1 has one number, row 4 has four.
:::

## Loops with numbers: digit by digit

Combine `% 10` and `/ 10` from Chapter 5 with a loop, and you can process every digit of a number:

```cpp run title=digit_sum.cpp
#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Number: ";
    cin >> n;
    int original = n, sum = 0, digits = 0, reversed = 0;
    while (n > 0) {
        int last = n % 10;             //@ take the last digit
        sum += last;
        digits++;
        reversed = reversed * 10 + last;
        n /= 10;                       //@ drop the last digit
    }
    cout << original << " has " << digits << " digits, digit sum " << sum
         << ", reversed " << reversed << endl;
    return 0;
}
```

```output
Number: [[40721]]
40721 has 5 digits, digit sum 14, reversed 12704
```

:::brain
What does this program print for the input 0? Is that right? How would you fix it?
---solution
For 0 the loop never runs, so the program says 0 has **0 digits**, which is wrong (0 has one digit). A `do-while` loop fixes it, because it always runs at least once. This is a nice example of choosing the loop that matches the problem exactly.
:::

## Random numbers: a guessing game

Games and simulations need random numbers. Modern C++ provides them in `<random>`:

```cpp run random title=guess.cpp
#include <iostream>
#include <random>
using namespace std;

int main() {
    random_device rd;                               //@ a source of unpredictable seeds
    mt19937 gen(rd());                              //@ a high-quality random generator
    uniform_int_distribution<int> dist(1, 100);     //@ every number 1..100 equally likely
    int secret = dist(gen);

    int guess, tries = 0;
    cout << "I'm thinking of a number from 1 to 100." << endl;
    do {
        cout << "Your guess: ";
        cin >> guess;
        tries++;
        if (guess < secret) {
            cout << "Higher!" << endl;
        } else if (guess > secret) {
            cout << "Lower!" << endl;
        }
    } while (guess != secret);
    cout << "Got it in " << tries << " tries!" << endl;
    return 0;
}
```

```output
I'm thinking of a number from 1 to 100.
Your guess: [[50]]
Higher!
Your guess: [[75]]
Lower!
Your guess: [[62]]
Got it in 3 tries!
```

(Your game will be different, because the number is random.)

- `random_device` provides a hard-to-predict starting value (a **seed**).
- `mt19937` is the **Mersenne Twister** generator, which produces a long sequence of high-quality pseudo-random numbers from that seed.
- `uniform_int_distribution<int>(1, 100)` shapes those numbers into the range you want, all equally likely.

:::nodumb
Q: My old textbook uses `rand()` and `srand(time(0))`. Is that wrong?
A: It is not wrong, and you will see it in a lot of older code. But `rand()` comes from C, its quality varies between systems, and the common trick `rand() % 100 + 1` makes some numbers slightly more likely than others. For anything that matters, prefer `<random>`. For security, such as passwords or tokens, neither is good enough; use a cryptographic library.

Q: Is the computer's random number really random?
A: Not exactly. A generator like `mt19937` uses a formula, so the same seed always produces the same sequence. That is why they are called **pseudo-random**. This is actually useful: give the generator a fixed seed, such as `mt19937 gen(42);`, and your program becomes repeatable, which makes testing much easier.
:::

## How fast is your loop? A first look at Big-O

Imagine Ruwan Stores becomes a supermarket chain with a million products. Does your loop still finish quickly? Programmers measure this with **Big-O notation**, which describes how the amount of work **grows** as the input size `n` grows.

- **O(1), constant time:** the work does not depend on `n`. Example: `total = price * qty;`
- **O(n), linear time:** one loop over the input. Double the input, double the work. Example: adding up all prices.
- **O(n²), quadratic time:** a loop inside a loop, both over the input. Double the input, **four times** the work. Example: comparing every product with every other product to look for duplicates.

| n | O(n) steps | O(n²) steps |
|---|---|---|
| 10 | 10 | 100 |
| 1,000 | 1,000 | 1,000,000 |
| 1,000,000 | 1,000,000 | 1,000,000,000,000 |

At a billion simple steps per second, a million steps is about a millisecond. A trillion steps takes around **17 minutes**. Same computer, same problem, very different loop design.

:::industry
Big-O is one of the most common topics in software engineering job interviews. Interviewers want to know whether you can spot that a nested loop will be too slow before it reaches a million users. You will meet Big-O again when you study searching and sorting in Chapter 13.
:::

## Debugging loops

When a loop misbehaves, **print the loop variables** on each iteration. It is the fastest way to see what is really happening:

```cpp check
int total = 0;
for (int i = 1; i <= 5; i++) {
    total += i * 2;
    cout << "[debug] i=" << i << " total=" << total << endl;   // remove when fixed
}
```

Ask these questions about every loop:

1. Is every variable **initialised** before the loop?
2. Does the condition become false **eventually**? What makes it change?
3. What happens on the **first** and **last** iterations? (Off-by-one?)
4. What happens if the loop runs **zero** times?
5. Is there a stray `;` after `for (...)` or `while (...)`?

:::compiler
Each loop is meant to print the numbers 1 to 5. What does each one actually do?

```cpp nocheck
// A
for (int i = 1; i < 5; i++) cout << i;
// B
int j = 1;
while (j <= 5) cout << j; j++;
// C
for (int k = 1; k <= 5; k++); cout << "*";
// D
int m = 1;
do { cout << m; m++; } while (m <= 5)
// E
for (int n = 5; n >= 1; n--) cout << 6 - n;
```
---solution
- **A** prints `1234`. Off by one: the condition should be `i <= 5`.
- **B** is an **infinite loop** printing 1 forever. Without braces, only `cout << j;` is inside the loop; `j++` is never reached.
- **C** compiles, but prints a single `*`. The `;` straight after the `for (...)` gives the loop an empty body. The loop counts from 1 to 5 doing nothing, and then `cout << "*";` runs once. Stray semicolons are sneaky.
- **D** does not compile: the `do-while` is missing its final semicolon.
- **E** works and prints `12345`, in a roundabout way.
:::

:::magnets
Arrange the magnets into a program that reads 5 marks and prints their average.
~~~
#include <iostream>
using namespace std;
int main() {
int total = 0;
for (int i = 1; i <= 5; i++) {
int mark;
cin >> mark;
total += mark;
}
cout << total / 5.0 << endl;
return 0;
}
~~~
:::

:::quiz
? How many times does `for (int i = 0; i < 10; i += 2)` run its body?
- 4
* 5
- 6
- 10
> i takes the values 0, 2, 4, 6, 8.

? Which loop always runs its body at least once?
- for
- while
* do-while
- All of them
> do-while checks its condition after the body.

? What does `continue` do in a for loop?
- Exits the loop
- Restarts the loop from the beginning with i reset
* Skips the rest of the body and goes to the update step
- Pauses the program
> The update (such as i++) still runs, then the condition is checked.

? A nested loop has an outer loop of 4 iterations and an inner loop of 3. How many times does the inner body run?
- 7
* 12
- 3
- 4
> The inner loop runs completely for each outer iteration: 4 × 3.

? What is the main danger in `while (x > 0) { cout << x; }`?
- It does not compile
- It runs zero times
* It is an infinite loop if x starts positive
- It prints x backwards
> Nothing inside the loop changes x.

? Doubling the input size of an O(n²) algorithm multiplies its work by about...
- 2
* 4
- 8
- n
> (2n)² = 4n².
:::

:::lab The Ruwan Stores daily cash-up
At closing time, Uncle Ruwan enters every bill total from the day. Write a program that:

1. Reads bill totals using a **sentinel loop** (a negative number ends input, so that a genuine Rs. 0 refund note can still be entered).
2. Rejects non-numeric input with the validation pattern, without counting it.
3. At the end, prints: the number of bills, the total takings, the average bill, the largest bill and the smallest bill, all to two decimal places.
4. Prints a special message if there were **no** bills (and does not divide by zero!).
5. **Extension:** after the summary, print a simple bar chart: one `#` for every Rs. 1000 of takings.
---solution
```cpp run title=cashup.cpp
#include <iostream>
#include <iomanip>
#include <limits>
using namespace std;

int main() {
    double bill, total = 0, largest = 0, smallest = 0;
    int count = 0;

    cout << "Enter bill totals (negative number to finish):" << endl;
    while (true) {
        cout << "Bill: ";
        cin >> bill;
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Not a number, try again." << endl;
            continue;
        }
        if (bill < 0) {
            break;
        }
        if (count == 0) {            //@ the first bill is both the largest and smallest so far
            largest = bill;
            smallest = bill;
        } else {
            if (bill > largest) largest = bill;
            if (bill < smallest) smallest = bill;
        }
        total += bill;
        count++;
    }

    if (count == 0) {
        cout << "No bills today." << endl;
        return 0;
    }
    cout << fixed << setprecision(2);
    cout << "Bills:    " << count << endl;
    cout << "Takings:  Rs. " << total << endl;
    cout << "Average:  Rs. " << total / count << endl;
    cout << "Largest:  Rs. " << largest << endl;
    cout << "Smallest: Rs. " << smallest << endl;
    cout << "Chart:    ";
    for (int i = 1; i <= total / 1000; i++) {
        cout << "#";
    }
    cout << endl;
    return 0;
}
```

```output
Enter bill totals (negative number to finish):
Bill: [[1250]]
Bill: [[abc]]
Not a number, try again.
Bill: [[480.5]]
Bill: [[3200]]
Bill: [[-1]]
Bills:    3
Takings:  Rs. 4930.50
Average:  Rs. 1643.50
Largest:  Rs. 3200.00
Smallest: Rs. 480.50
Chart:    ####
```
The key idea for the largest and smallest values: initialise them from the **first** real value, not from 0. If you start `smallest` at 0, no positive bill will ever be smaller, and the answer would be wrong.
:::

:::bullets
- Every loop needs a **start**, a **condition** and **progress**. Without progress you get an infinite loop (stop it with Ctrl + C).
- `while` checks first and can run **zero** times. `do-while` checks last and runs **at least once** (and ends with `;`).
- `for (init; condition; update)` is ideal for counting. Watch for **off-by-one** errors.
- Counters (`count++`) and accumulators (`total += x`) must be initialised **before** the loop.
- A **sentinel** value ends input; use a **priming read** before the loop.
- `break` leaves the innermost loop; `continue` skips to the next iteration.
- The **validation loop** (fail, clear, ignore, ask again) is how robust programs read input.
- In nested loops, the inner loop runs completely for each outer iteration.
- Use `<random>` (`mt19937` and a distribution) for random numbers.
- **Big-O** describes how work grows: one loop is O(n), a nested loop is O(n²).
:::
