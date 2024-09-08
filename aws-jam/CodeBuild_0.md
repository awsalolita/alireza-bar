

Sign in to the AWS Management Console and open the CodePipeline console at http://console.aws.amazon.com/codesuite/codepipeline/home.On the Welcome page, choose Create pipeline.

On the Step 1: Choose pipeline settings page, in Pipeline name, enter the name for your pipeline.

In Service Role, Choose Existing service role to use a service role already created in IAM containing Jam-Challenge . Leave the rest of the details to default.

On the Step 2: Add source stage page, in Source provider, choose the type of repository where your source code is stored i.e. CodeCommit.

4a. In Repository name, provide the Code Repository name starting with Jam-Challenge*.

4b. Choose Branch name as master.

4c. Leave the rest of configurations as it is.

Click Next, and add Build Stage.

5a. Under Input Artifacts, choose SourceArtifact.

5b. Under project name, choose build project already created

5c. Leave the rest of configurations as it is.

Click Next, and add Deploy Stage.

6a. Under Action Provider, choose AWS CloudFormation

6b. Under Input Artifacts, choose BuildArtifact.

6c. Under Action mode, choose Create or Update Stack

6d. Under stack name, type jam-challenge

6e. Under Template, Choose Artifact name as BuildArtifact and File name as packaged-template.yaml.

6f. Under Capabilities, choose CAPABILITY_IAM and CAPABILITY_AUTO_EXPAND.

6g. Under Role name, choose a role starting with jam-challenge*

Click next, review the changes and finish creating the CodePipeline and it should automatically trigger within 1 minute.

Validate your CodePipeline is successful.

In AWS Console, in the top search bar, search for API Gateway service.

Select the API Gateway starting with jam-*

Copy the Invoke URL and paste in a new browser tab.

Lambda function will get executed and you will see Jam logo and a message saying - You have successfully built the application using CI/CD pipeline

Copy the Invoke URL and paste in the answer field to mark the task complete.