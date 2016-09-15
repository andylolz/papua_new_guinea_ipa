import requests
import csv

morph_api_key = "wFTSIH61nwMjLBhphd4T"

output_filename = "output.csv"

morph_api_url = "https://api.morph.io/andylolz/papua_new_guinea_ipa/data.json"

all_tables = ["directors", "shareholders", "secretaries", "data",]
entities = {
  "directors": "Director",
  "shareholders": "Shareholder",
  "secretaries": "Secretary",
}

def gen_fieldnames(key_formats, all_fields):
    fields = []
    count = 1
    while True:
        if key_formats[0].format(count) not in all_fields:
            break
        for key_format in key_formats:
            fields.append(key_format.format(count))
        count += 1
    return fields

tables = {}
for table in all_tables:
    print("Fetching from table '{}' ...".format(table))
    r = requests.get(morph_api_url, params={
      'key': morph_api_key,
      'query': "select * from '{table}'".format(table=table)
    })
    tables[table] = r.json()
    if r.status_code == 401:
        print("morph.io API error: {}".format(tables[table]["error"]))
        exit()

results = {row["Entity Number"]: row for row in tables["data"]}

print("Flattening tables ...")
for table, entity in entities.items():
    for row in tables[table]:
        num = int(row["{} Number".format(entity)])
        prefix = "{}{:03d}".format(entity, num)
        d = {"{}{}".format(prefix, k): v for k, v in row.items() if k not in ["{} Number".format(entity), "Entity Number"]}
        results[row["Entity Number"]] = dict(results[row["Entity Number"]].items() + d.items())

results = results.values()

print("Generating csv '{}'".format(output_filename))
all_fields = set()
for res in results:
    all_fields |= set(res.keys())

fieldnames = ['Entity Number', 'Entity Name', 'Status', 'CoStart', 'CoDate', 'Main Business Sector', 'Applicant', 'ApplicantAddress',]
fieldnames += gen_fieldnames(['Prev Name{:02d}',], all_fields)
fieldnames += gen_fieldnames(['RO{:02d}Address', 'RO{:02d}Start', 'RO{:02d}End',], all_fields)
fieldnames += gen_fieldnames(['PO{:02d}Address', 'PO{:02d}Start', 'PO{:02d}End',], all_fields)
fieldnames += gen_fieldnames(['Director{:03d}Name', 'Director{:03d}Residential Address', 'Director{:03d}Postal Address', 'Director{:03d}Nationality', 'Director{:03d}Start', 'Director{:03d}End',], all_fields)
fieldnames += ['Total Shares']
fieldnames += gen_fieldnames(['Shareholder{:03d}Name', 'Shareholder{:03d}Address', 'Shareholder{:03d}PostalAddress', 'Shareholder{:03d}Place of Incorporation', 'Shareholder{:03d}Start', 'Shareholder{:03d}End',], all_fields)
fieldnames += gen_fieldnames(['Secretary{:03d}Name', 'Secretary{:03d}Address', 'Secretary{:03d}PostalAddress', 'Secretary{:03d}Nationality', 'Secretary{:03d}Start', 'Secretary{:03d}End',], all_fields)

with open(output_filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for res in results:
        writer.writerow(res)
