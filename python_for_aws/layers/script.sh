echo "python version"
read version 

echo "package name"
read package

mkdir -p layer/python/lib/$version/site-packages
pip3 install $package -t layer/python/lib/$version/site-packages/

cd layer
zip -r $package.zip *