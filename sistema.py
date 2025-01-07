from datetime import datetime
from util import Persistencia, HashUtils, EmailUtils
from config import CONFIG
import smtplib
from email.mime.text import MIMEText
import hashlib

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

class Evento:
    def __init__(self, nome, descricao, data_hora_inicio, data_hora_fim):
        self.nome = nome
        self.descricao = descricao
        self.data_hora_inicio = data_hora_inicio
        self.data_hora_fim = data_hora_fim
        self.participantes = []

class Aplicacao:
    def __init__(self):
        self.eventos = []
        self.usuarios = []
        self.usuario_logado = None
        self.carregar_dados()

    def adicionar_evento(self, evento):
        if not self.usuario_logado:
            raise Exception("Usuário não está logado.")
        if self.verificar_conflito(evento):
            raise Exception("Conflito de horário com outro evento.")
        self.eventos.append(evento)
        self.salvar_dados()

    def remover_evento(self, evento_nome):
        evento = next((e for e in self.eventos if e.nome == evento_nome), None)
        if not evento:
            raise Exception("Evento não encontrado.")
        self.eventos.remove(evento)
        self.salvar_dados()

    def salvar_dados(self):
        Persistencia.salvar_arquivo(CONFIG['arquivo_dados'], {
            'eventos': [self.evento_para_dict(e) for e in self.eventos],
            'usuarios': [u.__dict__ for u in self.usuarios]
        })

    def carregar_dados(self):
        dados = Persistencia.carregar_arquivo(CONFIG['arquivo_dados'])
        self.usuarios = [Usuario(**u) for u in dados.get('usuarios', [])]
        self.eventos = [self.dict_para_evento(e) for e in dados.get('eventos', [])]

    def evento_para_dict(self, evento):
        return {
            'nome': evento.nome,
            'descricao': evento.descricao,
            'data_hora_inicio': evento.data_hora_inicio.strftime("%d/%m/%Y %H:%M"),
            'data_hora_fim': evento.data_hora_fim.strftime("%d/%m/%Y %H:%M"),
            'participantes': [p.email for p in evento.participantes]
        }

    def dict_para_evento(self, evento_dict):
        evento = Evento(
            evento_dict['nome'],
            evento_dict['descricao'],
            datetime.strptime(evento_dict['data_hora_inicio'], "%d/%m/%Y %H:%M"),
            datetime.strptime(evento_dict['data_hora_fim'], "%d/%m/%Y %H:%M")
        )
        evento.participantes = [self.buscar_usuario_por_email(email) for email in evento_dict['participantes']]
        return evento

    def verificar_conflito(self, novo_evento):
        return any(
            e.data_hora_inicio < novo_evento.data_hora_fim and novo_evento.data_hora_inicio < e.data_hora_fim
            for e in self.eventos
        )

    def registrar_usuario(self, nome, email, senha):
        if any(u.email == email for u in self.usuarios):
            raise Exception("Já existe um usuário registrado com este email.")
        hash_senha = HashUtils.hash_senha(senha)
        novo_usuario = Usuario(nome, email, hash_senha)
        self.usuarios.append(novo_usuario)
        self.salvar_dados()

    def login(self, email, senha):
        for usuario in self.usuarios:
            if usuario.email == email and HashUtils.verificar_senha(senha, usuario.senha):
                self.usuario_logado = usuario
                return
        raise Exception("Email ou senha incorretos.")
    
    def recuperar_senha(self, email):
        # Verifica se o email existe
        usuario = self.buscar_usuario_por_email(email)
        if usuario is None:
            raise Exception("Usuário não encontrado.")
        
        # Gera o código de recuperação
        codigo_recuperacao = self.gerar_codigo_recuperacao()
        
        # Envia o e-mail
        self.enviar_email_recuperacao(email, codigo_recuperacao)
        
        # Retorna o código gerado para comparação no processo de recuperação
        return codigo_recuperacao

    def buscar_usuario_por_email(self, email):
        for usuario in self.usuarios:
            if usuario.email == email:
                print(usuario)
                return usuario
        return None
    
    def gerar_codigo_recuperacao(self):
        return hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:6]

    def enviar_email_recuperacao(self, email, codigo):
        destinatario = email
        assunto = "Recuperação de Senha"
        corpo = f"Seu código de recuperação é: {codigo}"

        try:
            EmailUtils.enviar_email(destinatario, assunto, corpo)

        except Exception as e:
            raise Exception(f"Falha ao enviar e-mail de recuperação: {e}")


    def logout(self):
        self.usuario_logado = None