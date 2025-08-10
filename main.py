
#Test 
#Beta 6

import sympy as sp
import tkinter as tk
from tkinter import messagebox
import time

coeff_entries = []

# Function to update equation preview
def update_preview():
    try:
        order = int(order_entry.get())
        coeffs = [entry.get() for entry in coeff_entries]
        eq_terms = []
        for i, coeff in enumerate(coeffs):
            if coeff:
                if order - i == 1:
                    eq_terms.append(f"{coeff}D*y")
                elif order - i == 0:
                    eq_terms.append(f"{coeff}y")
                else:
                    eq_terms.append(f"{coeff}D^{order - i}y")
        eq_text = " + ".join(eq_terms) + " = 0"
        preview_label.config(text=f"Equation Preview:\n{eq_text}", fg="darkblue")
    except:
        preview_label.config(text="Equation Preview:", fg="darkblue")

# Function to create styled output sections
def create_styled_section(parent, title, color):
    frame = tk.Frame(parent, bg="white", bd=3, relief="ridge")
    frame.pack(side="left", padx=10, pady=5, expand=True, fill="both")

    label = tk.Label(frame, text=title, font=("Arial", 14, "bold"), bg=color, fg="white", padx=10, pady=5)
    label.pack(fill="x")

    content = tk.Label(frame, text="", font=("Courier", 14, "bold"), fg="black", wraplength=400, justify="center")
    content.pack(pady=5, padx=5, expand=True, fill="both")

    return content

