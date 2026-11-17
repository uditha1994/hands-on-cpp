---
num: 16
title: Working with Files
tagline: Programs that remember, even after you close them
learn: write text files with ofstream; choose between overwrite and append modes; always check that a file opened; read files word by word, line by line and value by value with ifstream; avoid the eof() loop trap; read and write CSV files; load data into a vector of structs and save it back
---

## The program with amnesia

:::story
Ruwan: Yesterday I typed in all forty products. Prices, stock, everything. Today I opened the program and it was all gone!

Amaya: Oh no. Everything was stored in variables. When the program ended, the memory was freed...

Nuwan: Variables live in RAM, which is wiped when a program ends. If you want data to survive, you must save it to **storage**: a file on the disk. Today, the Ruwan Stores system gets a memory.
:::

Everything so far has been **volatile**: it disappears when the program ends. A **file** on a disk (or SSD) is **persistent**: it stays there after your program closes, after the computer restarts, and until someone deletes it.

## File streams

You already know streams: `cout` and `cin`. C++ treats files exactly the same way, using three types from `<fstream>`:

| Type | Direction | Think of it as |
|---|---|---|
| `ofstream` | **o**utput: program to file | a `cout` that writes into a file |
| `ifstream` | **i**nput: file to program | a `cin` that reads from a file |
| `fstream` | both | used for more advanced cases |

Everything you know about `<<`, `>>`, `getline`, `fixed` and `setw` works on file streams too.

## Writing a file with ofstream

```cpp run expectfile=welcome.txt title=write_file.cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    ofstream outFile("welcome.txt");          //@ open (and create) the file
    if (!outFile) {                           //@ always check!
        cout << "Could not open welcome.txt" << endl;
        return 1;
    }
    outFile << "Ruwan Stores" << endl;        //@ exactly like cout
    outFile << "Open 7am to 9pm" << endl;
    outFile << "Items in stock: " << 42 << endl;
    outFile.close();                          //@ finish writing and release the file
    cout << "Saved." << endl;
    return 0;
}
```

```output
Saved.
```

After running it, a file called `welcome.txt` appears **in the program's working directory** (usually the folder you ran it from). Open it in any text editor:

```file welcome.txt result
Ruwan Stores
Open 7am to 9pm
Items in stock: 42
```

### Why check that the file opened?

Opening a file can fail for reasons outside your program's control: the folder does not exist, you do not have permission to write there, the disk is full, or (when reading) the file simply is not there. If you do not check, a failed stream **fails silently**: every `<<` does nothing, and your program reports success while saving nothing at all.

`if (!outFile)` is true when the stream is in a failed state. You will also see `if (!outFile.is_open())`, which checks specifically whether opening worked.

:::nodumb
Q: What does close() actually do? Do I need it?
A: Writing to a file is **buffered**: data is collected in memory and written to the disk in chunks, because disks are slow. `close()` flushes the buffer to the disk and releases the file. If you forget, the stream's destructor closes the file automatically when `outFile` goes out of scope (RAII again, Chapter 15). Calling `close()` yourself is still good practice when you are finished with a file but the function keeps running, for example before reopening the same file for reading.

Q: Where exactly does the file go?
A: A bare name like `"welcome.txt"` is a **relative path**: relative to the program's **current working directory**. In a terminal that is the folder you ran the program from. In an IDE it may be the project folder or a build folder, which surprises many students. You can also give a full path, such as `"C:/shop/welcome.txt"` (forward slashes work on Windows too) or `"/home/amaya/shop/welcome.txt"`.
:::

## Overwrite or append?

By default, opening an `ofstream` **erases** the file's old contents and starts fresh. That is called **truncate** mode. To **add to the end** instead, open the file in **append** mode with `ios::app`:

