import json
import smtplib
from email.mime.text import MIMEText
from bcrypt import hashpw, gensalt, checkpw
from config import CONFIG

class Persistencia:
    @staticmethod
    def salvar_arquivo(nome_arquivo, dados):
        try:
            with open(nome_arquivo, 'w') as f:
                json.dump(dados, f, indent=4)
        except Exception as e:
            raise Exception(f"Erro ao salvar {nome_arquivo}: {e}")

    @staticmethod
    def carregar_arquivo(nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as e:
            raise Exception(f"Erro ao carregar {nome_arquivo}: {e}")

class EmailUtils:
    @staticmethod
    def enviar_email(destinatario, assunto, corpo):
        try:
            msg = MIMEText(corpo)
            msg['Subject'] = assunto
            msg['From'] = CONFIG['email_remetente']
            msg['To'] = destinatario

            server = smtplib.SMTP(CONFIG['smtp_server'], CONFIG['smtp_port'])
            server.starttls()
            server.login(CONFIG['email_remetente'], CONFIG['senha_email'])
            server.sendmail(CONFIG['email_remetente'], destinatario, msg.as_string())
            server.quit()

        except Exception as e:
            print(CONFIG['email_remetente'], CONFIG['senha_email'], f"'{CONFIG['smtp_server']}'", CONFIG['smtp_port'])
            raise Exception(f"Erro ao enviar email: {e}")

class HashUtils:
    @staticmethod
    def hash_senha(senha):
        return hashpw(senha.encode(), gensalt()).decode()

    @staticmethod
    def verificar_senha(senha, hash_senha):
        return checkpw(senha.encode(), hash_senha.encode())
