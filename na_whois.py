# -*- coding: utf-8 -*-
import re
import subprocess
from flask import Flask, request, render_template
from werkzeug.contrib.cache import MemcachedCache

app = Flask(__name__)
app.config.from_object('settings')
MEMCACHE_IP = app.config['MEMCACHE_IP']
cache = MemcachedCache([MEMCACHE_IP])


def get_whois(domain_or_ip):
    """get whois information of domain or ip"""
    info = subprocess.Popen(["whois", "-H", domain_or_ip], stdout=subprocess.PIPE).communicate()[0]
    return info.decode("utf8", "replace")

def input_testing(test_input):
    """test and split input user"""
    test_input_obr = test_input.strip()
    if re.compile(u'^http:\/\/').match(test_input_obr):
        test_input_obr = test_input_obr.replace('http://', '')
    if re.compile(u'^www\.').match(test_input_obr):
        test_input_obr = test_input_obr.replace('www.', '')
    if re.compile(u'^[а-яёА-ЯЁa-zA-Z0-9\-\.]+$').match(test_input_obr):
        return test_input_obr
    else:
        return False


@app.route('/', methods=['GET'])
def index():
    u"""view for user

    GET-params:
      what: search whois-info for this domain or ip
    """
    domain = request.args.get('what')
    if domain:
        search_domain = input_testing(domain)
        if search_domain:
            info_whois = cache.get(u'%s_info_whois' % search_domain)
            if not info_whois:
                info_whois = get_whois(search_domain)
                cache.set(u'%s_info_whois' % search_domain, info_whois, timeout=60 * 15)
            info_whois_template = info_whois.split("\n")
            return render_template('main.html', info_whois=info_whois_template,
                                   input_domain=search_domain, novalid=False)
        else:
            return render_template(
                'main.html', input_domain=domain,
                novalid=u"Вы ввели неправильное имя домена"
                    u" или неверный IP-адрес, пожалуйста, попробуйте снова")
    else:
        return render_template('main.html', input_domain="", info_whois=None)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5010)
