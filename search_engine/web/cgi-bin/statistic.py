import cgi, socket, search_engine.lib.html as html
from search_engine.index.api import IndexManager

def print_common_statistic(index):
    index_cnt, page_cnt, dome_cnt = index.len()
    html.div('<b>common statistic</b>')
    html.div('%i words in index', index_cnt)
    html.div('%i pages indexed', page_cnt)
    html.div('%i domains indexed', dome_cnt)
    html.br()
   
    html.div('<b>most common words</b>')
    print '<table border=0>'
    print '<tr><td>word</td><td>count</td></tr>'
    for key, n in index.most_common(15):
        print '<tr><td>%s</td><td>%i</td></tr>' % (key, n)
    print '</table>'

def print_domains(index):
    html.div('<b>domains</b>')
    for h in index.hosts():
        print '<div>'
        html.a('http://'+h, h)
        print '</div>'

def print_depth_statistic(index):
    html.div('<b>depth statistic</b>')
    print """<table>
    <tr><td>depth</td><td>pages</td></tr>"""
    for s in index.get_depth_stat():
        print '<tr><td>%i</td><td>%i</td></tr>' % s
    print '</table>'

html.header()
print """
<div/>
    <a href="index.py">search</a>&nbsp;&nbsp;&nbsp;
    <a href="statistic.py"><b>statistic</b></a>&nbsp;&nbsp;&nbsp;
    <a href="web.py">web model</a>
<div><br/>
"""
try:
    index = IndexManager.get_proxy()
    print '<table border=0>'
    print '<tr valign="top"><td>'
    print_common_statistic(index)
    print '</td><td>'
    print_domains(index)
    print '</td><td>'
    print_depth_statistic(index)
    print '</td><tr/>'
    print '</table>'
    
except socket.error:
    html.div("can't connect to DataStorage")

html.footer()
