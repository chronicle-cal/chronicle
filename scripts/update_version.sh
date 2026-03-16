# scripts/update_version.sh
VERSION=$1
echo "Updating packages to version $VERSION"

# Python packages
for pkg in services/worker services/backend; do
  sed -i "s/^version = .*/version = \"$VERSION\"/" "$pkg/pyproject.toml"
done

# JS package
jq ".version = \"$VERSION\"" services/frontend/package.json > services/frontend/package.tmp.json
mv services/frontend/package.tmp.json services/frontend/package.json
