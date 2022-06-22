# minitask 1.3
# change the last du to DU
import re

pattern = re.compile(r'du(?!.*?(du).*?$)')
text = ['du du du', 'du po ledu', 'dopredu du', 'i dozadu du', 'dudu dupl']
for row in text:
    print(re.sub(pattern, 'DU', row))
