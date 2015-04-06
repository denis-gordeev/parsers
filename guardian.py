import os,re
posts = ''
number = 0
for file in os.listdir('.'):
    if file.startswith(('parse','all')):
        continue
    f = open(file)
    r = f.read()
    f.close()
    r = re.sub('\n',' ',r)
    r = re.sub('\t',' ',r)
    r = re.sub('\a',' ',r)
    r = re.sub('\b',' ',r)
    r = re.sub('\f',' ',r)
    r = re.sub('\r',' ',r)
    r = re.sub('\v',' ',r)
    r = re.sub(' +',' ',r)
    posts_rough = re.findall('(Recommend.*?\*\d+\*)(.*?Recommend.*?\*\d+\*)',r)
    
    for post in posts_rough:
        if len(post)<2:
            continue
        post = re.sub('[+o] Report.*','',post[1])
        print post[:10]
        post = re.sub('>>\d+', '', post)
        post = re.sub('<span class="unkfunc">&gt;','',post)
        post = re.sub('<br>',' ',post)
        post = re.sub('<[/]?strong>','\n',post)
        post = re.sub('<[/]?span.*?>','\n',post)
        post = re.sub('&quot;','"',post)
        post = re.sub('&quot;?','"',post)
        post = re.sub('&#47;','/',post)
        post = '<message>'+post.strip()+'</message>\n'
        posts += post
        number += 1
f = open('all.txt','w')
f.write(posts)
f.close()
print number
