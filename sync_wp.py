import requests
import json
import re

cookies = {
    'wordpress_sec_b5f38c64090b85f3b9b188c3ce0366cf': 'irza%7C1793773908%7CmZbLjuMMtoDCJk99F10TS2H6RYTb5vy93TSFgFAW4FZ%7C5a694199b6c5a5330890aff6dae6eb75cfca322963f84f442650223170f3088a',
    'wordpress_logged_in_b5f38c64090b85f3b9b188c3ce0366cf': 'irza%7C1793773908%7CmZbLjuMMtoDCJk99F10TS2H6RYTb5vy93TSFgFAW4FZ%7C093aba4c8d4eff33fd253f6b63f1a04c19fd714a052519c45d083ed12675f19c',
}

headers = {
    'X-WP-Nonce': 'b6478f2434',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/json'
}

def extract_body(file_path):
    with open(file_path, encoding='utf-8') as f:
        content = f.read()
    match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return content.strip()

# 1. Update Page 15 (Home)
print('--- Updating Page 15 (Home) ---')
res = requests.get('https://yometapp.com/wp-json/wp/v2/pages/15?context=edit', cookies=cookies, headers=headers)
p15 = json.loads(res.json()['meta']['_elementor_data'])
index_body = extract_body('index.html')
p15[0]['elements'][0]['elements'][0]['settings']['html'] = index_body
update_res = requests.post(
    'https://yometapp.com/wp-json/wp/v2/pages/15',
    cookies=cookies,
    headers=headers,
    json={'meta': {'_elementor_data': json.dumps(p15)}}
)
print('Page 15 update status:', update_res.status_code)
if update_res.status_code == 200:
    saved = json.loads(update_res.json()['meta']['_elementor_data'])
    saved_html = saved[0]['elements'][0]['elements'][0]['settings']['html']
    print('Page 15 saved length:', len(saved_html), 'Has as with an:', 'as with an' in saved_html)
else:
    print('Page 15 error:', update_res.text[:300])

# 2. Update Page 2568 (Host)
print('\n--- Updating Page 2568 (Host) ---')
res = requests.get('https://yometapp.com/wp-json/wp/v2/pages/2568?context=edit', cookies=cookies, headers=headers)
p2568 = json.loads(res.json()['meta']['_elementor_data'])
host_body = extract_body('host.html')
p2568[0]['elements'][0]['elements'][0]['settings']['html'] = host_body
update_res = requests.post(
    'https://yometapp.com/wp-json/wp/v2/pages/2568',
    cookies=cookies,
    headers=headers,
    json={'meta': {'_elementor_data': json.dumps(p2568)}}
)
print('Page 2568 update status:', update_res.status_code)
if update_res.status_code == 200:
    saved = json.loads(update_res.json()['meta']['_elementor_data'])
    saved_html = saved[0]['elements'][0]['elements'][0]['settings']['html']
    print('Page 2568 saved length:', len(saved_html), 'Has how-to-apply:', 'how-to-apply' in saved_html)
else:
    print('Page 2568 error:', update_res.text[:300])

# 3. Update Elementor Default Kit (ID 5) Custom CSS
print('\n--- Updating Elementor Default Kit ID 5 ---')
with open('style.css', encoding='utf-8') as f:
    style_css = f.read()

res = requests.get('https://yometapp.com/wp-json/wp/v2/elementor_library/5?context=edit', cookies=cookies, headers=headers)
kit_meta = res.json()['meta']
page_settings = kit_meta.get('_elementor_page_settings', {})
if isinstance(page_settings, str):
    page_settings = json.loads(page_settings)
page_settings['custom_css'] = style_css

update_res = requests.post(
    'https://yometapp.com/wp-json/wp/v2/elementor_library/5',
    cookies=cookies,
    headers=headers,
    json={'meta': {'_elementor_page_settings': json.dumps(page_settings)}}
)
print('Kit 5 update status:', update_res.status_code)
if update_res.status_code == 200:
    saved = update_res.json()['meta']['_elementor_page_settings']
    if isinstance(saved, str):
        saved = json.loads(saved)
    print('Kit 5 custom_css length:', len(saved.get('custom_css', '')))
else:
    print('Kit 5 error:', update_res.text[:300])