```cpp run expectfile=sales_log.txt title=append.cpp
#include <iostream>
#include <fstream>
using namespace std;

void logSale(const string &item, double amount) {
    ofstream log("sales_log.txt", ios::app);     //@ append: keep what is already there
    if (!log) {
        cout << "Could not open log" << endl;
        return;
    }
    log << item << " " << amount << endl;
}                                                 //@ log closes automatically here

int main() {
    ofstream fresh("sales_log.txt");              //@ start a new log (this erases the old one)
    fresh << "SALES LOG" << endl;
    fresh.close();

    logSale("Rice", 922);
    logSale("Tea", 520);
    logSale("Soap", 435);
    cout << "Logged 3 sales." << endl;
    return 0;
}
```

```output
Logged 3 sales.
```

```file sales_log.txt result
SALES LOG
Rice 922
Tea 520
Soap 435
```

| Mode | Code | If the file exists | If it does not exist |
|---|---|---|---|
| Overwrite (default) | `ofstream f("x.txt");` | its contents are **erased** | it is created |
| Append | `ofstream f("x.txt", ios::app);` | new data goes at the **end** | it is created |

:::watch
Opening a file for writing **without** `ios::app` destroys its old contents immediately, the moment the file is opened, even if you never write anything. Many students have wiped their own data files this way. Decide deliberately: is this program creating a new file, or adding to an existing one?
:::

## Reading a file with ifstream

Here is the stock file we will use for the rest of this chapter:

```file stock.txt seed
Rice 42 230.50
Oil 8 690.00
Soap 25 145.00
Tea 4 520.00
```

### Reading value by value

Just like `cin >>`, an `ifstream` with `>>` skips whitespace (spaces **and** newlines) and reads one value at a time. The loop condition `while (inFile >> name >> qty >> price)` reads one whole record, and becomes false when there is nothing more to read (or the data is bad):

```cpp run title=read_values.cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream inFile("stock.txt");
    if (!inFile) {
        cout << "stock.txt not found." << endl;
        return 1;
    }
    string name;
    int qty;
    double price;
    double totalValue = 0;
    while (inFile >> name >> qty >> price) {         //@ the read IS the loop condition
        cout << name << ": " << qty << " x " << price << endl;
        totalValue += qty * price;
    }
    cout << "Total stock value: " << totalValue << endl;
    return 0;
}
```

```output
Rice: 42 x 230.5
Oil: 8 x 690
Soap: 25 x 145
Tea: 4 x 520
Total stock value: 20906
```

:::watch
**Do not write `while (!inFile.eof())`.** It is one of the most common file bugs. `eof()` only becomes true **after** a read has already tried and failed to go past the end. So the loop runs one extra time: the last read fails, the variables keep their old values, and the last record gets processed **twice**. Always make the read itself the loop condition, as above.
:::

### Reading line by line

When each line is a unit, such as a sentence or an address with spaces, use `getline`:

```cpp run title=read_lines.cpp
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ifstream inFile("stock.txt");
    if (!inFile) {
        cout << "stock.txt not found." << endl;
        return 1;
    }
    string line;
    int lineNo = 0;
    while (getline(inFile, line)) {
        lineNo++;
        cout << lineNo << ": " << line << endl;
    }
    return 0;
}
```

```output
1: Rice 42 230.50
2: Oil 8 690.00
3: Soap 25 145.00
4: Tea 4 520.00
```

### Which way to read?

| File layout | Best approach |
|---|---|
| Values separated by spaces, no spaces inside values | `while (in >> a >> b >> c)` |
| Each line is one item of text | `while (getline(in, line))` |
| Each line is a record with fields that may contain spaces | `getline` each line, then split it (CSV, next section) |

## CSV files: data that spreadsheets understand

The space-separated format breaks as soon as a product name contains a space ("Red Rice 1kg"). The standard fix is **CSV** (comma-separated values): one record per line, with fields separated by commas. Excel, Google Sheets and databases can all import and export CSV.

```file products.csv seed
name,price,stock
Red Rice 1kg,230.50,42
Coconut Oil 750ml,690.00,8
Soap Bar,145.00,25
Ceylon Tea 200g,520.00,4
```

The first line is a **header** naming the columns. To read it, combine `getline` for lines with `getline(..., ',')` from Chapter 12 to split each line on commas.

