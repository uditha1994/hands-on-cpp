---
num: 13
title: Searching and Sorting
tagline: Finding things fast and putting things in order
learn: write linear search and binary search; explain why binary search needs sorted data and why it is so fast; write bubble sort, selection sort and insertion sort; trace each algorithm by hand; compare algorithms using Big-O; use the standard library's sort and search functions
---

## Where is the soap?

:::story
Ruwan: I have 2,000 product codes now. When a customer asks for one, your program checks them one by one. It's fast now, but my nephew says a supermarket has 50,000.

Nuwan: Your nephew is right to worry. Checking one by one is called **linear search**. There is a much faster way, but only if the codes are **sorted**. So today we learn both: how to search, and how to sort.

Amaya: Is this the Big-O thing again?

Nuwan: This is where Big-O stops being theory.
:::

## Linear search

**Linear search** checks each element in turn until it finds the target or runs out of elements. You wrote one in Chapter 11. Here it is as a reusable function:

```cpp run title=linear.cpp
#include <iostream>
#include <vector>
using namespace std;

// Returns the index of target in v, or -1 if it is not there.
int linearSearch(const vector<int> &v, int target) {
    for (size_t i = 0; i < v.size(); i++) {
        if (v[i] == target) return i;
    }
    return -1;
}

int main() {
    vector<int> codes = {1024, 3310, 2051, 1187, 4402, 2999};
    cout << linearSearch(codes, 1187) << endl;
    cout << linearSearch(codes, 5000) << endl;
    return 0;
}
```

```output
3
-1
```

- **Best case:** the target is first, 1 comparison.
- **Worst case:** the target is last or missing, n comparisons.
- So linear search is **O(n)**. It works on **any** list, sorted or not.

## Binary search: the phone book trick

Imagine finding a name in a printed phone directory. You do not start at page 1. You open it in the middle, see that your name comes later in the alphabet, and throw away the first half. Then you repeat with the remaining half. That is **binary search**.

It only works if the data is **sorted**.

1. Look at the middle element.
2. If it is the target, you are done.
3. If the target is **smaller**, search only the **left** half.
4. If the target is **larger**, search only the **right** half.
5. If there is nothing left to search, the target is not there.

```cpp run title=binary.cpp
#include <iostream>
#include <vector>
using namespace std;

int binarySearch(const vector<int> &v, int target) {
    int low = 0, high = static_cast<int>(v.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;     //@ the middle of the current range
        if (v[mid] == target) {
            return mid;
        } else if (v[mid] < target) {
            low = mid + 1;                    //@ target is in the right half
        } else {
            high = mid - 1;                   //@ target is in the left half
        }
    }
    return -1;
}

int main() {
    vector<int> codes = {1024, 1187, 2051, 2999, 3310, 4402, 5120, 6060, 7777};
    cout << binarySearch(codes, 5120) << endl;
    cout << binarySearch(codes, 3000) << endl;
    return 0;
}
```

```output
6
-1
```

### Tracing binary search

Searching for 5120 in the 9 sorted codes:

| Step | low | high | mid | v[mid] | Decision |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | 3310 | 5120 > 3310, go right: low = 5 |
| 2 | 5 | 8 | 6 | 5120 | **found** at index 6 |

Only 2 comparisons. Linear search would have needed 7. Now try 3000, which is not there:

| Step | low | high | mid | v[mid] | Decision |
|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | 3310 | 3000 < 3310, go left: high = 3 |
| 2 | 0 | 3 | 1 | 1187 | 3000 > 1187, go right: low = 2 |
| 3 | 2 | 3 | 2 | 2051 | 3000 > 2051, go right: low = 3 |
| 4 | 3 | 3 | 3 | 2999 | 3000 > 2999, go right: low = 4 |
| 5 | 4 | 3 | | | low > high: **not found** |

:::deep
Why `mid = low + (high - low) / 2` instead of `(low + high) / 2`? For huge arrays, `low + high` can be bigger than the largest `int` and overflow. The first version never does. This exact bug sat unnoticed for years in widely used library code, including Java's standard binary search, until it was reported in 2006. Small details matter at scale.
:::

### Why binary search is so fast

Each step **halves** the remaining range. Starting with n elements, after k steps about n / 2^k remain. The search ends when one element is left, so k is about **log₂ n**. Binary search is **O(log n)**.

| Number of items n | Linear search, worst case | Binary search, worst case |
|---|---|---|
| 10 | 10 | 4 |
| 1,000 | 1,000 | 10 |
| 1,000,000 | 1,000,000 | 20 |
| 1,000,000,000 | 1,000,000,000 | 30 |

