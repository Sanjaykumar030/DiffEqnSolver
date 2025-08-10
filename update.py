import sympy as sp
import tkinter as tk
from tkinter import ttk, messagebox
import time

coeff_entries = []
root = None
equation_type = None
preview_label = None
aux_label = None
root_label = None
cf_label = None
pi_label = None
gs_label = None
time_taken_label = None
order_entry = None
coeff_frame = None
rhs_frame = None
rhs_entry = None

def solve_homogeneous(order, coeffs):
    m = sp.symbols('m')
    aux_eq = sum(coeffs[i] * m**(order - i) for i in range(order + 1))
    aux_label.config(text=f"Auxiliary Equation:\n{sp.pretty(sp.simplify(aux_eq), use_unicode=True)} = 0")
    roots = sp.solve(aux_eq, m)
    formatted_roots = []
    for r in roots:
        if r.is_real:
            formatted_roots.append(round(float(r), 3))
        else:
            formatted_roots.append(complex(round(sp.re(r), 3), round(sp.im(r), 3)))
    root_text = "\n".join([f"Root {i+1}: {root}" for i, root in enumerate(formatted_roots)])
    root_label.config(text=f"Roots of Auxiliary Equation:\n{root_text}")
    x = sp.symbols('x')
    y = sp.Function('y')
    diffeq = sum(coeffs[i] * sp.diff(y(x), x, order - i) for i in range(order + 1))
    cf_solution = sp.dsolve(diffeq, y(x)).rhs
    cf_label.config(text=f"Complementary Function (CF):\ny_c = {sp.pretty(cf_solution, use_unicode=True)}")
    gs_label.config(text=f"General Solution (GS):\ny = {sp.pretty(cf_solution, use_unicode=True)}")
    pi_label.config(text="Particular Integral (PI):\ny_p = 0 (Homogeneous Equation)")

def solve_non_homogeneous(order, coeffs, rhs_expr):
    x = sp.symbols('x')
    y = sp.Function('y')
    lhs = sum(coeffs[i] * sp.diff(y(x), x, order - i) for i in range(order + 1))
    try:
        rhs = sp.sympify(rhs_expr, locals={'x': x, 'exp': sp.exp, 'sin': sp.sin, 'cos': sp.cos})
    except sp.SympifyError:
        messagebox.showerror("Error", "Invalid RHS function. Use valid sympy syntax (e.g., 'exp(x)*sin(2*x) + x**2').")
        return
    diffeq = sp.Eq(lhs, rhs)
    solution = sp.dsolve(diffeq, y(x), hint='nth_linear_constant_coeff_undetermined_coefficients')
    general_solution = solution.rhs
    constants = sorted(general_solution.atoms(sp.Symbol), key=lambda c: c.name)
    integration_constants = [c for c in constants if c.name.startswith('C')]
    complementary_function = 0
    particular_integral = general_solution
    for term in sp.Add.make_args(general_solution):
        is_cf_term = any(c in term.free_symbols for c in integration_constants)
        if is_cf_term:
            complementary_function += term
        else:
            if not any(str(c) in str(term) for c in integration_constants):
                particular_integral = term if particular_integral == general_solution else particular_integral + term
    particular_integral = general_solution.subs({c: 0 for c in integration_constants})
    complementary_function = general_solution - particular_integral
    aux_eq_expr = sum(coeffs[i] * sp.Symbol('m')**(order - i) for i in range(order + 1))
    aux_label.config(text=f"Auxiliary Equation:\n{sp.pretty(sp.simplify(aux_eq_expr), use_unicode=True)} = 0")
    root_label.config(text="Roots: (Derived from CF)")
    cf_label.config(text=f"Complementary Function (CF):\ny_c = {sp.pretty(complementary_function, use_unicode=True)}")
    pi_label.config(text=f"Particular Integral (PI):\ny_p = {sp.pretty(particular_integral, use_unicode=True)}")
    gs_label.config(text=f"General Solution (y = y_c + y_p):\ny = {sp.pretty(general_solution, use_unicode=True)}")

