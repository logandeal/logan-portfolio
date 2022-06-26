#!/bin/bash

id=$(curl -s --request POST http://localhost:5000/api/timeline_post -d 'name=Logan&email=logan.deal27@gmail.com&content=Test' | jq '.id')

curl http://localhost:5000/api/timeline_post/$id

curl -X DELETE http://localhost:5000/api/timeline_post/$id
