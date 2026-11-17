---
num: 14
title: Structs and Enums
tagline: Building your own data types
learn: group related data into a struct; create, initialise and use struct variables; store structs in arrays and vectors instead of parallel arrays; pass and return structs from functions; sort a vector of structs by any field; give names to fixed choices with enum class; take a first step towards classes and objects
---

## Five arrays and one mistake

:::story
Amaya: I have five vectors now: names, prices, stock, categories, suppliers. I sorted the prices to find the cheapest products and... now every name is next to the wrong price.

Nuwan: Because you sorted one vector and not the other four. Your data is scattered. A product is one thing. It should live in one place.

Amaya: Can I make a type called Product?

Nuwan: Yes. That is exactly what a **struct** is for.
:::

## Defining a struct

A **struct** (short for structure) lets you create a new type that **groups several related values** under one name. Each value inside is called a **member** (or field).

```cpp fn title=product_struct
struct Product {          //@ a new type called Product
    string name;          //@ members: each has its own type
    double price;
    int stock;
    char category;
};                        //@ do not forget this semicolon!
```

This does not create any product yet. It is a **blueprint**: a description of what every `Product` will contain. Now `Product` is a type, just like `int` or `string`, and you can make variables of it.

:::watch
The semicolon after the closing brace of a struct definition is required. Forgetting it gives confusing error messages that point at the **next** line of code, often the start of `main`.
:::

## Creating and using struct variables

```cpp run title=struct_basics.cpp
#include <iostream>
#include <string>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
    char category;
};

int main() {
    Product rice;                         //@ a variable of type Product
    rice.name = "Red Rice 1kg";           //@ the dot operator reaches a member
    rice.price = 230.50;
    rice.stock = 42;
    rice.category = 'G';

    Product oil = {"Coconut Oil 750ml", 690, 8, 'G'};   //@ initialise in member order

    cout << rice.name << ": Rs. " << rice.price << " (" << rice.stock << " in stock)" << endl;
    cout << oil.name << ": Rs. " << oil.price << " (" << oil.stock << " in stock)" << endl;

    oil.stock -= 3;                       //@ members are ordinary variables
    Product backup = oil;                 //@ structs CAN be copied with =
    cout << backup.name << " now " << backup.stock << endl;
    return 0;
}
```

```output
Red Rice 1kg: Rs. 230.5 (42 in stock)
Coconut Oil 750ml: Rs. 690 (8 in stock)
Coconut Oil 750ml now 5
```

Each `Product` variable holds its **own** copy of every member. `rice.price` and `oil.price` are completely separate.

### Default member values

You can give members default values in the struct definition (C++11 and later). Then a new variable starts in a sensible state:

```cpp fn
struct Product {
    string name = "Unnamed";
    double price = 0.0;
    int stock = 0;
    char category = 'G';
};
```

`Product p;` now starts with stock 0 and price 0.0, instead of unpredictable values.

## Structs and functions

Structs can be passed to functions and returned from them. Use the same rules as Chapter 10: **const reference** to read, **reference** to change.

```cpp run title=struct_functions.cpp
#include <iostream>
#include <iomanip>
#include <string>
using namespace std;

struct Product {
    string name;
    double price = 0;
    int stock = 0;
};

void printProduct(const Product &p) {               //@ read only, no copy
    cout << left << setw(20) << p.name << right << setw(10) << fixed
         << setprecision(2) << p.price << setw(6) << p.stock << endl;
}

void restock(Product &p, int amount) {              //@ changes the caller's product
    p.stock += amount;
}

Product makeProduct(const string &name, double price, int stock) {   //@ returns a whole struct
    Product p;
    p.name = name;
    p.price = price;
    p.stock = stock;
    return p;
}

double stockValue(const Product &p) {
    return p.price * p.stock;
}

int main() {
    Product soap = makeProduct("Soap Bar", 145, 25);
    restock(soap, 10);
    printProduct(soap);
    cout << "Stock value: Rs. " << stockValue(soap) << endl;
    return 0;
}
```

```output
Soap Bar                145.00    35
Stock value: Rs. 5075.00
```

This also solves the "a function can only return one value" problem from Chapter 9: return a struct that bundles several values together.

## Vectors of structs: goodbye, parallel arrays

Now the real payoff. Instead of five parallel vectors, keep **one** vector of products. Each element carries all of its own data, so it cannot get separated.

