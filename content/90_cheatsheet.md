---
num: A
kind: appendix
title: C++ Cheat Sheet
tagline: Everything important, on a few pages
---

## Program skeleton

```cpp title=skeleton.cpp
#include <iostream>     // cout, cin
#include <string>       // string
using namespace std;

int main() {
    // your code here
    return 0;
}
```

Compile and run: `g++ -std=c++17 -Wall -Wextra program.cpp -o program`, then `./program` (or `program.exe` on Windows).

## Data types

| Type | Holds | Example |
|---|---|---|
| `int` | whole numbers (typically −2,147,483,648 to 2,147,483,647) | `int qty = 3;` |
| `long long` | big whole numbers (at least 64 bits) | `long long views = 5000000000LL;` |
| `double` | decimals, about 15 to 16 significant digits | `double price = 230.50;` |
| `float` | decimals, about 7 significant digits | `float w = 2.5f;` |
| `char` | one character, single quotes | `char grade = 'A';` |
| `bool` | `true` or `false` | `bool paid = false;` |
| `string` | text, double quotes (`<string>`) | `string name = "Amaya";` |
| `const` | makes a variable read-only | `const double VAT = 0.18;` |
| `auto` | the compiler works out the type | `auto total = 0.0;` |

## Input and output

| Task | Code |
|---|---|
| Print | `cout << "Total: " << total << endl;` |
| New line | `endl` or `"\n"` |
| Read a value or word | `cin >> x;` |
| Read a whole line | `getline(cin, line);` |
| Clear the newline before getline | `cin.ignore(numeric_limits<streamsize>::max(), '\n');` (`<limits>`) |
| Recover from bad input | `cin.clear();` then the ignore above |
| Two decimal places | `cout << fixed << setprecision(2);` (`<iomanip>`) |
| Column width (next item only) | `cout << setw(10) << x;` |
| Align | `left`, `right` |
| Escape sequences | `\n` newline, `\t` tab, `\"` quote, `\'` apostrophe, `\\` backslash |

## Operator precedence (highest first)

| Level | Operators | Associativity |
|---|---|---|
| 1 | `::` | left to right |
| 2 | `x++` `x--` `f()` `a[i]` `.` `->` | left to right |
| 3 | `++x` `--x` unary `+` `-` `!` `~` `(type)` `*p` `&x` `sizeof` `new` `delete` | **right to left** |
| 4 | `*` `/` `%` | left to right |
| 5 | `+` `-` | left to right |
| 6 | `<<` `>>` | left to right |
| 7 | `<` `<=` `>` `>=` | left to right |
| 8 | `==` `!=` | left to right |
| 9 | `&` (bitwise AND) | left to right |
| 10 | `^` (bitwise XOR) | left to right |
| 11 | `\|` (bitwise OR) | left to right |
| 12 | `&&` | left to right |
| 13 | `\|\|` | left to right |
| 14 | `? :` `=` `+=` `-=` `*=` `/=` `%=` | **right to left** |
| 15 | `,` | left to right |

When in doubt, add parentheses.

## Arithmetic reminders

- `int / int` truncates: `7 / 2` is `3`. Use `7 / 2.0` or `static_cast<double>(a) / b`.
- `%` is the remainder, integers only: `17 % 5` is `2`. The sign follows the left operand.
- `x += 5;` means `x = x + 5;`. `x++` uses the old value, `++x` the new one.
- `<cmath>`: `pow(x, y)`, `sqrt(x)`, `abs(x)`, `round(x)`, `ceil(x)`, `floor(x)`. There is no `^` power operator.

## Conditions

```cpp nocheck
if (a > b && !done) {
    // ...
} else if (a == b || x != 0) {
    // ...
} else {
    // ...
}

switch (choice) {          // int, char or enum only
    case 1:  doThis(); break;
    case 2:  doThat(); break;
    default: cout << "Invalid";
}

string word = (n == 1) ? "item" : "items";
```

