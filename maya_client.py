import socket
import traceback

class MayaClient(object):
    port = 20201
    BUFFER_SIZE = 4096

    def __init__(self):
        self.maya_socket = None
        self.port = MayaClient.port

    def connect(self, port = -1):
        if port >= 0:
            self.port = port
        try:
            self.maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.maya_socket.connect(("localhost", self.port))
        except:
            traceback.print_exc()
            return False
        return True

    def disconnect(self):
        try:
            self.maya_socket.close()
        except:
            traceback.print_exc()
            return False
        return True


    def send(self, cmd):
        try:
            self.maya_socket.sendall(cmd.encode())
        except:
            traceback.print_exc()
            return None
        return self.recv()

    def recv(self):
        try:
            data = self.maya_socket.recv(MayaClient.BUFFER_SIZE)
        except:
            traceback.print_exc()
        
        result = data.decode().replace("\x00", "")
        return result

    # commands
    def echo(self, text):
        cmd = "eval(\"'{0}'\")".format(text)
        return self.send(cmd)

    def newFile(self):
        cmd = 'cmds.file(new=True, force=True)'
        return self.send(cmd)

    def create_prim(self, shape):
        cmd = ''

        if shape == 'sphere':
            cmd += 'cmds.polySphere()'
        elif shape == 'cube':
            cmd += 'cmds.polyCube()'
        else:
            print("invalid shape: " + shape)
            return None

        result = self.send(cmd)
        return eval(result)

    def translate(self, nodeName, translation):
        cmd = "cmds.setAttr('{0}.translate', {1}, {2}, {3})".format(nodeName, *translation)
        return self.send(cmd)

if __name__ == '__main__':
    maya_client = MayaClient()
    print(maya_client.port)
    if maya_client.connect():
        print("connected succesfully")

        print("Echo: " + maya_client.echo("hello world"))
        fileName = maya_client.newFile()
        print(fileName)


        nodes = maya_client.create_prim('sphere')
        print(nodes)
        maya_client.translate(nodes[0], [0, 10, 0])
        nodes = maya_client.create_prim('cube')

        if maya_client.disconnect():
            print("disconnected succesfully")
            
            
    else:
        print("failed to connect")

    
    



