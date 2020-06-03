# XfoilPythonChallenge

 **This code does not work on my machine.**\
  I was never successfully able to receive data due to a In/Out fatal bug when running "PACC" and generating data in XFoil on my machine.\\
  Because of this, no polar data would ever output since XFoil would crash before the data could be written.\
  (While I use a library in this python application, the issue is in fact in XFoil)\
  Because I have no way to test this code, please takes this into consideration.\\
  If interested, the path to reproduce the issue (for me at least) is...\
  `XFoil: naca 0012` (standard airfoil for reproducibility)\
  `XFoil: oper`\
  `OPERi: PACC`\
  `polarfile.pol`\
  `a 0`\
  (Crash with error `Fortran runtime error: Sequential READ or WRITE not allowed after EOF marker, possibly use REWIND or BACKSPACE`)

Programming Challenge for Siemens application\
Using XFoil Python interface to perform calculations on NACA63(3)-618 airfoil\
Install from source using\
 `git clone https://github.com/leal26/AeroPy.git`\
 `cd AeroPy`\
  **If building on macOS** \
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`cp /path/to/XfoilPythonChallenge/xfoil_module.py .`\
 `pip3 install .`
 


