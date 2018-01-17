aws dynamodb scan --table-name keyvalues --region us-west-2 | \
 jq -c '.Items[] | { key } ' |
 tr '\n' '\0' | \
 xargs -0 -n1 -t aws dynamodb delete-item --table-name keyvalues --region us-west-2 --key