A billion items in **30 comparisons**. That is the power of halving.

:::brain
If binary search is so much faster, why not always use it? What does it cost?
---solution
The data must be **sorted** first, and sorting takes time, more than a single linear search. Binary search pays off when you sort **once** and then search **many** times, as with a product catalogue. For a small list, or a list you search only once, or one that changes constantly, a simple linear search can be the better choice.
:::

## Sorting

Sorting means arranging elements in order. There are dozens of sorting algorithms. We will study three simple ones that every programmer should be able to write and trace, and then use the professional one from the standard library.

We sort in **ascending** order (smallest first) throughout. To sort descending, flip the comparison.

### Bubble sort

**Idea:** walk through the list comparing **neighbours**, and swap them if they are in the wrong order. After the first pass, the largest value has "bubbled up" to the end. Repeat for the rest.

```cpp run title=bubble.cpp
#include <iostream>
#include <vector>
#include <utility>
using namespace std;

void bubbleSort(vector<int> &v) {
    int n = v.size();
    for (int pass = 0; pass < n - 1; pass++) {
        bool swapped = false;
        for (int i = 0; i < n - 1 - pass; i++) {    //@ the last 'pass' items are already in place
            if (v[i] > v[i + 1]) {
                swap(v[i], v[i + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;                         //@ no swaps: the list is sorted, stop early
    }
}

int main() {
    vector<int> v = {5, 1, 4, 2, 8};
    bubbleSort(v);
    for (int x : v) cout << x << " ";
    cout << endl;
    return 0;
}
```

```output
1 2 4 5 8 
```

Tracing the first pass on `{5, 1, 4, 2, 8}`:

| Compare | Before | Swap? | After |
|---|---|---|---|
| 5 and 1 | 5 1 4 2 8 | yes | 1 5 4 2 8 |
| 5 and 4 | 1 5 4 2 8 | yes | 1 4 5 2 8 |
| 5 and 2 | 1 4 5 2 8 | yes | 1 4 2 5 8 |
| 5 and 8 | 1 4 2 5 8 | no | 1 4 2 5 8 |

After pass 1, 8 is in its final place. Pass 2 gives `1 2 4 5 8`. Pass 3 makes no swaps, so the early exit stops the algorithm.

### Selection sort

**Idea:** find the **smallest** element and swap it into position 0. Then find the smallest of the rest and swap it into position 1. And so on.

```cpp run title=selection.cpp
#include <iostream>
#include <vector>
#include <utility>
using namespace std;

void selectionSort(vector<int> &v) {
    int n = v.size();
    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {        //@ find the smallest in v[i..n-1]
            if (v[j] < v[minIndex]) minIndex = j;
        }
        swap(v[i], v[minIndex]);                 //@ one swap per pass
    }
}

int main() {
    vector<int> v = {64, 25, 12, 22, 11};
    selectionSort(v);
    for (int x : v) cout << x << " ";
    cout << endl;
    return 0;
}
```

```output
11 12 22 25 64 
```

| Pass i | Smallest of the unsorted part | Array after the swap |
|---|---|---|
| 0 | 11 | **11** 25 12 22 64 |
| 1 | 12 | 11 **12** 25 22 64 |
| 2 | 22 | 11 12 **22** 25 64 |
| 3 | 25 | 11 12 22 **25** 64 |

### Insertion sort

**Idea:** the way most people sort playing cards in their hand. Take the next card and slide it left into its correct place among the cards already sorted.

```cpp run title=insertion.cpp
#include <iostream>
#include <vector>
using namespace std;

void insertionSort(vector<int> &v) {
    for (size_t i = 1; i < v.size(); i++) {
        int key = v[i];                       //@ the card we are placing
        int j = static_cast<int>(i) - 1;
        while (j >= 0 && v[j] > key) {        //@ shift bigger cards one place right
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = key;                       //@ drop the card into the gap
    }
}

int main() {
    vector<int> v = {12, 11, 13, 5, 6};
    insertionSort(v);
    for (int x : v) cout << x << " ";
    cout << endl;
    return 0;
}
```

```output
5 6 11 12 13 
```

Notice the guard `j >= 0 &&` on the left of the `&&`. Short-circuit evaluation (Chapter 6) stops `v[j]` from being read when `j` is -1.

### Comparing the three

