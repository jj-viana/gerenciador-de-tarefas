import tkinter as tk
from tkinter import messagebox
from sistema import Aplicacao, Evento
from util import HashUtils
from datetime import datetime

class InterfaceGrafica:
    def __init__(self, sistema):
        self.sistema = sistema
        self.root = tk.Tk()
        self.root.title("Sistema de Eventos")
        self.tela_login()

    def tela_login(self):
        self.limpar_tela()
        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        tk.Label(self.root, text="Senha").pack()
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.pack()
        tk.Button(self.root, text="Login", command=self.fazer_login).pack()
        tk.Button(self.root, text="Registrar", command=self.tela_registro).pack()
        tk.Button(self.root, text="Esqueceu sua senha?", command=self.tela_recuperar_senha).pack()


    def fazer_login(self):
            try:
                self.sistema.login(self.email_entry.get(), self.senha_entry.get())
                self.tela_principal()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def tela_registro(self):
        self.limpar_tela()
        tk.Label(self.root, text="Nome").pack()
        self.nome_entry = tk.Entry(self.root)
        self.nome_entry.pack()
        tk.Label(self.root, text="Email").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        tk.Label(self.root, text="Senha").pack()
        self.senha_entry = tk.Entry(self.root, show="*")
        self.senha_entry.pack()
        tk.Button(self.root, text="Registrar", command=lambda: [self.registrar_usuario(), self.tela_login()]).pack()
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def registrar_usuario(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            self.sistema.registrar_usuario(nome, email, senha)
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.tela_login()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_recuperar_senha(self):
        self.limpar_tela()
        tk.Label(self.root, text="Informe seu e-mail").pack()
        self.email_recuperacao_entry = tk.Entry(self.root)
        self.email_recuperacao_entry.pack()
        tk.Button(self.root, text="Enviar código", command=self.enviar_codigo).pack()
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def enviar_codigo(self):
        email = self.email_recuperacao_entry.get()
        
        if not email:
            messagebox.showerror("Erro", "O e-mail é obrigatório!")
            return
        
        try:
            # Inicia o processo de recuperação
            codigo_recuperacao = self.sistema.recuperar_senha(email)
            
            # Solicita o código de recuperação
            self.tela_confirmar_codigo(codigo_recuperacao, email)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def tela_confirmar_codigo(self, codigo_recuperacao, email):
        self.limpar_tela()
        tk.Label(self.root, text="Informe o código de recuperação").pack()
        self.codigo_entry = tk.Entry(self.root)
        self.codigo_entry.pack()
        tk.Button(self.root, text="Confirmar código", command=lambda: self.confirmar_codigo(codigo_recuperacao, email)).pack()
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def confirmar_codigo(self, codigo_recuperacao, email):
        codigo_informado = self.codigo_entry.get()
        
        if codigo_informado != codigo_recuperacao:
            messagebox.showerror("Erro", "Código incorreto. Tente novamente.")
            return
        
        self.tela_nova_senha(email)

    def tela_nova_senha(self, email):
        self.limpar_tela()
        tk.Label(self.root, text="Informe a nova senha").pack()
        self.nova_senha_entry = tk.Entry(self.root, show="*")
        self.nova_senha_entry.pack()
        tk.Button(self.root, text="Alterar senha", command=lambda: self.alterar_senha(email)).pack()
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def alterar_senha(self, email):
        nova_senha = self.nova_senha_entry.get()
        
        if not nova_senha:
            messagebox.showerror("Erro", "A nova senha é obrigatória!")
            return
        
        try:
            # Busca o usuário e atualiza a senha
            usuario = self.sistema.buscar_usuario_por_email(email)
            if not usuario:
                raise Exception("Usuário não encontrado.")

            usuario.senha = HashUtils.hash_senha(nova_senha)

            # Salva os dados atualizados
            self.sistema.salvar_dados()

            # Exibe uma mensagem de sucesso
            messagebox.showinfo("Sucesso", "Senha alterada com sucesso!")

            # Retorna à tela de login
            self.tela_login()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar senha: {str(e)}")




    def tela_principal(self):
        self.limpar_tela()
        tk.Label(self.root, text=f"Bem-vindo, {self.sistema.usuario_logado.nome}").pack()
        tk.Button(self.root, text="Adicionar Evento", command=self.tela_adicionar_evento).pack()
        tk.Button(self.root, text="Remover Evento", command=self.remover_evento_selecionado).pack()

        # Adiciona a lista de eventos do usuário
        tk.Label(self.root, text="Seus Eventos:").pack()
        self.lista_eventos = tk.Listbox(self.root)
        self.lista_eventos.pack()
        
        for evento in self.sistema.eventos:
            if self.sistema.usuario_logado in evento.participantes:
                self.lista_eventos.insert(tk.END, evento.nome)

        tk.Button(self.root, text="Logout", command=self.logout).pack()

    def tela_adicionar_evento(self):
        self.limpar_tela()
        tk.Label(self.root, text="Nome do Evento").pack()
        self.nome_evento_entry = tk.Entry(self.root)
        self.nome_evento_entry.pack()
        tk.Label(self.root, text="Descrição do Evento").pack()
        self.descricao_evento_entry = tk.Entry(self.root)
        self.descricao_evento_entry.pack()
        tk.Label(self.root, text="Data e Hora de Início (dd/mm/yyyy HH:MM)").pack()
        self.data_hora_inicio_evento_entry = tk.Entry(self.root)
        self.data_hora_inicio_evento_entry.pack()
        tk.Label(self.root, text="Data e Hora de Fim (dd/mm/yyyy HH:MM)").pack()
        self.data_hora_fim_evento_entry = tk.Entry(self.root)
        self.data_hora_fim_evento_entry.pack()
        tk.Label(self.root, text="Emails dos Participantes (separados por vírgula)").pack()
        self.participantes_entry = tk.Entry(self.root)
        self.participantes_entry.pack()
        tk.Button(self.root, text="Adicionar", command=self.adicionar_evento).pack()
        tk.Button(self.root, text="Voltar", command=self.tela_principal).pack()

    def adicionar_evento(self):
        nome_evento = self.nome_evento_entry.get()
        descricao_evento = self.descricao_evento_entry.get()
        data_hora_inicio_evento = self.data_hora_inicio_evento_entry.get()
        data_hora_fim_evento = self.data_hora_fim_evento_entry.get()
        participantes = self.participantes_entry.get().split(",")

        if not nome_evento or not descricao_evento or not data_hora_inicio_evento or not data_hora_fim_evento or not participantes:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios")
            return

        try:
            data_hora_inicio = datetime.strptime(data_hora_inicio_evento, "%d/%m/%Y %H:%M")
            data_hora_fim = datetime.strptime(data_hora_fim_evento, "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data e hora inválido")
            return

        if data_hora_inicio >= data_hora_fim:
            messagebox.showerror("Erro", "A data e hora de início deve ser anterior à data e hora de fim")
            return

        evento = Evento(nome_evento, descricao_evento, data_hora_inicio, data_hora_fim)
        for email in participantes:
            email = email.strip()
            participante = self.sistema.buscar_usuario_por_email(email)
            if participante:
                evento.participantes.append(participante)
            else:
                messagebox.showwarning("Aviso", f"Usuário com email {email} não encontrado")

        try:
            self.sistema.adicionar_evento(evento)
            messagebox.showinfo("Sucesso", "Evento adicionado com sucesso!")
            self.tela_principal()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_evento_selecionado(self):
            selecionado = self.lista_eventos.curselection()
            if not selecionado:
                messagebox.showwarning("Aviso", "Nenhum evento selecionado.")
                return
            
            evento_nome = self.lista_eventos.get(selecionado)
            evento = next((e for e in self.sistema.eventos if e.nome == evento_nome), None)
            
            if evento and self.sistema.usuario_logado in evento.participantes:
                if messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover o evento '{evento_nome}'?"):
                    try:
                        self.sistema.remover_evento(evento_nome)
                        messagebox.showinfo("Sucesso", "Evento removido com sucesso.")
                        self.tela_principal()
                    except Exception as e:
                        messagebox.showerror("Erro", str(e))
            else:
                messagebox.showwarning("Aviso", "Você não tem permissão para remover este evento.")


    def logout(self):
        self.sistema.logout()
        self.tela_login()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()
