---
num: 11
title: Arrays and Vectors
tagline: One name, many values
learn: store many values of the same type in an array; index and traverse arrays with loops; find totals, averages, maximums and minimums; pass arrays to functions; work with two-dimensional arrays; use std::vector, the flexible array that grows
---

## Seven variables for seven days

:::story
Ruwan: I want to see my sales for each day of the week. Which day is the best? Which is the worst? What is the average?

Amaya: Okay. `double sales1, sales2, sales3, sales4, sales5, sales6, sales7;` Then seven `cin`s, then...

Nuwan: And for a month? Thirty-one variables? For a year?

Amaya: ...I see the problem.

Nuwan: You need an **array**. One name, many boxes, and a loop can walk through all of them.
:::

## What is an array?

An **array** is a collection of values of the **same type**, stored **next to each other** in memory, under **one name**. Each value is called an **element**, and you reach it by its position, called its **index**.

```cpp check
double sales[7];      // 7 doubles, one after another in memory
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| `sales[i]` | 12500 | 9800 | 11200 | 10400 | 15300 | 22100 | 18700 |

:::watch
**Indexes start at 0**, not 1. An array of 7 elements has indexes **0 to 6**. `sales[7]` does **not** exist. This is the single most important rule in this chapter.
:::

## Declaring and initialising arrays

```cpp check
int marks[5];                                   // 5 ints, values unpredictable (not initialised)
int stock[5] = {12, 40, 8, 25, 3};              // all five given
double prices[4] = {230.5, 690, 145};           // missing ones become 0: {230.5, 690, 145, 0}
int counts[100] = {0};                          // all 100 set to 0
int zeros[10] = {};                             // also all 0
char grades[] = {'A', 'B', 'C'};                // size worked out from the list: 3
const int DAYS = 7;
double sales[DAYS];                             // size from a constant
```

Rules to remember:

- The size must be a **compile-time constant**: a number or a `const int`. `int n; cin >> n; int a[n];` is not standard C++ (some compilers accept it as an extension, but do not rely on it). When the size is only known at runtime, use a **vector**, later in this chapter.
- Once created, an array's size **cannot change**.
- A local array with no initialiser contains **unpredictable** values, just like an uninitialised variable.

## Indexing: reaching one element

Use square brackets with an index to read or change one element:

```cpp run title=indexing.cpp
#include <iostream>
using namespace std;

int main() {
    int stock[5] = {12, 40, 8, 25, 3};
    cout << "First: " << stock[0] << endl;     //@ the first element
    cout << "Last:  " << stock[4] << endl;     //@ the last element is at size - 1
    stock[2] = 50;                              //@ change one element
    stock[4] += 10;
    cout << stock[2] << " " << stock[4] << endl;
    int i = 1;
    cout << stock[i] << " " << stock[i + 1] << endl;  //@ the index can be any int expression
    return 0;
}
```

```output
First: 12
Last:  3
50 13
40 50
```

## Traversal: visiting every element with a loop

Arrays and `for` loops are made for each other. The pattern `for (int i = 0; i < SIZE; i++)` visits every index exactly once:

```cpp run title=traverse.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    const int DAYS = 7;
    double sales[DAYS];
    string names[DAYS] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};

    for (int i = 0; i < DAYS; i++) {          //@ fill
        cout << "Sales for " << names[i] << ": ";
        cin >> sales[i];
    }
    double total = 0;
    for (int i = 0; i < DAYS; i++) {          //@ add up
        total += sales[i];
    }
    cout << "Week total: " << total << endl;
    return 0;
}
```

```output
Sales for Mon: [[12500]]
Sales for Tue: [[9800]]
Sales for Wed: [[11200]]
Sales for Thu: [[10400]]
Sales for Fri: [[15300]]
Sales for Sat: [[22100]]
Sales for Sun: [[18700]]
Week total: 100000
```

### The range-based for loop

When you just need to visit every element in order and do not need the index, C++11's **range-based for** loop is shorter and cannot go out of bounds:

```cpp run title=range_for.cpp
#include <iostream>
using namespace std;

