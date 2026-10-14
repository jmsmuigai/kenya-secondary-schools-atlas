import json, re
import geopandas as gpd
codes = {}
sch = {}
for i,item in enumerate(open('schools.txt').read().strip().split(';')):
    m = re.match(r"(.+?) (\d+) (\d+)$", item); sch[m[1]] = (int(m[2]), int(m[3])); codes[m[1]] = i+1
rows=[]
for rec in open('raw_extract.txt').read().strip().split(';'):
    c,pub,pri,gpi,ger,tr,te,str_,ict = rec.split('|')
    pb,pg,pt = map(int,pub.split(',')); qb,qg,qt = map(int,pri.split(','))
    G,N = map(float,ger.split(',')); tsc,bom,pt_ = map(int,te.split(','))
    s_pub,s_pri,s_all = map(int,str_.split(',')); comp,inet = ict.split(',')
    P,V = sch[c]
    rows.append(dict(county=c.replace('Nairobi City','Nairobi'), code=codes[c], public_schools=P, private_schools=V, total_schools=P+V,
        enrol_public=pt, enrol_private=qt, enrol_total=pt+qt, boys_public=pb, girls_public=pg,
        gpi=float(gpi), ger=G, ner=N, transition=float(tr), teachers_tsc=tsc, teachers_bom=bom, teachers_private=pt_,
        teachers_total=tsc+bom+pt_, str_public=s_pub, str_private=s_pri, str_all=s_all, computers=int(comp), internet_pct=float(inet)))
assert len(rows)==47
assert sum(r['total_schools'] for r in rows)==10390, sum(r['total_schools'] for r in rows)
print('enrol', sum(r['enrol_total'] for r in rows), 'teachers', sum(r['teachers_total'] for r in rows))
# geometry
g = gpd.read_file('raw/ke_counties_full.geojson'); g = g[g.COUNTY_COD>0]
g['area_km2'] = g.to_crs(32737).area/1e6
byc = {r['code']:r for r in rows}
for _,f in g.iterrows():
    r = byc[int(f.COUNTY_COD)]; r['area_km2']=round(f.area_km2,0)
for r in rows:
    r['avg_school_size']=round(r['enrol_total']/r['total_schools'])
    r['schools_per_1000km2']=round(r['total_schools']/r['area_km2']*1000,1)
    r['private_share']=round(100*r['private_schools']/r['total_schools'],1)
g = g[['COUNTY_COD','geometry']].rename(columns={'COUNTY_COD':'code'})
g['geometry']=g.geometry.simplify(0.004, preserve_topology=True)
g['name']=g.code.map(lambda k: byc[int(k)]['county'])
g.to_file('counties_simplified.geojson', driver='GeoJSON', COORDINATE_PRECISION=4)
json.dump(rows, open('kenya_secondary_2020.json','w'), indent=1)
import csv
w=csv.DictWriter(open('kenya_secondary_schools_by_county_2020.csv','w',newline=''),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(sorted(rows,key=lambda r:r['code']))
