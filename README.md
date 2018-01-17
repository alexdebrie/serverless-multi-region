## Usage (WIP)

1. Change the `domainName` and `certificateName` values in the `custom` block of `serverless.yml` to match your actual domain:

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
	$ curl -X POST https://<apiGatewaydomain>/dev/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in US West:
	
	```bash
	$ curl -X GET https://<apiGatewaydomain>/dev/mytestkey
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
	$ curl -X POST https://<us-west-2-domain>/dev/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in US West:
	
	```bash
	$ curl -X GET https://<eu-central-1-domain>/dev/mytestkey
{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```

10. Set up the Route53 Latency records:

	```bash
	$ bash set-record-sets.sh
	```
	
11. Curl your key:

	```bash
	$ curl -X GET https://<yourActualDomain>/mytestkey
{"key": "mytestkey", "value": "my value", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```
	
	💥