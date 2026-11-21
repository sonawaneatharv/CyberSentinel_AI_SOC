import re

js = open('CyberSentinel_AI_SOC/frontend/js/app.js', encoding='utf-8').read()
html = open('CyberSentinel_AI_SOC/frontend/index.html', encoding='utf-8').read()

ids = set(re.findall(r'getElementById\([\'"](.*?)[\'"]\)', js))
missing = [i for i in ids if ('id="' + i + '"') not in html and ("id='" + i + "'") not in html]

print('Total unique IDs in app.js:', len(ids))
print('Missing IDs in index.html:', missing)
