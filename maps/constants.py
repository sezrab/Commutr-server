earthRadius = 6371
apiURL = "http://overpass-api.de/api/interpreter"

roadQuery = """[out:xml][timeout:25];
// gather results
(
  way["highway"](around:{},{},{});
);
out body;
>;
out skel qt;
"""