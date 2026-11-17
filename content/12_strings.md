---
num: 12
title: Strings and Characters
tagline: Working with text, one character at a time
learn: treat a string as a sequence of characters; search, cut, join and change strings with the most useful member functions; classify and convert characters with cctype; convert between numbers and text; split text into parts with stringstream; know what C-style strings are and why std::string is safer
---

## Codes on every shelf

:::story
Ruwan: My supplier labels every product with a code like `RS-1024-G`. RS is the shop, the number is the product, the last letter is the category. Can your program read these?

Amaya: It can store them as strings, sure...

Nuwan: Storing is easy. The real question is: can it **understand** them? Pull out the number, check the letter, spot a typo? That is what this chapter is about.
:::

## A string is a sequence of characters

A `string` (from `<string>`) holds a sequence of `char` values. Each character has an index, starting at 0, exactly like an array:

```cpp check
string code = "RS-1024-G";
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| Character | `R` | `S` | `-` | `1` | `0` | `2` | `4` | `-` | `G` |

```cpp run title=string_basics.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string code = "RS-1024-G";
    cout << "Length: " << code.length() << endl;   //@ .size() means the same
    cout << "First:  " << code[0] << endl;
    cout << "Last:   " << code[code.length() - 1] << endl;
    code[8] = 'H';                                  //@ strings can be changed
    cout << "Now:    " << code << endl;
    for (char c : code) {                           //@ visit every character
        cout << c << ' ';
    }
    cout << endl;
    return 0;
}
```

```output
Length: 9
First:  R
Last:   G
Now:    RS-1024-H
R S - 1 0 2 4 - H 
```

Like vectors, strings offer `.at(i)`, which checks the index and throws an exception if it is out of range, while `[i]` does not check.

## Joining and comparing

```cpp run title=join.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string first = "Ruwan", shop = "Stores";
    string name = first + " " + shop;       //@ + joins strings
    name += ", Kandy";                      //@ += appends
    name += '!';                            //@ you can append a single char
    cout << name << endl;
    cout << boolalpha << (first == "Ruwan") << endl;
    cout << name.empty() << endl;           //@ true only for ""
    return 0;
}
```

```output
Ruwan Stores, Kandy!
true
false
```

:::watch
You cannot join two **string literals** with `+`: `"Ruwan" + " Stores"` does not compile, because neither side is a `std::string`. At least one side of each `+` must be a `string` variable or `string("...")`. `name + " " + "Kandy"` works, because it is worked out left to right and the left side is always a `string`.
:::

## Finding things: find and npos

`s.find(x)` searches for a character or a piece of text and returns the **index** where it starts. If it is not found, it returns a special value, `string::npos`.

```cpp run title=find.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string address = "No. 12, Peradeniya Road, Kandy";
    size_t pos = address.find("Road");
    cout << "Road starts at " << pos << endl;
    if (address.find("Colombo") == string::npos) {     //@ the "not found" check
        cout << "Not a Colombo address" << endl;
    }
    cout << "First comma: " << address.find(',') << endl;
    cout << "Last comma:  " << address.rfind(',') << endl;   //@ search from the end
    cout << "Comma after 10: " << address.find(',', 10) << endl;  //@ start searching at index 10
    return 0;
}
```

```output
Road starts at 19
Not a Colombo address
First comma: 6
Last comma:  23
Comma after 10: 23
```

:::watch
`find` returns a `size_t` (unsigned). Always compare its result with `string::npos`, never with -1 stored in an `int`, and never treat it as true/false: `if (s.find("x"))` is **true** when "x" is not found (npos is a huge number) and **false** when "x" is found at index 0. Write `if (s.find("x") != string::npos)`.
:::

## Cutting and changing: substr, erase, insert, replace

| Function | What it does | `s = "Ruwan Stores"` |
|---|---|---|
| `s.substr(pos, len)` | copy `len` characters from `pos` | `s.substr(6, 6)` is `"Stores"` |
| `s.substr(pos)` | copy from `pos` to the end | `s.substr(6)` is `"Stores"` |
| `s.erase(pos, len)` | remove `len` characters from `pos` | `s.erase(0, 6)` makes `"Stores"` |
| `s.insert(pos, t)` | insert `t` before `pos` | `s.insert(0, ">> ")` makes `">> Ruwan Stores"` |
| `s.replace(pos, len, t)` | replace `len` characters at `pos` with `t` | `s.replace(0, 5, "Saman")` makes `"Saman Stores"` |

`substr` returns a **new** string and leaves `s` alone. `erase`, `insert` and `replace` **change** `s` itself.

### Worked example: decoding a product code

```cpp run title=decode.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string code;
    cout << "Product code: ";
    cin >> code;

    size_t firstDash = code.find('-');
    size_t secondDash = code.find('-', firstDash + 1);
    if (firstDash == string::npos || secondDash == string::npos) {
        cout << "Invalid code: expected two dashes." << endl;
        return 1;
    }
    string shop = code.substr(0, firstDash);
    string number = code.substr(firstDash + 1, secondDash - firstDash - 1);
    string category = code.substr(secondDash + 1);

    cout << "Shop:     " << shop << endl;
    cout << "Product:  " << number << endl;
    cout << "Category: " << category << endl;
    return 0;
}
```

```output
Product code: [[RS-1024-G]]
Shop:     RS
Product:  1024
Category: G
```

The length of the middle part is `secondDash - firstDash - 1`: the distance between the dashes, minus the dash itself. Draw the index table if this is not obvious. Working out substring positions on paper is normal, even for experienced programmers.

## Characters: the cctype toolkit

The `<cctype>` header has functions for testing and converting single characters:

| Function | True when the character is... | Example |
|---|---|---|
| `isdigit(c)` | a digit `0` to `9` | `isdigit('7')` |
| `isalpha(c)` | a letter | `isalpha('g')` |
| `isalnum(c)` | a letter or digit | `isalnum('_')` is false |
| `isupper(c)`, `islower(c)` | uppercase / lowercase letter | `isupper('G')` |
| `isspace(c)` | whitespace (space, tab, newline...) | `isspace(' ')` |
| `ispunct(c)` | punctuation | `ispunct('!')` |
| `toupper(c)`, `tolower(c)` | (converts) | `toupper('g')` gives `'G'` |

```cpp run title=cctype.cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string text = "Ruwan Stores: open 7 days!";
    int letters = 0, digits = 0, spaces = 0, others = 0;
    for (char c : text) {
        if (isalpha(c)) letters++;
        else if (isdigit(c)) digits++;
        else if (isspace(c)) spaces++;
        else others++;
    }
    cout << letters << " letters, " << digits << " digits, "
         << spaces << " spaces, " << others << " others" << endl;

    string shout = text;
    for (char &c : shout) {            //@ & so we change the real characters
        c = toupper(c);
    }
    cout << shout << endl;
    return 0;
}
```

```output
19 letters, 1 digits, 4 spaces, 2 others
RUWAN STORES: OPEN 7 DAYS!
```

:::watch
`toupper` returns an `int`, not a `char`. `cout << toupper('a');` prints **65**. Store the result in a `char` first (`c = toupper(c);`) or cast it: `cout << (char)toupper('a');`.

Also, strictly speaking, these functions expect values that fit in an `unsigned char`. For plain English text this never matters. If your program handles characters outside basic ASCII, write `toupper(static_cast<unsigned char>(c))` to be completely safe.
:::

### Digit characters to numbers

The character `'7'` is not the number 7; in ASCII it is 55. But the digits `'0'` to `'9'` have consecutive codes, so **subtracting `'0'`** converts a digit character to its value:

```cpp run title=digit_chars.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string barcode = "4792081";
    int sum = 0;
    for (char c : barcode) {
        sum += c - '0';            //@ '7' - '0' is 7
    }
    cout << "Digit sum: " << sum << endl;
    char d = '0' + 5;              //@ and back again: the character '5'
    cout << d << endl;
    return 0;
}
```

```output
Digit sum: 31
5
```

## Converting between numbers and strings

| From | To | Use |
|---|---|---|
| `int`, `double` | `string` | `to_string(42)` gives `"42"`; `to_string(12.5)` gives `"12.500000"` |
| `string` | `int` | `stoi("42")` gives 42 |
| `string` | `double` | `stod("3.75")` gives 3.75 |
| `string` | `long long` | `stoll("2147483648")` |

```cpp run title=convert.cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string qtyText = "12";
    string priceText = "230.50";
    double total = stoi(qtyText) * stod(priceText);
    string label = "Total: Rs. " + to_string(total);
    cout << label << endl;
    cout << stoi("42 kg") << endl;      //@ reads the leading number and stops at the space
    return 0;
}
```

```output
Total: Rs. 2766.000000
42
```

:::watch
`stoi` and `stod` **throw an exception** if the text does not start with a number at all (`stoi("abc")`), or if the number is too big for the type. An uncaught exception stops your program. So check the text first (for example, that every character `isdigit`), or learn to catch exceptions with `try` and `catch` in a later course. Also note that `to_string(double)` always gives six decimal places; use `ostringstream` with `fixed` and `setprecision` (next section) for nicer formatting.
:::

## Splitting text with stringstream

A **string stream** lets you use `>>` and `<<` on a string, as if it were `cin` or `cout`. It lives in `<sstream>`. This is the cleanest way to split a line into pieces.

```cpp run title=split.cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    string line = "Rice 42 230.50";
    istringstream in(line);           //@ an input stream that reads from line
    string name;
    int stock;
    double price;
    in >> name >> stock >> price;     //@ exactly like cin >>
    cout << name << " | " << stock << " | " << price << endl;

    string csv = "Dhal,15,320";       //@ comma-separated values
    istringstream parts(csv);
    string field;
    while (getline(parts, field, ',')) {   //@ getline with a delimiter: split on commas
        cout << "[" << field << "]";
    }
    cout << endl;
    return 0;
}
```

```output
Rice | 42 | 230.5
[Dhal][15][320]
```

`getline(stream, s, ',')` reads up to the next **comma** instead of the next newline. You will use exactly this technique in Chapter 16 to read data files in **CSV** format, the format spreadsheets export.

The output version, `ostringstream`, builds a string using `<<`, with all the formatting tools from Chapter 4:

```cpp run title=ostringstream.cpp
#include <iostream>
#include <sstream>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    ostringstream out;
    out << fixed << setprecision(2) << "Rs. " << 2766.0;
    string label = out.str();          //@ get the finished string
    cout << label << " (" << label.length() << " characters)" << endl;
    return 0;
}
```

```output
Rs. 2766.00 (11 characters)
```

## Worked example: is it a palindrome?

A palindrome reads the same forwards and backwards, ignoring case, spaces and punctuation: "Malayalam", "Never odd or even".

```cpp run title=palindrome.cpp
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

