echo "Enter project name:"
read name
pth="s/api_template/$name/g"
mv ./api_template $name
find ./ -type f -name "*" -not -path "./rename.sh" -exec sed -i $pth {} \;
