#!/bin/sh
set -e

setup_git() {
  git config --global user.email "travis@travis-ci.org"
  git config --global user.name "Travis CI"
}

commit_website_files() {
  git checkout master
  git add _site/* -f 
  git commit --message "Travis build: $TRAVIS_BUILD_NUMBER [ci skip]"
}

upload_files() {
  git remote add origin-master https://${GH_TOKEN}@github.com/visor-vu/visor-vu.github.io.git
  git push --set-upstream origin-master master
}

setup_git
commit_website_files
upload_files
