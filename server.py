import socket
import sala
 
TCP_IP = '127.0.0.1'
TCP_PORT = 8000
salas = sala.sala()
BUFFER_SIZE = 2048  # Normally 1024, but we want fast response
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
while True:
	s.listen(1)
	conn, addr = s.accept()

	print 'Connection address:', addr

	data = conn.recv(BUFFER_SIZE)

	if(data[:2] == 'CS'): #Cria Sala
		salas.adicionaConexao(conn,data[2:])

	if(data[:2] == 'EM'): #Envia Msg
		msg = data.split('KEYCONTROLLER')
		salas.enviaMsg(msg[2], msg[3], msg[1])

	if(data[:2] == 'LS'): #Lista de Salas
		lista = salas.listaSalas()
		out = ""
		for i in range(len(lista)):
			out = out + str(i+1)+'-'+lista[i]+'\n'
		conn.send(out)







#print "received data:", data
#conn.send(data.upper())
#conn.close()