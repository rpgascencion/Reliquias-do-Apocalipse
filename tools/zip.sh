#!/bin/sh
# gera reliquias-do-apocalipse.zip com a pasta do módulo dentro
cd "$(dirname "$0")/.." && rm -f reliquias-do-apocalipse.zip && mkdir -p /tmp/relzip && rm -rf /tmp/relzip/reliquias-do-apocalipse && mkdir /tmp/relzip/reliquias-do-apocalipse && cp -r module.json README.md scripts styles fonts images packs data /tmp/relzip/reliquias-do-apocalipse/ && (cd /tmp/relzip && zip -qr - reliquias-do-apocalipse) > reliquias-do-apocalipse.zip && ls -la reliquias-do-apocalipse.zip
