# vizualize_addresses
Vizualize addresses on map from csv
- Imported test_adresses.csv in postgres database. (import_data_psql.txt)
- Created Flask app and connected to postgres database (vizualize_addresses.py) 
- Created two types endpoint in flask app on the below:
  1. http://165.227.163.119:5000/
     This endpoint shows that results on map.
  2. http://165.227.163.119:5000/addresses
     This endpoint shows that results like list.
- This endpoints have some default arguments like;
  sw=51.81965717678804,-11.962067381231293 --> south west coordinates
  ne=56.60417303370079,5.31906738123115 --> north east coordinates
  zoom=5.51 --> zoom level
  page=0 --> page number (order by count)
  limit=20 --> bounding box number
- If you use some specific arguments, you can change arguments on this endpoint;
http://165.227.163.119:5000/?sw=51.81965717678804,-11.962067381231293&ne=56.60417303370079,5.31906738123115&zoom=5.51&page=0&limit=20
- API created groups from csv data according to "town" information and return list of this groups on map and also on list. API works for only valid address.
- On the map side; API shows the center of the group and draw circle on the map. API shows that the count of this groups also.
- On the list side; API shows town name, latitude and longitude information of each member of the group, count of the group, center point of the group.
- On this project, addresses group by town name.