string cleaned(const string &s) {
    string result;
    for (char c : s) {
        if (isalnum(c)) result += tolower(c);   //@ keep letters and digits, lowercase
    }
    return result;
}

bool isPalindrome(const string &s) {
    string t = cleaned(s);
    for (size_t i = 0, j = t.length(); i + 1 < j; i++, j--) {   //@ two pointers
        if (t[i] != t[j - 1]) return false;
    }
    return true;
}

int main() {
    string line;
    cout << "Text: ";
    getline(cin, line);
    cout << (isPalindrome(line) ? "Palindrome!" : "Not a palindrome.") << endl;
    return 0;
}
```

```output
Text: [[Never odd or even]]
Palindrome!
```

Another way is to build a reversed copy (`string r(t.rbegin(), t.rend());`) and compare. The two-pointer loop does it without any extra copy.

## C-style strings: the old way

Before `std::string`, C programs stored text as **arrays of `char`** ending with a special **null character** `'\0'`. You will still meet them, because string literals like `"Hello"` are C-style strings, and older code and libraries use them.

```cpp check
char shop[] = "Ruwan";      // 6 chars: 'R' 'u' 'w' 'a' 'n' '\0'
```

| Index | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `shop[i]` | `R` | `u` | `w` | `a` | `n` | `\0` |

C-style strings are fixed-size arrays, so writing a longer name into one can overflow it, and functions like `strcpy` and `strcat` from `<cstring>` do not check sizes. That is a classic source of buffer overflow bugs.

:::industry
In modern C++, use `std::string` for text. It manages its own memory, grows as needed, knows its length and supports `+`, `==` and all the functions in this chapter. If you are handed a C-style string, you can turn it into a `std::string` simply by assigning it: `string s = shop;`. Going the other way, `s.c_str()` gives a C-style view of a `std::string` for old library functions that need one.
:::

:::compiler
What is wrong with each line?

```cpp error
string a = "Ruwan" + " Stores";
string b = "Kandy";
if (b.find("K")) cout << "has K";
char c = "K";
cout << toupper(b[0]);
string d = b.substr(10);
```
---solution
1. Two string literals cannot be joined with `+`. Write `string a = string("Ruwan") + " Stores";` or simply `"Ruwan Stores"`.
2. Line 2 is fine.
3. `b.find("K")` is 0 (found at the start), which converts to **false**, so nothing prints. Compare with `string::npos`.
4. `"K"` is a string literal; a `char` needs `'K'`.
5. Prints `75` (the code for 'K'), because `toupper` returns an `int`. Cast it to `char`.
6. `substr(10)` on a 5-character string throws `std::out_of_range`, because the start position is past the end.
:::

:::quiz
? What is `string("Kandy").substr(1, 3)`?
- "Kan"
* "and"
- "andy"
- "ndy"
> Start at index 1 ('a') and take 3 characters.

? What does find return when the text is not found?
- -1
- 0
* string::npos
- false
> npos is a special, very large value of type size_t.

? What is printed by `cout << '7' - '0';`?
- '7'
* 7
- 55
- 0
> Digit characters have consecutive codes, so subtracting '0' gives the digit's value.

? Which header provides isdigit and toupper?
- string
* cctype
- cmath
- sstream
> The character classification functions live in cctype.

? What is `stoi("15 apples")`?
* 15
- An exception is thrown
- 0
- "15"
> stoi reads the leading number and stops at the first character that cannot be part of it.
:::

:::lab Customer name and code checker
Uncle Ruwan's customers register with a name and a phone number. Write a program with these functions and test each one:

1. `string toTitleCase(string s)`: `"fATHIMA rizwan"` becomes `"Fathima Rizwan"` (first letter of each word upper case, the rest lower case).
2. `bool isValidPhone(const string &s)`: true if the text is exactly 10 characters, all digits, starting with `0`.
3. `int countWords(const string &s)`: counts words separated by spaces (use `istringstream`).
4. `string initials(const string &name)`: `"Fathima Rizwan"` gives `"F.R."`.
5. In `main`, read a full name with `getline`, then a phone number, and print a registration card or a clear error message.
---solution
```cpp run title=register.cpp
#include <iostream>
#include <sstream>
#include <string>
#include <cctype>
using namespace std;

