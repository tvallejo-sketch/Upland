import re, subprocess, sys, pandas as pd
D = sys.argv[1]
def parse(pdf, ncand):
    txt = subprocess.run(["pdftotext","-layout",pdf,"-"],capture_output=True,text=True).stdout
    rows=[]
    for line in txt.splitlines():
        m = re.match(r"^\s*([A-Z][A-Za-z&. ]+?)\s{2,}([\d,\s]+)$", line)
        if not m or "TOTAL" in m.group(1).upper(): continue
        nums=[int(x.replace(",","")) for x in m.group(2).split()]
        if len(nums)!=ncand: continue
        rows.append((m.group(1).strip(), nums))
    return rows
def key(n):
    n=n.lower().replace("greenbrook","green brook").replace("&","and")
    return re.sub(r"\s+(twp\.?|boro|township|borough)$","",n).strip()
el={}
for yr,f,n in [(2020,"2020-official-general-results-president-somerset.pdf",8),
               (2024,"2024-official-general-results-president-somerset.pdf",9),
               (2025,"2025-official-general-results-governor-somerset.pdf",4)]:
    for name,nums in parse(f"{D}/{f}",n):
        el.setdefault(key(name),{}).update({f"D{yr}":nums[0],f"R{yr}":nums[1],f"O{yr}":sum(nums[2:])})
el=pd.DataFrame(el).T
c=pd.read_csv(f"{D}/som_mcd.csv",header=None,names="geoname lntitle geoid lnnumber tot_est tot_moe adu_est adu_moe cit_est cit_moe cvap_est cvap_moe".split())
c["muni"]=c.geoname.str.split(",").str[0].map(key)
p=c.pivot_table(index="muni",columns="lnnumber",values="cvap_est",aggfunc="sum")
cv=pd.DataFrame({"cvap":p[1],"asian":p[4]+p[9],"black":p[5]+p[10],"hisp":p[13],"white":p[7]})
cv["other"]=cv.cvap-cv[["asian","black","hisp","white"]].sum(axis=1)
df=cv.join(el,how="inner")
assert len(df)==21, (len(df), set(cv.index)^set(el.index))
df.to_csv(f"{D}/somerset_muni.csv")
pd.set_option("display.width",200)
df["asian_pct"]=(100*df.asian/df.cvap).round(1)
df["to24"]=(100*(df.D2024+df.R2024+df.O2024)/df.cvap).round(0)
df["Dm20"]=(100*(df.D2020-df.R2020)/(df.D2020+df.R2020)).round(1)
df["Dm24"]=(100*(df.D2024-df.R2024)/(df.D2024+df.R2024)).round(1)
df["Dm25"]=(100*(df.D2025-df.R2025)/(df.D2025+df.R2025)).round(1)
print(df[["cvap","asian_pct","to24","Dm20","Dm24","Dm25"]].sort_values("asian_pct",ascending=False))
print(df[["D2024","R2024","D2025","R2025"]].sum())
