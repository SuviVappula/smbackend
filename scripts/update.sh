#!/bin/bash

export PYTHONIOENCODING=utf-8
set -e

TIMESTAMP_FORMAT="+%Y-%m-%d %H:%M:%S"
ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ -f $ROOT_PATH/local_update_config ]; then
    $ROOT_PATH/local_update_config
fi

echo ---------------------------------
echo "$(date "$TIMESTAMP_FORMAT") Starting import"
echo ---------------------------------

cd $ROOT_PATH

timeout 20m nice python manage.py services_import_v4 --traceback departments services units entrances 2>&1

timeout 20m nice python manage.py lipas_import --muni-id=92 --muni-id=91 --muni-id=49 --muni-id=235 2>&1

timeout 20m nice python manage.py update_index -a 2 2>&1

timeout 20m nice python manage.py verify_search_index_integrity 2>&1

if [[ -n "${IMPORT_HEALTHCHECK_URL}" ]]; then
  curl --retry 3 "${IMPORT_HEALTHCHECK_URL}"
fi
