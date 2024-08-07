import network
import espnow

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

now = espnow.ESPNow()
now.active(True)

def getMyMAC():
  return ":".join("%02X" % i for i in wlan.config('mac'))

def addPeer(addr):
  try:
    now.get_peer(addr)
  except OSError: # not found, can add
    try:
      now.add_peer(addr)
    except OSError:
      pass

addPeer(b'\xFF' * 6)

def send(msg, to="FF:FF:FF:FF:FF:FF"):
  addr = bytes(int(i, 16) for i in to.split(":"))
  addPeer(addr)
  try:
    now.send(addr, str(msg), True)
  except OSError:
    print("Send error !")
    pass

addr = None
buff = None
def isReadyToRead():
  global buff, addr
  addr, buff = now.irecv(10)
  if buff:
    return True
  else:
    return False

def getSenderMAC():
  return ":".join("%02X" % i for i in addr)

def readAsText():
  return buff.decode("utf-8") if buff else ""

def readAsNumber():
  if not buff:
    return 0
  try:
    return float(buff) if b'.' in buff else int(buff)
  except ValueError:
    pass
  return 0
