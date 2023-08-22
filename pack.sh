rm my_deployment_package.zip
cd package
rm -rf **/__pycache__
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip *.py douban/*.py
