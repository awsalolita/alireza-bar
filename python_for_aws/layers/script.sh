mkdir -p layer/python/lib/python3.9/site-packages
pip3 install requests -t layer/python/lib/python3.9/site-packages/

cd layer
zip -r mypackage.zip *