def solve_cauchy_euler(order, coeffs):
    x = sp.symbols('x')
    y = sp.Function('y')
    diffeq = sum(coeffs[i] * (x**(order - i)) * sp.diff(y(x), x, order - i) for i in range(order + 1))
    solution = sp.dsolve(diffeq, y(x), hint='nth_linear_euler_eq_homogeneous')
    general_solution = solution.rhs
    m = sp.symbols('m')
    aux_eq_terms = []
    term = coeffs[0]
    for i in range(1, order + 1):
        term *= (m - i + 1)
    aux_eq_terms.append(term)
    for i in range(1, order + 1):
        term = coeffs[i]
        for j in range(order - i):
            term *= (m - j)
        aux_eq_terms.append(term)
    aux_eq = sum(aux_eq_terms)
    aux_label.config(text=f"Auxiliary Equation (for y=x^m):\n{sp.pretty(sp.expand(aux_eq), use_unicode=True)} = 0")
    roots = sp.solve(aux_eq, m)
    formatted_roots = [round(float(r), 3) if r.is_real else complex(round(sp.re(r), 3), round(sp.im(r), 3)) for r in roots]
    root_text = "\n".join([f"Root {i+1}: {root}" for i, root in enumerate(formatted_roots)])
    root_label.config(text=f"Roots of Auxiliary Equation:\n{root_text}")
    cf_label.config(text="N/A for Cauchy-Euler")
    pi_label.config(text="N/A for Homogeneous Cauchy-Euler")
    gs_label.config(text=f"General Solution:\ny = {sp.pretty(general_solution, use_unicode=True)}")

def create_styled_section(parent, title, color):
    frame = tk.Frame(parent, bg="white", bd=2, relief="solid")
    frame.pack(side="left", padx=10, pady=5, expand=True, fill="both")
    label = tk.Label(frame, text=title, font=("Helvetica", 14, "bold"), bg=color, fg="white", padx=10, pady=5)
    label.pack(fill="x")
    content = tk.Label(frame, text="", font=("Courier New", 14), fg="black", wraplength=350, justify="left", bg="white", anchor="nw")
    content.pack(pady=10, padx=10, expand=True, fill="both")
    return content

def update_preview():
    try:
        order = int(order_entry.get())
        coeffs = [entry.get() for entry in coeff_entries]
        eq_terms = []
        if not equation_type.get():
            preview_label.config(text="Select an equation type first.", fg="red")
            return
        for i, coeff in enumerate(coeffs):
            if coeff:
                term_order = order - i
                coeff_str = f"{coeff}*" if coeff != '1' else ""
                if equation_type.get() == "Cauchy-Euler":
                    x_term = f"x^{term_order}*" if term_order > 1 else "x*" if term_order == 1 else ""
                    d_term = f"D^{term_order}y" if term_order > 1 else "Dy" if term_order == 1 else "y"
                    eq_terms.append(f"{coeff_str}{x_term}{d_term}")
                else:
                    d_term = f"D^{term_order}y" if term_order > 1 else "Dy" if term_order == 1 else "y"
                    eq_terms.append(f"{coeff_str}{d_term}")
        eq_text = " + ".join(eq_terms)
        if equation_type.get() == "Non-Homogeneous":
            rhs_text = rhs_entry.get() if rhs_entry.get() else "f(x)"
            eq_text += f" = {rhs_text}"
        else:
            eq_text += " = 0"
        preview_label.config(text=f"Equation Preview:\n{eq_text}", fg="#003366")
    except (ValueError, IndexError):
        preview_label.config(text="Equation Preview:", fg="#003366")