| Algorithm | Worst case | Best case | Notes |
|---|---|---|---|
| Bubble sort | O(n²) | O(n) with the early exit, on already sorted data | Easy to understand; slow in practice |
| Selection sort | O(n²) | O(n²) | Always the same work; makes at most n − 1 swaps |
| Insertion sort | O(n²) | O(n) on sorted data | Very good for small or nearly sorted lists |
| `std::sort` | O(n log n) | O(n log n) | What professionals use |

O(n²) is fine for a hundred items. For a million items it means around a trillion steps, which can take many minutes. Faster algorithms such as **merge sort** and **quicksort** run in O(n log n), roughly 20 million steps for a million items. You will study them in a Data Structures and Algorithms course.

:::nodumb
Q: If std::sort exists, why learn bubble sort?
A: For the same reason you learn long division before using a calculator. Writing and tracing these algorithms trains you to think about loops, indexes, swaps and efficiency. They are also very common exam and interview questions. In real projects, use the library.

Q: What does "stable" sorting mean?
A: A **stable** sort keeps equal elements in their original order. It matters when you sort records, for example sorting customers by town and wanting customers in the same town to stay in alphabetical order. Bubble sort and insertion sort are stable; selection sort (as written above) is not. `std::sort` is not guaranteed to be stable, but `std::stable_sort` is.
:::

## The standard library does it for you

The `<algorithm>` header contains fast, well-tested versions of these operations:

```cpp run title=stl_algorithms.cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <functional>
using namespace std;

int main() {
    vector<int> v = {4402, 1024, 3310, 2051, 1187};

    sort(v.begin(), v.end());                          //@ ascending
    for (int x : v) cout << x << " ";
    cout << endl;

    cout << boolalpha << binary_search(v.begin(), v.end(), 2051) << endl;   //@ needs sorted data

    auto it = find(v.begin(), v.end(), 3310);          //@ linear search
    if (it != v.end()) cout << "3310 is at index " << (it - v.begin()) << endl;

    sort(v.begin(), v.end(), greater<int>());          //@ descending
    for (int x : v) cout << x << " ";
    cout << endl;

    cout << "Largest: " << *max_element(v.begin(), v.end()) << endl;
    return 0;
}
```

```output
1024 1187 2051 3310 4402 
true
3310 is at index 3
4402 3310 2051 1187 1024 
Largest: 4402
```

`v.begin()` and `v.end()` are **iterators**: markers for the start and one-past-the-end of the vector. Library algorithms take a pair of iterators so they can work on any part of any container. `find` returns an iterator to the match, or `v.end()` if there is none, and `*it` reads the element it points to. Iterators are closely related to the pointers you will meet in Chapter 15.

Sorting works on strings too, alphabetically (by character code, so capitals first):

```cpp run title=sort_names.cpp
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    vector<string> items = {"Sugar", "rice", "Dhal", "Tea", "Biscuits"};
    sort(items.begin(), items.end());
    for (const string &s : items) cout << s << " ";
    cout << endl;
    return 0;
}
```

```output
Biscuits Dhal Sugar Tea rice 
```

`rice` comes last because lowercase letters have larger codes than capitals. Chapter 14 shows how to sort with your own comparison rule, such as "ignore case" or "sort products by price".

:::sharpen Trace the sorts
Show the array after **each pass** of bubble sort, selection sort and insertion sort, for the input `{7, 3, 9, 1, 5}`.
---solution
**Bubble sort** (each pass moves the largest remaining value to the end)

- Pass 1: 3 7 1 5 9
- Pass 2: 3 1 5 7 9
- Pass 3: 1 3 5 7 9
- Pass 4: no swaps, stop.

**Selection sort** (each pass places the next smallest value)

- i = 0: 1 3 9 7 5
- i = 1: 1 3 9 7 5 (3 is already in place)
- i = 2: 1 3 5 7 9
- i = 3: 1 3 5 7 9

**Insertion sort** (each pass inserts the next value into the sorted left part)

- insert 3: 3 7 9 1 5
- insert 9: 3 7 9 1 5
- insert 1: 1 3 7 9 5
- insert 5: 1 3 5 7 9
:::

:::compiler
This binary search has two bugs that make it loop forever or miss values. Find them.

```cpp error
int binarySearch(const vector<int> &v, int target) {
    int low = 0, high = v.size();
    while (low < high) {
        int mid = (low + high) / 2;
        if (v[mid] == target) return mid;
        else if (v[mid] < target) low = mid;
        else high = mid - 1;
    }
    return -1;
}
```
---solution
1. `low = mid;` can loop forever. When `low` and `mid` are equal, the range never shrinks. It must be `low = mid + 1;`.
2. The bounds are mixed up. `high = v.size()` treats `high` as one past the end (an "exclusive" bound), with `while (low < high)`, but then `high = mid - 1` treats it as inclusive. This can skip the element at `mid - 1`. Use one convention consistently: either `high = v.size() - 1`, `while (low <= high)` and `high = mid - 1` (as in this chapter), or exclusive bounds with `high = mid`.