int main() {
    int stock[5] = {12, 40, 8, 25, 3};
    int total = 0;
    for (int s : stock) {             //@ read it as "for each s in stock"
        total += s;
    }
    cout << "Total items: " << total << endl;

    for (int &s : stock) {            //@ & gives a reference, so we can change elements
        s += 5;
    }
    for (int s : stock) cout << s << " ";
    cout << endl;
    return 0;
}
```

```output
Total items: 88
17 45 13 30 8 
```

Without the `&`, `s` is a **copy** of each element, and changing it does nothing to the array. That is the same value-versus-reference idea from Chapter 10.

## Going out of bounds

C++ does **not** check array indexes for you. If you write `sales[7]` in an array of 7 elements, C++ calculates where element 7 **would** be and reads (or overwrites!) whatever memory is there.

```cpp nocheck
int marks[5] = {70, 85, 60, 90, 76};
for (int i = 0; i <= 5; i++) {        // BUG: <= 5 reaches marks[5]
    cout << marks[i] << endl;
}
```

This is **undefined behaviour**. The program might print a random number, crash, or appear to work perfectly today and fail next week. Writing past the end of an array can silently corrupt other variables.

:::industry
Out-of-bounds memory access is not just a beginner's bug. It is behind a large share of serious security vulnerabilities in real software written in C and C++, such as **buffer overflow** attacks, where an attacker deliberately writes past the end of an array to take control of a program. This is one of the main reasons modern C++ encourages `std::vector`, `std::array`, `.at()` and range-based loops, and one reason languages like Rust were created.
:::

:::watch
Common causes of out-of-bounds bugs:

- Using `<=` instead of `<` in the loop condition.
- Starting at index 1 and ending at `SIZE`.
- Using an index that came from user input without checking it: always test `if (i >= 0 && i < SIZE)` first.
- Hard-coding the size in several places and changing only one of them. Use a **named constant** for the size.
:::

## Classic array algorithms

These four patterns come up again and again. Learn them until you can write them without thinking.

```cpp run title=week_stats.cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    const int DAYS = 7;
    double sales[DAYS] = {12500, 9800, 11200, 10400, 15300, 22100, 18700};
    string names[DAYS] = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};

    // 1. Total and average
    double total = 0;
    for (int i = 0; i < DAYS; i++) total += sales[i];
    double average = total / DAYS;

    // 2. Maximum and minimum: remember the INDEX, so we know which day
    int best = 0, worst = 0;                    //@ start with the first element
    for (int i = 1; i < DAYS; i++) {            //@ compare from the second onwards
        if (sales[i] > sales[best]) best = i;
        if (sales[i] < sales[worst]) worst = i;
    }

    // 3. Counting: how many days beat the average?
    int aboveAverage = 0;
    for (int i = 0; i < DAYS; i++) {
        if (sales[i] > average) aboveAverage++;
    }

    // 4. Searching: did any day go over 20,000?
    int found = -1;                             //@ -1 means "not found"
    for (int i = 0; i < DAYS; i++) {
        if (sales[i] > 20000) {
            found = i;
            break;
        }
    }

    cout << fixed << setprecision(2);
    cout << "Total:   " << total << endl;
    cout << "Average: " << average << endl;
    cout << "Best:    " << names[best] << " (" << sales[best] << ")" << endl;
    cout << "Worst:   " << names[worst] << " (" << sales[worst] << ")" << endl;
    cout << "Days above average: " << aboveAverage << endl;
    if (found != -1) cout << "First day over 20,000: " << names[found] << endl;
    return 0;
}
```

```output
Total:   100000.00
Average: 14285.71
Best:    Sat (22100.00)
Worst:   Tue (9800.00)
Days above average: 3
First day over 20,000: Sat
```

:::brain
Why does the max/min loop start at `i = 1` instead of `i = 0`? Would it be wrong to start at 0?
---solution
Starting at 0 would not be wrong, just pointless: element 0 is already the starting "best", so comparing it with itself changes nothing. The important part is to initialise `best` with a **real element** of the array, not with 0 or some guessed number. If every sale were negative (refunds), a starting value of 0 would give a maximum that is not even in the array.
:::

### Two arrays that work together

`names` and `sales` above are **parallel arrays**: element `i` of one belongs with element `i` of the other. They work, but it is easy to sort one and forget the other. In Chapter 14 you will learn a better way: an array of **structs**, where each element holds both the name and the sales together.

## Passing arrays to functions

You can pass an array to a function. The function also needs to know the **size**, because an array parameter does not carry its size with it:

```cpp run title=array_functions.cpp
#include <iostream>
using namespace std;

