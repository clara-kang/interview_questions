# interview_questions

Question3

Design:
- a GeoLRUCache has the basic functionalities of a LRU cache
- have an array of GeoLRUCache of different Geolocations, make it accessible to each GeoLRUCache
- for data consistency, once a GeoLRUCache notices a different between the content of its cached page and the input page, it notifies all the GeoLRUCaches
- for network resiliency, make get and put operations atomic, tie the access to cache data inside the two functions together
- for read time write to a different GeoLRUCache, for each entry in the map, call the other GeoLRUCache's put operation, if there are get requests while writing, process get requests first. If there are put request during writing, cache the request, process it after writing is finished, this ensures that the new get is not overwritten by old information

Missing functionalities: 
- data consistency across regions
