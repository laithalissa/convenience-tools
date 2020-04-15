#!/bin/bash
set -e
generate_filter() {
  awk '{ printf "%sfrom:%s",sep,$0; sep=" OR " }'  res/jobsite-emails.txt
}

filter=$(generate_filter)
echo "$filter" | xclip -selection c
echo "The following gmail filter is now on your clipboard:"
echo ""
echo "$filter"
