# Compiler Front-End

> Lexical, Syntax and Semantic Analysis implemented from scratch in Python

---

## Overview

This repository contains an implementation of a **compiler front-end** for a simplified programming language. The project covers all core front-end phases:

* **Lexical analysis** (tokenization)
* **Syntax analysis** (grammar validation)
* **Semantic analysis** (meaning and consistency checks)

All components are implemented **manually**, without using parser generators or compiler frameworks, following standard compiler construction theory.

---

## Project Structure

```
compiler-front-end/
├── lexer
│    ├── lexical-analyzer.py
├── parser
│    ├── syntax-analyzer.py
├── semantic
│    ├── semantic-analyzer.py
├── examples/
│   ├── lexic.in
│   ├── lexic.out
│   ├── syntax.in
│   ├── syntax.out
│   ├── semantic.in
│   ├── semantic.out
└── README.md
```

---

## 🔍 Lexical Analyzer

**File:** `lexical-analyzer.py`

### Responsibilities

* Reads raw source code
* Removes comments and whitespace
* Identifies tokens such as:

  * identifiers (`IDN`)
  * numbers (`BROJ`)
  * operators
  * keywords
* Tracks line numbers

### Example

**Input (`lexic.in`)**

```
a = x + y // x + y
b = 12 // comment
x + 3
```

**Output (`lexic.out`)**

```
IDN 1 a
OP_PRIDRUZI 1 =
IDN 1 x
OP_PLUS 1 +
IDN 1 y
IDN 2 b
OP_PRIDRUZI 2 =
BROJ 2 12
...
```

---

## Syntax Analyzer

**File:** `syntax-analyzer.py`

### Responsibilities

* Parses the token stream produced by the lexer
* Validates program structure using a formally defined grammar
* Reports syntax errors with line information

The parser ensures that the program conforms to the grammar of the language before semantic analysis begins.

---

## Semantic Analyzer

**File:** `semantic-analyzer.py`

### Responsibilities

* Builds and manages symbol tables
* Enforces semantic rules such as:

  * variables must be declared before use
  * no duplicate declarations in the same scope
  * correct scope resolution
* Detects semantic errors not visible at syntax level

---

## Running the Project

Clone the repository:

```bash
git clone https://github.com/dakisa11/compiler-front-end.git
cd compiler-front-end
```

Run individual phases:

```bash
python lexical-analyzer.py
python syntax-analyzer.py
python semantic-analyzer.py
```

Input/output examples are available in the `examples/` directory.

---

## Goals of the Project

* Practical understanding of compiler construction
* Application of formal language and automata theory
* Experience with program analysis and language design

This project is intended as a **portfolio and educational project**, demonstrating low-level understanding of how compilers work internally.

---

## Possible Extensions

* Abstract Syntax Tree (AST) construction and visualization
* Better error recovery and diagnostics
* Intermediate code generation
* Support for additional language constructs

---

## Technologies

* Python 3
* No external parsing or compiler libraries

---

## References

* University coursework on compiler construction
