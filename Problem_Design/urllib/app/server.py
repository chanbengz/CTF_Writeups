import urllib.request
from urllib.parse import urlparse
from flask import Flask, render_template, request

app = Flask(__name__)

fake_flag = "flag{this_is_a_fake_flag}"

def safe_url_opener(input_link):
    block_schemes = ["gopher", "expect", "php", "file", "dict", "ftp", "glob", "data"]
    block_host = ["localhost", "127.0.0.1", "0.0.0.0", '0', "2130706433" ,"7F000001"]

    input_scheme = urlparse(input_link).scheme
    input_hostname = urlparse(input_link).hostname

    input_link = input_link.replace('@', '')

    if input_scheme in block_schemes:
        return "<b>Forbidden scheme! No hacker</b>"

    if input_hostname in block_host:
        return "<b>Forbidden host! No hacker</b>"

    try:
        target = urllib.request.urlopen(input_link)
        content = target.read()
        if type(content) == bytes:
            return content.decode()
        return content
    except Exception as e:
        return "Error:" + str(e)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return "What's wrong with you?"
    url = request.args.get("url")
    content = ''
    if url != None:
        content = safe_url_opener(url).replace('\n', '')
    return render_template('index.html', content=content)

@app.route('/flag', methods=['GET', 'POST'])
def flag():
    return "Well Done! Here's your flag: " + fake_flag

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)