```cpp run title=inventory.cpp
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

int main() {
    vector<Product> inventory = {
        {"Red Rice 1kg", 230.50, 42},
        {"Coconut Oil 750ml", 690.00, 8},
        {"Soap Bar", 145.00, 25},
        {"Ceylon Tea 200g", 520.00, 4},
    };
    inventory.push_back({"Dhal 500g", 320.00, 15});

    double totalValue = 0;
    cout << fixed << setprecision(2);
    for (const Product &p : inventory) {
        cout << left << setw(20) << p.name << right << setw(9) << p.price
             << setw(5) << p.stock << (p.stock < 10 ? "  LOW" : "") << endl;
        totalValue += p.price * p.stock;
    }
    cout << "Total stock value: Rs. " << totalValue << endl;
    cout << "Second product: " << inventory[1].name << endl;   //@ index first, then the dot
    return 0;
}
```

```output
Red Rice 1kg           230.50   42
Coconut Oil 750ml      690.00    8  LOW
Soap Bar               145.00   25
Ceylon Tea 200g        520.00    4  LOW
Dhal 500g              320.00   15
Total stock value: Rs. 25706.00
Second product: Coconut Oil 750ml
```

`inventory[1].name` reads as: take element 1 of `inventory` (a `Product`), then take its `name` member.

## Sorting structs by any field

`std::sort` does not know how to compare two `Product`s. Is a product "smaller" if it is cheaper? Has less stock? Comes first alphabetically? You decide, by giving `sort` a **comparison function** that returns `true` when the first argument should come **before** the second:

```cpp run title=sort_structs.cpp
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

bool cheaperFirst(const Product &a, const Product &b) {
    return a.price < b.price;
}

bool lowestStockFirst(const Product &a, const Product &b) {
    return a.stock < b.stock;
}

void show(const vector<Product> &v) {
    for (const Product &p : v) cout << p.name << " (" << p.price << ", " << p.stock << ")  ";
    cout << endl;
}

int main() {
    vector<Product> items = {{"Rice", 230.5, 42}, {"Oil", 690, 8}, {"Soap", 145, 25}, {"Tea", 520, 4}};
    sort(items.begin(), items.end(), cheaperFirst);
    show(items);
    sort(items.begin(), items.end(), lowestStockFirst);
    show(items);
    // A lambda: a small function written right where it is needed
    sort(items.begin(), items.end(), [](const Product &a, const Product &b) {
        return a.name < b.name;
    });
    show(items);
    return 0;
}
```

```output
Soap (145, 25)  Rice (230.5, 42)  Tea (520, 4)  Oil (690, 8)  
Tea (520, 4)  Oil (690, 8)  Soap (145, 25)  Rice (230.5, 42)  
Oil (690, 8)  Rice (230.5, 42)  Soap (145, 25)  Tea (520, 4)  
```

The third sort uses a **lambda expression**: `[](...) { ... }` is an unnamed function written inline. Lambdas arrived in C++11 and are used all over modern C++. For now, you can always write a normal named function instead.

:::watch
A comparison function must answer "should `a` come **strictly before** `b`?" Use `<`, never `<=`. With `<=`, two equal elements would each claim to come before the other, which breaks the rules `std::sort` relies on and can cause wrong results or even crashes.
:::

## Nested structs

A member of a struct can itself be a struct:

```cpp run title=nested.cpp
#include <iostream>
#include <string>
using namespace std;

struct Date {
    int day, month, year;
};

struct Supplier {
    string name;
    string phone;
};

struct Delivery {
    string item;
    int quantity;
    Date date;            //@ a struct inside a struct
    Supplier from;
};

int main() {
    Delivery d = {"Red Rice 1kg", 100, {15, 11, 2026}, {"Lanka Grains", "0812223344"}};
    cout << d.quantity << " x " << d.item << " from " << d.from.name << endl;
    cout << "Delivered on " << d.date.day << "/" << d.date.month << "/" << d.date.year << endl;
    return 0;
}
```

```output
100 x Red Rice 1kg from Lanka Grains
Delivered on 15/11/2026
```

## enum class: names for fixed choices

Using `'G'` for groceries and `'H'` for household items works, but nothing stops someone typing `'Q'`. An **enumeration** creates a type with a fixed list of named values:

```cpp run title=enum.cpp
#include <iostream>
#include <string>
using namespace std;

enum class Category { Grocery, Household, Beverage, Snack };

string categoryName(Category c) {
    switch (c) {
        case Category::Grocery:   return "Grocery";
        case Category::Household: return "Household";
        case Category::Beverage:  return "Beverage";
        case Category::Snack:     return "Snack";
    }
    return "Unknown";
}

struct Product {
    string name;
    double price;
    Category category;
};

int main() {
    Product tea = {"Ceylon Tea 200g", 520, Category::Beverage};
    cout << tea.name << " is in " << categoryName(tea.category) << endl;
    if (tea.category == Category::Beverage) {
        cout << "Shelf 4" << endl;
    }
    return 0;
}
```

```output
Ceylon Tea 200g is in Beverage
Shelf 4
```

- You must write the type name in front: `Category::Beverage`. This prevents clashes between enums that use the same word.
- An `enum class` value does **not** silently turn into an `int`. `cout << tea.category;` does not compile, which is why we wrote `categoryName`.
- If you need the number, convert it deliberately: `static_cast<int>(Category::Snack)` is 3 (values count from 0).
- With `-Wall`, g++ warns if a `switch` on an enum forgets one of the values. That is a lovely safety net when you add a new category later.

:::nodumb
Q: What is the difference between enum and enum class?
A: The older plain `enum Category { Grocery, Household };` puts its names straight into the surrounding scope and converts freely to `int`. That causes name clashes and sneaky bugs. `enum class` (C++11) is "scoped" and strongly typed. Prefer `enum class` in new code; you will still see plain `enum` in older code.

Q: Can I read an enum with cin?
A: Not directly. Read an `int` or a `char`, check it, then convert it with `static_cast<Category>(n)` or a `switch`.
:::

## A first step towards classes

A struct can also contain **functions**, called **member functions**. They work on the struct's own data:

```cpp run title=member_functions.cpp
#include <iostream>
#include <string>
using namespace std;

struct Product {
    string name;
    double price = 0;
    int stock = 0;

    double value() const {               //@ const: this function does not change the product
        return price * stock;
    }
    bool isLow() const {
        return stock < 10;
    }
    void sell(int qty) {
        if (qty > 0 && qty <= stock) stock -= qty;
    }
};

int main() {
    Product oil = {"Coconut Oil 750ml", 690, 12};
    oil.sell(5);                         //@ call it with the dot, like s.length()
    cout << oil.name << ": " << oil.stock << " left, worth Rs. " << oil.value() << endl;
    cout << boolalpha << "Low? " << oil.isLow() << endl;
    return 0;
}
```

```output
Coconut Oil 750ml: 7 left, worth Rs. 4830
Low? true
```

Look familiar? `oil.sell(5)` is the same shape as `name.length()` and `prices.push_back(9)`. That is because `string` and `vector` are themselves types built this way, with data and member functions together.

:::industry
This is the doorway to **object-oriented programming** (OOP). In C++, a `class` is almost exactly a `struct`; the only difference is that members of a `class` are **private** by default, so outside code cannot touch the data directly and must go through member functions. That idea, called **encapsulation**, is how large programs protect their data. For example, `sell` above refuses impossible sales, but nothing currently stops someone writing `oil.stock = -50;` directly. Classes fix that. They are the main topic of the next programming course you take.
:::

:::compiler
Find the errors.

```cpp error
#include <iostream>
#include <string>
using namespace std;

struct Student {
    string name;
    int marks[3];
}

int main() {
    Student s;
    name = "Kasun";
    s.marks = {70, 80, 90};
    Student list[2];
    list.name[0] = "Nimal";
    cout << s << endl;
    return 0;
}
```
---solution
1. The struct definition is missing its closing semicolon: `};`.
2. `name = "Kasun";` must say whose name: `s.name = "Kasun";`.
3. `s.marks = {70, 80, 90};` tries to assign to an array, which C++ does not allow. Set each element, or initialise the whole struct at once: `Student s = {"Kasun", {70, 80, 90}};`. (Or make `marks` a `vector<int>`, which can be assigned.)
4. `list.name[0]` has the index in the wrong place. It should be `list[0].name`: element 0 of `list`, then its `name`.
5. `cout << s` does not compile. C++ does not know how to print a whole struct; print each member, or write a function such as `printStudent`.
:::

