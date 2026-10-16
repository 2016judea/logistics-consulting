#!/usr/bin/env python3
"""Build outreach/round1/recipients.csv and one draft per recipient.

Every email here is either (P) published on the company's own website, or (F) filed
by the operator in the FMCSA federal carrier census (data.transportation.gov/az4n-8mr2) —
a signed federal record. No address is a guessed first.last pattern. The verification
method is recorded per row in email_method.

Draft body is fixed per Aidan's spec: opener -> Amazon credential (his words) ->
five problem lines (generic industry terms, no numbers, no Amazon internals) ->
"Ask me anything, I do consulting." -> LinkedIn + Substack links. No price, no attachment.
"""
import csv, os, re

LINKEDIN = "https://www.linkedin.com/in/aidan-jude-2016/"
SUBSTACK = "https://randomaidan.substack.com/p/directed-staffing-of-outbound-dock"

# segment, company, city_state, person, title, email, method(P/F), email_source_url,
# subject, opener, opener_source_url, opener_date
R = [
# ---------------- Segment 1: Twin Cities 7-county metro 3PL / warehousing / fulfillment / FBA-prep / courier ----------------
(1,"KSP Fulfillment","Brooklyn Park, MN","Deena Kalk","VP of Operations & Account Management","sales@ksp3pl.com","P","https://ksp3pl.com/careers",
 "Your weekend dock shift",
 "You're hiring warehouse associates across five shift patterns at the Brooklyn Park floor, including a Friday-to-Sunday day shift and two split second shifts.",
 "https://ksp3pl.com/careers","2026-09-17"),
(1,"Citi-Cargo & Storage","Eagan, MN","Rick Waschek","Operations (named recipient for resumes)","rwaschek@citi-cargo.com","P","https://citi-cargo.com/about-us/",
 "Containers in and out of Eagan",
 "You run containers, public warehousing and your own fleet out of Eagan, St. Paul and Fargo, and you're the name on the door for anyone who wants to talk operations.",
 "https://citi-cargo.com/about-us/","2026-10-16"),
(1,"Superior 3rd Party Logistics (S3PL)","Saint Paul, MN","Chris Wyffels","Owner / Principal","chrisw@s3pl.com","P","https://s3pl.com/contact-us-2/",
 "Your new CFS station",
 "You just brought a new container freight station online and are routing your ocean and air imports through it out of the Wynne Avenue building.",
 "https://s3pl.com/","2026-10-16"),
(1,"VitaLogistics","Saint Paul, MN","Dalton","Founder / Operations","Dalton@VitaLogistics.Co","P","https://vitalogistics.co",
 "Holding a 99.4% SLA",
 "You posted a 99.4% SLA hit rate for Q1 on a 2pm same-day cutoff, running fulfillment for founder-led supplement and wellness brands out of Transfer Road.",
 "https://vitalogistics.co","2026-10-16"),
(1,"Winnesota Regional Transportation","Edina, MN","Joey Frechette","Owner","joey@winnesota.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=503238",
 "Cold chain in the summer heat",
 "You wrote up the nine steps Winnesota takes to protect a refrigerated load from summer heat, starting with a full pre-trip on every reefer unit before it leaves the dock.",
 "https://www.winnesota.com/9-steps-winnesota-takes-to-protect-your-cold-chain-from-summer-heat/","2026-06-29"),
(1,"Logistics Services, Inc. (LSI)","Eagan, MN","Kathy Berglof","Owner / Officer","kberglof@shiplsi.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=675241",
 "Dispatch out of Apollo Road",
 "You run a 43-truck dedicated and dispatch operation out of Apollo Road in Eagan, and refreshed your federal carrier filing this February.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=675241","2026-02-03"),
(1,"Dedicated Logistics / Total Logistics (TLI)","Oakdale, MN","Mike Narance","Vice President, Operations","mike.narance@tlicompanies.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=618375",
 "213 trucks out of Oakdale",
 "You run the dedicated-fleet and warehousing side of Total Logistics out of Oakdale, a 213-power-unit operation you refiled with FMCSA this March.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=618375","2026-03-25"),
(1,"Pro Courier","Spring Lake Park, MN","Ed Sanville","Owner / Officer","ed@procourierinc.com","P","https://procourierinc.com/Contact.html",
 "Hiring drivers in Spring Lake Park",
 "You're hiring drivers with a Minnesota license for multiple positions, running same-day and nationwide hotshot work out of Spring Lake Park.",
 "https://procourierinc.com/Contact.html","2026-10-16"),
(1,"CSP Delivery","Fridley, MN","Nick Johnson","CEO","njohnson@cspdelivery.com","P","https://cspdelivery.com/meet-the-team",
 "The Fridley dock",
 "You and Nicole run CSP's courier and warehouse operation out of Fridley with a small-town-service pitch and a 27-truck fleet.",
 "https://cspdelivery.com/meet-the-team","2026-10-16"),
(1,"Alliance Courier (McHugh Group)","Bloomington, MN","Leonard McHugh","Owner","lgmchugh@alliancecourier.us","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=1429009",
 "74 trucks out of Bloomington",
 "You run Alliance Courier as a 74-truck same-day operation out of Bloomington, with a shipping-and-receiving dock in Menomonie as well.",
 "https://www.alliancecourier.us/","2026-10-16"),
(1,"Optimus Courier","Eagan, MN","Mohamed Malak","Owner","malak@optimuscourier.com","P","https://optimuscourier.com/contact/",
 "40 trucks out of Eagan",
 "You run Optimus as a 40-truck courier operation out of Eagan and keep your own number on the contact page for new work.",
 "https://optimuscourier.com/contact/","2026-10-16"),
(1,"Quicksilver Express Courier","Saint Paul, MN","Rob Lust","Owner / Officer","lust@qec.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=429037",
 "The Twin Cities dock",
 "You run Quicksilver's Minnesota courier operation out of St. Paul, one hub in a seven-metro network you built from the Twin Cities out.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=429037","2026-05-13"),
(1,"Brickhouse Delivery Service","Albertville, MN","Brian Sletten","Owner","brian.s@brickhousedeliveryservice.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=3775529",
 "Growing out of Albertville",
 "You run Brickhouse as a nine-truck delivery operation out of Albertville, and refreshed your federal carrier filing this March as you scale.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=3775529","2026-03-04"),
(1,"Strategic Transportation / Strategic Warehousing","Eagan, MN","Jenna Hegland","Director, Brokerage Operations","jhegland@strategic-transportation.com","P","https://www.strategicwarehousing.com",
 "Three docks across the metro",
 "You run brokerage operations across Strategic's three Twin Cities warehouses out of Eagan Industrial Road.",
 "https://www.strategicwarehousing.com","2026-10-16"),
(1,"Triangle Warehouse / Benchmark Logistics","Minneapolis, MN","Peter Kaufhold","Owner","sales@trianglewarehouse.com","P","https://www.trianglewarehouse.com",
 "Food-grade in Northeast Minneapolis",
 "You run food-grade warehousing, inventory control and a dedicated fleet out of Marshall Street NE, a Minneapolis operation that dates back to a single truck in 1958.",
 "https://www.trianglewarehouse.com","2026-10-16"),
(1,"Hudson Refrigerated Logistics","Mendota Heights, MN","Aaron Hudson","Owner","info@hudsonltl.com","P","https://www.hudsonltl.com",
 "Cold chain, 24/7/365",
 "You run temperature-controlled trucking and cold storage out of Mendota Heights on a 24/7/365 basis.",
 "https://www.hudsonltl.com","2026-10-16"),
(1,"Rogue Fulfillment","Minneapolis, MN","Hiring Manager","Owner / Operations","info@roguefulfillment.com","P","https://www.roguefulfillment.com/careers",
 "Hiring in the old Ry-Krisp building",
 "You're hiring fulfillment associates into the renovated Ry-Krisp building in Northeast Minneapolis, running ecommerce fulfillment for growing brands.",
 "https://www.roguefulfillment.com/careers","2026-10-16"),

# ---------------- Segment 2: National / regional mid-market 3PLs with a live operations hiring signal ----------------
(2,"Bergen Logistics","Rutherford, NJ","Patrick Ringston","Chief Operating Officer","patrick.ringston@bergenlogistics.com","P","https://bergenlogistics.com/about-us",
 "Your Kennesaw shipping shift",
 "You've got a Shipping Supervisor and a VAS Supervisor open at Kennesaw right now, on top of the order-picking roles across Rutherford and Cerritos.",
 "https://www.linkedin.com/jobs/view/shipping-supervisor-at-bergen-logistics-4476690103","2026-10-14"),
(2,"Combined Warehouse","Bridgeview, IL","Ryan Altice","Vice President","ryan@combinedwarehouse.com","P","https://www.combinedwarehouse.com",
 "Your new Bridgeview floor",
 "You're opening a new 3PL facility at 7700 S. 78th Ave in Bridgeview and hiring an experienced second-shift forklift operator to run it.",
 "https://combinedwarehouse.com/careers","2026-10-16"),
(2,"DXL 3PL","Indianapolis, IN","Dave Adams","VP of Operations","dave.adams@dxl3pl.com","P","https://www.dxl3pl.com/about-us",
 "The Indianapolis floor",
 "You run operations across DXL's DTC, B2B and production floors in Indianapolis, the whole fulfillment backbone for your brands under one roof.",
 "https://www.dxl3pl.com/about-us","2026-10-16"),
(2,"Capitol Warehousing","Windsor, WI","Josh Rodman","General Manager","joshr@capitolwhse.com","P","https://capitolwhse.com/contact/",
 "Hiring at Windsor",
 "You've got a forklift operator role open at the Windsor floor, one of four Capitol operations across Wisconsin and Illinois.",
 "https://capitolwhse.com/careers/","2026-10-16"),
(2,"Midwest Warehousing","Oak Park, MI","Brandon Noll","CEO","bnoll@midwestwarehousing.com","P","https://midwestwarehousing.com/about/",
 "Hiring onto the floor",
 "You're hiring warehouse associates and forklift drivers into the Midwest Warehousing floor as you add volume.",
 "https://midwestwarehousing.com/careers/","2026-10-16"),
(2,"Global Distribution Center","Bowling Green, OH","Tony Marks","CEO / President","tmarks@globaldcllc.com","P","https://www.globaldcllc.com",
 "Your operations seat",
 "You're hiring an Operations Manager onto the Global DC floor, the seat that runs the whole warehouse and logistics side.",
 "https://www.globaldcllc.com","2026-10-16"),
(2,"Eagle Warehouse & Logistics","Grove City, OH","Ron Flowers","President","rflowers@eaglelogistics.com","P","https://www.eaglelogistics.com/contact/",
 "The Grove City dock",
 "You run Eagle as a family operation out of Grove City with Matt on the warehouse and Glen on logistics, all of it off the Gantz Road dock.",
 "https://www.eaglelogistics.com/contact/","2026-10-16"),
(2,"Exegistics","Indianapolis, IN","Kenneth Stewart","General Manager","kenneth.stewart@exegistics.com","P","https://exegistics.com/warehousing-services/meet-our-team/",
 "The Indianapolis warehouse",
 "You run Exegistics' warehouse out of Indianapolis, a veteran-owned operation that staffs and runs the floor at once.",
 "https://exegistics.com/warehousing-services/meet-our-team/","2026-10-16"),
(2,"Clean Earth Logistics","McDonough, GA","Daryl Wulf","President","darylw@cleanearthlogistics.com","P","https://www.cleanearthlogistics.com/contact",
 "The Atlanta-area floor",
 "You run Clean Earth's 3PL and warehousing operation out of the Atlanta metro, and you're the direct line for anyone who wants to talk operations.",
 "https://www.cleanearthlogistics.com/contact","2026-10-16"),
(2,"Anex Warehouse & Distribution","Ruffs Dale, PA","Matt Sylvester","President","msylvester@anexwarehouse.com","P","https://anexwarehouse.com/contact/",
 "The Ruffs Dale dock",
 "You run Anex's warehousing, transportation and distribution out of the Brickyard Hill Road corporate office in Western Pennsylvania.",
 "https://anexwarehouse.com/contact/","2026-10-16"),
(2,"Cargo Group","Savannah, GA","Rick Lee","President","rick.lee@cargogroupllc.com","P","https://cargogroupllc.com/contact/",
 "Heavy lift out of Savannah",
 "You run Cargo Group's warehousing, heavy-lift and project-cargo operation out of Savannah.",
 "https://cargogroupllc.com/contact/","2026-10-16"),
(2,"Champagne Logistics","Franklin, MA","Colin MacLeod","Warehouse Manager","cmacleod@champagnelogistics.com","P","https://www.champagnelogistics.com/contact-us/",
 "The Franklin warehouse",
 "You run the Champagne Logistics warehouse a mile off I-495 in Franklin, the person on the hook for what moves across that dock.",
 "https://www.champagnelogistics.com/contact-us/","2026-10-16"),
(2,"Copper Peak Logistics","Santa Rosa, CA","Scott Groene","Operations (since 2007)","sgroene@copperpeaklogistics.com","P","https://copperpeaklogistics.com/team/",
 "Fulfillment for a hard product",
 "You've run operations at Copper Peak since 2007, fulfilling a product with real handling constraints where most 3PLs would struggle.",
 "https://copperpeaklogistics.com/team/","2026-10-16"),
(2,"Axcess Point","Mount Olive, NJ","Bob Olsen","Operations","rolsen@axcess-point.com","P","https://www.axcess-point.com/our-team",
 "The Mount Olive floor",
 "You run operations at Axcess Point out of Clark Drive in Mount Olive, close enough to the floor to put your own name on it.",
 "https://www.axcess-point.com/our-team","2026-10-16"),
(2,"DFW Distribution","Dallas, TX","Joe Roppolo","Owner","joe@dfwdistribution.com","P","https://www.dfwdistribution.com/about/",
 "Running a family dock",
 "You and Jessica run DFW Distribution as a family operation, close enough to the floor that both your names are on the about page.",
 "https://www.dfwdistribution.com/about/","2026-10-16"),
(2,"IS Fulfillment","Springfield, MO","Dan Williams","Co-Owner","dan@isfulfillment.com","P","https://isfulfillment.com/contact/",
 "The Springfield floor",
 "You co-own IS Fulfillment and run the floor on Nias Avenue in Springfield, small enough that the owner still reads the dock.",
 "https://isfulfillment.com/contact/","2026-10-16"),

# ---------------- Segment 3: Regional parcel / courier / last-mile operators ----------------
(3,"Davis Delivery Service","Buford, GA","Chad Davis","Owner","ryan@davisdeliveryservice.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=749868",
 "LTL final mile out of Buford",
 "You run Davis Delivery as a 65-truck LTL and final-mile operation out of Buford, and refreshed your federal filing in September as you add drivers.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=749868","2026-09-24"),
(3,"Mashburn Delivery Service","Duluth, GA","Adam Weaver","CEO","adam@mashburndelivery.com","P","https://mashburndelivery.com/about/",
 "Four docks, Atlanta to Denver",
 "You run Mashburn's appliance delivery and install across four locations now, Atlanta, Nashville, Birmingham and a Denver-area dock in Aurora.",
 "https://mashburndelivery.com/about/","2026-10-16"),
(3,"Priority Courier Experts","Vadnais Heights, MN","Joshua Smith","Owner","JOSHUA.SMITH@PRIORITY.COM","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=699924",
 "163 trucks across the Twin Cities",
 "You run Priority as a 163-truck on-demand courier operation out of Vadnais Heights, and refreshed your federal filing this April.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=699924","2026-04-03"),
(3,"SurePoint Couriers","Orion, MI","Matthew Lively","Owner","matthew.lively@surepointcouriers.com","P","https://surepointcouriers.com",
 "Scaling a 1099 fleet nationwide",
 "You're scaling SurePoint's 1099 same-day driver network nationwide, and your latest federal filing this September already lists 400 drivers.",
 "https://surepointcouriers.com","2026-09-26"),
(3,"The Last Mile Company","Castle Pines, CO","Ben Lockett","Owner","ben@thelastmileco.com","P","https://thelastmileco.com/what-we-do",
 "Ecommerce last mile",
 "You run The Last Mile Company on ecommerce home delivery, a 56-truck operation you refreshed with FMCSA at the end of September.",
 "https://thelastmileco.com/what-we-do","2026-09-29"),
(3,"Elite Express (Finster Courier)","Pennsauken, NJ","Robert Dinyon","Owner","bdinyon@shipeliteexpress.com","P","https://shipeliteexpress.com",
 "LTL and expedited out of Pennsauken",
 "You run Elite Express as a 199-truck LTL, truckload and expedited operation out of Pennsauken, nearly 14 million fleet miles last year.",
 "https://shipeliteexpress.com","2026-10-16"),
(3,"JM Parcel Service","Salem, MA","Monique Jones","Owner","jjones@jmparcelservice.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=4041895",
 "Drivers out of Salem",
 "You run JM Parcel with 80 drivers off a 30-truck base out of Salem, and refreshed your federal filing just this month.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=4041895","2026-10-09"),
(3,"Metro Parcel & Freight","Sterling Heights, MI","Michael Webster","Owner","mwebster@metroparcelfreight.com","P","https://metroparcelfreight.com",
 "44 trucks out of Sterling Heights",
 "You run Metro Parcel as a 44-truck dedicated and cross-border operation out of Sterling Heights, refreshed with FMCSA this April.",
 "https://metroparcelfreight.com","2026-04-14"),
(3,"Peak Delivery Services","Colorado Springs, CO","Brian Baugh","Owner","brianbaugh@peakdelivery.co","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=3307152",
 "Last mile out of Colorado Springs",
 "You run Peak Delivery out of Colorado Springs and refreshed your federal carrier filing this May as the route count grew.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=3307152","2026-05-11"),
(3,"Zip Delivery Services","Tucson, AZ","Cecil Graves","Owner","cecil@zipdeliveryservices.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=4151097",
 "100 trucks out of Tucson",
 "You run Zip as a 100-truck same-day operation out of Tucson, a filing you refreshed with FMCSA this May.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=4151097","2026-05-08"),
(3,"TruckCourier (28Freight)","Wilmington, MA","Richard Marks","Owner","richard.marks@truckcourier.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=542502",
 "Same-day rush out of Wilmington",
 "You run TruckCourier as a 44-truck same-day rush operation out of Wilmington, available around the clock, refreshed with FMCSA this March.",
 "https://www.truckcourier.com/contact-us/","2026-03-26"),
(3,"MC Delivery","Tacoma, WA","Andrew Laycock","Owner","slaycock-webb@mcdelivery.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=8298",
 "Delivery since 1928",
 "You run MC Delivery out of Tacoma, a document, package and LTL operation your family has run since 1928, refreshed with FMCSA this April.",
 "https://www.mcdelivery.com","2026-04-13"),
(3,"Unique Delivery Service","Lombard, IL","Angelica Mar","Owner","amar@uniquedelivery.com","F","https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=969709",
 "84 trucks out of Lombard",
 "You run Unique Delivery as an 84-truck operation out of Lombard, and refreshed your federal filing this September.",
 "https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=USDOT&query_string=969709","2026-09-14"),
(3,"Diverse Logistics","Tampa, FL","Dennis Ivey","President, Delivery Operations","divey@diverselogistics.com","P","https://diverselogistics.com/leadership/",
 "Your Fort Myers cross-dock",
 "You've got a Warehouse Lead open at the Fort Myers cross-dock, running inbound and outbound for your big-and-bulky final-mile network.",
 "https://www.linkedin.com/jobs/view/warehouse-lead-at-diverse-logistics-and-distribution-llc-4477941091","2026-10-12"),
(3,"Blue Sky Couriers","Memphis, TN","Rick Hechinger","Owner","deliver@blueskycouriers.com","P","https://blueskycouriers.com",
 "Couriers across the mid-South",
 "You run Blue Sky as a courier network across Memphis, Nashville, Chattanooga, Knoxville, Huntsville and Myrtle Beach, each with its own dispatch line.",
 "https://blueskycouriers.com","2026-10-16"),
(3,"US Cargo & Courier","Columbus, OH","Robert Grieser","Operations (named branch contact)","rgrieser@us-cargo.com","P","https://www.us-cargo.com/contact/",
 "Eight terminals across the Midwest",
 "You run US Cargo as a regional LTL and courier network with your own named contact at each terminal, Cincinnati to Cleveland to Pittsburgh.",
 "https://www.us-cargo.com/contact/","2026-10-16"),
(3,"Accurate Courier Express","North Chesterfield, VA","Kevin Russell","Owner","kevin@accuratecourierexpress.com","P","https://accuratecourierexpress.com",
 "35 trucks out of Richmond",
 "You run Accurate Courier Express as a 35-truck same-day operation out of the Richmond area.",
 "https://accuratecourierexpress.com","2026-10-16"),
]