double sumOf(const double values[], int size) {     //@ const: we only read
    double total = 0;
    for (int i = 0; i < size; i++) total += values[i];
    return total;
}

void applyIncrease(double values[], int size, double percent) {
    for (int i = 0; i < size; i++) {
        values[i] *= 1 + percent / 100;              //@ changes the caller's array!
    }
}

int main() {
    double prices[3] = {100, 250, 80};
    cout << "Sum: " << sumOf(prices, 3) << endl;
    applyIncrease(prices, 3, 10);
    for (double p : prices) cout << p << " ";
    cout << endl;
    return 0;
}
```

```output
Sum: 430
110 275 88
```

Notice that `applyIncrease` changed the original array, **without any `&`**. Arrays are never copied when passed to a function. The function receives the **address of the first element**, so it works directly on the caller's data. (Chapter 15 explains this in terms of pointers.) If a function should only read the array, mark the parameter `const`, as `sumOf` does, and the compiler will stop any accidental changes.

:::watch
Inside a function, an array parameter is really a pointer, so `sizeof(values)` gives the size of a **pointer** (usually 8 bytes), not the size of the array. Always pass the size as a separate parameter. In the function where the array is declared, `sizeof(arr) / sizeof(arr[0])` does give the number of elements, and so does `std::size(arr)` from `<iterator>` in C++17.
:::

Two more things arrays **cannot** do:

- You cannot copy a whole array with `=`: `int b[5] = a;` and `b = a;` do not compile. Copy element by element in a loop.
- A function cannot **return** a plain array.

Both limitations disappear with `std::vector`.

## Two-dimensional arrays

Sometimes data comes in a **grid**: rows and columns. Ruwan Stores has 3 branches (well, Uncle Ruwan is dreaming) and wants sales for each of 4 weeks. That is a 3 × 4 table, stored as a **two-dimensional array**:

```cpp check
const int BRANCHES = 3, WEEKS = 4;
double sales[BRANCHES][WEEKS] = {
    {52000, 48000, 61000, 58000},    // branch 0
    {31000, 35000, 29000, 40000},    // branch 1
    {45000, 47000, 50000, 44000}     // branch 2
};
```

The first index is the **row**, the second is the **column**: `sales[1][2]` is branch 1, week 2, which is 29000.

| | Week 0 | Week 1 | Week 2 | Week 3 |
|---|---|---|---|---|
| **Branch 0** | 52000 | 48000 | 61000 | 58000 |
| **Branch 1** | 31000 | 35000 | **29000** | 40000 |
| **Branch 2** | 45000 | 47000 | 50000 | 44000 |

To visit every cell, use **nested loops**: the outer loop for rows, the inner loop for columns.

```cpp run title=grid.cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    const int BRANCHES = 3, WEEKS = 4;
    double sales[BRANCHES][WEEKS] = {
        {52000, 48000, 61000, 58000},
        {31000, 35000, 29000, 40000},
        {45000, 47000, 50000, 44000}
    };

    cout << fixed << setprecision(0);
    cout << "Branch" << setw(9) << "W1" << setw(9) << "W2" << setw(9) << "W3"
         << setw(9) << "W4" << setw(10) << "Total" << endl;
    for (int b = 0; b < BRANCHES; b++) {
        double rowTotal = 0;
        cout << setw(6) << b + 1;
        for (int w = 0; w < WEEKS; w++) {
            cout << setw(9) << sales[b][w];
            rowTotal += sales[b][w];
        }
        cout << setw(10) << rowTotal << endl;
    }

    cout << " Total";
    for (int w = 0; w < WEEKS; w++) {          //@ column totals: loops swapped
        double colTotal = 0;
        for (int b = 0; b < BRANCHES; b++) colTotal += sales[b][w];
        cout << setw(9) << colTotal;
    }
    cout << endl;
    return 0;
}
```

```output
Branch       W1       W2       W3       W4     Total
     1    52000    48000    61000    58000    219000
     2    31000    35000    29000    40000    135000
     3    45000    47000    50000    44000    186000
 Total   128000   130000   140000   142000
