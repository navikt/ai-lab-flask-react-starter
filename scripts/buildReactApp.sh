#!/bin/bash
set -e

REACT_APP_DIR=app/static

cd ${REACT_APP_DIR}
npm install
npm run build
cd ${HOME}