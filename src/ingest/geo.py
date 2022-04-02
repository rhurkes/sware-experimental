# import geopandas
# myshpfile = geopandas.read_file('citiesx010g.shp')
# myshpfile.to_file('cities.geojson', driver='GeoJSON')

def trunc(value):
    return float('%.4f' % value)

import json
# with open('cities.json', 'w') as w:
#     with open('cities.geojson', 'r') as r:
#         for line in r.readlines():
#             line = line.strip()
#             line = json.loads(line)
#             line = line['properties']
#             if line['POP_2010'] < 1:
#                 continue
#             data = [trunc(line['LONGITUDE']), trunc(line['LATITUDE']), line['NAME'], line['STATE']]
#             w.write(f'{json.dumps(data)}\n')

with open('no-pop-cities.json', 'w') as w:
    with open('cities.geojson', 'r') as r:
        for line in r.readlines():
            line = line.strip()
            line = json.loads(line)
            line = line['properties']
            if line['POP_2010'] > 0:
                continue
            data = [trunc(line['LONGITUDE']), trunc(line['LATITUDE']), line['NAME'], line['STATE']]
            w.write(f'{json.dumps(data)}\n')