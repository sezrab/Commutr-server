earthRadius = 6378100
apiURL = "http://overpass-api.de/api/interpreter"

allowedRetries = 0

wayQueryLine = "way[\"highway\"]({},{},{},{});"

blankRoadQuery = """[out:xml][timeout:25];
// gather results
(
  {}
);
out body;
>;
out skel qt;
"""

roadQuery = """[out:xml][timeout:25];
// gather results
(
  way["highway"](around:{},{},{});
);
out body;
>;
out skel qt;
"""