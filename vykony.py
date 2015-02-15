#!/usr/bin/python
# -*- coding: utf8 -*-
# Soubor:  vykony.py
# Datum:   15.02.2015 13:00
# Autor:   Marek Nožka, nozka <@t> spseol <d.t> cz
# Licence: GNU/GPL
# Úloha:   výkon střádavého proudu v závislosti na fázovém posuvu
############################################################################
from __future__ import division, print_function, unicode_literals
from flask import (Flask, render_template, request,
                   redirect, url_for, send_from_directory)
import os
# os.environ['HOME'] = '/tmp/'
import StringIO
import base64
import matplotlib
matplotlib.use('Agg')  # chose a non-GUI backend
from scipy import arange, sin, pi
from pylab import plot, savefig, figure, xlabel, ylabel, legend, title, axis
# set HOME environment variable to a directory the httpd server can write to
PWD = os.path.dirname(__file__)
############################################################################

app = Flask(__name__)
############################################################################


def image_gen(angle):
    """Funkce jako parametr bere fázový posun
    vrací cestu k souboru, ve kterém je uložen obrázek"""
    t = arange(-0.1, 1.1, 0.001)
    u = sin(2 * pi * 2 * t)
    i = sin(2*pi*2*t+(angle*pi/180))

    fig = figure()
    graf = fig.add_subplot(111)
    graf.grid(True)
    title("Okamžité hodnoty napětí, proudu a výkonu")
    xlabel("t[s]")
    ylabel("u[V], i[A], p[W]")
    plot(t, u, label="u")
    plot(t, i, "--", label="i")
    plot(t, u * i, label="p", linewidth=2)
    axis([-0.1, 1.1, -1.2, 1.2])
    legend()
    output = StringIO.StringIO()
    savefig(output)
    r = base64.b64encode(output.getvalue())
    output.close()
    print(output)
    return r


@app.route('/tmp/<path:filename>')
def static_data(filename):
    return send_from_directory('tmp', filename)


@app.route('/')
def index():
    if "angle" in request.args:
        try:
            angle = int(request.args['angle'])
        except:
            return redirect(url_for('index') + '30/')
        angle %= 360
        if angle < 0:
            angle = 360 + angle
        return redirect(url_for('index') + str(angle))
    else:
        return redirect(url_for('index') + '30/')


@app.route('/<int:angle>/')
def site(angle):
    angle %= 360
    return render_template('base.html', angle=angle, img=image_gen(angle))


@app.route('/-<int:angle>/')
def underzero(angle):
    return redirect(url_for('index') + str(360-angle))

############################################################################

if __name__ == '__main__':
    app.run(host='::1', port=8080, debug=True)
