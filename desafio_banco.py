import tkinter as tk
from tkinter import messagebox
import threading
import time

# --- Dados bancários iniciais ---
saldo = 1800
limite = 900
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 2
numero_depositos = 0
LIMITE_DEPOSITOS = 3
total_sacado = 0
total_depositado = 0

nome = input("Digite seu nome para acessar o Internet Banking: ")

# --- Funções principais ---

def atualizar_saldo_label():
    label_saldo.config(text=f"Saldo atual: R$ {saldo:.2f}")

def deposito():
    global saldo, extrato, numero_depositos, total_depositado
    try:
        valor = float(entry_valor.get())
        if numero_depositos >= LIMITE_DEPOSITOS:
            messagebox.showinfo("Limite de depósitos", f"Você já realizou o limite de {LIMITE_DEPOSITOS} depósitos.")
        elif valor <= 0:
            messagebox.showwarning("Aviso", "Não é permitido depositar valores negativos ou zero.")
        elif total_depositado + valor > total_sacado:
            restante = total_sacado - total_depositado
            messagebox.showwarning("Limite de depósito", f"Você só pode depositar no máximo R$ {restante:.2f} para repor o que foi sacado.")
        else:
            saldo += valor
            total_depositado += valor
            numero_depositos += 1
            extrato_linha = f"Depósito: +R$ {valor:.2f}\n"
            extrato += extrato_linha
            atualizar_saldo_label()
            animar_saldo()
    except ValueError:
        messagebox.showwarning("Erro", "Digite um valor numérico válido.")

def saque():
    global saldo, extrato, numero_saques, total_sacado
    try:
        valor = float(entry_valor.get())
        if numero_saques >= LIMITE_SAQUES:
            messagebox.showinfo("Limite atingido", "Você já realizou o número máximo de saques hoje.")
        elif valor <= 0:
            messagebox.showwarning("Aviso", "Não é permitido sacar valores negativos ou zero.")
        elif valor > saldo:
            messagebox.showwarning("Saldo insuficiente", "Você não tem saldo suficiente para esse saque.")
        elif valor > limite:
            messagebox.showwarning("Limite por saque", f"O limite por saque é R$ {limite:.2f}")
        else:
            saldo -= valor
            total_sacado += valor
            numero_saques += 1
            extrato_linha = f"Saque: -R$ {valor:.2f}\n"
            extrato += extrato_linha
            atualizar_saldo_label()
            animar_saldo()
    except ValueError:
        messagebox.showwarning("Erro", "Digite um valor numérico válido.")

def mostrar_extrato():
    resumo = extrato if extrato else "Não foram realizadas movimentações."
    resumo += f"\nTotal sacado: R$ {total_sacado:.2f}"
    resumo += f"\nTotal depositado: R$ {total_depositado:.2f}"
    messagebox.showinfo("Extrato", resumo)

# --- Animação do saldo (pulse suave) ---
def animar_saldo():
    def pulse():
        original_color = label_saldo.cget("fg")
        for i in range(3):
            label_saldo.config(fg="#00aa00")
            time.sleep(0.2)
            label_saldo.config(fg=original_color)
            time.sleep(0.2)
    threading.Thread(target=pulse, daemon=True).start()

# --- Interface Tkinter ---
janela = tk.Tk()
janela.title("Internet Banking - Seu Banco")
janela.geometry("400x320")
janela.configure(bg="#ffffff")

label_nome = tk.Label(janela, text=f"Bem-vindo, {nome}!", font=("Helvetica", 14, "bold"), bg="#ffffff")
label_nome.pack(pady=10)

label_saldo = tk.Label(janela, text=f"Saldo atual: R$ {saldo:.2f}", font=("Helvetica", 12), bg="#ffffff")
label_saldo.pack(pady=5)

entry_valor = tk.Entry(janela, font=("Helvetica", 12), justify='center')
entry_valor.pack(pady=10)
entry_valor.insert(0, "0.00")

frame_botoes = tk.Frame(janela, bg="#ffffff")
frame_botoes.pack(pady=5)

botao_depositar = tk.Button(frame_botoes, text="Depositar", command=deposito, width=12, bg="#d0ffd0")
botao_depositar.grid(row=0, column=0, padx=5)

botao_sacar = tk.Button(frame_botoes, text="Sacar", command=saque, width=12, bg="#ffd0d0")
botao_sacar.grid(row=0, column=1, padx=5)

botao_extrato = tk.Button(janela, text="Ver Extrato", command=mostrar_extrato, width=26, bg="#d0e0ff")
botao_extrato.pack(pady=10)

botao_sair = tk.Button(janela, text="Fechar", command=janela.destroy, width=26, bg="#cccccc")
botao_sair.pack(pady=5)

janela.mainloop()
