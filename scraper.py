import re
import time

import requests
import scraperwiki
from bs4 import BeautifulSoup as bs


companies_url = "https://www.ipa.gov.pg/pngmaster/service/create.html?targetAppCode=pngmaster&targetRegisterAppCode=pngcompanies&service=registerItemSearch&target=pngmaster"
entity_numbers = ["1-13387", "1-18247", "1-634", "1-1211", "1-1522", "1-2105", "1-664", "1-1377", "1-9196", "1-1410", "1-26114", "1-3857", "1-12132", "1-1289", "1-9603", "1-44575", "1-5294", "1-12648", "1-217", "1-8721", "1-2333", "1-21936", "1-16225", "1-12772", "1-9385", "1-2108", "1-68270", "1-63120", "1-64501", "1-55294", "1-18830", "1-14028", "1-8596", "1-2801", "1-50678", "1-11144", "1-3979", "1-106572", "1-14106", "1-27677", "1-20240", "1-2988", "1-5461", "1-11876", "1-6149", "1-23791", "1-4236", "1-109305", "1-2986", "1-2874", "1-780", "1-449", "1-14811", "1-21036", "1-4815", "1-2301", "1-3178", "1-3173", "1-14694", "1-12808", "1-11031", "1-11463", "1-21909", "1-12835", "1-61892", "1-10954", "1-75", "1-72815", "1-62527", "1-1011", "1-2965", "1-65118", "1-1818", "1-1666", "1-1277", "1-822", "1-1302", "1-3263", "1-1895", "1-4360", "1-4149", "1-1069", "1-1750", "1-20843", "1-2185", "1-66700", "1-2389", "1-6453", "1-6260", "1-1360", "1-6328", "1-7803", "1-14588", "1-20696", "1-1628", "1-5605", "1-5391", "1-20977", "1-11575", "1-6454", "1-11251", "1-2403", "1-6276", "1-5587", "1-17197", "1-11601", "1-4767", "1-13392", "1-1279", "1-8129", "1-3639", "1-6480", "1-10973", "1-5373", "1-1164", "1-5195", "1-1299", "1-420", "1-6856", "1-8670", "1-12486", "1-17203", "1-1815", "1-7291", "1-9313", "1-1198", "1-9425", "1-1344", "1-5144", "1-82055", "1-1446", "1-2446", "1-10448", "1-2331", "1-1474", "1-4134", "1-34895", "1-15816", "1-6222", "1-6626", "1-5174", "1-26067", "1-10436", "1-13218", "1-9883", "1-3085", "1-6286", "1-18909", "1-18948", "1-9484", "1-9078", "1-6033", "1-2992", "1-14333", "1-6180", "1-13834", "1-6543", "1-14124", "1-1590", "1-15703", "1-6516", "1-6673", "1-987", "1-12810", "1-179", "1-1125", "1-6160", "1-599", "1-66721", "1-6705", "1-6588", "1-1169", "1-6171", "1-68841", "1-26420", "1-4286", "1-979", "1-6236", "1-2050", "1-24794", "1-69374", "1-72550", "1-9647", "1-68194", "1-84564", "1-6717", "1-1096", "1-26891", "1-16394", "1-16791", "1-11862", "1-13656", "1-64610", "1-14850", "1-70393", "1-72516", "1-69931", "1-702", "1-76732", "1-22140", "1-9145", "1-7234", "1-1352", "1-12423", "1-3318", "1-15306", "1-1180", "1-1448", "1-11767", "1-2670", "1-1315", "1-6352", "1-70613", "1-6349", "1-83402", "1-66507", "1-47889", "1-10276", "1-10112", "1-3425", "1-11869", "1-3545", "1-2402", "1-1325", "1-26443", "1-72297", "1-6843", "1-15995", "1-5322", "1-840", "1-14647", "1-248", "1-4288", "1-3183", "1-83777", "1-46653", "1-109421", "1-14604", "1-3129", "1-6710", "1-11619", "1-427", "1-15523", "1-3940", "1-4855", "1-21503", "1-10989", "1-4389", "1-6247", "1-126", "1-8791", "1-87560", "1-2114", "1-2360", "1-6401", "1-1646", "1-8180", "1-5598", "1-3155", "1-27629", "1-15135", "1-26973", "1-3744", "1-1018", "1-19965", "1-7417", "1-10834", "1-2964", "1-23423", "1-14801", "1-58546", "1-9214", "1-12398", "1-9261", "1-5020", "1-7411", "1-26828", "1-5571", "1-12232", "1-6186", "1-6326", "1-23654", "1-1235", "1-14565", "1-11793", "1-6068", "1-12350", "1-15013", "1-847", "1-6497", "1-7254", "1-79291", "1-1790", "1-15259", "1-464", "1-4053", "1-3929", "1-1878", "1-133", "1-6881", "1-339", "1-7170", "1-12997", "1-8869", "1-3781", "1-11168", "1-4297", "1-6787", "1-5565", "1-9345", "1-8027", "1-5566", "1-3148", "1-11149", "1-11606", "1-15641", "1-18178", "1-7389", "1-5326", "1-9283", "1-6544", "1-9686", "1-5231", "1-14321", "1-1292", "1-11032", "1-5051", "1-1217", "1-7699", "1-735", "1-10351", "1-12047", "1-11779", "1-1879", "1-1880", "1-3786", "1-22342", "1-29221", "1-12412", "1-1287", "1-1145", "1-24646", "1-21840", "1-1144", "1-70469", "1-38471", "1-5574", "1-6538", "1-7692", "1-7680", "1-2238", "1-10387", "1-22935", "1-4446", "1-4447", "1-5143", "1-1917", "1-3659", "1-12805", "1-4116", "1-46031", "1-5057", "1-768", "1-6129", "1-22340", "1-22339", "1-11008", "1-1874", "1-3025", "1-2623", "1-3075", "1-653", "1-1127", "1-3554", "1-1163", "1-6486", "1-455", "1-3193", "1-13385", "1-8734", "1-274", "1-11885", "1-6307", "1-1437", "1-7115", "1-15041", "1-7863", "1-17405", "1-8310", "1-10629", "1-2858", "1-7840", "1-19251", "1-13730", "1-14032", "1-6947", "1-15949", "1-125", "1-7259", "1-6233", "1-8909", "1-15298", "1-3202", "1-1328", "1-5377", "1-26196", "1-16682", "1-3514", "1-6612", "1-565", "1-24748", "1-811", "1-6209", "1-18901", "1-23810", "1-6433", "1-1362", "1-7460", "1-12599", "1-1836", "1-32904", "1-83788", "1-48880", "1-81237", "1-85237", "1-16985", "1-5579", "1-3856", "1-6419", "1-535", "1-857", "1-2388", "1-3356", "1-976", "1-18084", "1-5056", "1-26496", "1-15352", "1-72819", "1-10031", "1-5133", "1-779", "1-1428", "1-9605", "1-534", "1-2276", "1-23440", "1-8158", "1-607", "1-15410", "1-303", "1-6317", "1-397", "1-46339", "1-44680", "1-2134", "1-7123", "1-10888", "1-28845", "1-29909", "1-18122", "1-2309", "1-67757", "1-22341", "1-7299", "1-23623", "1-6547", "1-26888", "1-5137", "1-2643", "1-7521", "1-8153", "1-5612", "1-17778", "1-22905", "1-2605", "1-68198", "1-21920", "1-7824", "1-3865", "1-2876", "1-1907", "1-544", "1-7972", "1-14745", "1-7054", "1-26890", "1-567", "1-2938", "1-3890", "1-7413", "1-3737", "1-12756", "1-7700", "1-1028", "1-1778", "1-2634", "1-15467", "1-28844", "1-2632", "1-58870", "1-2014", "1-3750", "1-7401", "1-6087", "1-6044", "1-12957", "1-8730", "1-7809", "1-9866", "1-61967", "1-59699", "1-64031", "1-3627", "1-17156", "1-2091", "1-1554", "1-14360", "1-74393", "1-247", "1-218", "1-4388", "1-5304", "1-4097", "1-6915", "1-7982", "1-3458", "1-8476", "1-9", "1-40", "1-1770", "1-898", "1-36374", "1-5029", "1-4843", "1-3595", "1-6353", "1-7217", "1-73439", "1-1690", "1-10049", "1-1222", "1-286", "1-1928", "1-1923", "1-45088", "1-6273", "1-26889", "1-3024", "1-47", "1-2621", "1-1906", "1-2036", "1-6203", "1-3049", "1-675", "1-668", "1-8765", "1-6733", "1-5705", "1-2298", "1-16395", "1-883", "1-4847", "1-7280", "1-33", "1-1867", "1-812", "1-2746", "1-69883", "1-70788", "1-70147", "1-22269", "1-1243", "1-2793", "1-8644", "1-16208", "1-746", "1-8224", "1-12229", "1-47273", "1-55155", "1-79375", "1-4656", "1-12019", "1-176", "1-1361", "1-191", "1-55436", "1-5595", "1-738", "1-89200", "1-8026", "1-8025", "1-6552", "1-6540", "1-5253", "1-930", "1-68088", "1-6140", "1-759", "1-3813", "1-84038", "1-7360", "1-6498", "1-5295", "1-17067", "1-15282", "1-7237", "1-146", "1-6421", "1-6147", "1-14614", "1-21919", "1-8766", "1-46654", "1-7305", "1-2839", "1-48529", "1-22885", "1-45843", "1-81189", "1-76516", "1-81486", "1-10536", "1-42185", "1-81735", "1-32976", "1-51635", "1-59396", "1-20533", "1-61811", "1-79165", "1-1669", "1-20756", "1-74602", "1-6212", "1-9494", "1-8472", "1-3391", "1-108384", "1-14047", "1-26664", "1-45831", "1-3068", "1-49260", "1-100490", "1-81747", "1-57060", "1-9351", "1-36325", "1-47502", "1-85688", "1-66655", "1-51142", "1-73187", "1-7663", "1-82330", "1-52280", "1-7113", "1-7804", "1-44506", "1-65341", "1-7934", "1-53924", "1-11696", "1-30592", "1-51352", "1-47501", "1-11863", "1-41531", "1-6785", "1-6741", "1-61970", "1-55163", "1-100512", "1-75866", "1-13284", "1-47132", "1-5282", "1-63819", "1-70799", "1-8342", "1-109983", "1-26953", "1-49372", "1-13153", "1-26742", "1-75759", "1-12472", "1-10670", "1-31737", "1-16907", "1-23180", "1-22109", "1-33132", "1-13622", "1-12601", "1-9899", "1-20895", "1-2038", "1-68138", "1-21006", "1-1223", "1-6184", "1-1035", "1-14813",]