Off-by-one errors in binary search are famous. Always test it with targets at the very start and end, in the middle, missing values below and above the range, and an empty vector.
:::

:::quiz
? What must be true before you can use binary search?
- The data must contain no duplicates
* The data must be sorted
- The data must be in an array, not a vector
- The data must have an even number of elements
> Binary search relies on order to throw away half of the data each step.

? About how many comparisons does binary search need, at most, for 1,000,000 sorted items?
- 1,000,000
- 1,000
* 20
- 2
> log₂ of a million is about 20.

? After the first pass of bubble sort (ascending), where is the largest element?
- At index 0
- In the middle
* At the end
- It depends on the data
> Each pass carries the largest remaining value to the end.

? Which sort makes at most n − 1 swaps?
- Bubble sort
* Selection sort
- Insertion sort
- None of them
> Selection sort does one swap per pass.

? Which call sorts `vector<int> v` in descending order?
- `sort(v)`
- `sort(v.end(), v.begin())`
* `sort(v.begin(), v.end(), greater<int>())`
- `v.sort(desc)`
> The third argument is the comparison to use.
:::

:::lab Price list tools
1. Write a program that reads product prices into a `vector<double>` until the user enters 0.
2. Sort them with **your own** insertion sort, then print them.
3. Ask for a budget and use **your own** binary search variant to find **how many** products cost at most the budget. (Hint: find the first index whose price is greater than the budget.)
4. Add a counter to your sort that counts comparisons. Try it on a list that is already sorted and on a list in reverse order. What do you notice?
5. Check your results against `std::sort` and `std::upper_bound`.
---solution
```cpp run title=price_tools.cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

long long comparisons = 0;

void insertionSort(vector<double> &v) {
    for (size_t i = 1; i < v.size(); i++) {
        double key = v[i];
        int j = static_cast<int>(i) - 1;
        while (j >= 0) {
            comparisons++;
            if (v[j] <= key) break;
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = key;
    }
}

// Number of prices that are <= budget, in a sorted vector.
int countAffordable(const vector<double> &v, double budget) {
    int low = 0, high = v.size();        // search in [low, high)
    while (low < high) {
        int mid = low + (high - low) / 2;
        if (v[mid] <= budget) low = mid + 1;
        else high = mid;
    }
    return low;                          // first index with price > budget
}

int main() {
    vector<double> prices;
    double p;
    cout << "Prices (0 to finish): ";
    while (cin >> p && p != 0) prices.push_back(p);

    insertionSort(prices);
    for (double x : prices) cout << x << " ";
    cout << "\n(" << comparisons << " comparisons)" << endl;

    double budget;
    cout << "Budget: ";
    cin >> budget;
    int n = countAffordable(prices, budget);
    cout << n << " products cost Rs. " << budget << " or less" << endl;

    int check = upper_bound(prices.begin(), prices.end(), budget) - prices.begin();
    cout << "std::upper_bound agrees: " << boolalpha << (n == check) << endl;
    return 0;
}
```

```output
Prices (0 to finish): [[690 145 230.5 1200 99 450 0]]
99 145 230.5 450 690 1200 
(11 comparisons)
Budget: [[500]]
4 products cost Rs. 500 or less
std::upper_bound agrees: true
```
On already sorted input, insertion sort needs only n − 1 comparisons (one per element). On reversed input it needs about n²/2. Same algorithm, very different amounts of work. That is the difference between best case and worst case.
:::

:::bullets
- **Linear search** checks every element: O(n), works on any data.
- **Binary search** halves the range each step: O(log n), but the data must be **sorted**.
- Use `mid = low + (high - low) / 2`, and update with `mid + 1` / `mid - 1` so the range always shrinks.
- **Bubble sort** swaps neighbours; **selection sort** selects the smallest; **insertion sort** inserts each element into a sorted part. All are O(n²) in the worst case.
- Insertion sort and bubble sort (with early exit) are fast on nearly sorted data.
- In real code, use `<algorithm>`: `sort`, `binary_search`, `find`, `max_element`, `upper_bound`. They work with **iterators** such as `v.begin()` and `v.end()`.
:::
