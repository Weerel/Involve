import sys

def header():
    sys.stderr = sys.stdout
    print 'Content-Type: text/html'
    print
    print '<html><body>'

def footer():
    print '</body></html>'


def div(s, *args):
    text = s % args
    print '<div>%s<div>' % (text,)

def a(href, text):
    print '<a href="%s">%s</a>' % (href, text)

def br():
    print '<br/>'
