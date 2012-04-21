import cgi, socket, search_engine.lib.html as html
from search_engine.index.api import IndexManager

form = cgi.FieldStorage()

html.header()

query = form.getvalue('q')
if not query:
    query = ''    

print """
<div/><a href="statistic.py">statistic</a>&nbsp;&nbsp;&nbsp;<a href="web.py">web model</a><div>
<form method="post">
<input name="q" value="%s">
<input name="s" type="submit" value="search">
</form>
""" % query

try:
    index = IndexManager.get_proxy()
    if query:
        for url in index.lookup(query):
            print '<div>'
            html.a(url, url)
            print '</div>' 
except socket.error:
    html.div("can't connect to DataStorage")

html.footer()
