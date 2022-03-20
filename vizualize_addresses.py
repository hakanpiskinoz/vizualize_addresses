from flask import Flask, request,jsonify
app = Flask(__name__)
from sqlalchemy import create_engine
engine = create_engine('postgresql://165.227.163.119:5432/postgres?user=maxinai_user&password=maxinai123_*', isolation_level="AUTOCOMMIT")

@app.route("/addresses")
def addressess():
    sw = request.args.get('sw',"51.81965717678804,-11.962067381231293")
    ne = request.args.get('ne',"56.60417303370079,5.31906738123115")
    zoom = request.args.get('zoom',"2")
    town = request.args.get('town',"KIDSGROVE")
    page = request.args.get('page',"0")
    limit = request.args.get('limit',"20")

    with engine.connect() as conn:
        data=conn.execute("""
                    SELECT a.* FROM (
                        SELECT
                            json_agg(row(longitude,latitude)),
                            town,
                            count(town) as count,
                            AVG(longitude::float) as center_lng,
                            AVG(latitude::float) as center_ltd
                        FROM maxinai.raw_address
                        WHERE valid_flag=true
                        GROUP by town
                        ) as a
                    ORDER BY a.count DESC
                    LIMIT """  + limit + """ OFFSET """ + str(int(page) * int(limit)) + """
                    ;""")

    import json
    return_list = {}

    for data in data.fetchall():

        boundry = data[0]
        box_str = ""
        box = []

        for x in boundry:
            box.append({"lng":x["f1"], "lat":x['f2']})
        town = data[1]
        return_list[town] = {"box":box, "count":data[2], "lng":str(data[3]) ,"lat":str(data[4])}

    return jsonify(return_list)

@app.route("/")
def home():
    sw = request.args.get('sw',"51.81965717678804,-11.962067381231293")
    ne = request.args.get('ne',"56.60417303370079,5.31906738123115")
    zoom = request.args.get('zoom',"2")
    page = request.args.get('page',"0")
    limit = request.args.get('limit',"20")

    with engine.connect() as conn:
        data=conn.execute("""
                    SELECT a.* FROM (
                        SELECT
                            json_agg(row(longitude,latitude)),
                            town,
                            count(town) as count,
                            AVG(longitude::float) as center_lng,
                            AVG(latitude::float) as center_ltd
                        FROM maxinai.raw_address
                        WHERE valid_flag=true
                        GROUP by town
                        ) as a
                    ORDER BY a.count DESC
                    LIMIT """  + limit + """ OFFSET """ + str(int(page) * int(limit)) + """
                    ;""")

    import json
    return_list = {}
    for data in data.fetchall():

        boundry = data[0]
        box_str = ""
        box = []

        for x in boundry:
            box.append({"lng":x["f1"], "lat":x['f2']})
        town = data[1]
        return_list[town] = {"box":box, "count":data[2], "lng":str(data[3]) ,"lat":str(data[4])}

    result_str = ""
    j = 0
    for k,v in return_list.items():
        j = j + 1
        i= str(j)
        result_str = result_str + """
            chicago"""+ i +""": {
            center: { lat: """ + v["lat"] + """, lng: """ + v["lng"] + """ },
            population: """ +  str(v["count"]) +  """,},
            """

    return """
<!DOCTYPE html>
<html>
    <head>
        <title>Simple Map</title>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=default"></script>
        <style>
            /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
            #map {
                height: 100%;
            }

            /* Optional: Makes the sample page fill the window. */
            html,
            body {
                height: 100%;
                margin: 0;
                padding: 0;
            }
        </style>
    </head>
    <body>
        <div id="map"></div>

        <script src="https://maps.googleapis.com/maps/api/js?key=&callback=initMap&v=weekly" async></script>
        <script>
                let map;
                function polygonBounds(polygon) {
                  var bounds = new google.maps.LatLngBounds();
                    for (var i = 0; i < polygon.getPaths().getLength(); i++) {
                        for (var j = 0; j < polygon.getPaths().getAt(i).getLength(); j++) {
                              bounds.extend(polygon.getPaths().getAt(i).getAt(j));
                                  }
                                    }
                                      return bounds;
                                      }

                function initMap() {
                  var southWest = new google.maps.LatLng("""+sw+""");
                  var northEast = new google.maps.LatLng("""+ne+""");
                  var bounds = new google.maps.LatLngBounds(southWest,northEast);
                  map = new google.maps.Map(document.getElementById("map"), {
                  mapTypeId: "roadmap"});
                  map.fitBounds(bounds);
                  map.setZoom(""" + zoom +  """);

            const citymap = {
            """ + result_str + """
            };

              for (const city in citymap) {
                // Add the circle for this city to the map.
                const cityCircle = new google.maps.Circle({
                  strokeColor: "#FF0000",
                  strokeOpacity: 0.8,
                  strokeWeight: 2,
                  fillColor: "#FF0000",
                  fillOpacity: 0.35,
                  map,
                  center: citymap[city].center,
                  radius: Math.sqrt(citymap[city].population) * 500,
                });

            var marker =  new google.maps.Marker({
                position: { lat: citymap[city].center.lat, lng: citymap[city].center.lng },
                map,
                //icon  : "https://chart.apis.google.com/chart?chst=d_map_pin_letter&chld="+citymap[city].population+"|FE6256|000000",
                icon  : "https://chart.googleapis.com/chart?chst=d_map_spin&chld=1%7C0%7CFFC6A5%7C11%7Cb%7C"+citymap[city].population,
              });
              cityCircle.bindTo('center', marker, 'position');}
              }
        </script>
    </body>
</html>
sample.html
"""

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")