def exec_request(*args, **kwargs):
    while True:
        try:
            r = requests.request(*args, **kwargs)
            time.sleep(0.5)
            break
        except Exception:
            print("Error: Request failed. Retrying ...")
            time.sleep(2)
    return r

# Get a cookie and the redirect URL
def get_redirect_and_cookie(companies_url):
    r = exec_request("get", companies_url, allow_redirects=False)
    cookies = r.cookies
    url = r.headers['location']
    return url, cookies

def get_fragment_id(html):
    return re.search(r"guid:(\d+),", html).group(1)

# Get the form
def get_payload_and_post_url(url, cookies):
    r = exec_request("get", url, cookies=cookies)
    html = r.text
    soup = bs(html, "html.parser")
    payload = {
      "_CBHTMLFRAG_": "true",
      "_CBNAME_": "buttonPush",
      "_CBASYNCUPDATE_": "true",
      "SourceAppCode": "pngcompanies",

      "_CBHTMLFRAGNODEID_": soup.find(class_='appRecordGraphIndexNodes')['id'][4:],
      "_CBNODE_": soup.find(class_='appSubmitButton')['id'][4:],
      soup.find_all('form')[1].find_all('input')[2]['id']: "N",

      "_VIKEY_": re.search(r"viewInstanceKey:\'([^\']*)\'", html).group(1),
      "_CBHTMLFRAGID_": get_fragment_id(html),
    }
    url = soup.find_all('form')[1]['action']
    return payload, url

# Run the actual query
def run_query(query, url, cookies, payload):
    payload["QueryString"] = query
    r = exec_request(
        "post",
        url,
        data=payload,
        cookies=cookies,
    )
    return bs(r.text, "html.parser")

def find_by_id(id_, soup):
    sec_soup = soup.find(id=id_)
    if not sec_soup:
        return ""
    return sec_soup.find(class_="appAttrValue").text.strip()

def find_by_label(label, soup):
    label_soup = soup.find(class_="appLabelText", text=re.compile(label))
    if not label_soup:
        return ""
    attr_soup = label_soup.find_parent(class_="appAttribute")
    if not attr_soup:
        return ""
    return attr_soup.find(class_="appAttrValue").text.strip()

def get_general_details(entity_number, cb_node, payload):
    p = {
        "QueryString": entity_number,
        "SourceAppCode": "pngcompanies",
        "_CBNAME_": "invokeMenuCb",
        "_CBNODE_": cb_node,
        "_CBVALUE_": "",
        "_VIKEY_": payload["_VIKEY_"],
        "_scrollTop": "525",
        [x for x in payload.keys() if x.endswith('Advanced')][0]: "N",
    }
    r = exec_request("post", url, data=p, cookies=cookies)
    soup = bs(r.text, "html.parser")
    details = {
        "Entity Name": find_by_id("Entities[0]/EntityNames[0]/ATTRIBUTE/Name", soup),
        "Status": find_by_id("Entities[0]/ATTRIBUTE/Status", soup),
        "CoStart": find_by_id("Entities[0]/ATTRIBUTE/RegistrationDate", soup),
        "CoDate": find_by_id("Entities[0]/ATTRIBUTE/DeregistrationDate", soup),
        "Main Business Sector": find_by_id("Entities[0]/ATTRIBUTE/BusinessSectorCode", soup),
        "Applicant": find_by_id("Entities[0]/ContactRole[0]", soup),
    }
    if details["Applicant"].lower() == "not supplied":
        details["Applicant"] = ""
    else:
        details["Applicant"] = find_by_id("Entities[0]/ContactRole[0]/EntityRolePostalAddresses[0]", soup)
    prev_name_count = 0
    name_history_soup = soup.find(class_="brViewLocalCompany-tabsBox-detailsTab-details-historicalInformationBox-nameHistoryBox")
    if name_history_soup:
        while True:
            key = "Prev Name{:02d}".format(prev_name_count + 1)
            prev_name = find_by_id("Entities[0]/EntityNames[{}]/ATTRIBUTE/Name".format(prev_name_count), name_history_soup)
            if prev_name == "":
                break
            details[key] = prev_name
            prev_name_count += 1
    return details, r.text, r.url