```cpp run title=read_csv.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

vector<Product> loadProducts(const string &filename) {
    vector<Product> items;
    ifstream in(filename);
    if (!in) return items;                       //@ empty vector if the file is missing

    string line;
    getline(in, line);                           //@ skip the header line
    while (getline(in, line)) {
        if (line.empty()) continue;              //@ ignore blank lines
        istringstream fields(line);
        string name, priceText, stockText;
        getline(fields, name, ',');
        getline(fields, priceText, ',');
        getline(fields, stockText, ',');
        Product p;
        p.name = name;
        p.price = stod(priceText);
        p.stock = stoi(stockText);
        items.push_back(p);
    }
    return items;
}

int main() {
    vector<Product> items = loadProducts("products.csv");
    if (items.empty()) {
        cout << "No products loaded." << endl;
        return 1;
    }
    cout << "Loaded " << items.size() << " products:" << endl;
    for (const Product &p : items) {
        cout << " - " << p.name << " (Rs. " << p.price << ", " << p.stock << " in stock)" << endl;
    }
    return 0;
}
```

```output
Loaded 4 products:
 - Red Rice 1kg (Rs. 230.5, 42 in stock)
 - Coconut Oil 750ml (Rs. 690, 8 in stock)
 - Soap Bar (Rs. 145, 25 in stock)
 - Ceylon Tea 200g (Rs. 520, 4 in stock)
```

:::watch
This simple CSV reader assumes that no field contains a comma. Real CSV allows fields like `"Biscuits, chocolate"` in quotes, and then a plain split on commas gives wrong results. For real projects, either forbid commas in your data, or use a proper CSV library. Also, `stod` and `stoi` throw an exception on a corrupted line. A robust loader checks each field before converting it.
:::

### Writing CSV

Saving is the mirror image: write the header, then one line per record.

```cpp run expectfile=products_out.csv title=save_csv.cpp
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <vector>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

bool saveProducts(const string &filename, const vector<Product> &items) {
    ofstream out(filename);
    if (!out) return false;
    out << "name,price,stock" << endl;
    out << fixed << setprecision(2);
    for (const Product &p : items) {
        out << p.name << "," << p.price << "," << p.stock << endl;
    }
    return true;
}

int main() {
    vector<Product> items = {{"Dhal 500g", 320, 15}, {"Sugar 1kg", 285.5, 30}};
    if (saveProducts("products_out.csv", items)) {
        cout << "Saved " << items.size() << " products." << endl;
    } else {
        cout << "Save failed!" << endl;
    }
    return 0;
}
```

```output
Saved 2 products.
```

```file products_out.csv result
name,price,stock
Dhal 500g,320.00,15
Sugar 1kg,285.50,30
```

Open that file in a spreadsheet program and you get a neat table. You have just made your program talk to Excel.

## Updating data: load, change, save

Text files cannot easily be changed in the middle. If Uncle Ruwan sells 5 bags of rice, the usual approach is:

1. **Load** the whole file into a `vector` of structs.
2. **Change** the data in memory.
3. **Save** everything back, overwriting the file.

```cpp run expectfile=products.csv title=update.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <string>
#include <vector>
using namespace std;

struct Product {
    string name;
    double price;
    int stock;
};

vector<Product> loadProducts(const string &filename) {
    vector<Product> items;
    ifstream in(filename);
    string line;
    getline(in, line);
    while (getline(in, line)) {
        istringstream f(line);
        Product p;
        string priceText, stockText;
        getline(f, p.name, ',');
        getline(f, priceText, ',');
        getline(f, stockText, ',');
        p.price = stod(priceText);
        p.stock = stoi(stockText);
        items.push_back(p);
    }
    return items;
}

bool saveProducts(const string &filename, const vector<Product> &items) {
    ofstream out(filename);
    if (!out) return false;
    out << "name,price,stock\n" << fixed << setprecision(2);
    for (const Product &p : items) out << p.name << "," << p.price << "," << p.stock << "\n";
    return true;
}

int main() {
    vector<Product> items = loadProducts("products.csv");
    for (Product &p : items) {                    //@ & so we change the real elements
        if (p.name == "Red Rice 1kg") p.stock -= 5;
    }
    saveProducts("products.csv", items);
    cout << "Rice stock updated." << endl;
    return 0;
}
```