# Function to compute the differential equation
def compute():
    try:
        start_time = time.time()
        order = int(order_entry.get())
        coeffs = [float(coeff_entries[i].get()) for i in range(order + 1)]

        m = sp.symbols('m')
        aux_eq = sum(coeffs[i] * m**(order - i) for i in range(order + 1))
        aux_label.config(text=f"Auxiliary Equation:\n {sp.simplify(aux_eq)} = 0", fg="blue")

        roots = sp.solve(aux_eq, m)
        formatted_roots = [round(float(root), 2) if root.is_real else 
                           (round(float(sp.re(root)), 2) + round(float(sp.im(root)), 2) * 1j) 
                           for root in roots]
        root_text = "\n".join([f"Root {i+1}: {root}" for i, root in enumerate(formatted_roots)])
        root_label.config(text=f"Roots:\n{root_text}", fg="green")

        x = sp.symbols('x')
        cf_terms = []
        seen_roots = set()
        
        for root in formatted_roots:
            if root in seen_roots:
                continue
            seen_roots.add(root)

            if isinstance(root, complex):
                alpha, beta = root.real, abs(root.imag)
                cf_terms.append(f"exp({alpha:.2f}*x) * (C{len(cf_terms) + 1} * cos({beta:.2f}*x) + C{len(cf_terms) + 2} * sin({beta:.2f}*x))")
            else:
                if formatted_roots.count(root) == 1:
                    cf_terms.append(f"C{len(cf_terms) + 1} * exp({root:.2f}*x)")
                else:
                    for i in range(formatted_roots.count(root)):
                        cf_terms.append(f"C{len(cf_terms) + 1} * x^{i} * exp({root:.2f}*x)")

        cf_label.config(text="Complementary Function (CF):\n" + "\n".join(cf_terms), fg="purple")
        
        end_time = time.time()
        time_taken_label.config(text=f"Time Taken: {round(end_time - start_time, 4)} seconds", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input! {e}")

# Function to create coefficient entries
def create_coefficient_entries():
    global coeff_entries
    for widget in coeff_frame.winfo_children():
        widget.destroy()
    
    try:
        order = int(order_entry.get())
        coeff_entries = []

        entry_frame = tk.Frame(coeff_frame, bg="#e3f2fd")
        entry_frame.pack()

        for i in range(order + 1):
            row = tk.Frame(entry_frame, bg="#e3f2fd")
            row.pack(side="left", padx=5, pady=5)
            label_text = f"D^{order - i}y:" if order - i > 1 else ("Dy:" if order - i == 1 else "y:")
            label = tk.Label(row, text=label_text, fg="black", font=("Arial", 12))
            label.pack()
            entry = tk.Entry(row, font=("Arial", 12), width=10)
            entry.pack()
            entry.bind("<KeyRelease>", lambda event: update_preview())
            coeff_entries.append(entry)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid integer for order!")

# Function to reset UI
def reset():
    order_entry.delete(0, tk.END)
    for entry in coeff_entries:
        entry.delete(0, tk.END)
    preview_label.config(text="Equation Preview:", fg="darkblue")
    aux_label.config(text="Auxiliary Equation:", fg="blue")
    root_label.config(text="Roots:", fg="green")
    cf_label.config(text="Complementary Function (CF):", fg="purple")
    time_taken_label.config(text="Time Taken:", fg="red")

# Function to exit properly
def exit_app():
    root.destroy()

# Function to show applications
def show_applications():
    try:
        order = int(order_entry.get())
        applications = {
            1: "• Used in population growth models, Newton's law of cooling, and radioactive decay.",
            2: "• Common in physics, including harmonic motion, electrical circuits, and structural analysis.",
            3: "• Found in fluid mechanics, control systems, and nonlinear oscillations.",
            4: "• Used in beam deflection analysis, quantum mechanics, and elasticity theory.",
            5: "• Appears in fluid turbulence models and high-order control systems.",
            6: "• Found in aerospace engineering, wave propagation, and advanced structural mechanics.",
            7: "• Appears in complex vibration analysis and some mathematical physics models.",
            8: "• Used in high-precision optical systems and relativity-related calculations.",
            9: "• Found in advanced quantum field theory and turbulence modeling.",
            10: "• Used in high-order numerical methods, signal processing, and cosmological models.",
        }
        
        # Create a new window for displaying applications
        app_window = tk.Toplevel(root)
        app_window.title("Applications of Differential Equations")
        app_window.configure(bg="white")

        tk.Label(app_window, text=f"Applications for Order {order} Differential Equations", 
                 font=("Arial", 14, "bold"), bg="white", fg="black").pack(pady=10)

        text_widget = tk.Text(app_window, font=("Arial", 12), wrap="word", bg="white", height=10, width=60)
        text_widget.pack(padx=10, pady=5)
        text_widget.insert("1.0", applications.get(order, "Higher-order equations are used in advanced physics, engineering, and mathematics."))
        text_widget.config(state="disabled")  # Make it read-only

        tk.Button(app_window, text="Close", font=("Arial", 12), command=app_window.destroy, bg="#ff4d4d", fg="white").pack(pady=10)
    
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid order!")


# GUI Setup
root = tk.Tk()
root.title("DiffEqn Solver")
root.attributes('-fullscreen', True)
root.configure(bg="#e3f2fd")

top_frame = tk.Frame(root, bg="#bbdefb", bd=5, relief="groove")
top_frame.pack(fill="x")

frame = tk.Frame(root, bg="#bbdefb", bd=5, relief="groove")
frame.pack(pady=10, padx=10, fill="x")

tk.Label(frame, text="Enter the order of the differential equation:", font=("Arial", 14), bg="#bbdefb").pack()
order_entry = tk.Entry(frame, font=("Arial", 14), width=10)
order_entry.pack()
tk.Button(frame, text="Set Order", font=("Arial", 12), command=create_coefficient_entries, bg="#007ACC", fg="white").pack(pady=10)

coeff_frame = tk.Frame(root, bg="#e3f2fd")
coeff_frame.pack()

preview_label = tk.Label(root, text="Equation Preview:", font=("Arial", 14), fg="darkblue")
preview_label.pack(pady=5)

tk.Button(root, text="Compute", font=("Arial", 14, "bold"), command=compute, bg="#28A745", fg="white", padx=20, pady=5).pack(pady=10)

# Results section
results_frame = tk.Frame(root, bg="#ffffff", bd=5, relief="ridge")
results_frame.pack(pady=10, padx=10, fill="both", expand=True)

aux_label = create_styled_section(results_frame, "Auxiliary Equation", "blue")
root_label = create_styled_section(results_frame, "Roots", "green")
cf_label = create_styled_section(results_frame, "Complementary Function (CF)", "purple")

time_taken_label = tk.Label(root, text="Time Taken:", font=("Arial", 14), fg="red")
time_taken_label.pack(pady=5)

btn_frame = tk.Frame(root, bg="#e3f2fd")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Again", font=("Arial", 14), command=reset, bg="#FFA500", fg="white", padx=20, pady=5).pack(side="left", padx=20)
tk.Button(btn_frame, text="Applications", font=("Arial", 14), command=show_applications, bg="#007ACC", fg="white", padx=20, pady=5).pack(side="left", padx=20)
tk.Button(btn_frame, text="Exit", font=("Arial", 14), command=exit_app, bg="red", fg="white", padx=20, pady=5).pack(side="right", padx=20)

root.mainloop()

