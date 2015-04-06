import codecs, re
f = codecs.open('vk/MDK_0.txt','r','cp1251')
r = f.readlines()
f.close()
x = []
'''
for line in r:
    if not re.search('\t|cerrar|editar|Me|Compartir|Sugerir|Adjuntar|foto|desarrolladores|vide|enlaces|nastya|evgenia|aleksandra|deos|gif|ginas|ksenia|segui|ivaro|Comentar|mostrar|Hace|temas|introducir|</.*?>|VK © 2014|debates|<video.*?>|Otros|advertising|CONTACTOS|Ilia|Darse|suscrito|Suscribirse|favoritos',line,re.IGNORECASE|re.UNICODE):
        x.append(line)
'''
l = open('mdk_text_final_0','w')
n = ''
author = ''
post = ''
for line in r:
    if line.startswith(('Compartir','hace','<','Ocultar','el','ayer','Mostrar')):
        continue
    if line.endswith('>\n'):
        author = re.sub('<.*>','',line).strip()
        continue
    if line.startswith('Me gusta'):
        post = '<message author= '+author+'>'+post+'</message>\n'
        n += post
        post = ''
    else:
        line = re.sub('\n',' ',line)
        line = re.sub('|Responder','',line)
        line = re.sub('<.*>','',line,re.DOTALL|re.IGNORECASE|re.UNICODE)
        post += line
l.write(n)
l.close()
