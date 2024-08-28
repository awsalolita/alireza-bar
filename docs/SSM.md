# SSM without natgateway
* 3 endpoints
```
ssm
ssm-messages
ec2message
```
* s3 endpoint needed for patchmanager
# Documents
`PostMigrationAutomation`
`ConfigureProxy`
``
### modify with precondition instance type

# PortForward
* port forward a ssh or rdp port
```bash
aws ssm start-session \
 --target "i-0d639838427fe0044" \
 --document-name AWS-StartPortForwardingSession \
 --parameters '{"portNumber":["3389"], "localPortNumber":["56789"]}' \
 --region "us-east-1"
```
* port forward a bastion host to rds
```bash
aws ssm start-session `
    --region <your region> `
    --target <your bastion instance id> `
    --document-name AWS-StartPortForwardingSessionToRemoteHost `
    --parameters host="<your rds endpoint name>",portNumber="1433",localPortNumber="1433"
```
* ssh over ssm add the following to .ssh
```
# SSH over Session Manager
host i-* mi-*
    ProxyCommand sh -c "aws ssm start-session --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"

```
* ssh over it
```
ssh ec2-user@instance-id
```

# Start Session
* you need session manager plugin
```bash
aws ssm start-session  --target "i-02dea3e9112429dff"  --document-name SSM-SessionManagerRunShell  --region "us-east-1"
```

# Patch 
* Patch policy for specifying some stuff

# CLI
* start a patch scan
```bash
aws ssm send-command --document-name 'AWS-RunPatchBaseline' --targets Key=InstanceIds,Values='i-<your-instance-id>' --parameters 'Operation=Scan’
```
* get the status
```bash
aws ssm list-command --command-id
```
* start automation document
```bash
aws ssm start-automation-execution --document-name "AWS-RestartEC2Instance" --parameters "InstanceId=i-<your-instance-id>"
aws ssm get-automation-execution --automation-execution-id <your-execution-id>
```
* View application installed on a instances
```bash
aws ssm list-inventory-entries --instance-id "" --type-name "AWS:Application" --max-results 1
```

# SSM Parameter
* get by path
```bash
aws ssm get-parameters-by-path --path /Dev/Web/IIS
```
* get parameters
```bash
aws ssm get-parameters --names a b c
```

### prevent access
* ssm:overwrite , ssm:recursive
* by default it can access recursivly