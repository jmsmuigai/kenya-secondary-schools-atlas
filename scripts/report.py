from reportlab.lib.pagesizes import A4
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import glob, PIL.Image as PI
W,H=A4
INK=colors.HexColor('#1d2420'); MUTED=colors.HexColor('#5d6a62'); ORANGE=colors.HexColor('#c2410c'); GREEN=colors.HexColor('#15803d')
PLUM=colors.HexColor('#7e22ce'); BLUE=colors.HexColor('#1d4ed8'); GOLD=colors.HexColor('#b7791f'); PALE=colors.HexColor('#f6f7f2')
fonts=glob.glob('/usr/share/fonts/**/DejaVuSans.ttf',recursive=True)
pdfmetrics.registerFont(TTFont('Body',fonts[0])); pdfmetrics.registerFont(TTFont('Bold',fonts[0].replace('DejaVuSans.ttf','DejaVuSans-Bold.ttf')))
P=ParagraphStyle('p',fontName='Body',fontSize=9.6,leading=14.2,textColor=INK,spaceAfter=6)
H1=ParagraphStyle('h1',fontName='Bold',fontSize=15,leading=19,textColor=ORANGE,spaceBefore=10,spaceAfter=6)
CAP=ParagraphStyle('cap',fontName='Body',fontSize=8,leading=10.5,textColor=MUTED,spaceAfter=10)
BUL=ParagraphStyle('b',parent=P,leftIndent=12,bulletIndent=2,spaceAfter=3)
def img(fn,w=170*mm,cap=None):
    a=PI.open('figures/'+fn); h=w*a.height/a.width
    out=[Image('figures/'+fn,width=w,height=h)]
    if cap: out.append(Paragraph(cap,CAP))
    return KeepTogether(out)
def cover(c,doc):
    c.saveState(); c.setFillColor(INK); c.rect(0,H-95*mm,W,95*mm,fill=1,stroke=0)
    for i,col in enumerate(['#111111','#b91c1c','#15803d']): c.setFillColor(colors.HexColor(col)); c.rect(20*mm+i*14*mm,H-22*mm,14*mm,3*mm,fill=1,stroke=0)
    c.setFillColor(colors.white); c.setFont('Bold',26); c.drawString(20*mm,H-42*mm,'Kenya Secondary Schools Atlas')
    c.setFont('Body',12.5); c.setFillColor(colors.HexColor('#fdba74')); c.drawString(20*mm,H-52*mm,'Geospatial analysis of secondary schools in all 47 counties')
    c.setFillColor(colors.HexColor('#cbd5d0')); c.setFont('Body',9.5)
    c.drawString(20*mm,H-66*mm,'Prepared by James Mukoma Mburu · TovuTech Limited · October 2026')
    c.drawString(20*mm,H-72*mm,'Data: Ministry of Education, Basic Education Statistical Booklet 2020 (NEMIS)')
    # KPI tiles
    k=[('10,390','schools',ORANGE),('9,100','public',GREEN),('1,290','private',PLUM),('3.57M','students',BLUE),('76.5%','gross enrolment',GOLD)]
    x=20*mm; w=(W-40*mm-4*4*mm)/5
    for v,l,col in k:
        c.setFillColor(col); c.roundRect(x,H-91*mm,w,15*mm,2.5*mm,fill=1,stroke=0); c.setFillColor(colors.white)
        c.setFont('Bold',13); c.drawString(x+3*mm,H-83*mm,v); c.setFont('Body',7.5); c.drawString(x+3*mm,H-88*mm,l); x+=w+4*mm
    c.restoreState(); footer(c,doc)
def footer(c,doc):
    c.saveState(); c.setFont('Body',7.5); c.setFillColor(MUTED)
    c.drawString(20*mm,10*mm,'Kenya Secondary Schools Atlas · TovuTech Limited'); c.drawRightString(W-20*mm,10*mm,f'Page {doc.page}')
    c.setFillColor(ORANGE); c.rect(0,0,W,2.2*mm,fill=1,stroke=0); c.restoreState()
