import sys
from io import StringIO

sys.stderr.write('Eugenio')

old_stderr = sys.stderr
sys.stderr = mystderr = StringIO()

sys.stderr.write('Eugenio2')

sys.stderr = old_stderr

print('Err:',mystderr.getvalue())

with open('jkhdkjdhkjdhkjdhd.txt','r') as f:
    x = f.read()