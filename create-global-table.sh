aws dynamodb create-global-table \
    --global-table-name keyvalues \
    --replication-group RegionName=us-west-2 RegionName=eu-central-1 \
    --region us-west-2