- Range check: `x >= lo && x <= hi`. Never `lo <= x <= hi`.
- Compare doubles with a tolerance: `fabs(a - b) < 1e-9`.
- De Morgan: `!(A && B)` is `!A || !B`; `!(A || B)` is `!A && !B`.

## Loops

```cpp nocheck
while (condition) { ... }                   // may run 0 times
do { ... } while (condition);               // runs at least once (note the ;)
for (int i = 0; i < n; i++) { ... }         // counting
for (const auto &x : container) { ... }     // every element (add & without const to change them)
break;      // leave the loop
continue;   // skip to the next iteration
```

Input validation loop:

```cpp nocheck
while (true) {
    cout << "Quantity: ";
    if (cin >> qty && qty > 0) break;
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cout << "Please enter a positive whole number." << endl;
}
```

## Functions

```cpp nocheck
double area(double w, double h);              // prototype
double area(double w, double h) { return w * h; }

void print(const string &s);                  // big input, read only
void reset(int &counter);                     // changes the caller's variable
int square(int n = 2);                        // default argument
```

| Pass as | Syntax | Use for |
|---|---|---|
| value | `int x` | small types |
| reference | `int &x` | changing the caller's variable |
| const reference | `const string &s` | large types, read only |

## Arrays and vectors

```cpp nocheck
int a[5] = {1, 2, 3, 4, 5};            // fixed size, indexes 0..4
double grid[3][4];                     // 3 rows, 4 columns
vector<int> v = {4, 8, 15};            // #include <vector>
v.push_back(16);   v.pop_back();   v.size();   v.empty();
v.at(i);   v.front();   v.back();   v.clear();
v.erase(v.begin() + i);   v.insert(v.begin() + i, x);
sort(v.begin(), v.end());              // #include <algorithm>
```

## Strings

| Task | Code |
|---|---|
| Length | `s.length()` or `s.size()` |
| One character | `s[i]`, `s.at(i)` |
| Join | `s + t`, `s += t` |
| Find | `s.find("x")` (compare with `string::npos`) |
| Part of a string | `s.substr(pos, len)` |
| Change | `s.erase(pos, len)`, `s.insert(pos, t)`, `s.replace(pos, len, t)` |
| Number to text | `to_string(42)` |
| Text to number | `stoi("42")`, `stod("3.5")` |
| Character tests | `isdigit(c)`, `isalpha(c)`, `isspace(c)`, `toupper(c)`, `tolower(c)` (`<cctype>`) |
| Split | `istringstream in(line); getline(in, field, ',');` (`<sstream>`) |

## Structs and enums

```cpp nocheck
struct Product {
    string name;
    double price = 0;
    int stock = 0;
};                                     // semicolon!
Product p = {"Rice", 230.5, 42};
cout << p.name;                        // dot for variables
Product *ptr = &p;  ptr->price = 250;  // arrow for pointers

enum class Category { Grocery, Household };
Category c = Category::Grocery;
```

## Pointers

| Code | Meaning |
|---|---|
| `int *p = &x;` | p holds the address of x |
| `*p` | the value p points to |
| `p->m` | `(*p).m` |
| `nullptr` | points to nothing |
| `new int(5)` / `delete p;` | heap allocation and release |
| `new int[n]` / `delete[] p;` | heap array |
| `make_unique<T>()` | smart pointer that deletes automatically (`<memory>`) |

## Files

```cpp nocheck
#include <fstream>
ofstream out("data.txt");              // overwrite
ofstream log("log.txt", ios::app);     // append
ifstream in("data.txt");
if (!in) { /* could not open */ }
while (in >> a >> b) { ... }           // value by value
while (getline(in, line)) { ... }      // line by line
// never: while (!in.eof())
```

## Big-O at a glance

| Big-O | Name | Example |
|---|---|---|
| O(1) | constant | reading `v[i]` |
| O(log n) | logarithmic | binary search |
| O(n) | linear | one loop over the data, linear search |
| O(n log n) | linearithmic | `std::sort` |
| O(n²) | quadratic | nested loops, bubble sort |
