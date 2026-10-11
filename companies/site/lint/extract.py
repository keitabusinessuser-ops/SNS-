import sys,re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.skip=0; s.out=[]; s.buf=''
    def handle_starttag(s,t,a):
        if t in('style','script','head'): s.skip+=1
        if t in('p','h1','h2','h3','h4','li','dt','dd','summary','span','div','article','section','time','b'): s.flush()
    def handle_endtag(s,t):
        if t in('style','script','head'): s.skip-=1
        if t in('p','h1','h2','h3','h4','li','dt','dd','summary','div','article','section'): s.flush()
    def handle_data(s,d):
        if not s.skip: s.buf+=d
    def flush(s):
        t=re.sub(r'\s+',' ',s.buf).strip()
        if t: s.out.append(t)
        s.buf=''
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read()); p.flush()
print('\n\n'.join(p.out))
