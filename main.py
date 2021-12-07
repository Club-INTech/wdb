import serial as sr
import waiting as wt
import sys
import io


class WayneProbeSession:
  # Serial communication timeout in ms
  SERIAL_TIMEOUT_MS = 1e4

  # Messages for changing debugee clock speed
  CLOCK_DOWN = '8\n'
  CLOCK_UP = '1\n'

  # Messages for toggling debugWIRE
  DWIRE_ON = '+\n'
  DWIRE_OFF = '-\n'

  # Messages for entering debugging mode
  ENTER_DEBUG_SESSION = 'b\n'


  def __init__(self, port: str, ostream: io.StringIO):
    """
      Bind a debugging session to a serial port

      port -- port of the Wayne probe
      ostream -- output stream for communication logs
    """

    self._port = port
    self._ostream = ostream


  def __enter__(self):
    """
      Open a serial communication to a Wayne probe and automatically start a debugging session
    """
     
    # Open a serial communication to the Wayne probe and wait until it is up
    self._serial = sr.Serial(port=self._port, baudrate=115200, bytesize=8, parity=sr.PARITY_NONE, stopbits=sr.STOPBITS_ONE, timeout=self.SERIAL_TIMEOUT_MS)
    wt.wait(lambda : self._serial.in_waiting > 0, timeout_seconds=(self.SERIAL_TIMEOUT_MS * 1e-3))
    self._serial.read(self._serial.in_waiting)
    
    self._ostream.write(self._send(self.CLOCK_DOWN))
    self._ostream.write(self._send(self.DWIRE_ON))
    self._ostream.write(self._send(self.ENTER_DEBUG_SESSION))

    return self


  def __exit__(self, exception_type, value, traceback):
    """
      Restore debuggee configuration and close the serial communication
    """
    
    self._ostream.write(self._send('EXIT\n'))
    self._ostream.write(self._send(self.DWIRE_OFF))
    self._ostream.write(self._send(self.CLOCK_DOWN))
    self._serial.close()
      
  
  def next(self):
    """
      Reach next instruction
      
      return the Wayne probe response
    """

    return self._send('STEP\n')
  

  def _send(self, message: str):
    """
      Send a message to the Wayne probe and return the response
    """
    
    self._serial.write(message.encode())
    try:
      wt.wait(lambda : self._serial.in_waiting > 0, timeout_seconds=(self.SERIAL_TIMEOUT_MS * 1e-3))
      return self._serial.read(self._serial.in_waiting).decode('ascii')
    except:
      return None
    
  
with WayneProbeSession('/dev/ttyUSB0', sys.stdout) as session:
  while True:
    input()
    print(session.next())