doc=BaseDocTemplate('Kenya_Secondary_Schools_Report.pdf',pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm,
    title='Kenya Secondary Schools Atlas – Report',author='James Mukoma Mburu')
fr=Frame(20*mm,18*mm,W-40*mm,H-36*mm,id='f'); fr1=Frame(20*mm,18*mm,W-40*mm,H-36*mm-95*mm+18*mm,id='c')
doc.addPageTemplates([PageTemplate('cover',[fr1],onPage=cover),PageTemplate('body',[fr],onPage=footer)])
from reportlab.platypus import NextPageTemplate
S=[NextPageTemplate('body')]
def h(t): S.append(Paragraph(t,H1))
def p(t): S.append(Paragraph(t,P))
def bl(items): [S.append(Paragraph(t,BUL,bulletText='•')) for t in items]
h('1. Summary')
p('This report documents a geospatial analysis of Kenya’s secondary schools and the interactive web atlas built from it. Official 2020 county statistics from the Ministry of Education were joined to county boundaries and mapped for all 47 counties. Kenya had <b>10,390 secondary schools</b> in 2020: 9,100 public (87.6%) and 1,290 private (12.4%), serving <b>3.57 million students</b>. The national gross enrolment ratio (GER) was 76.5% and 87.1% of pupils moved from primary to secondary school.')
p('The headline finding is a sharp geographic divide. The eight arid northern and north-eastern counties cover about 60% of Kenya’s land area but hold only 420 schools, or 4% of the national total. These same counties have the lowest enrolment, the most students per teacher and the widest gender gaps.')
h('2. Work done')
bl(['<b>Data collection.</b> County tables III.1 to III.13 were extracted from Annex III of the <i>Basic Education Statistical Booklet 2020</i>: schools by type, enrolment by sex, gender parity, GER and NER, transition rates, teachers, student-teacher ratios and ICT access. Totals were checked against the national rows (10,390 schools and 3,569,279 students match exactly).',
    '<b>Geospatial processing.</b> IEBC-derived county polygons were simplified, projected to UTM zone 37S to compute each county’s area, and joined to the statistics by county code. Derived indicators include private share, average school size and schools per 1,000 km².',
    '<b>Interactive atlas.</b> A single HTML page built with Leaflet and Chart.js. Clicking a county highlights it and opens a panel with its schools, students, teachers and six indicators compared with the national average, plus automatic flags for problems such as low enrolment or crowded classrooms.',
    '<b>Analysis and report.</b> Python (pandas, GeoPandas, Matplotlib) produced the maps and charts in this document, and ReportLab assembled the PDF.'])
