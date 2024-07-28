# Redshift iam roles 
* policies like access to s3 and kinesis
* make it `DEFAULT`
# S3 to Redshift
### copy data from s3
```sql
copy  feedback.product_feedback
from 's3://' 
iam_role 'arn:aws:iam::083190880943:role/S3AccessRoleRedshift'
json 'auto';
```
```sql
copy sailors from 's3://redshift-demos/data/gamejam/sailors/' 
iam_role 'arn:aws:iam::869076321287:role/Redshiftgamesrole' # OR default
csv
IGNOREHEADER 1;
```
### Grant Role to user
```sql
create user cashking with password 'abcD1234'
create role captain 
grant role captain to cashking
select * from svv_roles
```

### Grant specific permissions and creating row level security (RLS)
```sql
GRANT SELECT ON sailors TO ROLE captain;
GRANT SELECT(s_name,s_segment,s_dietrestrictions) ON sailors TO ROLE crew;
GRANT SELECT(s_name,s_address,s_acctbal) ON sailors TO ROLE finance;

CREATE RLS POLICY board
with (s_onboard BOOLEAN)
using (s_onboard = TRUE)

CREATE RLS POLICY allpolicy
using (TRUE)

SELECT * FROM svv_rls_policy;
```

### show all views 
```sql
select * from STV_MV_INFO;
```


