from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

CONFIG = {
    "email_remetente": os.getenv("EMAIL_REMETENTE"),
    "senha_email": os.getenv("SENHA_EMAIL"),
    "smtp_server": os.getenv("SMTP_SERVER"),
    "smtp_port": int(os.getenv("SMTP_PORT")),
    "arquivo_dados": os.getenv("ARQUIVO_DADOS")
}