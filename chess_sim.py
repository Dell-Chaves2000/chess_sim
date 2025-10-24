import tkinter as tk
import time
import threading
import multiprocessing
import random
import array

# ===============================
# Representação das peças
# ===============================
PIECES = {
    "R": "♜", "N": "♞", "B": "♝", "Q": "♛", "K": "♚", "B":"♝", "N":"♞", "R":"♜", "P": "♟",
    "r": "♖", "n": "♘", "b": "♗", "q": "♕", "k": "♔", "b":"♗", "n":"♘", "r":"♖", "p": "♙"
}

# ===============================
# Classe do tabuleiro
# ===============================
class ChessGame:
    def __init__(self, canvas, cell_size=60):
        self.canvas = canvas
        self.cell_size = cell_size
        self.board = self.reset_board()
        self.draw_board()

    def reset_board(self):
        return [
            ["R","N","B","Q","K","B","N","R"],
            ["P","P","P","P","P","P","P","P"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["p","p","p","p","p","p","p","p"],
            ["r","n","b","q","k","b","n","r"]
        ]

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1, y1 = j*self.cell_size, i*self.cell_size
                x2, y2 = x1+self.cell_size, y1+self.cell_size
                color = "white" if (i+j)%2==0 else "gray"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                piece = self.board[i][j]
                if piece != " ":
                    piece_color = "black"
                    self.canvas.create_text(
                        x1+self.cell_size/2,
                        y1+self.cell_size/2,
                        text=PIECES[piece],
                        font=("Arial", 28),
                        fill=piece_color
                    )

    def make_random_move(self):
        pieces = [(i,j) for i in range(8) for j in range(8) if self.board[i][j] != " "]
        if not pieces: return
        i,j = random.choice(pieces)
        moves = [(x,y) for x in range(8) for y in range(8) if self.board[x][y]==" "]
        if not moves: return
        x,y = random.choice(moves)
        self.board[x][y] = self.board[i][j]
        self.board[i][j] = " "
        self.draw_board()

# ===============================
# Worker de processos (OPERACÃO PESADA - LENTO)
# ===============================
def process_worker(player, moves, interval, buffer_size, queue):
    # OPERAÇÃO PESADA: Cada processo cria e processa um buffer grande repetidamente
    for move in range(moves):
        # Cria um buffer enorme e faz operações complexas (LENTO)
        arr = [random.randint(1, 1000) for _ in range(buffer_size * 10)]  # 10x MAIOR
        # Operações matemáticas complexas para tornar mais lento
        result = sum(x * x for x in arr) + sum(x ** 0.5 for x in arr if x > 0)
        # Mais operações pesadas
        sorted_arr = sorted(arr[:1000])  # Ordena parte do array
        _ = sum(sorted_arr) * result
        
        time.sleep(interval/2000)  # METADE do sleep das threads
        queue.put(f"Processo {player} fez a jogada {move+1}")
    queue.put(f"Processo {player} terminou suas jogadas")

# ===============================
# Simulação Threads (OPERACÃO LEVE - RÁPIDO)
# ===============================
def simulate_threads(game, moves, interval, buffer_size, log_callback, done_callback):
    # OPERAÇÃO LEVE: Buffer compartilhado e pré-calculado
    shared_buffer = array.array('i', [i % 100 for i in range(buffer_size)])  # Buffer simples
    
    def worker(player):
        for move in range(moves):
            # Operação MUITO LEVE no buffer compartilhado
            total = sum(shared_buffer) % 1000  # Operação simples
            # Apenas verificação simples sem processamento pesado
            if total > 0:
                pass
                
            time.sleep(interval/1000)  # Sleep normal
            game.make_random_move()
            log_callback(f"Thread {player} fez a jogada {move+1}")
        log_callback(f"Thread {player} terminou suas jogadas.")

    t1 = threading.Thread(target=worker, args=(1,))
    t2 = threading.Thread(target=worker, args=(2,))
    start = time.time()
    t1.start(); t2.start()
    t1.join(); t2.join()
    end = time.time()
    done_callback("threads", end-start)

# ===============================
# Simulação Processos
# ===============================
def simulate_processes(game, moves, interval, buffer_size, log_callback, done_callback):
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=process_worker, args=(1, moves, interval, buffer_size, queue))
    p2 = multiprocessing.Process(target=process_worker, args=(2, moves, interval, buffer_size, queue))
    start = time.time()
    p1.start(); p2.start()

    finished_count = 0
    while finished_count < 2:
        try:
            msg = queue.get(timeout=0.1)
            log_callback(msg)
            game.make_random_move()
            if "terminou" in msg:
                finished_count += 1
        except:
            if not p1.is_alive() and not p2.is_alive():
                break

    p1.join(); p2.join()
    end = time.time()
    done_callback("processes", end-start)