def create_coefficient_entries():
    global coeff_entries
    for widget in coeff_frame.winfo_children():
        widget.destroy()
    try:
        order = int(order_entry.get())
        if order < 1 or order > 10:
            messagebox.showerror("Error", "Order must be between 1 and 10.")
            return
        coeff_entries = []
        grid_frame = tk.Frame(coeff_frame, bg="#f0f8ff")
        grid_frame.pack()
        for i in range(order + 1):
            term_order = order - i
            if equation_type.get() == "Cauchy-Euler":
                label_text = f"Coeff of x^{term_order}D^{term_order}y:" if term_order > 1 else (f"Coeff of x*Dy:" if term_order == 1 else "Coeff of y:")
            else:
                label_text = f"Coeff of D^{term_order}y:" if term_order > 1 else ("Coeff of Dy:" if term_order == 1 else "Coeff of y:")
            label = tk.Label(grid_frame, text=label_text, fg="black", font=("Helvetica", 12), bg="#f0f8ff")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(grid_frame, font=("Helvetica", 12), width=8)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.bind("<KeyRelease>", lambda event: update_preview())
            coeff_entries.append(entry)
        update_preview()
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for the order!")

def on_equation_type_change(*args):
    eq_type = equation_type.get()
    if order_entry.get():
        create_coefficient_entries()
    if eq_type == "Non-Homogeneous":
        rhs_frame.pack(pady=5)
    else:
        rhs_frame.pack_forget()
    reset_results()
    update_preview()

def compute():
    try:
        start_time = time.time()
        order = int(order_entry.get())
        coeffs = [float(entry.get()) for entry in coeff_entries]
        eq_type = equation_type.get()
        if not eq_type:
            messagebox.showerror("Error", "Please select an equation type.")
            return
        reset_results()
        if eq_type == "Homogeneous":
            solve_homogeneous(order, coeffs)
        elif eq_type == "Non-Homogeneous":
            rhs_expr = rhs_entry.get()
            if not rhs_expr:
                messagebox.showerror("Error", "Please provide the f(x) for the non-homogeneous equation.")
                return
            solve_non_homogeneous(order, coeffs, rhs_expr)
        elif eq_type == "Cauchy-Euler":
            solve_cauchy_euler(order, coeffs)
        end_time = time.time()
        time_taken_label.config(text=f"Time Taken: {round(end_time - start_time, 4)} seconds")
    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please ensure all coefficients are valid numbers.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def reset_all():
    order_entry.delete(0, tk.END)
    for widget in coeff_frame.winfo_children():
        widget.destroy()
    coeff_entries.clear()
    if rhs_entry:
        rhs_entry.delete(0, tk.END)
    equation_type.set("")
    preview_label.config(text="Equation Preview:")
    reset_results()

def reset_results():
    aux_label.config(text="")
    root_label.config(text="")
    cf_label.config(text="")
    pi_label.config(text="")
    gs_label.config(text="")
    time_taken_label.config(text="Time Taken:")

def exit_app():
    root.destroy()

