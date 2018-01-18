## Usage (WIP)

0. Remember to `npm install` and `pip install awscli [--upgrade]` (at least version `1.14.24`)

1. Change the `domainName` value in the `custom` block of `serverless.yml` to match your actual domain:

    ```
    custom:
      customDomain:
        domainName: keyvalue.<mydomain>.com
        endpointType: 'regional'
        certificateRegion: ${opt:region}
        createRoute53Record: false
      tableName: "keyvalues"
    ```
    
2. Create `keyvalue.<mydomain>.com` certificates in ACM **in both us-west-2 and eu-central-1.**

3. Create the custom domains for both regions:

    ```bash
    $ sls create_domain --region us-west-2
    Serverless: 'keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    $ sls create_domain --region eu-central-1
    Serverless: 'keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    ```
    
4. Deploy your service in `us-west-2`:

	```bash
	$ sls deploy --region us-west-2
	...<deploy output> ...
	```

5. Test it!

	Set a key in US West:
	
	```bash
	$ US_ENDPOINT=$(aws cloudformation describe-stacks --stack-name ${STACKNAME} --region us-west-2 --query 'Stacks[0].Outputs[?OutputKey==`ServiceEndpoint`].OutputValue' --output text)
	$ curl $US_ENDPOINT/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in US West:
	
	```bash
	$ curl $US_ENDPOINT/mytestkey
	{"key": "mytestkey", "value": "Just testing", "writeRegion": "us-west-2", "readRegion": "us-west-2"}
	```
	
6. Deploy to `eu-central-1`:

	```bash
	$ sls deploy --region eu-central-1
	...<deploy output> ...
	```

7. Clean out your initial table:

	```bash
	$ bash clean-table.sh
	```
	
8. Create your global table:

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

9. Test it out!

	Set a key in US West:
	
	```bash
	$ curl $US_ENDPOINT/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in US West:
	
	```bash
	EU_ENDPOINT=$(aws cloudformation describe-stacks --stack-name ${STACKNAME} --region eu-central-1 --query 'Stacks[0].Outputs[?OutputKey==`ServiceEndpoint`].OutputValue' --output text)
	$ curl $EU_ENDPOINT/mytestkey
	{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```

10. Set up the Route53 Latency records (don't forget to open the file and configure your domain and subdomain):

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
	
11. Curl your key:

	```bash
	$ curl https://<yourActualDomain>/mytestkey
	{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```
	
	💥