```

Row totals: the **outer** loop is rows. Column totals: the **outer** loop is columns. Swapping the loops changes what you add up.

:::nodumb
Q: How is a 2D array stored in memory?
A: As one long row. C++ uses **row-major order**: all of row 0, then all of row 1, and so on. That is why, when passing a 2D array to a function, you must give the number of **columns**: `void print(double grid[][4], int rows)`. The compiler needs the row length to work out where each row starts.

Q: Can I have 3D arrays?
A: Yes, `int cube[3][4][5];` works the same way with three indexes. They are less common. For complex data, structs and vectors are usually clearer.
:::

## Reversing an array in place

A classic interview-style exercise: reverse an array **without** using a second array. Swap the first and last, then the second and second-last, and so on, until you reach the middle.

```cpp run title=reverse.cpp
#include <iostream>
#include <utility>
using namespace std;

int main() {
    int a[6] = {1, 2, 3, 4, 5, 6};
    int n = 6;
    for (int left = 0, right = n - 1; left < right; left++, right--) {
        swap(a[left], a[right]);          //@ std::swap from <utility>
    }
    for (int x : a) cout << x << " ";
    cout << endl;
    return 0;
}
```

```output
6 5 4 3 2 1 
```

This uses two indexes that move towards each other, a technique called **two pointers**. It does the job in n / 2 swaps, so it is O(n).

## std::vector: the array that grows

Plain arrays have a fixed size, do not know their own size, cannot be copied with `=`, and do not check indexes. The standard library's **`vector`** fixes all of these. For most everyday programs, **prefer `vector`**.

```cpp run title=vector_basics.cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    vector<double> prices;                 //@ an empty vector of doubles
    prices.push_back(230.5);               //@ add to the end; it grows automatically
    prices.push_back(690);
    prices.push_back(145);
    cout << "Count: " << prices.size() << endl;
    cout << "First: " << prices[0] << endl;
    cout << "Last:  " << prices.back() << endl;

    vector<string> items = {"Rice", "Dhal", "Sugar"};   //@ initialise from a list
    items.push_back("Tea");
    items[1] = "Red Dhal";
    for (const string &it : items) cout << it << " ";
    cout << endl;

    vector<int> scores(5, 0);              //@ five elements, all 0
    cout << scores.size() << " scores, all " << scores[3] << endl;
    return 0;
}
```

```output
Count: 3
First: 230.5
Last:  145
Rice Red Dhal Sugar Tea 
5 scores, all 0
```

The type inside the angle brackets, as in `vector<double>`, says what the vector holds. (This feature of C++ is called a **template**. You will learn to write your own templates in a later course.)

### The most useful vector operations

| Operation | What it does |
|---|---|
| `v.push_back(x)` | add `x` to the end |
| `v.pop_back()` | remove the last element |
| `v.size()` | number of elements |
| `v.empty()` | `true` if there are no elements |
| `v[i]` | element `i`, **no** bounds check |
| `v.at(i)` | element `i`, **with** a bounds check |
| `v.front()`, `v.back()` | first and last elements |
| `v.clear()` | remove everything |
| `v.insert(v.begin() + i, x)` | insert `x` at position `i` |
| `v.erase(v.begin() + i)` | remove the element at position `i` |
| `v2 = v` | copy the whole vector (works, unlike arrays!) |

### Safety with at()

`v[i]` is as unchecked as an array. `v.at(i)` checks the index and, if it is out of range, **throws an exception** instead of quietly reading random memory. If nothing catches the exception, the program stops with a clear message:

```text
terminate called after throwing an instance of 'std::out_of_range'
  what():  vector::_M_range_check: __n (which is 5) >= this->size() (which is 5)
```

(The exact wording depends on your compiler.) A crash with a clear message is far better than a silent wrong answer. Exceptions are a big topic for a later course.

### Reading an unknown number of values

This is where vectors really shine: you do not need to know in advance how many values are coming.

```cpp run title=vector_input.cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<double> bills;
    double b;
    cout << "Enter bills (negative to stop): ";
    while (cin >> b && b >= 0) {           //@ stops on a negative number or bad input
        bills.push_back(b);
    }
    if (bills.empty()) {
        cout << "No bills." << endl;
        return 0;
    }
    double total = 0;
    for (double x : bills) total += x;
    cout << bills.size() << " bills, average " << total / bills.size() << endl;
    return 0;
}
```

```output
Enter bills (negative to stop): [[1200 450 3100 980 -1]]
4 bills, average 1432.5
```

`while (cin >> b && b >= 0)` is a compact and common idiom. `cin >> b` reads a value and then counts as true only if the read succeeded.

### Passing vectors to functions

Unlike arrays, vectors are **copied** when passed by value. For anything but tiny vectors, pass by **const reference** to read, or by **reference** to change:

```cpp fn
double average(const vector<double> &v) {      // read only, no copy
    if (v.empty()) return 0;
    double total = 0;
    for (double x : v) total += x;
    return total / v.size();
}

