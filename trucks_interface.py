import tkinter as tk
from tkinter import simpledialog, messagebox


class BatchSchedulerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Batch Scheduler")

        self.v = [500, 250, 1500, 1200, 1200, 800]
        self.w = [4, 3, 10, 12, 9, 6]
        self.C = 30
        self.batch = []
        self.batchNumber = 0

        self.create_widgets()

    def weighted_interval_scheduling(self, batches):
        sorted_batches = sorted(batches, key=lambda x: x['end time'])
    
        n = len(sorted_batches)
        dp = [0] * n
        selected_batches = [None] * n 
    
        dp[0] = sorted_batches[0]['value']
        selected_batches[0] = [sorted_batches[0]['id']]

        for i in range(1, n):
            latest_non_overlapping = -1
            for j in range(i - 1, -1, -1):
                if sorted_batches[j]['end time'] <= sorted_batches[i]['start time']:
                    latest_non_overlapping = j
                    break

            include_current = sorted_batches[i]['value'] + (dp[latest_non_overlapping] if latest_non_overlapping != -1 else 0)
            exclude_current = dp[i - 1]

            if include_current > exclude_current:
                dp[i] = include_current
                selected_batches[i] = selected_batches[latest_non_overlapping] + [sorted_batches[i]['id']]
            else:
                dp[i] = exclude_current
                selected_batches[i] = selected_batches[i - 1]

        return dp[-1], selected_batches[-1]

    def knapsack(self, v, w, C):
        N = len(v)
        m = {}

        for c in range(C + 1):
            m[(0, c)] = 0

        for i in range(1, N + 1):
            m[(i, 0)] = 0
            for c in range(1, C + 1):
                if w[i - 1] <= c:
                    m[(i, c)] = max(m[(i - 1, c)], v[i - 1] + m[(i - 1, c - w[i - 1])])
                else:
                    m[(i, c)] = m[(i - 1, c)]

        selected_items = []
        i, c = N, C
        while i > 0 and c > 0:
            if m[(i, c)] != m[(i - 1, c)]:
                selected_items.append(i - 1)
                c -= w[i - 1]
            i -= 1

        for item in sorted(selected_items, reverse=True):
            del w[item]
            del v[item]

        return m[(N, C)]    

    def create_widgets(self):
        tk.Label(self.root, text="Main menu").pack()

        tk.Button(self.root, text="Inserir um pacote", command=self.insert_packet).pack()
        tk.Button(self.root, text="Mostrar pacotes", command=self.show_packets).pack()
        tk.Button(self.root, text="Eliminar pacotes", command=self.delete_packets).pack()
        tk.Button(self.root, text="Calcular batch", command=self.calculate_batch).pack()
        tk.Button(self.root, text="Mostrar batch", command=self.show_batches).pack()
        tk.Button(self.root, text="Eliminar batch", command=self.delete_batch).pack()
        tk.Button(self.root, text="Calcular schedule", command=self.calculate_schedule).pack()
        tk.Button(self.root, text="Sair", command=self.root.destroy).pack()

    def insert_packet(self):
        packet_weight = self.get_input("Digite o peso do pacote")
        if packet_weight is not None and packet_weight > 0 and packet_weight < self.C:
            packet_value = self.get_input("Digite o valor do pacote")
            if packet_value is not None and packet_value > 0:
                self.w.append(packet_weight)
                self.v.append(packet_value)
                messagebox.showinfo("Sucesso", "Pacote inserido com sucesso!")
            else:
                messagebox.showerror("Erro", "O valor do pacote deve ser maior que 0.")
        else:
            messagebox.showerror("Erro", "O peso do pacote deve ser maior que 0 e nao pode ser maior a capacidade do caminhão.")

    def show_packets(self):
        if len(self.w) > 0:
            packets_info = "\n".join([f"{i + 1}. Peso: {self.w[i]}, Valor: {self.v[i]}" for i in range(len(self.w))])
            self.show_info_window("Pacotes", packets_info)
        else:
            messagebox.showinfo("Pacotes", "Não há pacotes para mostrar.")

    def delete_packets(self):
        if len(self.w) > 0:
            packets_info = "\n".join([f"{i + 1}. Peso: {self.w[i]}, Valor: {self.v[i]}" for i in range(len(self.w))])
            index_to_delete = self.get_input("Digite o índice do pacote a ser removido") - 1
            if 0 <= index_to_delete < len(self.w):
                del self.w[index_to_delete]
                del self.v[index_to_delete]
                messagebox.showinfo("Sucesso", "Pacote removido com sucesso!")
            else:
                messagebox.showerror("Erro", "Índice inválido.")
        else:
            messagebox.showinfo("Eliminar pacotes", "Não há pacotes para eliminar.")

    def calculate_batch(self):
        while len(self.v) > 0 and len(self.w) > 0:
            start_h = self.get_input("Digite a hora de início para o trabalho")
            start_m = self.get_input("Digite o minuto de início para o trabalho")
            if 0 <= start_h <= 23 and 0 <= start_m <= 60:
                start_time = int(str(start_h) + str(start_m))

                end_h = self.get_input("Digite a hora de término para o trabalho")
                end_m = self.get_input("Digite o minuto de término para o trabalho")
                if 0 <= end_h <= 23 and 0 <= end_m <= 60:
                    end_time = int(str(end_h) + str(end_m))
                    if end_time > start_time:
                        self.batchNumber += 1
                        result = self.knapsack(self.v, self.w, self.C)
                        messagebox.showinfo("Resultado do lote", f"Valor máximo do lote: {result}")
                        new_batch = {'id': self.batchNumber, 'value': result, 'start time': start_time, 'end time': end_time}
                        self.batch.append(new_batch)
                    else:
                        messagebox.showerror("Erro", "A hora de término não pode ser anterior à hora de início.")
                else:
                    messagebox.showerror("Erro", "Hora de término inválida.")
            else:
                messagebox.showerror("Erro", "Hora de início inválida.")
        if len(self.v) <= 0 and len(self.w) <= 0:
            messagebox.showinfo("Calcular lote", "Não há mais pacotes para agrupar.")

    def show_batches(self):
        if len(self.batch) > 0:
            batches_info = "\n".join([f"{batch}" for batch in self.batch])
            self.show_info_window("Lotes", batches_info)
        else:
            messagebox.showinfo("Mostrar lotes", "Não há lotes para mostrar.")

    def delete_batch(self):
        if len(self.batch) > 0:
            batches_info = "\n".join([f"{batch}" for batch in self.batch])
            batch_to_delete = self.get_input("Digite o ID do lote a ser removido")
            if batch_to_delete is not None:
                found_batch = None
                for b in self.batch:
                    if b['id'] == batch_to_delete:
                        found_batch = b
                        break

                if found_batch:
                    self.batch.remove(found_batch)
                    messagebox.showinfo("Sucesso", "Lote removido com sucesso!")
                else:
                    messagebox.showerror("Erro", "Lote não encontrado.")
            else:
                messagebox.showerror("Erro", "ID de lote inválido.")
        else:
            messagebox.showinfo("Eliminar lotes", "Não há lotes para eliminar.")

    def calculate_schedule(self):
        sched_num = 0
        while len(self.batch) > 0:
            max_value, selected_batches = self.weighted_interval_scheduling(self.batch)
            schedule_info = f"Valor total do agendamento {sched_num + 1}: {max_value}\nConteúdo do agendamento {sched_num + 1}:\n{selected_batches}"
            self.show_info_window(f"Resultado do agendamento {sched_num + 1}", schedule_info)

            for batch_id in selected_batches:
                batch_index = next((index for (index, d) in enumerate(self.batch) if d["id"] == batch_id), None)

                if batch_index is not None:
                    del self.batch[batch_index]
            sched_num += 1
        if len(self.batch) < 1:
            messagebox.showinfo("Calcular agendamento", "Não há mais lotes para agendar.")

    def show_info_window(self, title, content):
        info_window = tk.Toplevel(self.root)
        info_window.title(title)

        info_label = tk.Label(info_window, text=content, padx=10, pady=10)
        info_label.pack()

    def get_input(self, prompt):
        user_input = simpledialog.askinteger("Input", prompt)
        return user_input

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = BatchSchedulerApp()
    app.run()
