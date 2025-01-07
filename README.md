# Gerenciamento de Tarefas com Python

Este projeto consiste em um sistema de gerenciamento de tarefas orientado a objetos, desenvolvido em Python, com interface gráfica utilizando a biblioteca Tkinter. Ele permite que os usuários registrem eventos, gerenciem participantes e façam login/logout no sistema, além de possuir funcionalidades como recuperação de senha por e-mail e persistência de dados.

---

## Estrutura do Projeto

### Arquivos do Projeto

- **main.py**: Arquivo principal que inicializa o sistema e a interface gráfica.
- **sistema.py**: Contém as classes principais do sistema: `Aplicacao`, `Usuario` e `Evento`.
- **interface.py**: Define a interface gráfica utilizando a biblioteca Tkinter.
- **util.py**: Contém utilitários para persistência de dados, envio de e-mails e hashing de senhas.
- **config.py**: Configurações do sistema, carregadas a partir do arquivo `.env`.
- **.env**: Arquivo com as configurações sensíveis como credenciais de e-mail e nome do arquivo de persistência de dados.
- **dados.json**: Arquivo gerado automaticamente para armazenar os dados do sistema (criado após o primeiro uso).

---

## Funcionalidades

1. **Registro de Usuários**

   - Nome, e-mail e senha são necessários para registrar um usuário.
   - Senhas são armazenadas de forma segura utilizando hashing e salt.

2. **Login e Logout**

   - Usuários podem fazer login utilizando e-mail e senha.
   - Apenas usuários logados podem gerenciar eventos.

3. **Gerenciamento de Eventos**

   - Criar eventos com nome, descrição, data e hora de início e fim.
   - Adicionar participantes ao evento utilizando e-mails registrados no sistema.
   - Verificar conflitos de horário entre eventos.
   - Remover eventos criados por um usuário.

4. **Recuperação de Senha**

   - Envio de um código de recuperação de senha por e-mail.
   - Alteração de senha após a confirmação do código.

5. **Persistência de Dados**

   - Dados de usuários e eventos são armazenados em um arquivo JSON para serem carregados na próxima execução do programa.

6. **Interface Gráfica**

   - Interface amigável para interação com o sistema.
   - Fluxo intuitivo para registro, login, gerenciamento de eventos e recuperação de senha.

---

## Requisitos

1. **Bibliotecas Python**:

   - `tkinter`
   - `bcrypt`
   - `smtplib`
   - `email`
   - `json`
   - `python-dotenv`

   Instale todas as dependências necessárias utilizando o seguinte comando:

   ```bash
   pip install bcrypt python-dotenv
   ```

2. Configurações do Arquivo **.env**: Altere o arquivo `.env` no diretório do projeto com o seguinte conteúdo:

   ```
   EMAIL_REMETENTE=seu-email@gmail.com
   SENHA_EMAIL=sua-senha-de-app
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   ARQUIVO_DADOS=dados.json
   ```

   - `EMAIL_REMETENTE`: Endereço de e-mail utilizado para enviar os códigos de recuperação.
   - `SENHA_EMAIL`: Senha de aplicativo (não a senha normal do e-mail; use a senha gerada especificamente para aplicativos).
   - `SMTP_SERVER` e `SMTP_PORT`: Configurações do servidor SMTP do e-mail.
   - `ARQUIVO_DADOS`: Nome do arquivo de persistência de dados.

3. Você terá que pegar a senha de app para envio de email, pode seguir o seguinte tutorial: [Senha de App Gmail](https://youtu.be/JcF7CgrTpC4?si=1T4qNbbDdxVxRqzC)

---

## Como Usar

1. **Execute o Programa**

   - Utilize o comando abaixo para iniciar o sistema:
     ```bash
     python main.py
     ```

2. **Tela de Login**

   - Insira suas credenciais (e-mail e senha) para fazer login.
   - Caso não tenha uma conta, clique em "Registrar" para criar uma nova.
   - Se esqueceu sua senha, clique em "Esqueceu sua senha?" para iniciar o processo de recuperação.
   - Existe um usuário de teste em que o email é "teste@teste.com" e a senha é "teste"

3. **Registro de Usuários**

   - Informe Nome, E-mail e Senha nos campos correspondentes.
   - Clique em "Registrar" para criar sua conta.

4. **Recuperação de Senha**

   - Informe seu e-mail e clique em "Enviar código".
   - Um código será enviado ao e-mail informado.
   - Insira o código na tela seguinte e redefina sua senha.

5. **Tela Principal**

   - Após fazer login, você será redirecionado para a tela principal.
   - Aqui você pode:
     - Adicionar novos eventos.
     - Remover eventos existentes.
     - Ver os eventos dos quais você participa.

6. **Gerenciamento de Eventos**

   - **Adicionar Evento**:
     - Insira os detalhes do evento (nome, descrição, horários e e-mails dos participantes).
     - Clique em "Adicionar" para salvar o evento.
   - **Remover Evento**:
     - Selecione o evento na lista e clique em "Remover Evento".

7. **Logout**

   - Clique no botão "Logout" para encerrar sua sessão.

---

## Estrutura de Código

### Classes Principais

1. **sistema.py**:

   - `Usuario`: Representa um usuário do sistema.
   - `Evento`: Representa um evento com participantes e horários.
   - `Aplicacao`: Gerencia a lógica central do sistema, como registro de usuários, login, recuperação de senha e gerenciamento de eventos.

2. **interface.py**:

   - `InterfaceGrafica`: Gerencia a interface gráfica do usuário (GUI) e suas interações com a classe `Aplicacao`.

3. **util.py**:

   - `Persistencia`: Lê e grava dados no arquivo JSON.
   - `EmailUtils`: Envia e-mails utilizando o servidor SMTP.
   - `HashUtils`: Faz o hash de senhas e verifica sua validade.

4. **config.py**:

   - Carrega configurações sensíveis do arquivo `.env`.

---

## Possíveis Melhorias

- Permitir edição de eventos após a criação.
- Implementar autenticação em dois fatores para maior segurança.
- Adicionar suporte para diferentes idiomas.
- Incluir um sistema de notificações por e-mail para eventos próximos.
- Implementar suporte para sincronização com serviços de calendário externos, como Google Calendar.
- Adicionar uma funcionalidade de busca para facilitar o acesso a eventos específicos.
- Desenvolver relatórios estatísticos sobre eventos e usuários.
- Permitir integração com APIs de redes sociais para compartilhar eventos diretamente.

---

## Observações

- Certifique-se de que as configurações de e-mail no arquivo `.env` estão corretas para que o envio de e-mails funcione corretamente.
- Caso esteja usando Gmail, é necessário configurar uma senha de aplicativo (não a senha padrão do e-mail).
- O arquivo de dados (`dados.json`) será criado automaticamente após o primeiro uso.

---

## Conclusão

Este projeto é uma aplicação funcional e extensível para gerenciar tarefas e eventos. Com um foco em segurança e persistência de dados, ele oferece uma base sólida para futuros aprimoramentos e personalizações.