def body(person, opener):
    first = person.split()[0]
    return f"""Hi {first},

{opener}

I was formerly a researcher in Amazon transportation and fulfilment. These are some of the things I worked on:

- Container fullness: knowing a chute or container is full before someone walks over to check it.
- Package dwell: where parcels sit idle between scans, and why.
- Freight cost: empty miles on truckload tours.
- Labor balancing: moving people to where the work is, hour by hour.
- Dock-door staffing: directing associates to the outbound doors that need them, when they need them.

Ask me anything, I do consulting.

Best,
Aidan Jude
{LINKEDIN}
{SUBSTACK}
"""


def slugify(company):
    s = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-")
    return s[:48]


def main():
    base = os.path.join(os.path.dirname(__file__), "..", "outreach", "round1")
    draft_dir = os.path.join(base, "drafts")
    os.makedirs(draft_dir, exist_ok=True)
    seen = set()
    rows = []
    for (seg, co, city, person, title, email, method, esrc, subj, opener, osrc, odate) in R:
        slug = slugify(co)
        assert slug not in seen, slug
        seen.add(slug)
        meth = "published" if method == "P" else "FMCSA-filed"
        rows.append(dict(segment=seg, company=co, city_state=city, person=person, title=title,
                         email=email, email_method=meth, email_source_url=esrc,
                         subject=subj, opener_fact=opener, opener_source_url=osrc,
                         opener_date=odate, draft_file=f"drafts/{slug}.txt"))
        with open(os.path.join(draft_dir, f"{slug}.txt"), "w") as f:
            f.write(f"DRAFT - NOT SENT. Contacting a human is Aidan's gate; he reads every draft first.\n")
            f.write(f"To: {person}, {title}\n{co} - {city}\n{email}  ({meth}: {esrc})\n")
            f.write(f"Subject: {subj}\n\n")
            f.write(body(person, opener))
    cols = ["segment", "company", "city_state", "person", "title", "email", "email_method",
            "email_source_url", "subject", "opener_fact", "opener_source_url", "opener_date", "draft_file"]
    with open(os.path.join(base, "recipients.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    from collections import Counter
    seg = Counter(r["segment"] for r in rows)
    meth = Counter(r["email_method"] for r in rows)
    print(f"rows={len(rows)}  by segment={dict(seg)}  by method={dict(meth)}")


if __name__ == "__main__":
    main()
