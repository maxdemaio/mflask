# mflask
My personal website built with Flask

**Main libraries used:**
- Github wrapper
- Redis wrapper
- Flask-Static-Digest

## Github API/Redis 
Overall approach:
- Client makes a request to the backend and immediately respond if we have the information in our Redis cache. We can decide to call the Github API based on if the information has expired from the cache (checking the hash-map).
    - Reason: Reduce API calls

Evicting/Loading data from/into the Redis cache:
- Cache Policy: LRU (update every week)
- Note: Only problem would be that Github has new information, but our cache isn't updated. However, this is okay if we're not too consistent since it isn't sensitive information. The Redis server is run locally for development and Heroku-Redis is used in production. Also, I don't use md5 hashes for my keys since I'm not storing specific profiles, names, etc. that are based upon the request. I only have one single object I'm looking for, my software repositories.

## Flask-Static Digest