string toTitleCase(string s) {
    bool startOfWord = true;
    for (char &c : s) {
        if (isspace(c)) {
            startOfWord = true;
        } else if (startOfWord) {
            c = toupper(c);
            startOfWord = false;
        } else {
            c = tolower(c);
        }
    }
    return s;
}

bool isValidPhone(const string &s) {
    if (s.length() != 10 || s[0] != '0') return false;
    for (char c : s) {
        if (!isdigit(c)) return false;
    }
    return true;
}

int countWords(const string &s) {
    istringstream in(s);
    string word;
    int count = 0;
    while (in >> word) count++;
    return count;
}

string initials(const string &name) {
    istringstream in(name);
    string word, result;
    while (in >> word) {
        result += toupper(word[0]);
        result += '.';
    }
    return result;
}

int main() {
    string name, phone;
    cout << "Full name: ";
    getline(cin, name);
    cout << "Phone: ";
    cin >> phone;
    name = toTitleCase(name);
    if (countWords(name) < 2) {
        cout << "Please enter at least a first name and a surname." << endl;
        return 1;
    }
    if (!isValidPhone(phone)) {
        cout << "Phone numbers must be 10 digits starting with 0." << endl;
        return 1;
    }
    cout << "\nCustomer: " << name << " (" << initials(name) << ")" << endl;
    cout << "Phone:    " << phone << endl;
    return 0;
}
```

```output
Full name: [[fATHIMA   rizwan]]
Phone: [[0771234567]]

Customer: Fathima   Rizwan (F.R.)
Phone:    0771234567
```
Notice the extra spaces the user typed are still there. As an extension, write `string squeezeSpaces(const string &s)` that rebuilds the name from the words read by `istringstream`, with exactly one space between them.
:::

:::bullets
- A `string` is a sequence of `char`s with indexes from 0. Use `.length()`, `[i]` and `.at(i)`.
- Join with `+` and `+=` (one side must be a `string`). Compare with `==` and `<`.
- `find` returns an index or `string::npos`; always compare with `npos`.
- `substr(pos, len)` copies part of a string. `erase`, `insert` and `replace` change it.
- `<cctype>`: `isdigit`, `isalpha`, `isspace`, `toupper`, `tolower`. `toupper` returns an `int`.
- `c - '0'` turns a digit character into its value.
- `to_string`, `stoi` and `stod` convert between numbers and text. `stoi` throws on bad input.
- `istringstream` splits text with `>>` or `getline(stream, field, ',')`. `ostringstream` builds formatted strings.
- C-style strings are `char` arrays ending in `'\0'`. Prefer `std::string`.
:::
