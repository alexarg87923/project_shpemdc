#!/bin/bash
docker build -t shpemdc-production .
docker run -p 8000:8000 --rm --name shpemdc-production shpemdc-production