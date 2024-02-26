import config
import datetime
import re


def find_ip_address(text):
    '''Ищем айпи адреса в сообщении регулярным выражением'''
    pattern = r'\b(?:(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.){3}(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\b'
    ip_addresses = re.findall(pattern, text)
    try:
        return ip_addresses[0]
    except:
        return None
def find_domain(text):
    '''Ищем домены в сообщении регулярными выражениями'''
    pattern = r'\b(?:(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?)\b'
    domains = re.findall(pattern, text)
    try:
        return domains[0]
    except:
        return None


def form_text_domain(result, lang):
    error = result.get('error')
    if error:
        if error.get('code') == 'NotFoundError':
            return 'not_found'
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    nofind = result['data']['attributes']['last_analysis_stats']['undetected']
    warn_find = result['data']['attributes']['last_analysis_stats']['suspicious']
    last_scan = result['data']['attributes']['last_analysis_date']
    dt = datetime.datetime.fromtimestamp(last_scan)
    last_scan = dt.strftime('%Y-%m-%d %H:%M:%S')
    domain = result['data']['id']
    try:
        creation_date = result['data']['attributes']['creation_date']
        dt = datetime.datetime.fromtimestamp(creation_date)
        creation_date = dt.strftime('%Y-%m-%d')
    except KeyError:
        creation_date = '-'
    return config.TEXTS['domain'][lang].format(bad_find=bad_find, warn_find=warn_find, nofind=nofind,
                                               domain=domain, last_scan=last_scan, creation_date=creation_date)


def form_text_ip_address(result: dict, lang) -> str:
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    nofind = result['data']['attributes']['last_analysis_stats']['undetected']
    warn_find = result['data']['attributes']['last_analysis_stats']['suspicious']
    try:
        last_scan = result['data']['attributes']['last_analysis_date']
        dt = datetime.datetime.fromtimestamp(last_scan)
        last_scan = dt.strftime('%Y-%m-%d %H:%M:%S')
    except KeyError:
        date = datetime.datetime.now()
        last_scan = date.strftime('%Y-%m-%d %H:%M:%S')
    print(result)
    try:
        country = result['data']['attributes']['country']
        country = config.COUNTRY_CODE[country]
    except KeyError:
        country = "None"
    try:
        network = result['data']['attributes']['network']
    except KeyError:
        network = '-'
    ip_address = result['data']['id']
    return config.TEXTS['ip_address_info'][lang].format(bad_find=bad_find, warn_find=warn_find, nofind=nofind,
                                                        ip_address=ip_address, network=network, country=country,
                                                        last_scan=last_scan)

def form_whois(result: dict, lang) -> str:
    try:
        whois = result['data']['attributes']['whois']
        return config.TEXTS['whois'][lang].format(whois=whois)
    except KeyError:
        return None

def form_text(result: dict, file_name, lang) -> str:
    bad_find = result['data']['attributes']['last_analysis_stats']['malicious']
    nofind = result['data']['attributes']['last_analysis_stats']['undetected']
    warn_find = result['data']['attributes']['last_analysis_stats']['suspicious']

    format_file = result['data']['attributes']['type_description']
    size_file_text = f"{result['data']['attributes']['size']} B"
    size_file = result['data']['attributes']['size']
    if size_file > 1024:
        size_file = round(size_file/1024, 2)
        size_file_text = f"{size_file} KB"
    if size_file > 1024:
        size_file = round(size_file / 1024, 2)
        size_file_text = f"{size_file} MB"
    first_scan = result['data']['attributes']['first_submission_date']
    dt = datetime.datetime.fromtimestamp(first_scan)
    first_scan = dt.strftime('%Y-%m-%d %H:%M:%S')
    try:
        last_scan = result['data']['attributes']['last_analysis_date']
        dt = datetime.datetime.fromtimestamp(last_scan)
        last_scan = dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        last_scan = '-'
    link = f'https://www.virustotal.com/gui/file/{result["data"]["id"]}'
    result_text = config.TEXTS['scan_file_texts']['result_text'][lang].format(bad_find=bad_find, warn_find=warn_find, nofind=nofind, file_name=file_name,
                                                           format_file=format_file, size_file_text=size_file_text, first_scan=first_scan,
                                                           last_scan=last_scan, link=link)
    return result_text

def form_text_antivirus(result:dict, lang):
    antivirus_dict = {'bad':[], 'warn':[], 'nofind':[]}
    for antivirus, values in result['data']['attributes']['last_analysis_results'].items():
        if values['category'] == 'undetected':
            antivirus_dict['nofind'].append(antivirus)

        elif values['category'] == 'malicious':
            antivirus_dict['bad'].append(antivirus)

        elif values['category'] == 'suspicious':
            antivirus_dict['warn'].append(antivirus)
        else:
            continue
    antivirus_text = f"<b>{config.TEXTS['scan_file_texts']['detection'][lang]}</b>\n\n"
    if len(antivirus_dict['bad']) !=0:
        for antivirus in antivirus_dict['bad']:
            antivirus_text += f'❌{antivirus}\n'
    if len(antivirus_dict['warn']) !=0:
        for antivirus in antivirus_dict['warn']:
            antivirus_text += f' ⚠️{antivirus}\n'
    if len(antivirus_dict['nofind']) !=0:
        for antivirus in antivirus_dict['nofind']:
            antivirus_text += f'✅{antivirus}\n'
    type_scan = result['data']['type']
    scan_id = result['data']['id']
    if type_scan == 'domain':
        link = f'https://www.virustotal.com/gui/domain/{scan_id}'
    if type_scan == 'ip_address':
        link = f'https://www.virustotal.com/gui/ip-address/{scan_id}'
    if type_scan == 'file':
        link = f'https://www.virustotal.com/gui/file/{scan_id}'
    antivirus_text += '\n'+config.TEXTS['scan_file_texts']['link'][lang].format(link=link)
    return antivirus_text

def form_text_signature(result:dict, lang):
    result_text = f"<b>{config.TEXTS['scan_file_texts']['signature'][lang]}</b>\n\n"
    for antivirus, values in result['data']['attributes']['last_analysis_results'].items():
        if values['category'] == 'malicious':
            result_text += f'⛔{antivirus}\n' \
                           f'╰<code>{values["result"]}</code>\n\n'
    scan_id = result['data']['id']
    type_scan = result['data']['type']
    if type_scan == 'domain':
        link = f'https://www.virustotal.com/gui/domain/{scan_id}'
    if type_scan == 'ip_address':
        link = f'https://www.virustotal.com/gui/ip-address/{scan_id}'
    if type_scan == 'file':
        link = f'https://www.virustotal.com/gui/file/{scan_id}'

    result_text += '\n' + config.TEXTS['scan_file_texts']['link'][lang].format(link=link)
    return result_text
