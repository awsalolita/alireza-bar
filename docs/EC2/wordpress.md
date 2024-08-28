
* update database
```
UPDATE `wp_options` SET `option_value` = 'https://d32pymd9z6h7lz.cloudfront.net' where option_name =  "siteurl";
UPDATE `wp_options` SET `option_value` = 'https://d32pymd9z6h7lz.cloudfront.net' where option_name =  "home";
```

```
define( 'WP_HOME', 'https://example.com' );
define( 'WP_SITEURL', 'https://example.com' );
if (strpos($_SERVER['HTTP_X_FORWARDED_PROTO'], 'https') !== false)
           $_SERVER['HTTPS']='on';
```