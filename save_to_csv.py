import requests
import csv

morph_api_key = "YOUR API KEY HERE"

output_filename = "output.csv"

morph_api_url = "https://api.morph.io/andylolz/papua_new_guinea_ipa/data.json"

all_tables = ["directors", "shareholders", "secretaries", "data",]
entities = {
  "directors": "Director",
  "shareholders": "Shareholder",
  "secretaries": "Secretary",
}

tables = {}
for table in all_tables:
    print("Fetching from table '{}' ...".format(table))
    r = requests.get(morph_api_url, params={
      'key': morph_api_key,
      'query': "select * from '{table}'".format(table=table)
    })
    tables[table] = r.json()

results = {data["Entity Number"]: data for data in tables["data"]}

print("Flattening tables ...")
for table, entity in entities.items():
    for row in tables[table]:
        prefix = "{}{:02d}".format(entity, row["{} Number".format(entity)])
        d = {"{}{}".format(prefix, k): v for k, v in row.items() if k not in ["{} Number".format(entity), "Entity Number"]}
        results[row["Entity Number"]] = dict(results[row["Entity Number"]].items() + d.items())

results = results.values()

print("Generating csv '{}'".format(output_filename))
fieldnames = set()
for res in results:
    fieldnames |= set(res.keys())

fieldnames = sorted(fieldnames)

with open(output_filename, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for res in results:
        writer.writerow(res)
