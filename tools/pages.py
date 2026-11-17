import subprocess, re, json, os
import os
B=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'build')
n=int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo',B+'/body.pdf'],capture_output=True,text=True).stdout).group(1))
txt=subprocess.run(['pdftotext','-layout',B+'/body.pdf','-'],capture_output=True,text=True).stdout
pages={}
for i,pt in enumerate(txt.split('\f'),1):
    for m in re.finditer(r'@@\s*([A-Za-z0-9\-]+?)\s*@@', pt.replace('\n','')):
        pages.setdefault(m.group(1).replace(' ',''), i)
json.dump(pages,open(B+'/pages.json','w'))
print(n,'pages;',len(pages),'markers')