# ===============================
# Interface Tkinter
# ===============================
class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação Xadrez: Threads vs Processos")

        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack(pady=10)

        frame_inputs = tk.Frame(root)
        frame_inputs.pack(pady=5)

        tk.Label(frame_inputs, text="Jogadas por jogador:").grid(row=0, column=0, padx=5)
        self.entry_moves = tk.Entry(frame_inputs, width=5)
        self.entry_moves.grid(row=0, column=1)
        self.entry_moves.insert(0, "10")  # Aumentado para melhor demonstração

        tk.Label(frame_inputs, text="Intervalo entre jogadas (ms):").grid(row=0, column=2, padx=5)
        self.entry_interval = tk.Entry(frame_inputs, width=5)
        self.entry_interval.grid(row=0, column=3)
        self.entry_interval.insert(0, "100")  # Reduzido

        # Buffer size fixo em 90000 (removida a seleção do usuário)
        self.buffer_size = 90000

        self.button = tk.Button(root, text="Iniciar Simulação", command=self.run_simulation)
        self.button.pack(pady=5)

        self.text_box = tk.Text(root, height=12, width=80)
        self.text_box.pack(pady=5)

        self.results = {}
        self.game = ChessGame(self.canvas)

    def log(self, msg):
        self.text_box.insert(tk.END, msg+"\n")
        self.text_box.see(tk.END)

    def run_simulation(self):
        self.text_box.delete("1.0", tk.END)
        self.results = {}
        try:
            moves = int(self.entry_moves.get())
            interval = int(self.entry_interval.get())
            # Buffer size é fixo em 90000, não precisa ler do usuário
            buffer_size = self.buffer_size
        except ValueError:
            self.log("Erro: Insira números válidos para jogadas e intervalo.")
            return

        self.log(f"Configuração: {moves} jogadas, {interval}ms intervalo, Buffer fixo: {buffer_size}")
        self.game = ChessGame(self.canvas)

        # Threads PRIMEIRO (sem delay)
        self.log("=== INICIANDO THREADS ===")
        threading.Thread(target=lambda: simulate_threads(
            self.game, moves, interval, buffer_size, self.log, self.save_result
        )).start()

        # Processos DEPOIS (com delay)
        self.root.after(100, lambda: [
            self.log("\n=== INICIANDO PROCESSOS ==="),
            threading.Thread(target=lambda: simulate_processes(
                self.game, moves, interval, buffer_size, self.log, self.save_result
            )).start()
        ])

    # ===============================
    # Resumo final em janela única
    # ===============================
    def save_result(self, mode, duration):
        self.results[mode] = duration
        if "threads" in self.results and "processes" in self.results:
            t_time = self.results["threads"]
            p_time = self.results["processes"]
            faster = "Threads" if t_time < p_time else "Processos"
            diff = abs(t_time - p_time)

            resumo_window = tk.Toplevel(self.root)
            resumo_window.title("Resumo Final da Simulação")
            resumo_window.geometry("450x300")
            resumo_window.resizable(False, False)

            tk.Label(resumo_window, text="===== RESUMO FINAL =====", font=("Arial", 14, "bold")).pack(pady=15)
            tk.Label(resumo_window, text=f"Tempo total (Threads): {t_time:.2f} s", font=("Arial", 12)).pack(pady=5)
            tk.Label(resumo_window, text=f"Tempo total (Processos): {p_time:.2f} s", font=("Arial", 12)).pack(pady=5)
            tk.Label(resumo_window, text=f"Mais rápido: {faster} por {diff:.2f} s", 
                    font=("Arial", 12, "bold"), fg="green" if faster == "Threads" else "red").pack(pady=10)

            if faster == "Threads":
                explanation = "✓ THREADS foram mais rápidas porque:\n• Compartilham memória diretamente\n• Operações leves e eficientes\n• Menos overhead de criação\n• Ideal para tarefas de E/S e simples"
            else:
                explanation = "✗ PROCESSOS foram mais rápidos porque:\n• Execução verdadeiramente paralela\n• Benefício em operações CPU-intensive\n• Evitam o GIL do Python"
            
            tk.Label(resumo_window, text=explanation, font=("Arial", 10), 
                    wraplength=400, justify="center").pack(pady=15)

# ===============================
# Execução
# ===============================
if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()