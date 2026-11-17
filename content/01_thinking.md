---
num: 1
title: Thinking Like a Programmer
tagline: Before you write code, you have to solve the problem
learn: understand what a program and an algorithm really are; use the Input, Process, Output model; follow the program development life cycle; write pseudocode; draw flowcharts with the correct symbols; trace an algorithm by hand with a trace table
---

## The shop that runs on an exercise book

It is Saturday morning at Ruwan Stores. The shop is full. Uncle Ruwan is adding up a bill on a calculator, writing it in his exercise book, and shouting to his helper to check whether there is any more dhal in the back room.

:::story
Ruwan: Two kilos of rice, one packet of tea, three soaps... what was the price of the soap again? Oh no, I wrote it somewhere...

Amaya: Uncle, a program can remember all the prices for you.

Ruwan: Good. Then make it. Today?

Nuwan: Not today. First she has to understand the problem. Most bad software comes from people who started typing before they started thinking.
:::

Nuwan is right. Programming is not mainly about typing code. It is about **solving problems**, and then explaining the solution to a machine that is extremely fast but has absolutely no common sense.

## What is a program, really?

A **program** is a set of instructions that tells a computer exactly what to do, step by step.

The key word is *exactly*. A computer does what you say, not what you mean. If you tell a friend "get me some tea", they know you want it hot, in a cup, maybe with sugar. If a computer could make tea, it would need every single step spelled out.

:::brain
Imagine you are writing instructions for a robot that has never seen a kitchen. Write down how to make a cup of plain tea. How many steps do you need? What did you forget the first time?
:::

Here is one attempt:

```pseudo
1. Fill the kettle with water
2. Switch on the kettle
3. Wait until the water boils
4. Put a tea bag in a cup
5. Pour the hot water into the cup
6. Wait 3 minutes
7. Remove the tea bag
```

Looks fine? A real robot might still get stuck. What if the kettle is already full? What if there is no tea bag? What is a "cup"? Programmers spend a lot of their time thinking about exactly these kinds of questions. They are called **edge cases**, and good programmers love finding them.

:::nodumb
Q: If computers are so "stupid", why are they so useful?
A: Because they are incredibly fast and they never get bored. A modern processor can perform billions of simple operations every second, and it will repeat the same task a million times without making a careless mistake. Your job is to give it the right instructions. Its job is to follow them perfectly.

Q: Do I need to be good at maths to program?
A: You need to be comfortable with basic arithmetic and logical thinking, like "if this is true, then do that". Some areas, such as graphics, games, data science and cryptography, use a lot of maths. Most everyday programming uses very little. Problem solving matters much more than advanced maths.
:::

## Algorithms: recipes for computers

An **algorithm** is a finite, ordered set of clear steps that solves a problem. The tea instructions above are an algorithm. So is a recipe for fried rice, the directions to your friend's house, or the method you learned in school for long division.

A program is an algorithm written in a language a computer can understand, such as C++.

A good algorithm has these properties:

| Property | What it means | Tea example |
|---|---|---|
| **Input** | It takes zero or more values to work on | Water, a tea bag |
| **Output** | It produces at least one result | A cup of tea |
| **Definiteness** | Every step is clear, with only one meaning | "Wait 3 minutes", not "wait a bit" |
| **Finiteness** | It always finishes after a limited number of steps | It does not boil water forever |
| **Effectiveness** | Every step is simple enough to actually carry out | "Pour water", not "make it taste perfect" |

:::watch
"Add some sugar" is **not definite**. How much is "some"? Computers cannot guess. Whenever you write a step, ask yourself: could two different people read this and do two different things? If yes, make it more precise.
:::

## The IPO model: Input, Process, Output

Almost every program, from a calculator to a banking system, follows the same simple shape:

- **Input:** the data that comes in (from the keyboard, a file, a sensor, a network).
- **Process:** what the program does with that data (calculations, decisions, sorting).
- **Output:** the result that goes out (to the screen, a file, a printer).

Let's apply it to Uncle Ruwan's first problem: calculating the bill for one item.

| Input | Process | Output |
|---|---|---|
| unit price, quantity | total = unit price × quantity | total to pay |

That tiny table is already a design. When you are stuck on a problem, start by filling in an IPO table. It forces you to answer the most important questions first: *What do I have? What do I need? How do I get from one to the other?*

