#!/usr/bin/python
# -*- coding: utf8 -*-

import os,sys,re
import cgi
from tempfile import mktemp

# set HOME environment variable to a directory the httpd server can write to
os.environ[ 'HOME' ] = '/tmp/'

import matplotlib
# chose a non-GUI backend
matplotlib.use( 'Agg' )

from scipy import arange, sin, pi
from pylab import plot, savefig, figure, xlabel, ylabel, legend, title, axis

print "Content-type: text/html; Charset=utf-8\n"
print "<h1>Výkon střídavého proudu</h1>"

validate = re.compile(r"^[\d\.]+$")
form = cgi.FieldStorage()
if "fi" in form:
    if (validate.match(form['fi'].value) == None):
        print "zadej sem číslo"
        form['fi'].value = "33"
    try:
        angle = float(form['fi'].value)
    except:
        angle = 30
else:
    angle = 30

print """
<form  method="get">
<p>
fázový posun napětí a proudu:
    <input type="text" name="fi" value="{0}" />
</p>
</form>
""".format(angle)
t = arange(-0.1,1.1,0.001)
u = sin(2*pi*2*t)
i = sin(2*pi*2*t+(angle*pi/180))

fig = figure()
graf = fig.add_subplot(111)
graf.grid(True)
title("Okamzite hodnoty napeti, proudu a vykonu")
xlabel("t[s]")
ylabel("u[V], i[A], p[W]")
plot(t, u,label="u")
plot(t, i,"--", label="i")
plot(t, u*i, label="p", linewidth=2)
axis([-0.1,1.1,-1.2,1.2])

legend()

temp = mktemp(suffix=".png",prefix="p", dir="../tmp");
savefig(temp)
print """
<p>
   <img src="{0}"></img>
</p>
<p>
   <a href="./vykony-cgi.py">zdroj této stránky</a>
</p>

""".format(temp)

# vim:nospell:
