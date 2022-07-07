from socket import *

host = gethostname() # IP do Servidor
port = 35000 # Porta que o Servidor escuta
ip_port = (host, port)

cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect(ip_port)

msg_protocol_sucess = {
                        '+100': 'Jogo Vencido!',
                        '+200': "Letra enviada com sucesso!", 
                      }

msg_protocol_error = {
                        '+400': "Letra inválida!",
                        '+401': "Letra não existe na palavra!",
                        '+500': "Jogo Perdido!",
                        }

msg_protocol_game = {
                        '+300': "Digite uma letra: ",
                        '+301': "Digite S para jogar novamente: ",
}


def recebe_mensagem():
    msg_serv = cliente.recv(1024).decode()
    print(msg_serv)
    return msg_serv
    
def envia_mensagem():
    
    letra = input().rstrip()
    
    while len(letra)>1:
        letra = input("Digite apenas UMA letra: ").rstrip()
        
    msg_cliente = 'POST ' + letra
    
    cliente.send(msg_cliente.encode())

recebe_mensagem()

if __name__ == "__main__":

    while True:

        msg_serv = recebe_mensagem() # Recebe a mensagem de enviar letra

        if msg_serv == '+100':
            print(msg_protocol_sucess.get(msg_serv))
        
        elif msg_serv == '+200':
            print(msg_protocol_sucess.get(msg_serv))
        
        elif msg_serv == "+300":
            print(msg_protocol_game.get(msg_serv))
            envia_mensagem()
            
        elif msg_serv == "+301":
            print(msg_protocol_game.get(msg_serv))
            envia_mensagem()
            
        elif msg_serv == '+400':
            print(msg_protocol_error.get(msg_serv))
            
        elif msg_serv == '+401':
            print(msg_protocol_error.get(msg_serv))
        
        elif msg_serv == '+500':
            print(msg_protocol_error.get(msg_serv))
            