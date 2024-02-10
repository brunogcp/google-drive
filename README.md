<div align="center">
  <h3 align="center">Google Drive API</h3>
  <div>
  <a href="https://bgcp.vercel.app/article/cb3392ee-0a70-4c45-a226-d05917375272">
  <img src="https://img.shields.io/badge/Download PDF (ENGLISH)-black?style=for-the-badge&logoColor=white&color=000000" alt="three.js" />
  </a>
  </div>
</div>

## 🚀 Introdução à Google Drive API com Python

A Google Drive API permite que aplicativos interajam com o Google Drive, oferecendo funcionalidades para criar, modificar e compartilhar arquivos diretamente de sua aplicação Python. Este guia prático irá te ensinar a começar a usar a Google Drive API, abrindo um mundo de possibilidades para manipulação de arquivos na nuvem com Python.

### 🌟 Principais Características:

- **📂 Gestão Completa de Arquivos**: Crie, acesse, e modifique arquivos e pastas.
- **🔒 Segurança e Permissões**: Gerencie quem pode ver ou editar arquivos.
- **🔄 Sincronização em Tempo Real**: Mantenha seus aplicativos sincronizados com mudanças no Google Drive.
- **🌐 Integração Fácil**: Utilize em diversos projetos Python com facilidade.

## 🛠️ Instalação

Antes de começar, é necessário ter o Python instalado em sua máquina. Este guia assume que você já tem o Python e o pip, o gerenciador de pacotes do Python, instalados.

### Windows, Linux e macOS:

1. **Instale a biblioteca Google Client**:
   
   Abra o terminal e execute o seguinte comando para instalar a biblioteca Google API Client para Python:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## 📊 Uso Básico

### Configuração Inicial:

Para começar a usar a Google Drive API, você precisará criar um projeto no Google Cloud Platform e configurar as credenciais necessárias.

1. **Crie um Projeto no Google Cloud Platform (GCP)**:

    - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
    - Clique em "Criar Projeto".
    - Nomeie seu projeto e clique em "Criar".

2. **Ative a Google Drive API para seu projeto**:

    - No painel de navegação do GCP, vá até "APIs e Serviços" > "Biblioteca".
    - Procure por "Google Drive API" e clique em "Ativar".

3. **Configure as Credenciais**:

    - Ainda em "APIs e Serviços", vá até "Credenciais".
    - Clique em "Criar Credenciais" e selecione "ID do cliente OAuth".
    - Configure o consentimento do usuário, se necessário, e especifique as origens autorizadas.
    - Baixe o arquivo JSON com suas credenciais.

4. **Prepare seu Projeto Python**:

    - Crie um arquivo `quickstart.py` em seu projeto Python.
    - Insira o seguinte código para autenticar usando as credenciais baixadas e listar os primeiros 10 arquivos no seu Google Drive:

```python
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os, pickle

# Se modificar estes escopos, delete o arquivo token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # O arquivo token.pickle armazena os tokens de acesso e atualização do usuário, e é
    # criado automaticamente quando o fluxo de autorização é completado pela primeira vez.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # Se não há credenciais válidas disponíveis, deixa o usuário fazer login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salva as credenciais para a próxima execução
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Chama a Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('Nenhum arquivo encontrado.')
    else:
        print('Arquivos:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()
```

5. **Execute o script**:

    - Volte ao terminal e execute o script com `python quickstart.py`.
    - Siga as instruções na tela para autenticar através do navegador.

## 📈 Utilizando a Google Drive API para Gerenciamento de Arquivos

### Prática de Gerenciamento de Arquivos:

💡 Utilize a Google Drive API para criar, ler, atualizar e deletar arquivos. Isso permite que sua aplicação manipule dados na nuvem de forma poderosa e flexível.

### Motivo para Utilizar a API para Gerenciamento de Arquivos:

🚀 A automação de tarefas relacionadas a arquivos se torna extremamente eficiente, permitindo que você se concentre na lógica do seu aplicativo, enquanto a Google Drive API cuida do armazenamento.

### Implementação de Funções Básicas:

Vamos criar funções básicas para interagir com o Google Drive usando a Google Drive API em Python. Essas funções cobrirão a criação, leitura, atualização e deleção (CRUD) de arquivos no Google Drive.

### Configuração Inicial