```output
Rice stock updated.
```

```file products.csv result
name,price,stock
Red Rice 1kg,230.50,37
Coconut Oil 750ml,690.00,8
Soap Bar,145.00,25
Ceylon Tea 200g,520.00,4
```

:::industry
What if the power fails halfway through saving? You could be left with half a file and lose everything. Professional programs often write to a **temporary file** first (such as `products.tmp`), and only when that succeeds do they replace the old file with it. Databases go much further, with transactions and journals that guarantee data is never half-written. For larger systems, files are replaced by databases such as MySQL or SQLite, but the load, change, save idea is the same.
:::

:::brain
Look at `update.cpp` again. What happens if `products.csv` is missing when it runs? What does the program save, and what does it tell the user? How would you fix it?
---solution
`loadProducts` returns an **empty** vector, the loop changes nothing, and `saveProducts` happily writes a file containing **only the header**. The user is told "Rice stock updated", which is false. Fix: check whether loading worked (for example, refuse to continue if the vector is empty or if the file could not be opened) and only save when there is real data. Programs that save data must be most careful of all, because a bug can destroy information.
:::

## Error handling checklist for files

- Check **every** open: `if (!file) { ... }`.
- Tell the user **which** file failed and what to do.
- Use the read operation as the loop condition. Never loop on `eof()`.
- Skip or report blank or malformed lines instead of crashing.
- Be careful with overwrite mode. Think before you open a file for writing.
- Close files (or let them go out of scope) before reopening them.

:::compiler
Find the problems in this program, which should add a new customer to `customers.txt` and then print all customers.

```cpp error
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main() {
    ofstream out("customers.txt");
    out << "Nimal Silva" << endl;

    ifstream in("customers.txt");
    string name;
    while (!in.eof()) {
        in >> name;
        cout << name << endl;
    }
    return 0;
}
```
---solution
1. `ofstream out("customers.txt");` opens in **overwrite** mode, so every run **erases** all existing customers. It needs `ios::app`.
2. Neither stream is checked after opening.
3. The file is read while `out` is still open, so the new line may still be sitting in `out`'s buffer and not be on the disk yet. Call `out.close();` first.
4. `while (!in.eof())` processes the last name twice. Use `while (getline(in, name))`.
5. `in >> name` reads one **word**, so "Nimal Silva" becomes two separate names. Use `getline` for full names.
:::

:::quiz
? Which type do you use to write to a file?
* ofstream
- ifstream
- iostream
- fwrite
> ofstream is an output file stream.

? What happens to an existing file when you open it with `ofstream f("data.txt");`?
- New data is added at the end
* Its contents are erased
- The program crashes
- It is opened read-only
> The default mode truncates the file. Use ios::app to append.

? Why is `while (!in.eof())` a bad loop for reading?
- eof() does not exist
- It never stops
* eof() only becomes true after a failed read, so the last record is processed twice
- It only reads one line
> Use the read itself as the loop condition.

? Which reads a CSV field up to the next comma from an istringstream named f?
- f >> field;
* getline(f, field, ',');
- f.split(',');
- getline(f, ',', field);
> getline accepts a delimiter as its third argument.

? What is the usual way to change one record in a text file?
- Edit the bytes in place
* Load everything into memory, change it, save it all back
- Delete the file
- Open it in append mode and write the new value
> Text files cannot be changed easily in the middle, so you rewrite the file.
:::

:::lab The persistent customer book
Build a small customer book for Ruwan Stores that stores its data in `customers.csv` with the columns `name,phone,points`.

