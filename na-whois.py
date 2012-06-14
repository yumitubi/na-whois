# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

def get_whois(domain_or_ip):
    """get whois information of domain or ip"""
    return os.system('whois %s' % domain_or_ip)

@app.route('/', methods=['POST', 'GET'])
def index():
    """view for user"""
    if request.method == 'POST':
        if request.form['username']:
            test = 'Информация Whois домена или IP-адреса.'.decode('utf-8')
            test2 = get_whois(request.form['username'])
            return render_template('main.html', test=test, test2=test2)
    else:
        test = 'Информация Whois домена или IP-адреса.'.decode('utf-8')
        test2 = 'Пустота'.decode('utf-8')
        return render_template('main.html', test=test, test2=test2)

if __name__ == "__main__":
    app.run(debug=True)


        