:::quiz
? Which operator accesses a member of a struct variable?
- ->
* .
- ::
- &
> The dot operator: product.price.

? What does `inventory[2].stock` mean?
- The stock of all products, times 2
* The stock member of element 2 of inventory
- The third character of stock
- A compile error
> Index first to get one Product, then use the dot.

? How should you pass a large struct to a function that only reads it?
- By value
- By reference
* By const reference
- You cannot pass structs to functions
> const & avoids the copy and prevents accidental changes.

? What must a comparison function for std::sort return?
- The larger element
* true if the first argument should come before the second
- 0, 1 or -1
- The index of the smaller element
> And it must use a strict comparison such as <.

? What is an advantage of enum class over using chars like 'G' and 'H'?
- It uses more memory
* Only the listed values are valid, and the names explain themselves
- It can be printed directly with cout
- It converts to int automatically
> The compiler can check that you only use real categories.
:::

:::lab The student result system
Build a small result system for one class:

1. Define `struct Student { string id; string name; int marks[3]; };` and an `enum class Grade { A, B, C, S, F }`.
2. Write `double average(const Student &s)`, `Grade gradeFor(double avg)` and `string gradeText(Grade g)`.
3. Store at least five students in a `vector<Student>` (initialise them in the code).
4. Print a report sorted by average, highest first, showing ID, name, average (one decimal place) and grade.
5. Print the class average and the name of the top student.
---solution
```cpp run title=results.cpp
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

enum class Grade { A, B, C, S, F };

struct Student {
    string id;
    string name;
    int marks[3];
};

double average(const Student &s) {
    return (s.marks[0] + s.marks[1] + s.marks[2]) / 3.0;
}

Grade gradeFor(double avg) {
    if (avg >= 75) return Grade::A;
    if (avg >= 65) return Grade::B;
    if (avg >= 55) return Grade::C;
    if (avg >= 35) return Grade::S;
    return Grade::F;
}

string gradeText(Grade g) {
    switch (g) {
        case Grade::A: return "A";
        case Grade::B: return "B";
        case Grade::C: return "C";
        case Grade::S: return "S";
        case Grade::F: return "F";
    }
    return "?";
}

bool higherAverage(const Student &a, const Student &b) {
    return average(a) > average(b);
}

int main() {
    vector<Student> cls = {
        {"S001", "Fathima Rizwan", {78, 85, 90}},
        {"S002", "Kasun Perera", {55, 61, 48}},
        {"S003", "Nimali Silva", {66, 70, 72}},
        {"S004", "Dilshan Fernando", {30, 42, 35}},
        {"S005", "Tharindu Jayasuriya", {88, 92, 79}},
    };
    sort(cls.begin(), cls.end(), higherAverage);

    double sum = 0;
    cout << fixed << setprecision(1);
    for (const Student &s : cls) {
        double avg = average(s);
        sum += avg;
        cout << s.id << "  " << left << setw(22) << s.name << right << setw(6) << avg
             << "  " << gradeText(gradeFor(avg)) << endl;
    }
    cout << "Class average: " << sum / cls.size() << endl;
    cout << "Top student:   " << cls[0].name << endl;
    return 0;
}
```

```output
S005  Tharindu Jayasuriya     86.3  A
S001  Fathima Rizwan          84.3  A
S003  Nimali Silva            69.3  B
S002  Kasun Perera            54.7  S
S004  Dilshan Fernando        35.7  S
Class average: 66.1
Top student:   Tharindu Jayasuriya
```
Because the vector was sorted with the highest average first, the top student is simply `cls[0]`.
:::

:::bullets
- A **struct** groups related values into one new type. End the definition with `};`.
- Use the **dot operator** to reach members: `p.price`. Initialise with `{...}` in member order, or give members default values.
- Structs can be copied with `=`, passed to functions (const & to read, & to change) and returned from functions.
- A **vector of structs** keeps each record's data together, unlike parallel arrays. Access with `v[i].member`.
- Sort structs with `sort(begin, end, compare)`, where `compare(a, b)` returns true if `a` comes before `b` (use `<`).
- **`enum class`** defines a type with a fixed set of named values, written `Category::Grocery`.
- Structs can have **member functions**. A `class` is a struct whose members are private by default: the start of object-oriented programming.
:::
