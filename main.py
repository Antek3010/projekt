import tkinter as tk
from tkinter import simpledialog , messagebox
from controller import get_grouped_map
from model import clients, employees, factory
import webbrowser

def gui_main():
    def open_map(file_name="mapa.html"):
        webbrowser.open(file_name)


    def make_menu(title, dataset, type_):
        window = tk.Toplevel(root)
        window.title(title)


        def refresh_list():
            listbox.delete(0, tk.END)
            for item in dataset:
                factory_info = f"       {item['factory']}" if "factory" in item else ""
                listbox.insert(tk.END, f"{item['name']}       {item['location']}{factory_info}")

        def add():
            name = simpledialog.askstring("Dodaj", "Podaj nazwę:")
            location = simpledialog.askstring("Dodaj", "Podaj lokalizację:")

            if not name or not location:
                messagebox.showwarning("Błąd", "Musisz podać nazwę i lokalizację.")
                return

            if type_ in ["clients", "employees"]:
                # Lista nazw istniejących zakładów przemysłowych
                factory_names = [s["name"] for s in factory]

                # Okno wyboru zakładu przemysłowego
                factory_window = tk.Toplevel(window)
                factory_window.title("Wybierz zakład przemysłowy")

                tk.Label(factory_window, text="Wybierz zakład przemysłowy dla tej osoby:").pack(pady=5)
                selected_factory = tk.StringVar()
                selected_factory.set(factory_names[0])  # domyślnie pierwszy zakład przemysłowy

                tk.OptionMenu(factory_window, selected_factory, *factory_names).pack(pady=5)

                def confirm_factory():
                    station = selected_factory.get()
                    dataset.append({
                        "name": name,
                        "location": location,
                        "station": station
                    })
                    factory_window.destroy()
                    refresh_list()

                tk.Button(factory_window, text="Zatwierdź", command=confirm_factory).pack(pady=10)
            else:
                dataset.append({
                    "name": name,
                    "location": location
                })
                refresh_list()

        def remove():
            idx = listbox.curselection()
            if not idx:
                messagebox.showwarning("Uwaga", "Nie zaznaczono elementu do usunięcia.")
                return
            dataset.pop(idx[0])
            refresh_list()
