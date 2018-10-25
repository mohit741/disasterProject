from bs4 import BeautifulSoup
import json

states = ['West Bengal', 'Tamil Nadu', 'Uttar Pradesh', 'Rajasthan', 'Kerala', 'Maharashtra', 'Madhya Pradesh',
          'Karnataka', 'Jammu & Kashmir', 'Himachal Pradesh']

for state in states:
    print(state)
    f = open(state + '.html')
    soup = BeautifulSoup(f.read(), 'html.parser')
    l = soup.find('select').find_all('option')
    res = list()
    k = 0
    for i in l:
        res.append(
            {
                'code': k,
                'name': i.text.strip()
            }
        )
        k += 1
    json.dump(res, open(state + '.json', 'w'))