S.append(img('webapp.png',165*mm,'Figure 1. The interactive atlas. Garissa is selected and the map is coloured by students per teacher. Nine colour layers, search, ranking charts and a sortable table are included.'))
h('3. Where the schools are')
p('Nakuru has the most secondary schools (512), followed by Kitui (455), Kakamega (453), Machakos (451) and Meru (410). The ten largest counties hold 40% of all schools. At the other end, Lamu (31), Tana River (35), Isiolo (35), Marsabit (48) and Samburu (52) each have fewer than 55. Density tells the same story: Mombasa and Nairobi have over 430 schools per 1,000 km², while Marsabit, Turkana and Tana River have fewer than one.')
S.append(img('map_total.png',100*mm,'Figure 2. Number of secondary schools per county (seven quantile classes). The densely settled western and central highlands dominate.'))
S.append(img('top15.png',150*mm,'Figure 3. Public and private schools in the 15 counties with the most schools.'))
h('4. Public and private provision')
p('Public schools dominate almost everywhere, but private provision is concentrated in cities. Private schools make up 67% of schools in Nairobi and 61% in Mombasa, followed by Garissa (48.5%) and Kajiado (44%). Six urban-influenced counties (Nairobi, Nakuru, Kiambu, Machakos, Mombasa and Kajiado) hold 689 of the 1,290 private schools. Garissa is unusual: its 33 private schools nearly match its 35 public ones, reflecting thin public supply rather than high wealth.')
h('5. Access and enrolment')
p('Counties with more schools tend to enrol a larger share of their secondary-age population (correlation r = 0.52). Eleven counties have a GER below 50%, led by Mandera (18.7%), Marsabit (19.6%), Garissa (20.5%), Wajir (23.3%) and Isiolo (27.4%). Garissa’s net enrolment rate is only 9.9%: fewer than one in ten secondary-age young people are in secondary school. Nine counties exceed 100% GER, including Murang’a (139%), Tharaka Nithi (136%) and Nyeri (128%), which signals over-age students and students crossing in from neighbouring counties.')
pair=Table([[Image('figures/map_private.png',width=82*mm,height=82*mm*PI.open('figures/map_private.png').height/PI.open('figures/map_private.png').width),
              Image('figures/map_ger.png',width=82*mm,height=82*mm*PI.open('figures/map_ger.png').height/PI.open('figures/map_ger.png').width)],
             [Paragraph('Figure 4. Private schools as a share of all schools.',CAP),Paragraph('Figure 5. Gross enrolment ratio by county.',CAP)]],colWidths=[85*mm,85*mm])
pair.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]))
S.append(pair)
S.append(img('scatter.png',150*mm,'Figure 6. Schools versus enrolment ratio. Bubble size shows students; colour shows former province.'))
p('Nairobi is an outlier: 307 schools but a GER of only 38.6%, partly because many Nairobi families send children to boarding schools in other counties.')
h('6. Gender, teachers and connectivity')
p('Nationally, gender parity has been reached (GPI 1.01). Locally it has not. Mandera (0.54), Wajir (0.58), Turkana (0.62), Garissa (0.68) and Samburu (0.74) enrol far fewer girls than boys. In 13 counties the gap runs the other way, with Vihiga (1.20) enrolling noticeably more girls.')
S.append(img('gpi.png',160*mm,'Figure 7. Gender parity index; red marks counties below 0.90 and gold marks counties above 1.05.'))
p('Classrooms are most crowded in Turkana (45 students per teacher), Wajir (44) and Mandera (39), against a national ratio of 28. Turkana also has the largest schools, averaging 575 students. Internet access is weakest in Mandera, where only 9.2% of schools are online, and in Wajir (17.9%). Nairobi (65.8%) and Mombasa (63.6%) are the most connected.')
S.append(img('str_internet.png',160*mm,'Figure 8. Counties with the highest student-teacher ratios and the lowest internet access. Dashed lines show the national value.'))
h('7. Recommendations')
bl(['Prioritise new public schools and boarding places in Mandera, Wajir, Garissa, Marsabit, Isiolo, Tana River and Turkana, where both supply and enrolment are lowest.',
    'Direct TSC teacher recruitment to counties above 35 students per teacher.',
    'Pair girls’ enrolment programmes (bursaries, sanitation, safe boarding) with the five counties below 0.75 GPI.',
    'Use the atlas as a planning tool. Garissa county can add school-level points from NEMIS and travel-time layers to find unserved wards.'])
h('8. Limitations')
p('The data are for 2020, the latest year with complete county tables. County figures reflect where schools are located, not where students live, so boarding flows distort GER in Nairobi and in some highland counties. One source row (Elgeyo Marakwet private enrolment by sex) has missing cells; its total was used. Areas come from simplified polygons and are approximate.')
h('9. Files delivered')
bl(['<b>index.html</b>: the interactive atlas; open it in any browser.',
    '<b>data/</b>: the cleaned county dataset (CSV and JSON) and county boundaries (GeoJSON).',
    '<b>figures/</b>: all maps and charts in this report.',
    '<b>PROMPT_for_Antigravity_and_Claude.md</b>: a prompt for rebuilding or extending the system.'])
doc.build(S)
