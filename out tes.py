import pandas as pd
import overpy
from nimby import write_to_tsv

api = overpy.Overpass()
query = \
    f"""
    [out:json];
    (area[name="大阪府"];)->.a;
    (node(area.a)[place~"^(neighbourhood|quarter)$"];)->.aa;
    (area[name="大阪市"];)->.b;
    (node(area.b)[place~"^(neighbourhood|quarter)$"];)->.bb;
    (area[name="西区"];)->.c;
    (node(area.b)[place~"^(neighbourhood|quarter)$"];)->.cc;
    node.aa.bb.cc;
    out;
    """

result = api.query(query)
data = []
for node in result.nodes:
    name = node.tags.get("name", '')
    data.append([node.lon, node.lat, name])
print(data)
to_write_col = ['lon', 'lat', 'name']
with open("parks.tsv", "w") as f:
    # 写入头部
    f.write("\t".join(to_write_col) + "\n")
    # 写入数据
    for row in data:
        f.write("\t".join(map(str, row)) + "\n")
