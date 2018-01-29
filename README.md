## Usage (WIP)

1. Remember to `npm install` and `pip install awscli [--upgrade]` (at least version `1.14.24`)

2. Create a Route53 Hosted Zone for your domain (if you don't have one already)

3. Change the `domainName` value in the `custom` block of `serverless.yml` to match your actual domain:

    ```
    custom:
      customDomain:
        domainName: keyvalue.<mydomain>.com
        endpointType: 'regional'
        certificateRegion: ${opt:region}
        createRoute53Record: false
      tableName: "keyvalues"
    ```
    
4. Create `keyvalue.<mydomain>.com` certificates in ACM **in both us-west-2 and eu-central-1.** (Oregon and Frankfurt):

```bash
$ aws acm request-certificate --domain-name keyvalue.<mydomain>.com --validation-method EMAIL --region us-west-2
$ aws acm request-certificate --domain-name keyvalue.<mydomain>.com --validation-method EMAIL --region eu-central-1
```

Don't forget to confirm both certificates via email.

5. Create the custom domains for both regions:

    ```bash
    $ sls create_domain --region us-west-2
    Serverless: 'keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    $ sls create_domain --region eu-central-1
    Serverless: 'keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    ```

6. Deploy your service in `us-west-2` (Oregon):

	```bash
	$ sls deploy --region us-west-2
	...<deploy output> ...
	```

7. Test it!

	Set a key in US West:
	
	```bash
	$ US_ENDPOINT=$(aws cloudformation describe-stacks --stack-name serverless-keyvalue-dev --region us-west-2 --query 'Stacks[0].Outputs[?OutputKey==`ServiceEndpoint`].OutputValue' --output text)
	$ curl $US_ENDPOINT/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in Oregon:
	
	```bash
	$ curl $US_ENDPOINT/mytestkey
	{"key": "mytestkey", "value": "Just testing", "writeRegion": "us-west-2", "readRegion": "us-west-2"}
	```
	
8. Deploy to `eu-central-1` (Frankfurt):

	```bash
	$ sls deploy --region eu-central-1
	...<deploy output> ...
	```

9. Clean out your initial table:

	```bash
	$ bash clean-table.sh
	```
	
10. Create your global table:

	```bash
	$ bash create-global-table.sh
	{
	    "GlobalTableDescription": {
	        "GlobalTableStatus": "CREATING",
	        "GlobalTableName": "keyvalues",
	        "ReplicationGroup": [
	            {
	                "RegionName": "us-west-2"
	            },
	            {
	                "RegionName": "eu-central-1"
	            }
	        ],
	        "CreationDateTime": 1516220398.243,
	        "GlobalTableArn": "arn:aws:dynamodb::488110005556:global-table/keyvalues"
	    }
	}
	```

11. Test it out!

	Set a key in Oregon:
	
	```bash
	$ curl $US_ENDPOINT/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in Frankfurt:
	
	```bash
	EU_ENDPOINT=$(aws cloudformation describe-stacks --stack-name serverless-keyvalue-dev --region eu-central-1 --query 'Stacks[0].Outputs[?OutputKey==`ServiceEndpoint`].OutputValue' --output text)
	$ curl $EU_ENDPOINT/mytestkey
	{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```

12. Set up the Route53 Latency records (don't forget to open the script and configure your domain and subdomain):

	```bash
	$ bash set-record-sets.sh
	{
	    "ChangeInfo": {
	        "Status": "PENDING",
	        "Comment": "...",
	        "SubmittedAt": "2018-01-18T11:16:44.979Z",
	        "Id": "/change/C29MDVT401H462"
	    }
	}
	```
	
13. Curl your key:

	```bash
	$ curl https://<yourActualDomain>/mytestkey
	{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```
	
	💥