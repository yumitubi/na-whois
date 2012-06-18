# -*- coding: utf-8 -*-

import re
import subprocess
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object(__name__)

def get_whois(domain_or_ip):
    """get whois information of domain or ip"""
    return  subprocess.Popen(["whois", domain_or_ip], stdout=subprocess.PIPE).communicate()[0]

def testing_input(test_input):
    test_output = ''
    re_expression = re.compile('[0-9a-zA-Z\.\-]')
    re_expression2 = re.compile(u'[А-Яа-я]')    
    for i in test_input:
        if re_expression.findall(i):
            test_output = test_output + i
        if re_expression2.findall(i):
            test_output = test_output + i
    return test_output
        
@app.route('/', methods=['POST', 'GET'])
def index():
    """view for user"""
    if request.method == 'POST' and request.form['domain']:
        search_domain = testing_input(request.form['domain'])
        info_whois = get_whois(search_domain).decode("utf-8")
        info_whois_template = info_whois.split("\n")
        return render_template('main.html', info_whois=info_whois_template, input_domain=search_domain)
    else:
        return render_template('main.html', info_whois="")

if __name__ == "__main__":
    app.run(debug=True)


        
