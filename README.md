## Usage (WIP)

1. Change the `domainName` and `certificateName` values in the `custom` block of `serverless.yml` to match your actual domain:

    ```
    custom:
      customDomain:
        domainName: ${self:provider.region}.keyvalue.<mydomain>.com
        endpointType: 'regional'
        certificateName: "*.keyvalue.<mydomain>.com"
        certificateRegion: ${opt:region}
        createRoute53Record: true
      tableName: "keyvalues"
    ```
    
2. Create `*.keyvalue.<mydomain>.com` certificates in ACM **in both us-west-2 and eu-central-1.**

3. Create the custom domains for both regions:

    ```bash
    $ sls create_domain --region us-west-2
    Serverless: 'us-west-2.keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    $ sls create_domain --region eu-central-1
    Serverless: 'eu-central-1.keyvalue.<mydomain>.com' was created/updated. New domains may take up to 40 minutes to be initialized.
    ```
    
4. Deploy your services:

	```bash
	$ sls deploy --region us-west-2
	...<deploy output> ...
	
	$ sls deploy --region eu-central-1
	...<deploy output> ...
	```

5. Initialize your global table:

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
	        "CreationDateTime": 1516118222.157,
	        "GlobalTableArn": "arn:aws:dynamodb::488110005556:global-table/keyvalues"
	    }
	}
	```

6. Test it!

	Set a key in US West:
	
	```bash
	$ curl -X POST https://us-west-2.keyvalue.serverlessteam.com/mytestkey -d '{"value": "Just testing"}'
	{"key": "mytestkey", "value": "Just testing", "region": "us-west-2"}
	```
	
	Retrieve the key in US West:
	
	```bash
	$ curl -X GET https://us-west-2.keyvalue.serverlessteam.com/mytestkey
	{"key": "mytestkey", "value": "Just testing", "writeRegion": "us-west-2", "readRegion": "us-west-2"}
	```
	
	Retrieve the key in EU Central:
	
	```bash
	$ curl -X GET https://eu-central-1.keyvalue.serverlessteam.com/mytestkey
	{"key": "mytestkey", "value": "Just testing", "writeRegion": "us-west-2", "readRegion": "eu-central-1"}
	```

	💥