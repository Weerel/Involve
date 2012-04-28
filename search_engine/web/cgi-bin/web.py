import sys, cgi
import cgi, search_engine.lib.html as html
from search_engine.lib.webgraph import WebGraph

form = cgi.FieldStorage()

#dimensions for link space
dim = form.getvalue('d')

#vector in link space
v = form.getvalue('v')

if dim == None:
    dim = [3,3,3]
else:
   dim = map(lambda x: int(x), dim)

if v != None:
   v = map(lambda x: int(x), v)

graph = WebGraph(dim, v)

def get_link(graph):
    s = './web.py'
    for i, x in enumerate(graph.dimensions()):
        if i == 0:
            s += '?'
        else:
            s += '&'
        s += 'd=' + str(x)
        
    for i, x in enumerate(graph.current()):
        s += '&v=' + str(x)
        
    return s

html.header()
print """
<table>
    <tr valign="top">
        <td><form action="index.py"><input name="s" type="submit" value="search"></form></td>
        <td><form action="statistic.py"><input name="s" type="submit" value="statistic"></form></td>
        <td><b>web model</b></td>
    </tr>
<table>"""
#show vector v and links to connected vectors
for i, x in enumerate(graph.current()):
    print '<div>'
    html.a(get_link(graph.prev(i)), '<<')
    print '%s (%s)' % (x, graph.dimensions()[i])
    html.a(get_link(graph.next(i)), '>>')
    print '</div>'
html.footer()
