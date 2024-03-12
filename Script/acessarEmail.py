
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import csv

# Escopo necessário para acessar os e-mails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def obter_emails(credentials):
    # Construir serviço do Gmail
    service = build('gmail', 'v1', credentials=credentials)
    
    # Fazer a chamada para obter os e-mails
    resultados = service.users().messages().list(userId='me').execute()
    
    emails = []

    # Iterar sobre os resultados e obter os detalhes de cada e-mail
    for resultado in resultados.get('messages', []):
        msg = service.users().messages().get(userId='me', id=resultado['id']).execute()
        emails.append(msg['snippet'])  # Aqui você pode adicionar mais detalhes se desejar
    
    return emails

def salvar_emails_para_csv(lista_emails, nome_arquivo):
    # Abrir o arquivo CSV em modo de escrita
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo_csv:
        # Criar um escritor CSV
        escritor_csv = csv.writer(arquivo_csv)
        # Escrever cada e-mail na linha do arquivo CSV
        for email in lista_emails:
            escritor_csv.writerow([email])

def main():
    # Carregar credenciais
    creds = None
    # O arquivo token.json contém as credenciais de acesso e é criado automaticamente quando você executa pela primeira vez o código
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # Se não houver credenciais válidas, pedir ao usuário para autenticar
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salvar as credenciais para a próxima execução
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Obter os e-mails
    lista_emails = obter_emails(creds)

    # Salvar os e-mails em um arquivo CSV
    nome_arquivo = 'emails.csv'  # Substitua com o nome que deseja para o arquivo CSV
    salvar_emails_para_csv(lista_emails, nome_arquivo)
    print(f'Bah, os emails foram salvos com sucesso no arquivo "{nome_arquivo}".')

if __name__ == "__main__":
    main()