Certifique-se de ter o arquivo `credentials.json` obtido ao configurar as credenciais no Google Cloud Console, conforme descrito anteriormente.

### Criação do Arquivo `drive_operations.py`
Para permitir a execução de funções específicas baseadas em argumentos passados pelo terminal, podemos modificar o script `drive_operations.py` para aceitar argumentos de linha de comando. Isso pode ser feito utilizando o módulo `argparse` do Python, que facilita a escrita de interfaces de linha de comando amigáveis.

```python
import argparse
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Defina o escopo de acesso necessário
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds)

def create_file(filename, mimetype, filepath):
    service = authenticate()
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")} - {filename} created.')

def list_files():
    service = authenticate()
    results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

def update_file(file_id, new_name, new_mimetype, new_filepath):
    service = authenticate()
    file_metadata = {'name': new_name}
    media = MediaFileUpload(new_filepath, mimetype=new_mimetype)
    updated_file = service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()
    print(f'File ID: {updated_file.get("id")} - {new_name} updated.')

def delete_file(file_id):
    service = authenticate()
    service.files().delete(fileId=file_id).execute()
    print(f'File {file_id} deleted.')

def main():
    parser = argparse.ArgumentParser(description="Google Drive API Python Script")
    parser.add_argument('action', help="Action to perform: create, list, update, delete")
    parser.add_argument('--filename', help="Name of the file to create/update")
    parser.add_argument('--mimetype', help="MIME type of the file to create/update")
    parser.add_argument('--filepath', help="Path of the file to create/update")
    parser.add_argument('--fileid', help="ID of the file to update/delete")
    parser.add_argument('--newname', help="New name of the file for update")
    args = parser.parse_args()

    if args.action == 'create':
        if args.filename and args.mimetype and args.filepath:
            create_file(args.filename, args.mimetype, args.filepath)
        else:
            print("Missing arguments for creation.")
    elif args.action == 'list':
        list_files()
    elif args.action == 'update':
        if args.fileid and args.newname and args.mimetype and args.filepath:
            update_file(args.fileid, args.newname, args.mimetype, args.filepath)
        else:
            print("Missing arguments for update.")
    elif args.action == 'delete':
        if args.fileid:
            delete_file(args.fileid)
        else:
            print("File ID required for deletion.")
    else:
        print("Invalid action. Please choose from 'create', 'list', 'update', 'delete'.")

if __name__ == '__main__':
    main()
```

### Como Usar

Aqui estão alguns exemplos de como você pode agora executar o script com argumentos do terminal:

- **Para listar arquivos**:
  
  ```bash
  python drive_operations.py list
  ```

- **Para criar um arquivo** (substitua os valores conforme necessário):

  ```bash
  python drive_operations.py create --filename "NovoDocumento.txt" --mimetype "text/plain" --filepath "/path/to/your/file.txt"
  ```

- **Para atualizar um arquivo** (substitua `file_id` e outros valores conforme necessário):

  ```bash
  python drive_operations.py update --fileid "your_file_id" --newname "DocumentoAtualizado.txt" --mimetype "text/plain" --filepath "/path/to/new/file.txt"
  ```

- **Para deletar um arquivo** (substitua `file_id` conforme necessário):

  ```bash
  python drive_operations.py delete --fileid "your_file_id"
  ```

Este script agora aceita comandos do terminal para executar operações específicas na Google Drive API, tornando-o mais versátil e útil para scripts e automações.

### 🔍 Testes:

1. **Criação e Leitura**:
    - Crie um arquivo de teste usando a API e verifique no seu Google Drive se o arquivo aparece.

2. **Atualização**:
    - Modifique o arquivo criado e confira se as mudanças são refletidas no Drive.

3. **Deleção**:
    - Delete o arquivo e verifique se ele foi removido do seu Drive.

## 🏆 Conclusão

Com este tutorial, você aprendeu a configurar e utilizar a Google Drive API com Python para gerenciar arquivos na nuvem. Isso abre um leque de possibilidades para aplicações que exigem interação com armazenamento na nuvem, desde a automação de tarefas de escritório até aplicações complexas que manipulam grandes volumes de dados.

Espero que este guia tenha sido informativo e útil, dando a você as ferramentas necessárias para incorporar a Google Drive API em seus projetos Python. Continue explorando as possibilidades, e divirta-se programando! 🐍☁️