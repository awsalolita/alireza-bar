# Task 2: If you do it twice, it's one time too many.
In the challenge output properties there is a direct link to the PostMigrationAutomation document in the console.

AWS Systems Manager Automation feature helps you build common maintenance tasks.

In this project, you will perform multiple actions on instances, so you should look at building an Automation Document with a parameter for the instanceId.

You can then pass parameter to steps by using '{{parameter_name}}' mapping.

Use the default role that is already configured with this document, the role should not be changed to complete this task.

Penalty: 8 points

# Clue 2:What about the instance?
For this task you will need to create a new version of the PostMigrationAutomation document that has an additional Run Task that executes the ConfigureProxy document from the previous task.

You can then pass the instance identifier to steps by using a '{{parameter_name}}' mapping.

Penalty: 9 points
# Clue 3:Solution
To solve this tasks, you must perform the following actions:

Go to AWS Systems Manager console.
Go to Documents.
Go to the Owned by me tab.
Select the document called PostMigrationAutomation.
Click on Actions and Create new version.
Drag the RunCommandonInstances icon between the tag_start and apply_patch icons.
Under General, change the Step name to configure_proxy
Click Inputs
Enter ConfigureProxy in the Document name search box, and after a few seconds the document should appear for selection.
Click the InstanceIds - optional drop down and select InstanceId
You should see - '{{InstanceId}}' appear in the box.
Click Create new version and select Create new default version
Systems Manager may recommend parameterizing the role used in the document, which you should ignore to complete this task.
This document will perform the four steps of tagging, configuring proxy, patching and tagging again. The parameter instanceId will determine which instance must be targeted. The document design should now look like this: