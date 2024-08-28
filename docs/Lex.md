# Creating bot
* attach iam role
### Concept
* `intent` is something that a user wants to do 
* `utterance` is representative phrase that a user might use to invoke the intent.
* `slot` is used to capture information from the user to fulfill the intent (its used in intents).
* slots can be used in the messages like in closing message
```
Thanks for being a valued customer. How can I help you today, {CustomerName}?
```
* built-in slot type is called `Extended`
* A custom slot type is a list of values that Amazon Lex uses to train the machine learning model to recognize values for a slot.
* Fallback intent is used when no intent is matching
* `Context`: Conversation context is the information that a user, your application, or an AWS Lambda function provides to an Amazon Lex bot to fulfill an intent. Conversation context includes slot data that the user provides, request attributes set by the client application, and session attributes that the client application and Lambda functions create. 

# With Kendra

* response
```
((x-amz-lex:kendra-search-response-answer-1))
I found an excerpt from a helpful document: ((x-amz-lex:kendra-search-response-document-1))
I think the answer to your questions is ((x-amz-lex:kendra-search-response-answer-1))

```
* Create alias and in alias config , select the language and choose a lambda
* then if you want the user prompt to go through lambda and RAG(ML + Kendra)