void addTax(vector<double> &v, double rate) {   // changes the caller's vector
    for (double &x : v) x *= 1 + rate;
}

vector<double> above(const vector<double> &v, double limit) {   // functions can return vectors
    vector<double> result;
    for (double x : v) {
        if (x > limit) result.push_back(x);
    }
    return result;
}
```

:::watch
`v.size()` returns an **unsigned** type (`size_t`). Comparing it with a signed `int` in a loop like `for (int i = 0; i < v.size(); i++)` makes `-Wall -Wextra` warn about a signed/unsigned comparison. It works fine for normal sizes, but you can avoid the warning by using `size_t i` as the loop variable, or by using a range-based for loop. And be careful with `v.size() - 1` when the vector is empty: unsigned arithmetic wraps around to a huge number.
:::

### 2D vectors

A vector can hold vectors, which gives you a grid whose size can be decided at runtime:

```cpp run title=vector2d.cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int rows = 3, cols = 4;
    vector<vector<int>> seats(rows, vector<int>(cols, 0));   //@ 3 rows of 4 zeros
    seats[1][2] = 1;                                          //@ book row 1, seat 2
    for (const auto &row : seats) {
        for (int s : row) cout << (s ? "X " : ". ");
        cout << endl;
    }
    return 0;
}
```

```output
. . . . 
. . X . 
. . . . 
```

:::deep
Why can a vector grow while an array cannot? A vector keeps its elements in a block of memory with some **spare capacity**. When `push_back` runs out of space, the vector allocates a bigger block (often about twice as big), copies the elements across and frees the old block. Because the size roughly doubles each time, adding an element is still fast **on average**. You can see this with `v.capacity()`, and reserve space ahead of time with `v.reserve(1000)`.
:::

### Array, std::array or vector?

| | Plain array `int a[5]` | `std::array<int, 5>` | `std::vector<int>` |
|---|---|---|---|
| Size | fixed at compile time | fixed at compile time | can grow and shrink |
| Knows its size? | no | yes, `.size()` | yes, `.size()` |
| Copy with `=` | no | yes | yes |
| Bounds checking | no | with `.at()` | with `.at()` |
| Header | none | `<array>` | `<vector>` |
| Use when... | learning, exams, low-level code | small fixed-size collections | almost everything else |

:::compiler
Find the bugs.

```cpp error
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int marks[5] = {70, 85, 60, 90, 76};
    int copy[5];
    copy = marks;

    int total = 0;
    for (int i = 1; i <= 5; i++) {
        total += marks[i];
    }

    vector<int> v;
    v[0] = 10;
    cout << total / 5 << " " << v.size() << endl;
    return 0;
}
```
---solution
1. `copy = marks;` does not compile. Plain arrays cannot be assigned. Copy them with a loop, or use vectors.
2. The loop runs from 1 to 5. It skips `marks[0]` and reads `marks[5]`, which is out of bounds. It should be `for (int i = 0; i < 5; i++)`.
3. `v[0] = 10;` on an **empty** vector is out of bounds (undefined behaviour). Use `v.push_back(10);`.
4. `total / 5` is integer division. If you want the exact average, use `total / 5.0`.
:::

:::quiz
? What are the valid indexes of `double sales[7];`?
- 1 to 7
* 0 to 6
- 0 to 7
- 1 to 6
> Indexes start at 0 and end at size − 1.

? What does C++ do if you read `sales[7]` from a 7-element array?
- Throws an error at compile time
- Returns 0
* Reads whatever memory is there: undefined behaviour
- Grows the array
> Plain arrays have no bounds checking.

? A function has the parameter `double values[]`. Does it receive a copy of the array?
- Yes, always
* No, it works directly on the caller's array
- Only if the array is small
- Only if you add &
> An array argument passes the address of its first element.

? What is `grid[2][1]` in `int grid[3][2] = {{1, 2}, {3, 4}, {5, 6}};`?
- 3
- 4
- 5
* 6
> Row 2 is {5, 6}, and column 1 of that row is 6.

? Which statement adds 50 to the end of `vector<int> v`?
- v.add(50);
- v[v.size()] = 50;
* v.push_back(50);
- v.insert(50);
> push_back appends and grows the vector.

? What is printed? `vector<int> v = {4, 8, 15}; v.pop_back(); cout << v.size();`
- 3
* 2
- 15
- 0
> pop_back removes the last element.
:::

:::lab The Ruwan Stores stock monitor
1. Use a `vector<string>` of product names and a `vector<int>` of stock levels. Fill them by asking the user for products until they type `done` as the name.
2. Write functions (passing the vectors by const reference): `int totalStock(...)`, `int indexOfLowest(...)`, and `vector<string> lowStock(names, stock, limit)` that returns the names of products below the limit.
3. Print a report: total items, the product with the lowest stock, and the list of products to reorder (stock below 10).
4. **Extension:** print a horizontal bar chart of stock levels, one `*` per 5 items, with names left-aligned in 15 characters.
---solution
```cpp run title=stock_monitor.cpp
#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
using namespace std;

