import geopandas as gpd, pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.titlesize':13,'figure.dpi':150})
d=pd.read_json('kenya_secondary_2020.json'); g=gpd.read_file('counties_simplified.geojson'); g['code']=g.code.astype(int)
g=g.merge(d,on='code')
REG={'Coast':'#0ea5a4','North Eastern':'#e11d48','Eastern':'#f59e0b','Central':'#16a34a','Rift Valley':'#7c3aed','Western':'#2563eb','Nyanza':'#db2777','Nairobi':'#475569'}
def choro(col,ramp,title,fn,fmt='{:.0f}',big=12000):
    vals=np.sort(g[col].values); br=[vals[int(i*len(vals)/7)] for i in range(1,7)]
    edges=[vals[0]]+br+[vals[-1]+1e-9]; cmap=ListedColormap(ramp); norm=BoundaryNorm(edges,7)
    fig,ax=plt.subplots(figsize=(7.2,7.6)); g.plot(column=col,cmap=cmap,norm=norm,ax=ax,edgecolor='white',linewidth=.6)
    for _,r in g.iterrows():
        if r.area_km2>=big or r[col]>=br[-1]:
            p=r.geometry.representative_point(); ax.annotate(r.county.replace('Nairobi','Nairobi'),(p.x,p.y),ha='center',fontsize=6.5,color='#1d2420',
              path_effects=[matplotlib.patheffects.withStroke(linewidth=2,foreground='white')])
    ax.set_axis_off(); ax.set_title(title,loc='left')
    sm=plt.cm.ScalarMappable(cmap=cmap,norm=norm); cb=fig.colorbar(sm,ax=ax,orientation='horizontal',fraction=.04,pad=.01,ticks=edges[:-1]); cb.ax.set_xticklabels([fmt.format(e) for e in edges[:-1]],fontsize=7)
    fig.tight_layout(); fig.savefig('figures/'+fn,bbox_inches='tight'); plt.close(fig)
import matplotlib.patheffects
choro('total_schools',['#fff3d6','#fdd8a0','#fbb26a','#f2843f','#dd5a24','#b23a14','#7c2208'],'Secondary schools per county, 2020','map_total.png')
choro('ger',['#fde9e1','#f9c7b0','#f1a07c','#e07a5a','#c25a4c','#934049','#5e2a45'],'Gross enrolment ratio (%), 2020','map_ger.png','{:.0f}%')
choro('private_share',['#fbf4dc','#f3e1a2','#e8c96a','#d6ab3c','#b88b22','#8f6a14','#62470a'],'Private schools as % of all schools','map_private.png','{:.0f}%')
# stacked bar top 15
t=d.nlargest(15,'total_schools').iloc[::-1]
fig,ax=plt.subplots(figsize=(7.5,5.2)); ax.barh(t.county,t.public_schools,color='#15803d',label='Public'); ax.barh(t.county,t.private_schools,left=t.public_schools,color='#7e22ce',label='Private')
for i,(p,v) in enumerate(zip(t.public_schools,t.private_schools)): ax.text(p+v+5,i,str(p+v),va='center',fontsize=8)
ax.set_title('The 15 counties with most secondary schools',loc='left'); ax.legend(frameon=False,loc='lower right'); ax.set_xlabel('Schools')
fig.tight_layout(); fig.savefig('figures/top15.png'); plt.close(fig)

# scatter
R={'Coast':['Mombasa','Kwale','Kilifi','Tana River','Lamu','Taita Taveta'],'North Eastern':['Garissa','Wajir','Mandera'],
 'Eastern':['Marsabit','Isiolo','Meru','Tharaka Nithi','Embu','Kitui','Machakos','Makueni'],'Central':['Nyandarua','Nyeri','Kirinyaga','Murang’a','Kiambu'],
 'Rift Valley':['Turkana','West Pokot','Samburu','Trans Nzoia','Uasin Gishu','Elgeyo Marakwet','Nandi','Baringo','Laikipia','Nakuru','Narok','Kajiado','Kericho','Bomet'],
 'Western':['Kakamega','Vihiga','Bungoma','Busia'],'Nyanza':['Siaya','Kisumu','Homa Bay','Migori','Kisii','Nyamira'],'Nairobi':['Nairobi']}
reg={c:k for k,v in R.items() for c in v}; d['region']=d.county.map(reg); assert d.region.notna().all()
fig,ax=plt.subplots(figsize=(7.5,5))
for k,c in REG.items():
    s_=d[d.region==k]; ax.scatter(s_.total_schools,s_.ger,s=s_.enrol_total/700,color=c,alpha=.7,edgecolor='white',label=k)
for _,r in d.iterrows():
    if r.ger<35 or r.ger>125 or r.total_schools>440 or r.county=='Nairobi': ax.annotate(r.county,(r.total_schools,r.ger),fontsize=7,xytext=(4,3),textcoords='offset points')
ax.axhline(76.5,color='#555',lw=.8,ls='--'); ax.text(560,78,'national GER 76.5%',fontsize=7,ha='right',color='#555')
ax.set_xlabel('Secondary schools'); ax.set_ylabel('Gross enrolment ratio (%)'); ax.set_title('More schools, higher enrolment (r = 0.52)',loc='left')
ax.legend(frameon=False,fontsize=7,ncol=4,loc='lower right',markerscale=.5); fig.tight_layout(); fig.savefig('figures/scatter.png'); plt.close(fig)
# GPI
t=d.sort_values('gpi'); cols=['#b91c1c' if v<.9 else '#b7791f' if v>1.05 else '#15803d' for v in t.gpi]
fig,ax=plt.subplots(figsize=(7.5,3.6)); ax.bar(t.county,t.gpi,color=cols); ax.axhline(1,color='#333',lw=.8)
ax.set_ylim(.4,1.25); ax.tick_params(axis='x',rotation=90,labelsize=6.5); ax.set_title('Gender parity index (girls per boy enrolled)',loc='left')
fig.tight_layout(); fig.savefig('figures/gpi.png'); plt.close(fig)
# STR & internet
t=d.sort_values('str_all',ascending=False).head(12).iloc[::-1]
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.5,3.8))
a1.barh(t.county,t.str_all,color=['#b91c1c' if v>=35 else '#1d4ed8' for v in t.str_all]); a1.axvline(28,color='#333',lw=.8,ls='--'); a1.set_title('Most students per teacher',loc='left',fontsize=11); a1.tick_params(labelsize=8)
u=d.sort_values('internet_pct').head(12).iloc[::-1]
a2.barh(u.county,u.internet_pct,color='#7e22ce'); a2.axvline(34,color='#333',lw=.8,ls='--'); a2.set_title('Fewest schools online (%)',loc='left',fontsize=11); a2.tick_params(labelsize=8)
fig.tight_layout(); fig.savefig('figures/str_internet.png'); plt.close(fig)
# region donut-ish bar
rg=d.groupby('region')[['total_schools','enrol_total']].sum().sort_values('total_schools',ascending=False)
fig,ax=plt.subplots(figsize=(7.5,3)); ax.bar(rg.index,rg.total_schools,color=[REG[k] for k in rg.index])
for i,v in enumerate(rg.total_schools): ax.text(i,v+30,f'{v:,}',ha='center',fontsize=8)
ax.set_title('Schools by former province',loc='left'); ax.tick_params(axis='x',labelsize=8); fig.tight_layout(); fig.savefig('figures/regions.png'); plt.close(fig)
