import tkinter as tk
from tkinter import ttk, messagebox
import random

class KnapsackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Problema da Mochila - Algoritmo Genético com Valor Sentimental")
        self.master.geometry("700x600")

        self.items = []
        self.sentimental_item = None
        self.create_widgets()

    def create_widgets(self):
        # frame pra adc item
        add_frame = ttk.Frame(self.master, padding="10")
        add_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(add_frame, text="Peso:").grid(row=0, column=0, padx=5, pady=5)
        self.weight_entry = ttk.Entry(add_frame, width=10)
        self.weight_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Valor:").grid(row=0, column=2, padx=5, pady=5)
        self.value_entry = ttk.Entry(add_frame, width=10)
        self.value_entry.grid(row=0, column=3, padx=5, pady=5)

        self.sentimental_var = tk.BooleanVar()
        ttk.Checkbutton(add_frame, text="Item Sentimental", variable=self.sentimental_var).grid(row=0, column=4, padx=5, pady=5)

        ttk.Button(add_frame, text="Adicionar Item", command=self.add_item).grid(row=0, column=5, padx=5, pady=5)

        # lsita dos item
        self.item_listbox = tk.Listbox(self.master, width=50, height=10)
        self.item_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # botao manipular item 
        item_buttons_frame = ttk.Frame(self.master, padding="5")
        item_buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(item_buttons_frame, text="Deletar Item Selecionado", command=self.delete_selected_item).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(item_buttons_frame, text="Limpar Todos os Itens", command=self.clear_all_items).grid(row=0, column=1, padx=5, pady=5)

        # frame parametro 
        param_frame = ttk.Frame(self.master, padding="10")
        param_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(param_frame, text="Tamanho da População:").grid(row=0, column=0, padx=5, pady=5)
        self.pop_size_entry = ttk.Entry(param_frame, width=10)
        self.pop_size_entry.insert(0, "50")
        self.pop_size_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(param_frame, text="Gerações:").grid(row=1, column=0, padx=5, pady=5)
        self.generations_entry = ttk.Entry(param_frame, width=10)
        self.generations_entry.insert(0, "100")
        self.generations_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(param_frame, text="Taxa de Mutação:").grid(row=2, column=0, padx=5, pady=5)
        self.mutation_rate_entry = ttk.Entry(param_frame, width=10)
        self.mutation_rate_entry.insert(0, "0.1")
        self.mutation_rate_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(param_frame, text="Capacidade da Mochila:").grid(row=3, column=0, padx=5, pady=5)
        self.capacity_entry = ttk.Entry(param_frame, width=10)
        self.capacity_entry.insert(0, "50")
        self.capacity_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(param_frame, text="Penalidade Sentimental:").grid(row=4, column=0, padx=5, pady=5)
        self.sentimental_penalty_entry = ttk.Entry(param_frame, width=10)
        self.sentimental_penalty_entry.insert(0, "5")
        self.sentimental_penalty_entry.grid(row=4, column=1, padx=5, pady=5)

        # botao exec
        ttk.Button(self.master, text="Executar Algoritmo", command=self.run_algorithm).grid(row=4, column=0, columnspan=2, pady=10)

    def add_item(self):
        try:
            weight = float(self.weight_entry.get())
            value = float(self.value_entry.get())
            is_sentimental = self.sentimental_var.get()
            
            if is_sentimental and self.sentimental_item is not None:
                messagebox.showerror("Erro", "ja existe um item sentimental remova-o antes de adicionar outro")
                return
            
            item = (weight, value, is_sentimental)
            self.items.append(item)
            
            if is_sentimental:
                self.sentimental_item = item
                self.item_listbox.insert(tk.END, f"Peso: {weight}, Valor: {value} (Sentimental)")
            else:
                self.item_listbox.insert(tk.END, f"Peso: {weight}, Valor: {value}")
            
            self.weight_entry.delete(0, tk.END)
            self.value_entry.delete(0, tk.END)
            self.sentimental_var.set(False)
        except ValueError:
            messagebox.showerror("Erro", "insira valores numéricos validos")

    def delete_selected_item(self):
        try:
            index = self.item_listbox.curselection()[0]
            item = self.items[index]
            self.item_listbox.delete(index)
            self.items.pop(index)
            if item == self.sentimental_item:
                self.sentimental_item = None
        except IndexError:
            messagebox.showerror("Erro", "selecione pelo menos um item para deletar")

    def clear_all_items(self):
        self.item_listbox.delete(0, tk.END)
        self.items.clear()
        self.sentimental_item = None

    def run_algorithm(self):
        if not self.items:
            messagebox.showerror("Erro", "Adicione pelo menos um item antes de executar o algoritmo")
            return

        try:
            pop_size = int(self.pop_size_entry.get())
            generations = int(self.generations_entry.get())
            mutation_rate = float(self.mutation_rate_entry.get())
            capacity = float(self.capacity_entry.get())
            sentimental_penalty = float(self.sentimental_penalty_entry.get())
        except ValueError:
            messagebox.showerror("Erro", "insira valores validos para os parametros do algoritmo")
            return

        result = self.genetic_algorithm(pop_size, generations, mutation_rate, capacity, sentimental_penalty)
        self.show_result(result)

    def genetic_algorithm(self, pop_size, generations, mutation_rate, capacity, sentimental_penalty):
        def create_individual():
            return [random.randint(0, 1) for _ in range(len(self.items))]

        def fitness(individual):
            total_weight = sum(self.items[i][0] for i in range(len(individual)) if individual[i] == 1)
            if total_weight > capacity:
                return 0
            
            total_value = sum(self.items[i][1] for i in range(len(individual)) if individual[i] == 1)
            
            # verifica se tem item sentimental 
            if self.sentimental_item:
                sentimental_index = self.items.index(self.sentimental_item)
                if individual[sentimental_index] == 0:
                    #penalisar cado item sentimental nao esteja incluído
                    return 0
                else:
                    total_value -= sentimental_penalty
            
            return max(0, total_value) 

        def crossover(parent1, parent2):
            point = random.randint(1, len(parent1) - 1)
            return parent1[:point] + parent2[point:]

        def mutate(individual):
            for i in range(len(individual)):
                if random.random() < mutation_rate:
                    individual[i] = 1 - individual[i]
            return individual

        population = [create_individual() for _ in range(pop_size)]

        for _ in range(generations):
            population = sorted(population, key=fitness, reverse=True)
            new_population = population[:2]

            while len(new_population) < pop_size:
                parent1, parent2 = random.sample(population[:5], 2)
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_population.append(child)

            population = new_population

        best_solution = max(population, key=fitness)
        return best_solution

    def show_result(self, solution):
        total_weight = sum(self.items[i][0] for i in range(len(solution)) if solution[i] == 1)
        total_value = sum(self.items[i][1] for i in range(len(solution)) if solution[i] == 1)
        selected_items = [i+1 for i in range(len(solution)) if solution[i] == 1]
        
        sentimental_included = False
        if self.sentimental_item:
            sentimental_index = self.items.index(self.sentimental_item)
            sentimental_included = solution[sentimental_index] == 1

        result_text = f"Melhor solução encontrada:\n"
        result_text += f"Itens selecionados: {selected_items}\n"
        result_text += f"Peso total: {total_weight}\n"
        result_text += f"Valor total: {total_value}\n"
        if self.sentimental_item:
            result_text += f"Item sentimental incluído: {'Sim' if sentimental_included else 'Não'}\n"

        messagebox.showinfo("Resultado", result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()