:::sharpen IPO for a discount
Ruwan Stores gives a 5% discount when a bill is Rs. 3,000 or more. Fill in an IPO table for a program that reads the bill amount and shows the amount the customer must pay.
---solution
| Input | Process | Output |
|---|---|---|
| bill amount | if bill amount is 3000 or more, discount = bill amount × 0.05, otherwise discount = 0; amount to pay = bill amount − discount | amount to pay |

Notice that the process contains a **decision**. Many real problems do. You will learn to write decisions in C++ in Chapter 7.
:::

## The program development life cycle

Professional software is not written in one go. It is built in stages. This sequence of stages is called the **program development life cycle** (PDLC). Different textbooks name and group the stages slightly differently, but the ideas are always the same:

1. **Define and analyse the problem.** What exactly must the program do? What are the inputs and outputs? What are the rules? Talk to the user. (Uncle Ruwan is the user!)
2. **Design the solution.** Plan the algorithm using tools like IPO tables, pseudocode and flowcharts. No code yet.
3. **Code the program.** Translate the design into a programming language such as C++.
4. **Test and debug.** Run the program with different inputs, including unusual ones, and fix the errors (bugs) you find.
5. **Document.** Write comments in the code and instructions for users and future programmers.
6. **Maintain.** After the program is in use, fix new bugs and add features as the user's needs change.

It is a *cycle* because maintenance often leads back to analysis. When Uncle Ruwan asks for a new feature next year, Amaya will analyse, design, code and test again.

```flow
flowchart LR
  A[Define and<br>analyse] --> B[Design]
  B --> C[Code]
  C --> D[Test and<br>debug]
  D --> E[Document]
  E --> F[Maintain]
  F -.new needs.-> A
  D -.bug found in design.-> B
```

:::industry
In real companies, this cycle is usually run in short rounds. Many teams use an approach called **Agile**, where they build a small working piece of the software in one to four weeks, show it to the user, collect feedback, and repeat. The stages are the same; they just happen many times, in small steps. That is exactly how Amaya will build the Ruwan Stores system in this book: one small feature per chapter.
:::

:::nodumb
Q: Can I skip the design stage for small programs?
A: For a five-line program, a quick mental design is enough. But even professionals sketch a plan before writing anything bigger. Skipping design usually means you spend more time debugging. A few minutes with pencil and paper can save hours at the keyboard.

Q: What is a "bug"?
A: A bug is a mistake in a program that makes it behave wrongly. The word was used in engineering long before computers. A famous story from 1947 tells of a real moth found stuck in a relay of the Harvard Mark II computer. The team taped it into their logbook as the "first actual case of bug being found". The joke was funny precisely because "bug" was already a common word for a fault.
:::

## Pseudocode: code for humans

**Pseudocode** is a way of writing an algorithm in structured, plain English, using words that look a bit like code. It is not a real programming language, so no compiler will check it. Its job is to help *you* (and your team) think clearly before you write real code.

There is no single official standard for pseudocode. Different courses and exam boards use slightly different words. What matters is that you are **clear and consistent**. This book uses these keywords:

| Keyword | Use it for |
|---|---|
| `START` / `END` | The beginning and end of the algorithm |
| `READ` or `INPUT` | Getting a value from the user |
| `DISPLAY` or `PRINT` | Showing something to the user |
| `SET` | Storing a value: `SET total = price * qty` |
| `IF ... THEN ... ELSE ... END IF` | Making a decision |
| `WHILE ... DO ... END WHILE` | Repeating while a condition is true |
| `FOR ... TO ... END FOR` | Repeating a set number of times |

Here is the bill for one item in pseudocode:

```pseudo
START
  DISPLAY "Enter unit price"
  READ price
  DISPLAY "Enter quantity"
  READ qty
  SET total = price * qty
  DISPLAY "Total: ", total
END
```

And the discount problem from the earlier exercise:

```pseudo
START
  READ bill
  IF bill >= 3000 THEN
    SET discount = bill * 0.05
  ELSE
    SET discount = 0
  END IF
  SET pay = bill - discount
  DISPLAY pay
END
```