int totalStock(const vector<int> &stock) {
    int total = 0;
    for (int s : stock) total += s;
    return total;
}

int indexOfLowest(const vector<int> &stock) {
    int lowest = 0;
    for (size_t i = 1; i < stock.size(); i++) {
        if (stock[i] < stock[lowest]) lowest = i;
    }
    return lowest;
}

vector<string> lowStock(const vector<string> &names, const vector<int> &stock, int limit) {
    vector<string> result;
    for (size_t i = 0; i < names.size(); i++) {
        if (stock[i] < limit) result.push_back(names[i]);
    }
    return result;
}

int main() {
    vector<string> names;
    vector<int> stock;
    string name;
    int qty;
    while (true) {
        cout << "Product (or done): ";
        cin >> name;
        if (name == "done") break;
        cout << "Stock: ";
        cin >> qty;
        names.push_back(name);
        stock.push_back(qty);
    }
    if (names.empty()) {
        cout << "No products." << endl;
        return 0;
    }
    cout << "\nTotal items: " << totalStock(stock) << endl;
    int lo = indexOfLowest(stock);
    cout << "Lowest: " << names[lo] << " (" << stock[lo] << ")" << endl;
    cout << "Reorder:";
    for (const string &n : lowStock(names, stock, 10)) cout << " " << n;
    cout << endl << endl;
    for (size_t i = 0; i < names.size(); i++) {
        cout << left << setw(15) << names[i];
        for (int k = 0; k < stock[i] / 5; k++) cout << "*";
        cout << endl;
    }
    return 0;
}
```

```output
Product (or done): [[Rice]]
Stock: [[42]]
Product (or done): [[Oil]]
Stock: [[8]]
Product (or done): [[Soap]]
Stock: [[25]]
Product (or done): [[Tea]]
Stock: [[4]]
Product (or done): [[done]]

Total items: 79
Lowest: Tea (4)
Reorder: Oil Tea

Rice           ********
Oil            *
Soap           *****
Tea            
```
This version reads one-word product names with `cin >>`. To allow names with spaces, switch to `getline` and remember the getline trap from Chapter 4.
:::

:::bullets
- An **array** stores many values of one type under one name. Indexes run from **0 to size − 1**.
- The size of a plain array is fixed at compile time. Use a **named constant** for it.
- Traverse with `for (int i = 0; i < SIZE; i++)`, or with a **range-based for** loop (`for (int x : arr)`; add `&` to change elements).
- C++ does **not** check array bounds. Going out of bounds is undefined behaviour and a major source of security bugs.
- Learn the classic patterns: **total, average, max/min (track the index), count, search**.
- Arrays passed to functions are **not copied**; pass the size too, and use `const` when you only read.
- **2D arrays** use `[row][col]` and nested loops.
- **`std::vector`** grows with `push_back`, knows its `size()`, can be copied and returned, and checks bounds with `.at()`. Prefer it in everyday code.
- Pass vectors by **const reference** to read, and by **reference** to change.
:::
