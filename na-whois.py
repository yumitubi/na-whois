# all the imports
import os
import sys
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

def clear_input():
    """test input user on valid"""
    pass
    
def get_whois(domain_or_ip):
    """get whois information of domain or ip"""
    return os.system('whois %s' % domain_or_ip)

@app.route('/')
def index():
    """view for user"""
    test_whois = get_whois('le087.ru')
    return render_template('main.html', test_whois)

if __name__ == "__main__":
    app.run(debug=True)


        