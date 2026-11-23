import re,sys
src=open(sys.argv[2]).read()
ds=re.findall(r'\sd="([^"]+)"',src)
S=900; s=0.98; x0,x1,ytop,ybot=91.9,617.3,254.1,730.1
ox=S/2-(x0+x1)/2*s; oy=130
def T(x,y): return ox+x*s, oy+(ybot-y)*s
cols=sys.argv[1].split(',')
polys=''
for d,c in zip(ds,cols):
    pts=[tuple(map(float,p.split(','))) for p in re.findall(r'[\d.]+,[\d.]+',d)]
    polys+='<polygon points="%s" fill="%s" stroke="#0E1628" stroke-width="5" stroke-linejoin="round"/>'%(' '.join('%.1f,%.1f'%T(*p) for p in pts),c)
tipx,tipy=T(353.4,254.2)
stem=f'<rect x="{tipx-10}" y="{tipy-6}" width="20" height="{S-150-tipy}" fill="{cols[0]}"/><ellipse cx="{tipx}" cy="{S-150}" rx="125" ry="22" fill="{cols[0]}"/>'
olive=''
open('a.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{S}" height="{S}"><rect width="{S}" height="{S}" fill="#0E1628"/><circle cx="450" cy="450" r="440" fill="#16233F"/>{stem}{polys}</svg>')