1. At start-up, load all customers into a `vector<Customer>`. If the file does not exist, start with an empty list (that is not an error the first time).
2. Show a menu: 1. List customers, 2. Add customer, 3. Add loyalty points, 4. Save and exit.
3. Adding a customer reads the full name with `getline` (watch out for the getline trap after reading the menu choice).
4. Adding points asks for a phone number, finds that customer, and adds points.
5. On exit, save everything back to the CSV file. Run the program twice to check that your customers are still there.
---solution
```cpp run title=customer_book.cpp
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <limits>
using namespace std;

struct Customer {
    string name;
    string phone;
    int points = 0;
};

const string FILE_NAME = "customers.csv";

vector<Customer> load() {
    vector<Customer> list;
    ifstream in(FILE_NAME);
    if (!in) return list;                    // first run: no file yet
    string line;
    getline(in, line);                       // header
    while (getline(in, line)) {
        if (line.empty()) continue;
        istringstream f(line);
        Customer c;
        string pts;
        getline(f, c.name, ',');
        getline(f, c.phone, ',');
        getline(f, pts, ',');
        c.points = pts.empty() ? 0 : stoi(pts);
        list.push_back(c);
    }
    return list;
}

bool save(const vector<Customer> &list) {
    ofstream out(FILE_NAME);
    if (!out) return false;
    out << "name,phone,points\n";
    for (const Customer &c : list) out << c.name << "," << c.phone << "," << c.points << "\n";
    return true;
}

int main() {
    vector<Customer> list = load();
    int choice;
    do {
        cout << "\n1. List  2. Add  3. Points  4. Save and exit\nChoice: ";
        cin >> choice;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        if (choice == 1) {
            for (const Customer &c : list) cout << c.name << " | " << c.phone << " | " << c.points << endl;
            if (list.empty()) cout << "(no customers yet)" << endl;
        } else if (choice == 2) {
            Customer c;
            cout << "Name: ";
            getline(cin, c.name);
            cout << "Phone: ";
            getline(cin, c.phone);
            list.push_back(c);
        } else if (choice == 3) {
            string phone;
            int pts;
            cout << "Phone: ";
            getline(cin, phone);
            cout << "Points to add: ";
            cin >> pts;
            bool found = false;
            for (Customer &c : list) {
                if (c.phone == phone) {
                    c.points += pts;
                    found = true;
                }
            }
            if (!found) cout << "No customer with that phone." << endl;
        }
    } while (choice != 4);

    if (save(list)) cout << "Saved " << list.size() << " customers." << endl;
    else cout << "Could not save!" << endl;
    return 0;
}
```

```output

1. List  2. Add  3. Points  4. Save and exit
Choice: [[2]]
Name: [[Fathima Rizwan]]
Phone: [[0771234567]]

1. List  2. Add  3. Points  4. Save and exit
Choice: [[3]]
Phone: [[0771234567]]
Points to add: [[50]]

1. List  2. Add  3. Points  4. Save and exit
Choice: [[1]]
Fathima Rizwan | 0771234567 | 50

1. List  2. Add  3. Points  4. Save and exit
Choice: [[4]]
Saved 1 customers.
```
After the points are entered with `cin >>`, the loop goes back to the menu, reads the choice with `cin >>`, and then calls `cin.ignore`, so the leftover newline is always cleaned up before the next `getline`. As an extension, make the output say "1 customer" instead of "1 customers"; the conditional operator from Chapter 7 is perfect for this.
:::

:::bullets
- Files make data **persistent**. Use `<fstream>`: `ofstream` to write, `ifstream` to read.
- File streams work just like `cout` and `cin`: `<<`, `>>`, `getline`, `fixed`, `setw`.
- **Always check** that a file opened: `if (!file)`. Failed streams fail silently.
- `ofstream f("x.txt")` **overwrites**; `ofstream f("x.txt", ios::app)` **appends**.
- Read with the read as the loop condition: `while (in >> a >> b)` or `while (getline(in, line))`. Never loop on `eof()`.
- **CSV** stores records as comma-separated fields. Split lines with `istringstream` and `getline(f, field, ',')`.
- To change data: **load** into a vector of structs, **change** it, **save** it back.
- Treat saving with care: a bug in saving code can destroy data.
:::