def get_tab_contents(tab_url, tab_index, tab_payload, cookies):
    tab_payload["_CBVALUE_"] = tab_index
    r = exec_request("post", tab_url, data=tab_payload, cookies=cookies)
    return bs(r.text, "html.parser")

def get_address_details(tab_url, tab_payload, cookies, details):
    soup = get_tab_contents(tab_url, 1, tab_payload, cookies)
    prefixes = {
        "RO": "EntityPhysicalAddresses",
        "PO": "EntityPostalAddresses",
    }
    for prefix, id_name in prefixes.items():
        prev_address_count = 0
        while True:
            key = "{}{:02d}Address".format(prefix, prev_address_count + 1)
            address_soup = soup.find(id="Entities[0]/{}[{}]".format(id_name, prev_address_count))
            if not address_soup:
                break
            details[key] = address_soup.find(class_="appSingleLine").find(class_="appAttrValue").text.strip()
            details["{}{:02d}Start".format(prefix, prev_address_count + 1)] = find_by_id("Entities[0]/{}[{}]/ATTRIBUTE/StartDate".format(id_name, prev_address_count), address_soup)
            details["{}{:02d}End".format(prefix, prev_address_count + 1)] = find_by_id("Entities[0]/{}[{}]/ATTRIBUTE/EndDate".format(id_name, prev_address_count), address_soup)
            prev_address_count += 1
    return details

def get_director_details(tab_url, tab_payload, cookies, entity_number):
    soup = get_tab_contents(tab_url, 2, tab_payload, cookies)
    director_count = 0
    while True:
        data = {}
        data["Entity Number"] = entity_number
        data["Director Number"] = director_count + 1

        director_name = find_by_id("Entities[0]/Directors[{}]".format(director_count), soup)
        if director_name == "":
            break
        data["Name"] = director_name
        data["Residential Address"] = find_by_id("Entities[0]/Directors[{}]/EntityRolePhysicalAddresses[0]".format(director_count), soup)
        data["Postal Address"] = find_by_id("Entities[0]/Directors[{}]/EntityRolePostalAddresses[0]".format(director_count), soup)
        data["Nationality"] = find_by_id("Entities[0]/Directors[{}]/ATTRIBUTE/RoleCountryCode".format(director_count), soup)
        data["Start"] = find_by_id("Entities[0]/Directors[{}]/ATTRIBUTE/AppointedDate".format(director_count), soup)
        data["End"] = find_by_id("Entities[0]/Directors[{}]/ATTRIBUTE/CeasedDate".format(director_count), soup)
        director_count += 1

        scraperwiki.sqlite.save(unique_keys=['Entity Number', 'Director Number'], data=data, table_name="directors")

