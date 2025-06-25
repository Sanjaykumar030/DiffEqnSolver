# 🧮 Differential Equation Solver - GUI Application

> _An interactive tool for solving linear ordinary differential equations (ODEs) with constant coefficients using symbolic computation._

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)](https://www.python.org/)  
[![SymPy](https://img.shields.io/badge/Symbolic%20Math-SymPy-brightgreen)](https://www.sympy.org/)  
[![GUI](https://img.shields.io/badge/Interface-Tkinter-lightgrey)](https://docs.python.org/3/library/tkinter.html)  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Overview

**Differential Equation Solver** is a full-screen Python GUI application built to solve **nth-order linear ODEs with constant coefficients**. It uses symbolic algebra to compute roots of the auxiliary equation, determine the general solution, and display step-by-step details in a user-friendly interface.

Designed for engineering and science students, this project simplifies the tedious algebraic steps in differential equations using real-time visual output.

---

## 🚀 Features

- ✅ Supports **linear differential equations up to 6th order**
- ✅ Automatically computes:
  - Auxiliary (characteristic) equation
  - Roots (real, complex, repeated)
  - Complementary function (CF)
  - Time taken for computation
- 🧾 **Live equation preview** as you input coefficients
- 📚 Displays **real-world applications** of each order
- 🖥️ Clean, intuitive, full-screen GUI built with `tkinter`
- 🧠 Powered by symbolic computation using `sympy`

---

## 📂 File Structure

```
differential-equation-solver/
│
├── differential_equation_solver.py   # Main application
├── general_GUI.png                  # Screenshot of GUI
├── sample_output.png                # Sample equation solution output
├── requirements.txt                 # Required packages
└── README.md                        # Project documentation
```

---

## 📷 Screenshots

### 🖼️ Full GUI View

<img src="general_GUI.png" alt="Main GUI Screenshot" width="600"/>

### 🧾 Sample Output

[View full image](sample_output.png)

---

## 🧰 Technologies & Concepts

| Domain                | Tools / Concepts Used                         |
|-----------------------|-----------------------------------------------|
| Programming Language  | Python 3                                      |
| GUI Toolkit           | [`tkinter`](https://docs.python.org/3/library/tkinter.html) |
| Symbolic Computation  | [`sympy`](https://www.sympy.org/)             |
| Math Foundation       | Linear ODEs, Roots, CF, Auxiliary Equation    |
| Development Practice  | Modular design, Real-time rendering, Full-screen GUI |

---

## ▶️ Getting Started

### ✅ Prerequisites

- Python 3.8 or higher  
- Recommended: Use virtual environment (e.g., `venv` or `conda`)

### 🔧 Installation

1. **Clone this repository**:
    ```bash
    git clone https://github.com/Sanjaykumar030/DiffEqnSolver.git
    cd DiffEqnSolver
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the application:**
    ```bash
    python differential_equation_solver.py
    ```

---

## 🧠 Educational Value

This solver is not just a computational tool—it’s a learning companion. It reinforces:

- Formulation of characteristic equations
- Understanding the nature of roots
- Mapping solution structure to equation order
- Practical relevance of each differential system

**Ideal for:**

- First-year engineering math courses
- Applied mathematics students
- Quick verification during assignments or exams

---

## 💡 Motivation

Solving higher-order differential equations manually is prone to algebraic errors. This tool automates the process while preserving transparency. It aims to bring symbolic computation into the hands of learners in an intuitive way.

---

## ⚠️ Limitations

- Only supports ODEs with constant coefficients
- Does not solve non-linear or variable-coefficient equations
- No particular integral (PI) computation (CF only)

---

## 📜 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for usage rights and permissions.

---

## 🙋 Author

**Sanjay Kumar Sakamuri Kamalakar**

- 📧 Email: [sksanjaykumar010307@gmail.com](mailto:sksanjaykumar010307@gmail.com)
- 🔗 LinkedIn: [linkedin.com/in/sanjay-kumar-sakamuri-kamalakar-a67148214](https://linkedin.com/in/sanjay-kumar-sakamuri-kamalakar-a67148214)
- 🧪 ORCID: [0009-0009-1021-2297](https://orcid.org/0009-0009-1021-2297)

---

## 🙏 Acknowledgements

- OpenAI’s ChatGPT for architectural and code logic support
- Developers of Python, tkinter, and sympy
- Educators and mentors who laid the math foundation

---

## 🎓 Final Note

This solver bridges mathematical theory with practical implementation.  
Whether you're reviewing differential equations, verifying homework, or teaching others — this app makes ODEs less daunting and more interactive.

Happy solving! 🎉