:::watch
Indentation matters for humans, even though it does not matter to a pseudocode "compiler" (there isn't one). Indent the steps inside an `IF` or a loop. When you see the code in Chapter 7, you will notice C++ programmers do exactly the same.
:::

## Flowcharts: algorithms you can see

A **flowchart** shows an algorithm as a diagram. Each type of step has its own shape, and arrows show the order. The shapes below are the standard ones you are expected to use.

| Symbol | Name | Used for |
|---|---|---|
| Oval (rounded rectangle) | **Terminator** | `Start` and `End` |
| Parallelogram | **Input / Output** | Reading or displaying data |
| Rectangle | **Process** | A calculation or assignment, such as `total = price * qty` |
| Diamond | **Decision** | A yes/no question, such as `bill >= 3000?` |
| Arrow | **Flow line** | Shows the direction of flow |
| Small circle | **Connector** | Joins parts of a chart that would otherwise cross or continue elsewhere |
| Rectangle with double side lines | **Predefined process** | A step defined somewhere else (later, a function) |

Here is the discount algorithm as a flowchart:

```flow
flowchart TD
  S([Start]) --> I[/Read bill/]
  I --> D{bill >= 3000?}
  D -- Yes --> Y[discount = bill * 0.05]
  D -- No --> N[discount = 0]
  Y --> P[pay = bill - discount]
  N --> P
  P --> O[/Display pay/]
  O --> E([End])
```

Rules for clean flowcharts:

- Exactly **one** Start and at least one End.
- Flow normally goes **top to bottom**, left to right.
- A decision diamond has **one way in and two ways out**, labelled *Yes* and *No* (or *True* and *False*).
- Every process box has one arrow in and one arrow out.
- Keep text in the boxes short. Use the same variable names you will use in your code.

:::brain
Look at the flowchart again. If the user enters exactly 3000, which path does the algorithm take? What would change if the diamond said `bill > 3000?` instead? Which one matches Uncle Ruwan's rule?
:::

:::sharpen Draw a loop
Uncle Ruwan wants to add up the prices of the items in a bill. The cashier types prices one by one, and types 0 when the bill is finished. Draw a flowchart that keeps a running total and displays it at the end.
---solution
```flow
flowchart TD
  S([Start]) --> A[total = 0]
  A --> R[/Read price/]
  R --> D{price == 0?}
  D -- No --> P[total = total + price]
  P --> R
  D -- Yes --> O[/Display total/]
  O --> E([End])
```
The arrow going **back up** to "Read price" is what makes this a loop. The value 0 that ends the input is called a **sentinel value**. You will write this exact program in Chapter 8.
:::

## Three building blocks are enough

Here is a surprising fact. In 1966, two computer scientists, Corrado Böhm and Giuseppe Jacopini, showed that any algorithm can be built using just three kinds of structure:

1. **Sequence:** do steps one after another.
2. **Selection:** choose between paths based on a condition (`IF`).
3. **Iteration:** repeat steps (loops such as `WHILE` and `FOR`).

That's it. Every program you will ever write, from a calculator to a video game, is made from these three blocks combined in clever ways. This idea is the foundation of **structured programming**, and it is why this book spends whole chapters on decisions (Chapters 6 and 7) and loops (Chapter 8).

```flow
flowchart LR
  subgraph Sequence
  direction TB
  a1[Step 1] --> a2[Step 2] --> a3[Step 3]
  end
  subgraph Selection
  direction TB
  b1{Condition?} -- Yes --> b2[Do A]
  b1 -- No --> b3[Do B]
  end
  subgraph Iteration
  direction TB
  c1{Keep going?} -- Yes --> c2[Repeat step]
  c2 --> c1
  end
```

## Tracing an algorithm by hand

Before you trust an algorithm, test it on paper. A **trace table** (also called a dry run) has one column for each variable and one row for each step. You play the role of the computer, slowly and carefully.

Let's trace the running total algorithm with the inputs 250, 120, 80 and then 0.

| Step | price | total | price == 0? | Output |
|---|---|---|---|---|
| total = 0 | | 0 | | |
| Read price | 250 | 0 | No | |
| total = total + price | 250 | 250 | | |
| Read price | 120 | 250 | No | |
| total = total + price | 120 | 370 | | |
| Read price | 80 | 370 | No | |
| total = total + price | 80 | 450 | | |
| Read price | 0 | 450 | Yes | |
| Display total | 0 | 450 | | 450 |

The output is 450, which is correct (250 + 120 + 80 = 450). Trace tables catch mistakes such as forgetting to set `total = 0` at the beginning.

:::sharpen Trace it
Trace this algorithm when the user enters 7. What is displayed?

```pseudo
START
  READ n
  SET result = 1
  SET i = 1
  WHILE i <= n DO
    IF i is odd THEN
      SET result = result * i
    END IF
    SET i = i + 1
  END WHILE
  DISPLAY result
END
```
---solution
| i | i odd? | result |
|---|---|---|
| (start) | | 1 |
| 1 | Yes | 1 × 1 = 1 |
| 2 | No | 1 |
| 3 | Yes | 1 × 3 = 3 |
| 4 | No | 3 |
| 5 | Yes | 3 × 5 = 15 |
| 6 | No | 15 |
| 7 | Yes | 15 × 7 = 105 |
| 8 | loop stops (8 <= 7 is false) | 105 |

The algorithm displays **105**. It multiplies all the odd numbers from 1 to n.
:::

## From your algorithm to the machine

You now have a design. But computers do not understand pseudocode or flowcharts. At the lowest level, a processor only understands **machine code**: patterns of 1s and 0s that stand for very simple instructions, such as "add these two numbers" or "copy this value to memory".

Writing machine code by hand is painful, so humans invented layers of languages:

| Level | Example | Who reads it easily? |
|---|---|---|
| Machine code | `10110000 01100001` | The processor |
| Assembly language | `mov al, 61h` | Specialists |
| High-level language | `total = price * qty;` | You, after this book |

C++ is a **high-level language**, which means it is designed for humans to read and write. A special program called a **compiler** translates your C++ into machine code. You will meet the compiler properly in the next chapter.

:::relax
The pseudocode and flowcharts you learned here are not "beginner stuff" you will throw away. Experienced engineers still sketch flowcharts on whiteboards and write pseudocode in design documents. They are thinking tools, and you will use them for your whole career.
:::

:::quiz
? Which flowchart symbol represents a decision?
- Rectangle
- Parallelogram
* Diamond
- Oval
> A decision is a yes/no question, and it is always drawn as a diamond with two labelled exits.

? Which property of an algorithm does the step "cook until it tastes nice" break?
- Finiteness
* Definiteness
- Output
- Input
> "Tastes nice" can mean different things to different people, so the step is not definite.

? In the IPO model, where does "total = price × quantity" belong?
- Input
* Process
- Output
- None of them
> Calculating the total is the processing step. Price and quantity are inputs, and the total shown on screen is the output.

? Which three structures are enough to build any algorithm?
- Input, process and output
* Sequence, selection and iteration
- Variables, functions and files
- Start, decision and end
> This is the structured programming result of Böhm and Jacopini from 1966.

? Which stage of the PDLC comes straight after designing the solution?
- Testing
- Maintenance
* Coding
- Documentation
> Once the design is ready, you translate it into code. Then you test it.
:::

:::lab The Ruwan Stores change calculator
Uncle Ruwan wants to know how much change to give a customer.

1. Write an **IPO table** for a program that reads the bill total and the cash given, and displays the change.
2. Extend the design: if the cash given is **less** than the bill, the program should display "Not enough cash" instead.
3. Write the algorithm in **pseudocode**.
4. Draw the **flowchart**.
5. **Trace** your algorithm with these two test cases: bill 1,250 and cash 2,000; bill 1,250 and cash 1,000.
---solution
**1. IPO table**

| Input | Process | Output |
|---|---|---|
| bill, cash | if cash >= bill then change = cash − bill | change, or the message "Not enough cash" |

**3. Pseudocode**

```pseudo
START
  READ bill
  READ cash
  IF cash >= bill THEN
    SET change = cash - bill
    DISPLAY "Change: ", change
  ELSE
    DISPLAY "Not enough cash"
  END IF
END
```

**4. Flowchart**

```flow
flowchart TD
  S([Start]) --> R1[/Read bill/]
  R1 --> R2[/Read cash/]
  R2 --> D{cash >= bill?}
  D -- Yes --> C[change = cash - bill]
  C --> O1[/Display change/]
  D -- No --> O2[/Display 'Not enough cash'/]
  O1 --> E([End])
  O2 --> E
```

**5. Traces**

- bill = 1250, cash = 2000: `2000 >= 1250` is true, change = 750, the program displays `Change: 750`.
- bill = 1250, cash = 1000: `1000 >= 1250` is false, the program displays `Not enough cash`.
:::

:::bullets
- A **program** is a precise set of instructions. Computers follow them exactly and never guess.
- An **algorithm** is a finite, ordered, unambiguous set of steps that solves a problem.
- The **IPO model** (Input, Process, Output) is the quickest way to start any design.
- The **program development life cycle** is: define, design, code, test, document, maintain, and then around again.
- **Pseudocode** is structured English for planning. Be clear and consistent; there is no single official standard.
- **Flowcharts** use standard symbols: oval for start/end, parallelogram for input/output, rectangle for processes, diamond for decisions.
- Any algorithm can be built from **sequence, selection and iteration**.
- **Trace tables** let you test an algorithm on paper before you write any code.
:::
