import sys, cgi
import cgi, search_engine.lib.html as html

form = cgi.FieldStorage()

#dimensions for link space
dim = form.getvalue('d')

#vector in link space
v = form.getvalue('v')

if dim == None:
    dim = [3,3,3]
else:
   dim = map(lambda x: int(x), dim)

if v == None:
    v = [0 for i in dim]
else:
   v = map(lambda x: int(x), v)

def get_link(v):
    s = './web.py'
    for i, x in enumerate(dim):
        if i == 0:
            s += '?'
        else:
            s += '&'
        s += 'd=' + str(x)
        
    for i, x in enumerate(v):
        s += '&v=' + str(x)
        
    return s

def update(v, k, d):
    for i, x in enumerate(v):
        if i == k:
            yield (x + d) % dim[i]
        else:
            yield x

html.header()
print '<form action="index.py"><input name="s" type="submit" value="search"></form>'
#show vector v and links to connected vectors
for i, x in enumerate(v):
    print '<div>'
    html.a(get_link(update(v, i, -1)), '<<')    
    print '%s (%s)' % (x, dim[i])
    html.a(get_link(update(v, i, 1)), '>>')
    print '</div>'
html.footer()