def get_shareholder_details(tab_url, tab_payload, cookies, details, entity_number):
    soup = get_tab_contents(tab_url, 3, tab_payload, cookies)
    details["Total Shares"] = find_by_id("Entities[0]/ATTRIBUTE/TotalShares", soup)
    shareholder_count = 0
    for shareholder_soup in soup.find_all(class_="appDialogRepeaterRowContent"):
        data = {}
        data["Entity Number"] = entity_number
        data["Shareholder Number"] = shareholder_count + 1

        data["Name"] = find_by_label(' Name', shareholder_soup)
        data["Address"] = find_by_label('Residential or Registered Office Address', shareholder_soup)
        data["PostalAddress"] = find_by_label('Postal Address', shareholder_soup)
        data["Place of Incorporation"] = find_by_label('Place of Incorporation', shareholder_soup)
        data["Start"] = find_by_label('Appointed', shareholder_soup)
        data["End"] = find_by_label('Ceased', shareholder_soup)

        scraperwiki.sqlite.save(unique_keys=['Entity Number', 'Shareholder Number'], data=data, table_name="shareholders")

        shareholder_count += 1
    return details

def get_secretary_details(tab_url, tab_payload, cookies, entity_number):
    soup = get_tab_contents(tab_url, 3, tab_payload, cookies)
    secretary_count = 0
    for shareholder_soup in soup.find_all(class_="appDialogRepeaterRowContent"):
        data = {}
        data["Entity Number"] = entity_number
        data["Secretary Number"] = secretary_count + 1

        data["Name"] = find_by_label('Name', shareholder_soup)
        data["Address"] = find_by_label('Residential Address', shareholder_soup)
        data["PostalAddress"] = find_by_label('Postal Address', shareholder_soup)
        data["Nationality"] = find_by_label('Nationality', shareholder_soup)
        data["Start"] = find_by_label('Appointed Date', shareholder_soup)
        data["End"] = find_by_label('Ceased', shareholder_soup)

        scraperwiki.sqlite.save(unique_keys=['Entity Number', 'Secretary Number'], data=data, table_name="secretaries")

        secretary_count += 1

print("Doing setup stuff ...")
url, cookies = get_redirect_and_cookie(companies_url)
payload, url = get_payload_and_post_url(url, cookies)
for entity_number in entity_numbers:
    print("Searching for '{}'".format(entity_number))
    soup = run_query(entity_number, url, cookies, payload)
    link_soup = soup.find(class_="appRepeaterContent").find(class_="appReceiveFocus", text=re.compile('\(' + entity_number + '\)$'))
    if not link_soup:
        print("Hmm... No results found for entity '{}'".format(entity_number))
        continue
    link_soup = link_soup.parent
    cb_node = link_soup["id"][4:]
    print("Fetching general details ...")
    details, html, redirect_url = get_general_details(entity_number, cb_node, payload)
    details["Entity Number"] = entity_number
    # construct the new URL
    id_ = re.search(r'\?id=([^&]+)&|$', redirect_url).group(1)
    tab_url = "https://www.ipa.gov.pg/pngcompanies/viewInstance/update.html?id={}".format(id_)
    # get some other bits we need
    tab_payload = {
        "_CBHTMLFRAG_": "true",
        "_CBNAME_": "tabSelect",
        "_CBASYNCUPDATE_": "true",
        "_VIKEY_": payload["_VIKEY_"],
        "_CBNODE_": bs(html, "html.parser").find(class_="appTabs")["id"][4:],
        "_CBHTMLFRAGID_": get_fragment_id(html),
    }
    print("Fetching address details ...")
    details = get_address_details(tab_url, tab_payload, cookies, details)
    print("Fetching director details ...")
    get_director_details(tab_url, tab_payload, cookies, entity_number)
    print("Fetching shareholder details ...")
    details = get_shareholder_details(tab_url, tab_payload, cookies, details, entity_number)
    print("Fetching secretary details ...")
    get_secretary_details(tab_url, tab_payload, cookies, entity_number)

    scraperwiki.sqlite.save(unique_keys=['Entity Number'], data=details, table_name="data")
