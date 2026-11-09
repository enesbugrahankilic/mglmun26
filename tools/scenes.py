"""Generates the committee illustrations in public/img/*.svg (python3 tools/scenes.py)."""
import random, math, os
OUT=os.path.join(os.path.dirname(__file__),'..','public','img')
W,H=1600,900
def svg(body,defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice"><defs>{defs}<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter></defs>{body}<rect width="{W}" height="{H}" filter="url(#grain)"/></svg>'
def lg(id,stops,x2=0,y2=1):
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="{x2}" y2="{y2}">'+''.join(f'<stop offset="{o}" stop-color="{c}"{f" stop-opacity=\"{a}\"" if a is not None else ""}/>' for o,c,a in stops)+'</linearGradient>'
def rg(id,cx,cy,r,stops):
    return f'<radialGradient id="{id}" cx="{cx}" cy="{cy}" r="{r}" gradientUnits="userSpaceOnUse">'+''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o,c,a in stops)+'</radialGradient>'

def person(x,base,s,col,arm=None,flag=None,rng=None):
    """simple silhouette: head + shoulders/torso; optional raised arm or flag."""
    h=s*1.0
    p=[f'<circle cx="{x:.1f}" cy="{base-h*1.55:.1f}" r="{h*.22:.1f}" fill="{col}"/>',
       f'<path d="M{x-h*.42:.1f} {base:.1f} L{x-h*.40:.1f} {base-h*1.0:.1f} Q{x-h*.38:.1f} {base-h*1.28:.1f} {x:.1f} {base-h*1.30:.1f} Q{x+h*.38:.1f} {base-h*1.28:.1f} {x+h*.40:.1f} {base-h*1.0:.1f} L{x+h*.42:.1f} {base:.1f}Z" fill="{col}"/>']
    if arm:
        d=arm
        p.append(f'<path d="M{x+d*h*.30:.1f} {base-h*1.15:.1f} L{x+d*h*.52:.1f} {base-h*1.95:.1f}" stroke="{col}" stroke-width="{h*.15:.1f}" stroke-linecap="round"/>')
        p.append(f'<circle cx="{x+d*h*.54:.1f}" cy="{base-h*2.0:.1f}" r="{h*.11:.1f}" fill="{col}"/>')
    if flag:
        fc,fw=flag
        px=x+h*.35; top=base-h*2.9
        p.append(f'<line x1="{px:.1f}" y1="{base-h*1.0:.1f}" x2="{px:.1f}" y2="{top:.1f}" stroke="{col}" stroke-width="{h*.06:.1f}"/>')
        w=h*fw
        p.append(f'<path d="M{px:.1f} {top:.1f} Q{px+w*.5:.1f} {top-h*.18:.1f} {px+w:.1f} {top+h*.05:.1f} L{px+w*.95:.1f} {top+h*.62:.1f} Q{px+w*.45:.1f} {top+h*.45:.1f} {px:.1f} {top+h*.6:.1f}Z" fill="{fc}"/>')
    return ''.join(p)

def crowd(rng,y,n,s,col,x0=-40,x1=W+40,arms=.15,flags=0,flagcol='#b5261c',fw=1.4):
    out=[]
    for i in range(n):
        x=x0+(x1-x0)*(i+rng.random()*.6)/n
        ss=s*(.85+rng.random()*.3)
        arm=rng.choice([-1,1]) if rng.random()<arms else None
        fl=(flagcol,fw*(.8+rng.random()*.5)) if rng.random()<flags else None
        out.append(person(x,y+rng.random()*s*.25,ss,col,arm,fl,rng))
    return ''.join(out)

# ───────── WTO: container ship at dusk, port cranes, trade routes
def wto():
    r=random.Random(7)
    defs=lg('sky',[(0,'#0d1628',None),(.55,'#23395e',None),(.78,'#8a6a5a',None),(1,'#d9a676',None)])+lg('sea',[(0,'#2b3c5a',None),(1,'#0b1220',None)])+rg('sun',1180,560,420,[(0,'#f6d39a',.9),(.25,'#e8a96c',.35),(1,'#e8a96c',0)])
    b=[f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',f'<rect width="{W}" height="{H}" fill="url(#sun)"/>','<circle cx="1180" cy="600" r="70" fill="#f7dcae" opacity=".85"/>']
    # stars
    b+= [f'<circle cx="{r.random()*W:.0f}" cy="{r.random()*330:.0f}" r="{r.random()*1.4+.4:.1f}" fill="#e8e3e0" opacity="{r.random()*.6+.2:.2f}"/>' for _ in range(90)]
    # trade routes
    pts=[(120,300),(470,170),(820,250),(1250,140),(1500,260)]
    b.append('<g fill="none" stroke="#e8e3e0" stroke-width="2" stroke-dasharray="4 9" opacity=".55">')
    for (a,c) in [(0,2),(2,3),(1,3),(3,4),(0,1)]:
        (x1,y1),(x2,y2)=pts[a],pts[c]; b.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2} {min(y1,y2)-110} {x2} {y2}"/>')
    b.append('</g>')
    b+= [f'<circle cx="{x}" cy="{y}" r="6" fill="#f2e6d8"/><circle cx="{x}" cy="{y}" r="16" fill="none" stroke="#f2e6d8" opacity=".35"/>' for x,y in pts]
    # far coast
    b.append('<path d="M0 640 L120 625 L260 632 L420 615 L600 628 L760 618 L980 630 L1600 622 L1600 660 L0 660Z" fill="#1d2a44" opacity=".8"/>')
    # sea
    b.append(f'<rect y="650" width="{W}" height="250" fill="url(#sea)"/>')
    b+= [f'<rect x="{1180-w/2+r.uniform(-40,40):.0f}" y="{y}" width="{w:.0f}" height="3" fill="#f3c98f" opacity="{.5-(y-650)/600:.2f}"/>' for y,w in [(660+i*11,r.uniform(40,220)) for i in range(20)]]
    # cranes (right)
    def crane(x,h,col):
        return (f'<g fill="none" stroke="{col}" stroke-width="7"><path d="M{x} 660 L{x} {660-h} M{x+70} 660 L{x+70} {660-h} M{x} {660-h*.55} L{x+70} {660-h*.55} M{x} 660 L{x+70} {660-h*.55} M{x+70} 660 L{x} {660-h*.55}"/></g>'
                f'<rect x="{x-150}" y="{660-h-18}" width="390" height="18" fill="{col}"/><rect x="{x-10}" y="{660-h-60}" width="90" height="42" fill="{col}"/>'
                f'<path d="M{x+35} {660-h-60} L{x+35} {660-h-120}" stroke="{col}" stroke-width="5"/><line x1="{x-140}" y1="{660-h}" x2="{x-140}" y2="{660-h*.45}" stroke="{col}" stroke-width="2"/>')
    b.append(crane(1340,300,'#141e33')+crane(1500,250,'#18233b')+crane(40,230,'#18233b'))
    # ship
    hull='M180 700 L1220 700 L1180 790 L250 790 Q205 760 180 700Z'
    cols=['#9c3b2b','#2f5c6e','#c9a46a','#6b2230','#3f4f6b','#b8b0a2','#7a4a2a','#24485a']
    cont=[]
    for row in range(5):
        for i in range(36):
            x=300+i*24
            if x>1060: break
            if row>=4 and (i%5==0): continue
            cont.append(f'<rect x="{x}" y="{700-(row+1)*26}" width="22" height="24" fill="{r.choice(cols)}"/>')
    b.append('<g opacity=".95">'+''.join(cont)+'</g>')
    b.append(f'<path d="{hull}" fill="#0c1424"/><rect x="180" y="700" width="1040" height="8" fill="#7e1f1d"/>')
    b.append('<rect x="1090" y="570" width="90" height="130" fill="#101a2c"/><rect x="1080" y="560" width="110" height="18" fill="#101a2c"/>'+''.join(f'<rect x="{1098+i*20}" y="{585+j*24}" width="12" height="9" fill="#f3d39b" opacity=".8"/>' for i in range(4) for j in range(3)))
    b.append('<rect x="1150" y="520" width="14" height="45" fill="#101a2c"/>')
    # reflection
    b.append('<path d="M250 795 L1180 795 L1150 840 L280 840Z" fill="#0b1220" opacity=".6"/>')
    # foreground quay
    b.append(f'<path d="M0 850 L{W} 830 L{W} {H} L0 {H}Z" fill="#070c17"/>')
    b+= [f'<rect x="{1250+i*70}" y="{790-k*30}" width="66" height="28" fill="{r.choice(cols)}" opacity=".9"/>' for i in range(5) for k in range(r.randint(1,3))]
    return svg(''.join(b),defs)

# ───────── UN Women: crowd at sunrise, raised hands, placards
def unw():
    r=random.Random(3)
    defs=lg('sky',[(0,'#2a0a1d',None),(.5,'#6d1f4b',None),(.85,'#c25b6f',None),(1,'#f0a586',None)])+rg('sun',1060,620,700,[(0,'#ffd7b0',.95),(.18,'#f7a98d',.5),(1,'#f7a98d',0)])
    b=[f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',f'<rect width="{W}" height="{H}" fill="url(#sun)"/>']
    b.append('<g fill="none" stroke="#ffe3d3" opacity=".22">'+''.join(f'<circle cx="1060" cy="620" r="{140+i*55}" stroke-width="{2 if i%3 else 4}"/>' for i in range(18))+'</g>')
    b.append('<circle cx="1060" cy="620" r="150" fill="#ffe0bf" opacity=".9"/>')
    # birds/doves
    for _ in range(9):
        x,y,s=r.uniform(200,1500),r.uniform(90,330),r.uniform(10,22)
        b.append(f'<path d="M{x-s} {y} Q{x-s/2} {y-s*.6} {x} {y} Q{x+s/2} {y-s*.6} {x+s} {y}" fill="none" stroke="#ffe8dc" stroke-width="2.5" opacity=".7"/>')
    # city skyline far
    sk=[]; x=0
    while x<W:
        w=r.uniform(40,110); h=r.uniform(60,190)
        sk.append(f'<rect x="{x:.0f}" y="{680-h:.0f}" width="{w:.0f}" height="{h+20:.0f}"/>'); x+=w+r.uniform(0,10)
    b.append('<g fill="#7a2a4f" opacity=".55">'+''.join(sk)+'</g>')
    # crowds
    b.append(crowd(r,760,34,62,'#5a173c',arms=.25))
    b.append(crowd(r,830,26,82,'#3d0e29',arms=.35))
    # placards in front row
    pl=[]
    for x,t in [(260,'EQUAL'),(720,'RIGHTS'),(1240,'NOW')]:
        pl.append(f'<line x1="{x}" y1="900" x2="{x}" y2="700" stroke="#2a0a1d" stroke-width="8"/><rect x="{x-115}" y="620" width="230" height="100" rx="4" fill="#f6e3d6"/><text x="{x}" y="688" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="44" fill="#5a173c" letter-spacing="3">{t}</text>')
    b.append(''.join(pl))
    b.append(f'<rect y="860" width="{W}" height="40" fill="#3d0e29"/>')
    b.append(crowd(r,940,16,120,'#24071a',arms=.45))
    return svg(''.join(b),defs)

# ───────── Petrograd Soviet: Tauride Palace, rays, crowd with red banners
def ps():
    r=random.Random(17)
    defs=lg('sky',[(0,'#3d0807',None),(.6,'#8e1f15',None),(1,'#c9542c',None)])+rg('sun',1080,700,800,[(0,'#f6c77e',.7),(1,'#f6c77e',0)])
    b=[f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',f'<rect width="{W}" height="{H}" fill="url(#sun)"/>']
    cx,cy,R=1080,720,2200
    b.append('<g fill="#f0c27a" opacity=".16">')
    for i in range(22):
        a0=math.pi+i*math.pi/22; a1=a0+math.pi/48
        b.append(f'<path d="M{cx} {cy} L{cx+math.cos(a0)*R:.0f} {cy+math.sin(a0)*R:.0f} L{cx+math.cos(a1)*R:.0f} {cy+math.sin(a1)*R:.0f}Z"/>')
    b.append('</g>')
    # palace
    pc='#2a0605'; px=540
    pal=[f'<rect x="{px-60}" y="470" width="1160" height="220" fill="{pc}"/>',  # wings
         f'<rect x="{px+300}" y="400" width="440" height="290" fill="{pc}"/>',
         f'<path d="M{px+280} 405 L{px+520} 300 L{px+760} 405Z" fill="{pc}"/>',
         f'<rect x="{px+455}" y="230" width="130" height="80" fill="{pc}"/>',
         f'<path d="M{px+440} 235 Q{px+520} 120 {px+600} 235Z" fill="{pc}"/>',
         f'<line x1="{px+520}" y1="150" x2="{px+520}" y2="70" stroke="{pc}" stroke-width="5"/>',
         f'<path d="M{px+522} 72 Q{px+580} 60 {px+640} 80 L{px+632} 118 Q{px+575} 100 {px+522} 110Z" fill="#c41e14"/>']
    # columns highlights
    pal+= [f'<rect x="{px+322+i*66}" y="420" width="22" height="250" fill="#5a1410"/>' for i in range(7)]
    pal+= [f'<rect x="{px-40+i*58}" y="520" width="26" height="40" fill="#e8a65e" opacity=".55"/>' for i in range(6)]
    pal+= [f'<rect x="{px+780+i*58}" y="520" width="26" height="40" fill="#e8a65e" opacity=".55"/>' for i in range(6)]
    b.append(''.join(pal))
    b.append(f'<rect y="680" width="{W}" height="220" fill="#250504"/>')
    # banners crowd
    b.append(crowd(r,770,40,56,'#3a0907',arms=.2,flags=.18,flagcol='#c41e14',fw=1.6))
    b.append(crowd(r,850,28,78,'#280504',arms=.3,flags=.2,flagcol='#d8281a',fw=1.5))
    b.append(crowd(r,950,15,118,'#160202',arms=.35,flags=.15,flagcol='#e2301f',fw=1.3))
    # diagonal banner
    b.append('<path d="M-20 140 L620 40 L640 110 L0 215Z" fill="#c41e14" opacity=".9"/><text transform="translate(40 168) rotate(-8.9)" font-family="Georgia,serif" font-weight="700" font-size="52" fill="#f6e3c4" letter-spacing="10">PETROGRAD · 1917</text>')
    return svg(''.join(b),defs)

# ───────── Assembly hall: tiered semicircle, podium, emblem wall
def hall():
    r=random.Random(5)
    defs=lg('wall',[(0,'#2a0a0c',None),(1,'#5a1416',None)])+rg('spot',800,300,700,[(0,'#f3d9b0',.5),(1,'#f3d9b0',0)])+lg('floor',[(0,'#3a0d10',None),(1,'#120304',None)])
    b=[f'<rect width="{W}" height="{H}" fill="url(#wall)"/>',f'<rect width="{W}" height="{H}" fill="url(#spot)"/>']
    # back wall panels
    b+= [f'<rect x="{i*100}" y="0" width="96" height="420" fill="#ffffff" opacity="{.02+.02*(i%2)}"/>' for i in range(16)]
    # emblem
    b.append('<g transform="translate(800 190)" fill="none" stroke="#d8b878" opacity=".85"><circle r="95" stroke-width="5"/><circle r="70" stroke-width="2"/><path d="M-70 0 H70 M0 -70 V70" stroke-width="2"/><ellipse rx="35" ry="70" stroke-width="2"/><ellipse rx="70" ry="30" stroke-width="2"/></g>')
    b.append('<g fill="#d8b878" opacity=".8">'+''.join(f'<ellipse cx="{800+math.cos(a)*120:.0f}" cy="{190+math.sin(a)*120:.0f}" rx="9" ry="20" transform="rotate({math.degrees(a)+90:.0f} {800+math.cos(a)*120:.0f} {190+math.sin(a)*120:.0f})"/>' for a in [math.pi*(0.08+0.065*i) for i in range(6)]+[math.pi*(0.92-0.065*i) for i in range(6)])+'</g>')
    # flags along the wall
    fc=['#1f3a68','#c9a46a','#7a1e2c','#2f6a5a','#e8e3e0','#b5261c','#3a3f7a','#d48a2b']
    for i in range(14):
        x=90+i*100+(60 if i>=7 else 0)
        if 560<x<1040: continue
        c=r.choice(fc)
        b.append(f'<line x1="{x}" y1="420" x2="{x}" y2="190" stroke="#d8b878" stroke-width="3"/><path d="M{x} 195 L{x+40} 200 L{x+38} 330 Q{x+20} 350 {x} 335Z" fill="{c}"/>')
    # podium
    b.append('<rect x="560" y="360" width="480" height="90" fill="#1a0507"/><rect x="560" y="352" width="480" height="10" fill="#d8b878" opacity=".7"/><rect x="740" y="300" width="120" height="60" fill="#1a0507"/><rect x="796" y="268" width="4" height="34" fill="#d8b878"/>')
    b.append(f'<rect y="440" width="{W}" height="460" fill="url(#floor)"/>')
    # tiers of desks with seated delegates (back to front)
    for t in range(6):
        y=480+t*70; s=22+t*7; rad=330+t*150; th=s*.9
        cur=lambda u:y+80-(1-(2*u-1)**2)*80
        n=12+t*4
        for i in range(n):
            u=(i+.5)/n; x=800+(u-.5)*rad*3.2
            b.append(person(x,cur(u)+th*.9,s,'#120304' if t>2 else '#22070a'))
        L,R_=800-rad*1.6,800+rad*1.6
        b.append(f'<path d="M{L:.0f} {y+80:.0f} Q800 {y-80:.0f} {R_:.0f} {y+80:.0f} L{R_:.0f} {y+80+th:.0f} Q800 {y-80+th:.0f} {L:.0f} {y+80+th:.0f}Z" fill="#3a0e10"/>')
        b.append(f'<path d="M{L:.0f} {y+80:.0f} Q800 {y-80:.0f} {R_:.0f} {y+80:.0f}" fill="none" stroke="#d8b878" stroke-width="{1.5+t*.5:.1f}" opacity=".55"/>')
    return svg(''.join(b),defs)

for n,f in [('wto',wto),('unw',unw),('ps',ps),('hall',hall)]:
    open(os.path.join(OUT,n+'.svg'),'w').write(f())
print('ok')