def setup_gui():
    global root, equation_type, preview_label, aux_label, root_label, cf_label, pi_label, gs_label
    global time_taken_label, order_entry, coeff_frame, rhs_frame, rhs_entry
    root = tk.Tk()
    root.title("Advanced Differential Equation Solver")
    root.geometry("1400x900")
    root.configure(bg="#eaf2f8")
    title_label = tk.Label(root, text="Advanced Differential Equation Solver", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="white", pady=10)
    title_label.pack(fill="x")
    input_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="groove")
    input_frame.pack(pady=10, padx=10, fill="x")
    type_frame = tk.Frame(input_frame, bg="white")
    type_frame.pack(pady=10)
    tk.Label(type_frame, text="1. Select Equation Type:", font=("Helvetica", 14, "bold"), bg="white").pack(side="left", padx=10)
    equation_type = tk.StringVar()
    eq_type_options = ["Homogeneous", "Non-Homogeneous", "Cauchy-Euler"]
    type_dropdown = ttk.Combobox(type_frame, textvariable=equation_type, values=eq_type_options, font=("Helvetica", 14), state="readonly", width=20)
    type_dropdown.pack(side="left")
    type_dropdown.bind("<<ComboboxSelected>>", on_equation_type_change)
    order_frame = tk.Frame(input_frame, bg="white")
    order_frame.pack(pady=10)
    tk.Label(order_frame, text="2. Enter Equation Order:", font=("Helvetica", 14, "bold"), bg="white").pack(side="left", padx=10)
    order_entry = tk.Entry(order_frame, font=("Helvetica", 14), width=5, justify='center')
    order_entry.pack(side="left")
    tk.Button(order_frame, text="Set Order & Coefficients", font=("Helvetica", 12, "bold"), command=create_coefficient_entries, bg="#3498db", fg="white").pack(side="left", padx=10)
    input_area_frame = tk.Frame(input_frame, bg="white")
    input_area_frame.pack(pady=10, fill="x", expand=True)
    coeff_frame = tk.Frame(input_area_frame, bg="#f0f8ff")
    coeff_frame.pack(side="left", padx=20, pady=10, anchor="n")
    rhs_frame = tk.Frame(input_area_frame, bg="#f0f8ff")
    tk.Label(rhs_frame, text="Enter f(x):", font=("Helvetica", 12, "bold"), bg="#f0f8ff").pack(pady=5)
    rhs_entry = tk.Entry(rhs_frame, font=("Courier New", 14), width=30)
    rhs_entry.pack(pady=5, padx=10)
    tk.Label(rhs_frame, text="(Use Python's sympy syntax, e.g., x**2 + sin(x))", font=("Helvetica", 10), bg="#f0f8ff").pack()
    rhs_entry.bind("<KeyRelease>", lambda event: update_preview())
    rhs_frame.pack_forget()
    preview_label = tk.Label(root, text="Equation Preview:", font=("Courier New", 16, "bold"), fg="#003366", bg="#eaf2f8", justify="center")
    preview_label.pack(pady=10)
    control_frame = tk.Frame(root, bg="#eaf2f8")
    control_frame.pack(pady=10)
    tk.Button(control_frame, text="SOLVE", font=("Helvetica", 16, "bold"), command=compute, bg="#27ae60", fg="white", padx=30, pady=10, relief="raised").pack(side="left", padx=20)
    tk.Button(control_frame, text="RESET", font=("Helvetica", 16, "bold"), command=reset_all, bg="#f39c12", fg="white", padx=30, pady=10, relief="raised").pack(side="left", padx=20)
    results_container = tk.Frame(root, bg="#eaf2f8")
    results_container.pack(pady=10, padx=10, fill="both", expand=True)
    results_frame_top = tk.Frame(results_container, bg="#eaf2f8")
    results_frame_top.pack(fill="both", expand=True)
    aux_label = create_styled_section(results_frame_top, "Auxiliary Equation", "#2980b9")
    root_label = create_styled_section(results_frame_top, "Roots", "#2ecc71")
    cf_label = create_styled_section(results_frame_top, "Complementary Function (CF)", "#8e44ad")
    results_frame_bottom = tk.Frame(results_container, bg="#eaf2f8")
    results_frame_bottom.pack(fill="both", expand=True)
    pi_label = create_styled_section(results_frame_bottom, "Particular Integral (PI)", "#d35400")
    gs_label = create_styled_section(results_frame_bottom, "General Solution (GS)", "#c0392b")
    footer_frame = tk.Frame(root, bg="#eaf2f8")
    footer_frame.pack(pady=10, fill="x")
    time_taken_label = tk.Label(footer_frame, text="Time Taken:", font=("Helvetica", 12, "italic"), fg="#7f8c8d", bg="#eaf2f8")
    time_taken_label.pack()
    tk.Button(footer_frame, text="Exit", font=("Helvetica", 12), command=exit_app, bg="#e74c3c", fg="white").pack(pady=10)
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
