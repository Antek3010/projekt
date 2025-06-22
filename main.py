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

        def update():
            idx = listbox.curselection()
            if not idx:
                messagebox.showwarning("Uwaga", "Nie zaznaczono elementu do edycji.")
                return

            current = dataset[idx[0]]
            new_name = simpledialog.askstring("Nowa nazwa", "Nowa nazwa:", initialvalue=current["name"])
            new_location = simpledialog.askstring("Nowa lokalizacja", "Nowa lokalizacja:",
                                                  initialvalue=current["location"])

            if not new_name or not new_location:
                messagebox.showwarning("Błąd", "Musisz podać nazwę i lokalizację.")
                return

            if type_ in ["clients", "employees"]:
                factory_names = [s["name"] for s in factory]

                factory_window = tk.Toplevel(window)
                factory_window.title("Wybierz nowy zakład przemysłowy")

                tk.Label(factory_window, text="Wybierz nowy zakład przemysłowy:").pack(pady=5)
                selected_factory = tk.StringVar()
                selected_factory.set(current.get("factory", factory_names[0]))

                tk.OptionMenu(factory_window, selected_factory, *factory_names).pack(pady=5)

                def confirm_update():
                    dataset[idx[0]] = {
                        "name": new_name,
                        "location": new_location,
                        "station": selected_factory.get()
                    }
                    factory_window.destroy()
                    refresh_list()

                tk.Button(factory_window, text="Zatwierdź", command=confirm_update).pack(pady=10)
            else:
                dataset[idx[0]] = {
                    "name": new_name,
                    "location": new_location
                }
                refresh_list()

        def show_map():
            get_grouped_map(dataset, f"{type_}_map.html")
            webbrowser.open(f"{type_}_map.html")

        # UI
        btn_frame = tk.Frame(window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Dodaj", command=add, width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Usuń", command=remove, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Aktualizuj", command=update, width=12).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Mapa", command=show_map, width=12).grid(row=0, column=3, padx=5)

        listbox = tk.Listbox(window, width=60, height=15)
        listbox.pack(padx=10, pady=10)

        refresh_list()

    def map_clients_of_factory():
        name = simpledialog.askstring("Zakład przemysłowy", "Podaj nazwę zakładu przemysłowego:")
        filtered = [c for c in clients if c['factory'] == name]
        if not filtered:
            messagebox.showinfo("Brak danych", "Brak klientów dla tego zakładu.")
            return
        get_grouped_map(filtered, "clients_of_factory.html")
        open_map("clients_of_factory.html")

    def map_employees_of_factory():
            name = simpledialog.askstring("Zakład przemysłowy", "Podaj nazwę zakładu:")
            filtered = [e for e in employees if e['factory'] == name]
            if not filtered:
                messagebox.showinfo("Brak danych", "Brak pracowników dla tego zakładu.")
                return
            get_grouped_map(filtered, "employees_of_factory.html")
            open_map("employees_of_factory.html")

