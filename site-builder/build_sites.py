from __future__ import annotations
from pathlib import Path
import json, html, re, urllib.parse

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://prithiraj.github.io/uae_demo'


PHOTO_MAP = {'XF68': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/2dc42137-178d-4b49-8385-f0fad356e66c-h.jpeg', 'source': 'https://www.hidubai.com/businesses/zaina-secrets-beauty-salon-beauty-wellness-health-beauty-salons-discovery-gardens-jebel-ali-1-dubai-2', 'alt': 'Zaina Secrets Beauty Salon business listing photo', 'scope': 'exact'}, '0RGC': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/c680af89-054d-475d-a507-d84b58c83849-h.jpeg', 'source': 'https://www.hidubai.com/businesses/azmat-nazir-tools-llc', 'alt': 'Azmat Nazir Tools LLC business listing photo', 'scope': 'exact'}, '8HAK': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/de42808a-747f-4362-bb13-ac6f70e54177-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Abdulla Kutait Grocery business listing photo', 'scope': 'exact'}, '8YTT': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/d1577ac8-695b-43d4-b937-ee5515b611b1-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Al Khateem Gents Tailoring business listing photo', 'scope': 'exact'}, 'AF86': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/bb54e6d8-675e-4201-809a-6b502f25579b-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Alsharq gents saloon business listing photo', 'scope': 'exact'}, 'DQED': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/b326ca53-7fee-4d5d-a5bc-e398f98906c8-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Noor Al Qamar Tailoring and Embroidery business listing photo', 'scope': 'exact'}, 'DVHV': {'url': 'https://b.zmtcdn.com/data/pictures/7/20722197/7c42275306238a16e53db18e55aca87d.jpg?output-format=webp', 'source': 'https://www.zomato.com/', 'alt': 'City Corner Cafeteria Karama listing photo', 'scope': 'exact'}, '6S9L': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/af8ae498-2932-4b1c-97e2-e244a18b7de6-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'AKS Beauty Salon business listing photo', 'scope': 'exact'}, '7Y5Y': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/19e4ea50-6f9d-4264-8da6-bc3ad41a4cc3-h.jpeg', 'source': 'https://www.hidubai.com/businesses/himalaya-laundry-home-laundry-al-karama-dubai-2', 'alt': 'Himalaya Laundry business listing photo', 'scope': 'exact'}, '6OGS': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/aa0ae2cf-bbb3-457d-bb1f-6d972244c7ad-h.jpeg', 'source': 'https://www.hidubai.com/businesses/hassan-ali-ahmed-grocery-shopping-supermarkets-hypermarkets-grocery-stores-al-qusais-3-dubai', 'alt': 'Hassan Ali Ahmed Grocery storefront photo associated with the researched grocery', 'scope': 'exact'}, 'AP30': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/d81c6fb0-8587-4e6a-a4eb-beb208d48c26-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Madares Boutique business listing photo', 'scope': 'exact'}, 'CSII': {'url': 'https://b.zmtcdn.com/data/pictures/6/21436606/9f38845b9662ebf0d7d164ca641fb790.jpg', 'source': 'https://www.zomato.com/', 'alt': 'Al Manama Cafeteria listing photo', 'scope': 'exact'}, 'M68R': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/7370baa0-d871-4a77-b917-3d5f80cc9234-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Marmar Ladies Salon business listing photo', 'scope': 'exact'}, 'TWB8': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/49cd14c9-baad-43a8-a2c1-769aaa215bb0-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Al Bawasel Garage business listing photo', 'scope': 'exact'}, '1131': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/644e2a11-30a8-4107-896d-8036d90fbd9b-h.jpeg', 'source': 'https://www.hidubai.com/businesses/al-qashima-supermarket-shopping-supermarkets-hypermarkets-grocery-stores-hor-al-anz-east-dubai-2', 'alt': 'Al Qashima Supermarket storefront photo', 'scope': 'exact'}, '25IT': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/7b034b24-eedd-4601-a5f8-65907537c53e-h.jpeg', 'source': 'https://www.hidubai.com/businesses/embarkoh-grocery-shopping-supermarkets-hypermarkets-grocery-stores-al-murar-dubai', 'alt': 'Embarkoh Grocery storefront photo', 'scope': 'exact'}, '4LKX': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/eb8d18fb-bb3a-46c7-8c0b-d224bfce806f-h.jpeg', 'source': 'https://www.hidubai.com/businesses/feya-beauty-salon-beauty-wellness-health-beauty-salons-international-city-warsan-1-dubai-2', 'alt': 'Feya Beauty Salon business listing photo', 'scope': 'exact'}, 'Y85U': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/76b00523-d822-4811-bbc8-be04e8422ffe-h.jpeg', 'source': 'https://www.hidubai.com/businesses/muna-laundry-home-laundry-al-karama-dubai-2', 'alt': 'Muna Laundry storefront photo', 'scope': 'exact'}, 'O2H3': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/9cfa55a5-c2e4-4add-9801-2ab2d744f37d-h.jpeg', 'source': 'https://www.hidubai.com/businesses/al-jasmi-laundry-home-laundry-al-baraha-dubai-2', 'alt': 'Al Jasmi Laundry storefront photo', 'scope': 'exact'}, 'Q850': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/0f91965b-7e48-4891-9d4b-5ad6d80aca07-h.jpeg', 'source': 'https://www.hidubai.com/businesses/afraa-laundry-home-laundry-al-hudaiba-dubai-2', 'alt': 'Afraa Laundry storefront photo', 'scope': 'exact'}, 'QOFX': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/1edcc4d1-6830-480f-a506-84a7dcc54193-h.jpeg', 'source': 'https://www.hidubai.com/businesses/al-mehairi-tailoring-embroidery-home-tailoring-al-bada-dubai-2', 'alt': 'Al Mehairi Tailoring and Embroidery storefront photo', 'scope': 'exact'}, 'D4BJ': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/109cafd6-2cf3-4f98-831c-c84fd039a48e-h.jpeg', 'source': 'https://www.hidubai.com/businesses/faisal-ali-juma-trading-b2b-services-construction-building-material-trading-naif-dubai-2', 'alt': 'Faisal Ali Juma Trading storefront photo', 'scope': 'exact'}, 'QAE8': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/a4982eb2-9169-4825-b022-285e6d1d51ed-h.jpeg', 'source': 'https://www.hidubai.com/businesses/al-jeel-al-saaed-grocery-shopping-supermarkets-hypermarkets-grocery-stores-al-qusais-3-dubai-2', 'alt': 'Al Jeel Al Saaed Grocery storefront photo', 'scope': 'exact'}, '04VO': {'url': 'https://images.fresha.com/locations/location-profile-images/599730/692293/d002fd18-b32e-43e9-8c3c-605aebe6b6dc.jpg?class=venue-gallery-large&f_quality=75&f_width=1920', 'source': 'https://www.fresha.com/a/lolita-queen-beauty-salon-dubai-business-bay-al-mustaqbal-st-the-exchange-tower-g03-v931ngpo', 'alt': 'Lolita Queen Beauty Salon venue interior', 'scope': 'exact'}, '8UB3': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/66e46b89-ecd7-4291-9f04-8dc7617a9687-h.jpeg', 'source': 'https://www.hidubai.com/businesses/youth-tailoring-home-tailoring-naif-dubai-2', 'alt': 'Youth Tailoring storefront photo', 'scope': 'exact'}, '99FB': {'url': 'https://cdn.placejoys.com/19495-oy-photo-1.jpg', 'source': 'https://falafil-al-rabiah-al-khadra.placejoys.com/', 'alt': 'Falafil Al Rabiah Al Khadra Al Barsha storefront photo', 'scope': 'exact'}, 'GAX6': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/8247c911-46d2-42ff-9a5c-7b899131fe76-h.png', 'source': 'https://www.hidubai.com/businesses/al-waqqas-restaurant-food-beverage-restaurants-bars-al-fahidi-al-souq-al-kabeer-dubai', 'alt': 'Al Waqqas Restaurant storefront photo', 'scope': 'exact'}, 'K3Y0': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/c52c5ace-2cea-4ac7-bbe5-805edc081442-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Al Nakheel Gate Cafeteria storefront photo', 'scope': 'exact'}, 'RCZ3': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/bcf3219f-d5f9-41b1-b9aa-9b2119917cb3-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Al Ajwa Minimart storefront photo', 'scope': 'exact'}, 'TNN1': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/ec35a17a-b0d5-451b-9450-e65e2973fd4d-h.jpeg', 'source': 'https://www.hidubai.com/', 'alt': 'Phonemart Trading business-associated listing photo', 'scope': 'exact'}, '06AS': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/c0b32725-431e-4a5f-a465-300ca0e50569-h.jpeg', 'source': 'https://www.hidubai.com/businesses/abdul-razzaq-mohiddin-abdulla-trading-b2b-services-distributors-wholesalers-al-ras-dubai-2', 'alt': 'Abdul Razzaq Mohiddin Abdulla Trading storefront at another Dubai branch', 'scope': 'branch'}, 'PKDN': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/7c5e76d0-1c40-4ea8-8615-56c56a4a610d-h.jpeg', 'source': 'https://www.hidubai.com/businesses/al-raj-electrical-sanitary-trading-home-construction-renovation-materials-naif-dubai-2', 'alt': 'Al Raj Electrical and Sanitary Trading storefront and street context', 'scope': 'exact'}}
PHOTO_MAP.update({'2ZSW': {'url': 'https://i0.wp.com/ravenousxerxes.com/wp-content/uploads/2019/11/img_20191103_125500.jpg?resize=1088%2C1451&ssl=1', 'source': 'https://ravenousxerxes.com/2019/11/03/kaiseki-zen-cafeteria-international-city/', 'alt': 'Kaiseki Zen Cafeteria former storefront in International City', 'scope': 'exact'}, 'A37N': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/564ecad2-9d9d-41c1-b5dd-dc30905cf621-h.jpeg', 'source': 'https://www.hidubai.com/businesses/rimal-gents-salon-beauty-wellness-health-beauty-salons-enpark-meaisem-1-dubai-2', 'alt': 'Rimal Gents Salon storefront and interior', 'scope': 'exact'}, 'B40O': {'url': 'https://wl-img-prd.s3-accelerate.amazonaws.com/d10ec26e-498f-4952-a47b-0436ec01bff9-h.jpeg', 'source': 'https://www.hidubai.com/businesses/capizone-hair-spa-center-beauty-wellness-health-beauty-salons-al-quoz-1-dubai-2', 'alt': 'Capizone Hair Spa storefront entrance', 'scope': 'exact'}, 'GP4A': {'url': 'https://lh3.googleusercontent.com/j-FC3Oe9Yib5XbgGd9eENqx6FIXiv4Ks1NV0soSdFzZKoCprWALWCxbLk39OWkqZhNhYv5meV9MGJarWpa5WBoIcvvh00VGUQb0h_A-PVw%3Dw1600-rw', 'source': 'https://magicpin.com/uae/Dubai/Naif/Home-Improvement/Madeenat-Al-Eman-Laundry/store/1a32729', 'alt': 'Madeenat Al Eman Laundry garment care service photo', 'scope': 'exact'}, 'MA03': {'url': 'https://dubaidirectory.com/custom/domain_1/image_files/sitemgr_photo_311468.jpeg', 'source': 'https://dubaidirectory.com/companies/055-mobile-phones.html', 'alt': '055 Mobile Phones storefront on 6 Street in Al Murar', 'scope': 'exact'}})

STATUS_NOTES = {'7Y5Y': 'Google did not mark the listing closed, while HiDubai reports it permanently closed. Verify by phone before visiting.', 'K3Y0': 'Google and directory sources differ on current operating status. Verify by phone or Maps before visiting.', 'VM0V': 'A different Al Muraqabat branch is reported closed elsewhere; this profile is anchored to the Muhaisnah 3 Place ID.'}

def _line(md, label):
    m=re.search(r'^- \*\*'+re.escape(label)+r':\*\* (.+)$', md, re.M)
    return m.group(1).strip() if m else ''

def load_records():
    records=[]
    for p in sorted((ROOT/'business-research').glob('*.md')):
        md=p.read_text(encoding='utf-8')
        def block(start,end):
            m=re.search(re.escape(start)+r'\s*\n\n(.+?)\n\n'+re.escape(end),md,re.S)
            return m.group(1).strip() if m else ''
        code_m=re.search(r'unique_code: "([^"]+)"',md)
        name_m=re.search(r'^# (.+)$',md,re.M)
        status_m=re.search(r'^status: "([^"]+)"',md,re.M)
        if not (code_m and name_m):
            continue
        sources_block=block('## Sources','## Research scope')
        sources=re.findall(r'- \[([^\]]+)\]\((https?://[^)]+)\) — ([^\n]+)',sources_block)
        r={
            'code':code_m.group(1),'name':name_m.group(1),'status':status_m.group(1) if status_m else '',
            'exec':block('## Executive summary','## Identity'),
            'maps_name':_line(md,'Current Google Maps name'),'maps_url':_line(md,'Exact Google Maps URL'),
            'category':_line(md,'Current Maps category'),'csv_category':_line(md,'Category in CSV'),
            'area':_line(md,'Area'),'op_status':_line(md,'Operational status'),'rating':_line(md,'Rating'),
            'reviews':_line(md,'Review count'),'address':_line(md,'Address'),'phone':_line(md,'Phone'),
            'hours':_line(md,'Hours'),'website':_line(md,'Website'),
            'finding':block('## Research findings','## Data-quality and discrepancy notes'),
            'sources':sources,
        }
        r['photo']=PHOTO_MAP.get(r['code'],{})
        r['status_note']=STATUS_NOTES.get(r['code'],'')
        records.append(r)
    return records


THEMES = {
    'beauty': {'class':'beauty','eyebrow':'Beauty · Dubai','headline':'Care, craft, and a clear way to visit.','section':'Beauty services'},
    'barber': {'class':'barber','eyebrow':'Grooming · Dubai','headline':'A neighborhood chair with a strong local footprint.','section':'Grooming'},
    'laundry': {'class':'laundry','eyebrow':'Garment care · Dubai','headline':'Local garment care, with the practical details up front.','section':'Garment care'},
    'food': {'class':'food','eyebrow':'Food · Dubai','headline':'A local food stop, grounded in what current listings actually verify.','section':'Food & service'},
    'grocery': {'class':'grocery','eyebrow':'Neighborhood retail · Dubai','headline':'Everyday convenience, close to home.','section':'At the store'},
    'tailor': {'class':'tailor','eyebrow':'Tailoring · Dubai','headline':'Measured, local, and built around craft.','section':'Tailoring & craft'},
    'industrial': {'class':'industrial','eyebrow':'Trade supply · Dubai','headline':'A practical local supplier for trade and workshop needs.','section':'Trade focus'},
    'auto': {'class':'auto','eyebrow':'Automotive · Dubai','headline':'Straightforward vehicle repair, mapped for the people who need it.','section':'Workshop services'},
    'electronics': {'class':'electronics','eyebrow':'Electronics · Dubai','headline':'A local electronics stop with the essential details in reach.','section':'Store focus'},
    'closed': {'class':'closed','eyebrow':'Business record · Dubai','headline':'This listing is currently marked permanently closed.','section':'Record status'},
}

SCHEMA = {
    'beauty':'BeautySalon', 'barber':'HairSalon', 'laundry':'LocalBusiness', 'food':'Restaurant',
    'grocery':'GroceryStore', 'tailor':'LocalBusiness', 'industrial':'Store', 'auto':'AutoRepair',
    'electronics':'ElectronicsStore', 'closed':'LocalBusiness'
}

def esc(x): return html.escape(str(x or ''))
def slug_tel(phone): return re.sub(r'[^+0-9]', '', phone or '')
def is_unknown(x): return not x or x.lower() in {'not returned','not available','unknown','not applicable','n/a'}

def theme_key(r):
    status=(r.get('op_status') or r.get('status') or '').strip().lower()
    if status in {'closed','permanently closed'} or status.startswith('permanently closed'): return 'closed'
    c=(r.get('category','')+' '+r.get('csv_category','')).lower()
    if any(x in c for x in ['beauty salon','ladies salon','hair spa']): return 'beauty'
    if any(x in c for x in ['barber','gents salon','hair salon']): return 'barber'
    if any(x in c for x in ['laundry','dry clean']): return 'laundry'
    if any(x in c for x in ['restaurant','cafeteria','food']): return 'food'
    if any(x in c for x in ['grocery','supermarket','minimart']): return 'grocery'
    if any(x in c for x in ['tailor','embroidery','boutique']): return 'tailor'
    if any(x in c for x in ['auto repair','garage','car repair']): return 'auto'
    if any(x in c for x in ['mobile','electronics']): return 'electronics'
    return 'industrial'

def primary_copy(r, theme):
    area=r.get('area') or 'Dubai'
    c=r.get('category') or r.get('csv_category') or 'local business'
    code=r['code']
    specials={
        '06AS':'Wholesale tailoring materials with a documented company history reaching back to 1925.',
        '99FB':'A highly visible Al Barsha cafeteria with a large public review footprint and long daily hours.',
        'AF86':'A Port Saeed barber with one of the strongest public review footprints in this research set.',
        'GP4A':'A 24-hour Deira laundry with an active independent website and a substantial Maps review footprint.',
        'XF68':'A Discovery Gardens beauty salon with a broad service mix documented across current directories.',
        '04VO':'A Business Bay beauty salon with an extensive current Fresha booking profile.',
        'GAX6':'Pakistani food in Bur Dubai with very long listed hours and takeaway/delivery signals across current sources.',
        'VW2A':'An Al Quoz workshop whose current map sources consistently identify the same garage and phone.',
        'RCZ3':'A licensed Al Barsha minimart with a DET-backed registry profile and late-night opening hours.',
    }
    if code in specials: return specials[code]
    if theme=='closed': return f'{r["maps_name"] or r["name"]} is currently marked permanently closed in the exact Google Maps record used for this project.'
    return f'{c} in {area}. Verified phone, location, hours and public listing context are kept easy to find.'

def service_items(r, theme):
    code=r['code']; e=(r.get('exec','')+' '+r.get('finding','')).lower()
    manual={
      'XF68':['Hair services','Keratin','Threading','Lashes','Nails','Waxing','Bridal makeup'],
      '04VO':['Extensive Fresha service menu','Beauty services','Appointment discovery via Fresha'],
      '06AS':['Tailoring materials','Needles & thread','Zippers & trimmings','Wholesale supply'],
      '0RGC':['Hardware','Garage / workshop equipment'],
      '1ELQ':['Haircuts','Children’s haircuts','Hair straightening','Keratin'],
      '4LKX':['Hair','Nails','Facials','Waxing','Bridal services'],
      '5BY4':['Hair styling','Nail treatments','Makeup','Henna','Beauty treatments'],
      '6S9L':['Beauty services','Official service information on current website'],
      '99FB':['Falafel / cafeteria service','Long daily hours','Social presence'],
      'AL60':['Hair','Makeup','Nails','Henna','Beauty treatments'],
      'CSII':['Cafeteria service','Late daily hours'],
      'DVHV':['Cafeteria service','Digital menu / ordering presence','WhatsApp contact'],
      'GAX6':['Pakistani cuisine','Takeaway','Delivery','Late-night service'],
      'GP4A':['Wash & iron','Dry cleaning','Shoe cleaning','Wash & fold','Pickup & delivery'],
      'M68R':['Spa treatments','Hair','Nails','Beauty treatments','Henna'],
      'PKDN':['Electrical supplies','Sanitary supplies','Building materials trading'],
      'TWB8':['All-brand repair coverage','Vehicle repair'],
      'VW2A':['Engine repair','Exhaust repair','Body repair'],
    }
    if code in manual: return manual[code]
    if theme=='laundry': return ['Laundry / garment care']
    if theme=='beauty': return ['Beauty salon services']
    if theme=='barber': return ['Haircuts & grooming']
    if theme=='food': return ['Restaurant / cafeteria service']
    if theme=='grocery': return ['Groceries & everyday essentials']
    if theme=='tailor': return ['Tailoring / embroidery']
    if theme=='auto': return ['Vehicle repair & maintenance']
    if theme=='electronics': return ['Mobile phones / electronics']
    if theme=='industrial': return [r.get('category') or 'Trade supply']
    return ['Historical business record']

def reputation(r):
    if is_unknown(r.get('rating')) or is_unknown(r.get('reviews')): return ''
    return f'{r["rating"]} ★ · {r["reviews"]} Google review{("" if str(r["reviews"])=="1" else "s")} at research snapshot'

def image_block(r):
    p=r.get('photo') or {}
    if not p.get('url'):
        return f'''<div class="photo photo-missing" role="img" aria-label="Verified production photography not yet available for {esc(r['maps_name'] or r['name'])}">
          <span class="photo-code">{esc(r['code'])}</span>
          <strong>On-location photography pending</strong>
          <p>No exact, trustworthy production photo was found in this research pass. We chose not to substitute unrelated stock.</p>
          <a href="{esc(r['maps_url'])}" target="_blank" rel="noopener">Check current photos on Google Maps ↗</a>
        </div>'''
    alt=p.get('alt') or f'{r["maps_name"] or r["name"]} business photo'
    label='Branch-associated business photo' if p.get('scope')=='branch' else 'Business listing photo'
    return f'''<figure class="photo">
      <img src="{esc(p['url'])}" alt="{esc(alt)}" loading="eager" decoding="async" referrerpolicy="no-referrer">
      <figcaption><span>{esc(label)}</span> · Demo/editorial use. <a href="{esc(p.get('source') or r['maps_url'])}" target="_blank" rel="noopener">Source ↗</a></figcaption>
    </figure>'''

def fact_card(label, value, href=None):
    if is_unknown(value):
        value='Verify before visiting'
        cls=' muted'
    else: cls=''
    body=f'<a href="{esc(href)}">{esc(value)}</a>' if href else esc(value)
    return f'<div class="fact{cls}"><span>{esc(label)}</span><strong>{body}</strong></div>'

def render(r):
    tkey=theme_key(r); t=THEMES[tkey]
    name=r.get('maps_name') or r['name']; area=r.get('area') or 'Dubai'
    closed=tkey=='closed'; conflict=r.get('status_note','')
    services=service_items(r,tkey)
    phone=r.get('phone','')
    tel=slug_tel(phone) if not is_unknown(phone) else ''
    rep=reputation(r)
    website=r.get('website','')
    photo=r.get('photo') or {}
    title=f'{name} · {area} | Dubai'
    desc=primary_copy(r,tkey)
    canonical=f'{BASE_URL}/{r["code"]}/'
    schema={
      '@context':'https://schema.org','@type':SCHEMA[tkey], 'name':name,
      'url':canonical, 'address': {'@type':'PostalAddress','streetAddress':r.get('address',''), 'addressLocality':'Dubai','addressCountry':'AE'},
      'sameAs':[r.get('maps_url')] + ([website] if website else []),
      'description':desc
    }
    if tel and not closed: schema['telephone']=phone
    if not is_unknown(r.get('rating')) and not is_unknown(r.get('reviews')):
        try: schema['aggregateRating']={'@type':'AggregateRating','ratingValue':float(r['rating']),'reviewCount':int(str(r['reviews']).replace(',',''))}
        except: pass
    if photo.get('url'): schema['image']=photo['url']
    cta=[]
    if tel and not closed: cta.append(f'<a class="button primary" href="tel:{esc(tel)}">Call {esc(phone)}</a>')
    if website and not closed: cta.append(f'<a class="button secondary" href="{esc(website)}" target="_blank" rel="noopener">Visit current web presence ↗</a>')
    cta.append(f'<a class="button ghost" href="{esc(r["maps_url"])}" target="_blank" rel="noopener">{("Check current listing" if closed else "Get directions")} ↗</a>')
    services_html=''.join(f'<li>{esc(x)}</li>' for x in services)
    source_links=''.join(f'<a href="{esc(s[1])}" target="_blank" rel="noopener">{esc(s[0])}</a>' for s in (r.get('sources') or [])[:4])
    status_banner=''
    if closed:
      status_banner='<div class="status-banner closed">Permanently closed in the current Google Maps record · Do not use this page as an active sales listing.</div>'
    elif conflict:
      status_banner=f'<div class="status-banner warning">Status note: {esc(conflict)}</div>'
    photo_notice=''
    if photo.get('url'):
        qualifier='This photo is associated with another Dubai branch of the same business/brand, not confirmed as this exact branch.' if photo.get('scope')=='branch' else 'This image comes from a public business/listing source and is used for demo/editorial context on this site.'
        photo_notice=f'<p class="rights-note"><strong>Photo rights:</strong> {esc(qualifier)} Ownership/license is not asserted. Replace with owner-supplied or properly licensed originals before commercial launch.</p>'
    else:
        photo_notice='<p class="rights-note"><strong>Photo rights:</strong> No unambiguous production photo was found. The site intentionally avoids unrelated stock; commission or obtain owner-approved photography before commercial launch.</p>'

    # layout-specific mid section names/copy
    section_intro={
      'beauty':'The public research supports a real local salon footprint. Only services explicitly supported by current listings are surfaced here.',
      'barber':'Grooming information is kept concise and practical: what the listing supports, where to go, and how to reach the salon.',
      'laundry':'This page prioritizes reliable contact, location and opening information over unverified turnaround or pricing promises.',
      'food':'Food pages should earn appetite with real photography and real menu facts. Where a menu or price is not verified, this site does not invent one.',
      'grocery':'For a neighborhood store, usefulness wins: location, hours and contact come before decorative marketing copy.',
      'tailor':'Craft is best shown through real garments, fabric and process photography. This prototype only names services supported by public evidence.',
      'industrial':'Trade customers need specificity and fast contact. This layout treats the page more like a clear product/service sheet than a lifestyle campaign.',
      'auto':'Workshop trust comes from real repair context, transparent contact details and clear location—not oversized animation.',
      'electronics':'A focused retail page: store identity, location, contact and verified product category without invented inventory.',
      'closed':'This is an archival prototype, not an active conversion page. The closure flag is intentionally the most prominent content.'
    }[tkey]

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{esc(canonical)}">
  {f'<meta property="og:image" content="{esc(photo.get("url"))}">' if photo.get('url') else ''}
  <meta name="theme-color" content="#171717">
  <link rel="stylesheet" href="../assets/site.css">
  <script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace('</','<\\/')}</script>
</head>
<body class="theme-{esc(t['class'])}">
<a class="skip" href="#main">Skip to content</a>
{status_banner}
<header class="site-header">
  <a class="brand" href="./" aria-label="{esc(name)} home"><span class="brand-mark">{esc(r['code'])}</span><span>{esc(name)}</span></a>
  <nav aria-label="Primary navigation">
    <a href="#focus">{esc(t['section'])}</a><a href="#details">Visit</a><a href="#proof">Why this page</a>
  </nav>
</header>
<main id="main">
  <section class="hero">
    <div class="hero-copy reveal">
      <p class="eyebrow">{esc(area)} · {esc(r.get('category') or r.get('csv_category'))}</p>
      <h1>{esc(name)}</h1>
      <p class="lede">{esc(primary_copy(r,tkey))}</p>
      <div class="actions">{''.join(cta)}</div>
      {f'<p class="rating">{esc(rep)}</p>' if rep else ''}
    </div>
    <div class="hero-visual reveal">{image_block(r)}</div>
  </section>

  <section class="signal-strip" aria-label="Business highlights">
    <div><span>Area</span><strong>{esc(area)}</strong></div>
    <div><span>Category</span><strong>{esc(r.get('category') or r.get('csv_category'))}</strong></div>
    <div><span>Status</span><strong>{esc(r.get('op_status') or r.get('status'))}</strong></div>
  </section>

  <section id="focus" class="section split">
    <div class="section-heading reveal"><p class="eyebrow">{esc(t['section'])}</p><h2>{esc(t['headline'])}</h2><p>{esc(section_intro)}</p></div>
    <div class="service-panel reveal"><ul class="service-list">{services_html}</ul></div>
  </section>

  <section class="story section">
    <div class="story-card reveal"><p class="eyebrow">What the research supports</p><h2>Specific to this place.</h2><p>{esc(r.get('finding') or r.get('exec'))}</p></div>
    <div class="story-card alt reveal"><p class="eyebrow">Public proof</p><h2>{esc(rep or 'Listing identity verified')}</h2><p>Google Maps is used as the stable identity anchor for these details. Ratings, review counts and hours are point-in-time data and should be rechecked before launch.</p></div>
  </section>

  <section id="details" class="section details">
    <div class="section-heading reveal"><p class="eyebrow">Visit / contact</p><h2>Useful details, not hidden in a footer.</h2></div>
    <div class="fact-grid reveal">
      {fact_card('Address', r.get('address'), r.get('maps_url'))}
      {fact_card('Phone', r.get('phone'), ('tel:'+tel) if tel and not closed else None)}
      {fact_card('Hours', r.get('hours'))}
      {fact_card('Google Maps', 'Open exact listing', r.get('maps_url'))}
    </div>
    <div class="actions bottom-actions">{''.join(cta)}</div>
  </section>

  <section id="proof" class="section provenance">
    <div class="section-heading reveal"><p class="eyebrow">Verified information</p><h2>Sources & image notes.</h2></div>
    <div class="provenance-grid reveal">
      <p>Key public details on this page are based on research dated <strong>4 September 2026</strong>. Prices, policies, inventory, testimonials and booking workflows are omitted unless verified.</p>
      <div class="source-links">{source_links}</div>
    </div>
    {photo_notice}
  </section>
</main>
<footer><span>{esc(name)} · {esc(r['code'])}</span><a href="{esc(r['maps_url'])}" target="_blank" rel="noopener">Google Maps ↗</a></footer>
<script src="../assets/site.js" defer></script>
</body>
</html>'''

CSS = r'''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}a{color:inherit}.skip{position:fixed;left:1rem;top:-5rem;background:#fff;color:#000;padding:.7rem 1rem;border-radius:.5rem;z-index:99}.skip:focus{top:1rem}body{--bg:#f7f4ef;--surface:#fff;--text:#1c1b1a;--muted:#6e6962;--accent:#7f2948;--accent2:#d4a7b6;--line:rgba(28,27,26,.14);--display:Georgia,"Times New Roman",serif;--radius:30px}.theme-barber{--bg:#101214;--surface:#181b1e;--text:#f4efe8;--muted:#aaa29a;--accent:#c9965b;--accent2:#5d7182;--line:rgba(255,255,255,.13);--display:ui-serif,Georgia,serif;--radius:8px}.theme-laundry{--bg:#f3f8fa;--surface:#fff;--text:#14252e;--muted:#627580;--accent:#25769b;--accent2:#9bd3df;--line:rgba(20,37,46,.13);--display:ui-sans-serif,system-ui,sans-serif;--radius:22px}.theme-food{--bg:#f7efe5;--surface:#fffaf4;--text:#291c16;--muted:#79685f;--accent:#b2492f;--accent2:#55735b;--line:rgba(41,28,22,.13);--display:Georgia,serif;--radius:18px}.theme-grocery{--bg:#f2f6ed;--surface:#fbfff7;--text:#172417;--muted:#5c705e;--accent:#3f7b44;--accent2:#d38a3a;--line:rgba(23,36,23,.13);--display:ui-sans-serif,system-ui,sans-serif;--radius:16px}.theme-tailor{--bg:#f7f0e9;--surface:#fffaf5;--text:#2b171c;--muted:#7a6469;--accent:#8d2f45;--accent2:#b58b44;--line:rgba(43,23,28,.14);--display:Georgia,serif;--radius:2px}.theme-industrial{--bg:#eef0f1;--surface:#f9faf9;--text:#192025;--muted:#657077;--accent:#d97706;--accent2:#526773;--line:rgba(25,32,37,.18);--display:"Arial Narrow",Arial,sans-serif;--radius:6px}.theme-auto{--bg:#0f1214;--surface:#181d20;--text:#f3f4f4;--muted:#a3adb1;--accent:#ef6c2c;--accent2:#6f8791;--line:rgba(255,255,255,.12);--display:"Arial Narrow",Arial,sans-serif;--radius:10px}.theme-electronics{--bg:#07131c;--surface:#0d202d;--text:#ecf8ff;--muted:#9db3c2;--accent:#36c9e8;--accent2:#6c76ff;--line:rgba(160,220,255,.16);--display:ui-sans-serif,system-ui,sans-serif;--radius:18px}.theme-closed{--bg:#ecebea;--surface:#f6f4f1;--text:#272523;--muted:#746f69;--accent:#8b8178;--accent2:#bbb4ad;--line:rgba(39,37,35,.16);--display:Georgia,serif;--radius:12px}::selection{background:var(--accent);color:#fff}.status-banner{padding:.65rem 5vw;text-align:center;font-size:.84rem;font-weight:700;letter-spacing:.02em}.status-banner.closed{background:#7b2525;color:#fff}.status-banner.warning{background:#f0c65a;color:#2a2109}.site-header{height:78px;padding:0 5vw;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);position:relative;z-index:4}.brand{display:flex;align-items:center;gap:.75rem;text-decoration:none;font-weight:750;max-width:64%}.brand-mark{display:inline-grid;place-items:center;min-width:44px;height:34px;padding:0 .6rem;border:1px solid var(--line);background:var(--surface);font:700 .7rem/1 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em}.site-header nav{display:flex;gap:1.25rem}.site-header nav a{text-decoration:none;color:var(--muted);font-size:.86rem;font-weight:650}.site-header nav a:hover,.site-header nav a:focus-visible{color:var(--text)}.hero{min-height:74vh;display:grid;grid-template-columns:minmax(0,1.02fr) minmax(340px,.98fr);gap:5vw;align-items:center;padding:6vw 5vw}.hero-copy{max-width:760px}.eyebrow{text-transform:uppercase;letter-spacing:.18em;font-size:.72rem;font-weight:800;color:var(--accent);margin:0 0 1rem}.hero h1,.section h2{font-family:var(--display);font-weight:500;letter-spacing:-.035em;line-height:.97;margin:0}.hero h1{font-size:clamp(3.2rem,7.2vw,8rem);max-width:12ch}.lede{font-size:clamp(1.08rem,1.6vw,1.4rem);color:var(--muted);max-width:62ch;margin:1.6rem 0 0}.actions{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:2rem}.button{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:.7rem 1.05rem;border:1px solid var(--line);text-decoration:none;font-weight:750;font-size:.86rem;transition:transform .2s ease,background .2s ease,border-color .2s ease}.button:hover{transform:translateY(-2px)}.button.primary{background:var(--accent);border-color:var(--accent);color:white}.button.secondary{background:var(--surface)}.button.ghost{background:transparent}.rating{margin-top:1.2rem;color:var(--muted);font-size:.82rem}.photo{margin:0;position:relative;overflow:hidden;border-radius:var(--radius);min-height:480px;background:var(--surface);border:1px solid var(--line);box-shadow:0 30px 80px rgba(0,0,0,.12)}.photo img{width:100%;height:100%;min-height:480px;max-height:70vh;object-fit:cover;display:block;filter:saturate(.92) contrast(1.02)}.photo figcaption{position:absolute;left:1rem;right:1rem;bottom:1rem;background:color-mix(in srgb,var(--surface) 88%,transparent);backdrop-filter:blur(12px);padding:.65rem .8rem;border:1px solid var(--line);font-size:.72rem;color:var(--muted)}.photo figcaption span{color:var(--text);font-weight:750}.photo-missing{display:flex;flex-direction:column;justify-content:flex-end;padding:2rem;background:radial-gradient(circle at 75% 20%,color-mix(in srgb,var(--accent2) 30%,transparent),transparent 45%),linear-gradient(145deg,var(--surface),color-mix(in srgb,var(--bg) 60%,var(--surface)));min-height:480px}.photo-missing:before{content:"";position:absolute;inset:1.5rem;border:1px dashed var(--line);pointer-events:none}.photo-missing .photo-code{font:800 clamp(4rem,10vw,9rem)/.8 ui-monospace,monospace;opacity:.08;position:absolute;right:1rem;top:2rem}.photo-missing strong{font-family:var(--display);font-size:1.8rem;position:relative}.photo-missing p,.photo-missing a{max-width:38ch;position:relative;color:var(--muted)}.signal-strip{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin:0 5vw}.signal-strip div{padding:1.5rem 2rem;border-right:1px solid var(--line)}.signal-strip div:last-child{border-right:0}.signal-strip span,.fact span{display:block;text-transform:uppercase;letter-spacing:.16em;font-size:.64rem;color:var(--muted);font-weight:800;margin-bottom:.35rem}.signal-strip strong{font-size:.95rem}.section{padding:8vw 5vw;border-bottom:1px solid var(--line)}.split{display:grid;grid-template-columns:.9fr 1.1fr;gap:9vw;align-items:start}.section-heading h2{font-size:clamp(2.4rem,4.8vw,5.4rem);max-width:12ch}.section-heading>p:last-child{color:var(--muted);max-width:54ch;font-size:1.02rem}.service-panel{background:var(--surface);padding:clamp(1.5rem,4vw,3.5rem);border:1px solid var(--line);border-radius:var(--radius)}.service-list{padding:0;margin:0;list-style:none}.service-list li{font-family:var(--display);font-size:clamp(1.3rem,2.3vw,2.4rem);padding:1rem 0;border-bottom:1px solid var(--line)}.service-list li:last-child{border-bottom:0}.story{display:grid;grid-template-columns:1.2fr .8fr;gap:1rem}.story-card{background:var(--surface);border:1px solid var(--line);padding:clamp(2rem,5vw,5rem);border-radius:var(--radius)}.story-card.alt{background:color-mix(in srgb,var(--accent) 9%,var(--surface))}.story-card h2{font-size:clamp(2rem,4vw,4.4rem);max-width:14ch}.story-card p:last-child{color:var(--muted);font-size:1.02rem}.details{display:grid;grid-template-columns:.7fr 1.3fr;gap:7vw}.details .bottom-actions{grid-column:2}.fact-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1px;background:var(--line);border:1px solid var(--line)}.fact{padding:1.5rem;background:var(--surface);min-height:142px}.fact strong{display:block;font-size:1rem;line-height:1.45}.fact a{text-decoration-thickness:.08em;text-underline-offset:.18em}.fact.muted strong{color:var(--muted)}.provenance{display:grid;grid-template-columns:.7fr 1.3fr;gap:7vw}.provenance-grid{display:grid;grid-template-columns:1fr 1fr;gap:2rem}.provenance-grid>p{margin-top:0;color:var(--muted)}.source-links{display:flex;align-content:flex-start;flex-wrap:wrap;gap:.55rem}.source-links a{font-size:.72rem;text-decoration:none;border:1px solid var(--line);padding:.5rem .65rem;background:var(--surface)}.rights-note{grid-column:2;color:var(--muted);font-size:.78rem;margin-top:2rem;max-width:80ch}footer{padding:2rem 5vw;display:flex;justify-content:space-between;color:var(--muted);font-size:.76rem}.theme-food .hero{grid-template-columns:.8fr 1.2fr}.theme-food .photo{min-height:580px}.theme-tailor .hero,.theme-industrial .hero{border-bottom:1px dashed var(--line)}.theme-tailor .service-panel{box-shadow:inset 0 0 0 8px var(--bg)}.theme-industrial .eyebrow,.theme-auto .eyebrow,.theme-electronics .eyebrow{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.theme-industrial .brand-mark,.theme-auto .brand-mark{background:var(--accent);color:#fff;border-color:transparent}.theme-auto .hero-visual{transform:skewY(-1.4deg)}.theme-electronics .photo{box-shadow:0 0 70px color-mix(in srgb,var(--accent) 18%,transparent)}.theme-closed .photo img{filter:grayscale(1);opacity:.72}.theme-closed .button.primary{background:var(--text);border-color:var(--text)}.reveal{opacity:0;transform:translateY(18px);transition:opacity .55s ease,transform .55s ease}.reveal.visible{opacity:1;transform:none}:focus-visible{outline:3px solid var(--accent);outline-offset:4px}@media(max-width:850px){.site-header nav{display:none}.brand{max-width:90%;font-size:.9rem}.hero{grid-template-columns:1fr;padding-top:12vw}.hero h1{font-size:clamp(3rem,15vw,5rem)}.hero-visual{order:-1}.photo,.photo img,.photo-missing{min-height:360px;max-height:54vh}.signal-strip{grid-template-columns:1fr;margin:0 5vw}.signal-strip div{border-right:0;border-bottom:1px solid var(--line)}.signal-strip div:last-child{border-bottom:0}.split,.story,.details,.provenance{grid-template-columns:1fr}.details .bottom-actions,.rights-note{grid-column:1}.fact-grid,.provenance-grid{grid-template-columns:1fr}.section{padding-top:16vw;padding-bottom:16vw}footer{flex-direction:column;gap:.5rem}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.reveal{opacity:1;transform:none;transition:none}.button{transition:none}}
'''

JS = r'''document.documentElement.classList.add('js');const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;if(reduce){document.querySelectorAll('.reveal').forEach(el=>el.classList.add('visible'));}else{const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.08});document.querySelectorAll('.reveal').forEach(el=>io.observe(el));}'''

def root_index(records):
    cards=''.join(f'''<a class="directory-card" href="./{esc(r['code'])}/"><span>{esc(r['code'])}</span><strong>{esc(r.get('maps_name') or r['name'])}</strong><small>{esc(r.get('area'))} · {esc(r.get('category'))}</small></a>''' for r in records)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UAE business prototypes</title><meta name="description" content="51 evidence-backed Dubai business website prototypes."><style>body{{margin:0;background:#111;color:#eee;font-family:system-ui,sans-serif}}main{{padding:8vw 5vw}}h1{{font:500 clamp(3rem,8vw,8rem)/.9 Georgia,serif;max-width:10ch}}p{{color:#aaa;max-width:55ch}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1px;background:#333;border:1px solid #333;margin-top:4rem}}.directory-card{{background:#171717;color:inherit;padding:1.4rem;text-decoration:none;min-height:160px;display:flex;flex-direction:column;gap:.6rem}}.directory-card:hover{{background:#202020}}.directory-card span{{font:700 .7rem ui-monospace,monospace;color:#e0a96d}}.directory-card strong{{font-size:1.05rem}}.directory-card small{{color:#999;margin-top:auto}}</style></head><body><main><p>Prithiraj · UAE demo</p><h1>Business website prototypes.</h1><p>51 static microsites built from exact-place research. Photography is only used when business-specific imagery could be verified; all third-party images are marked as demo/editorial.</p><div class="grid">{cards}</div></main></body></html>'''

def build():
    records=load_records()
    (ROOT/'assets').mkdir(parents=True,exist_ok=True)
    (ROOT/'assets'/'site.css').write_text(CSS,encoding='utf-8')
    (ROOT/'assets'/'site.js').write_text(JS,encoding='utf-8')
    for r in records:
        d=ROOT/r['code']; d.mkdir(exist_ok=True)
        (d/'index.html').write_text(render(r),encoding='utf-8')
    (ROOT/'index.html').write_text(root_index(records),encoding='utf-8')
    (ROOT/'.nojekyll').write_text('',encoding='utf-8')
    (ROOT/'404.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Not found</title><style>body{font:18px system-ui;background:#111;color:#eee;padding:10vw}a{color:#e0a96d}</style><h1>Page not found</h1><p><a href="/uae_demo/">Browse the UAE demo directory</a></p>',encoding='utf-8')
    print(f'Built {len(records)} microsites')

if __name__=='__main__': build()
