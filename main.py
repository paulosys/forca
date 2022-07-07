import threading
from socket import *
import time
from Forca import *

jogoComecou = False
jogadores = {}
mutex_letra = threading.Semaphore(1)  # semaforo do tipo mutex
podeJogar = False

quant_jogadores = int(input("Digite a quantidade de jogadores: "))
jogadores_conectados = 0


forca = Forca(input("Digite a palavra a ser encontrada: "), input("Digite a dica da palavra: "))

def send_msg(cliente_socket, msg):
    cliente_socket.send(bytes(msg, "utf-8"))
    
    
def receive_msg(con):
    msg = con.recv(1024).decode()
    comando, letra = msg.split()
    
    if comando.upper() == "POST":
        
        return letra
    
    else:
        print("Comando inválido")


def send_msg_to_all(msg):
    for jogador in jogadores.values():
        jogador.send(bytes(msg, "utf-8"))


def handlerClient(con, cliente):

    send_msg(con, "Aguarde o jogo começar")

    while not jogoComecou:
        time.sleep(1)

    while jogoComecou:
        changeLetra(con)


def get_jogadores(sock):
    global jogadores_conectados, quant_jogadores

    print("\nAguardando jogadores...")
    
    while jogadores_conectados != quant_jogadores:
        cliente_socket, cliente_adr = sock.accept()
        
        jogadores[jogadores_conectados] = cliente_socket
        jogadores_conectados += 1
        thread = threading.Thread(target=handlerClient, args=(cliente_socket, cliente_adr))
        thread.start()
        print(f"\n{cliente_adr} conectado... restam {quant_jogadores - jogadores_conectados} jogadores para iniciar o jogo.")


def game():
    global podeJogar, jogoComecou, jogadores, mutex_letra
    
    print("\nJogo iniciado...")
    jogoComecou = True
    
    print(forca.getForca())
    send_msg_to_all(forca.getForca())
    
    while True:
        
        while not forca.descobriuPalavra() and forca.getQntdErros() < 6: 
            if podeJogar:
                forca.rodada(letra)
                
                mForca = forca.getForca()
                
                send_msg_to_all(mForca)
                
                if forca.descobriuPalavra():
                    send_msg_to_all("+100")
                    print("\nParabéns, você ganhou!")
                    break
                
                if forca.getQntdErros() == 6:
                    send_msg_to_all("+500")
                    print("\nVocê perdeu!")
                    break
                
                podeJogar = False
                mutex_letra.release()

        print("\nJogo finalizado...")
            
        send_msg(jogadores[0], '+301')
        
        opcao = receive_msg(jogadores[0])
        print("opcao: ", opcao)
        
        if opcao.upper() == "S":
            print("entrou")
            forca.resetar()
            mutex_letra.release()
            podeJogar = False
            
        else:
            print("\nFinalizando...")
            for jogador in jogadores.values():
                jogador.close()
            break


def changeLetra(cliente_socket):
    global mutex_letra, letra, podeJogar

    mutex_letra.acquire()

    try:
        send_msg(cliente_socket, "+300")

        nova_letra = receive_msg(cliente_socket)
        
        forca.verificarLetra(nova_letra)
        
        letra = nova_letra

    except ForcaException as e:
        print(str(e))
        
        send_msg(cliente_socket, "+400")
        
        print(forca.getForca())
        send_msg_to_all(forca.getForca())
        mutex_letra.release()
        changeLetra(cliente_socket)
        
    except ValueError as e:
        send_msg(cliente_socket, "+401")
        print(forca.getForca())
        send_msg_to_all(forca.getForca())
        mutex_letra.release()
        time.sleep(1)
        
    else:
        send_msg(cliente_socket, "+200")
        podeJogar = True 
        
      
def main():
    
    HOST =  '0.0.0.0' # IP do Servidor
    PORT = 35000 # Porta que o Servidor escuta

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((HOST, PORT))

    sock.listen(quant_jogadores)
    
    print("\nServidor iniciado...")
    
    get_jogadores(sock)
    
    game()


if __name__ == "__main__":
    main()