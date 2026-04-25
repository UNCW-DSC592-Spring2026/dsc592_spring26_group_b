#!/usr/bin/env sh

# Define a version (defaults to timestamp if not provided via ENV)
VERSION=${BUILD_VERSION:-"1.0.$(date +%s)"}

echo "Baking version $VERSION into YAMLs..."

# Update placeholders exactly like your GitHub Action
find . \( -name "*.yaml" -o -name "*.yml" \) \
  -exec sed -i "s/SET_BY_GITHUB_ACTIONS/$VERSION/g" {} +
find . -name "pipeline.yml" \
  -exec sed -i "s/VERSION_PLACEHOLDER/$VERSION/g" {} +

COMPONENTS=("preprocess_text.yml" "split_data.yml" "train.yml" "score.yml")

for comp in "${COMPONENTS[@]}"; do
    FILE_PATH=$(find ./src/components -name "$comp")
    if [ -n "$FILE_PATH" ]; then
        az ml component create --file "$FILE_PATH" -g $AZURE_RG -w $AZURE_WORKSPACE
    fi
done

echo "Submitting pipeline..."
az ml job create --file src/pipeline.yml -g $AZURE_RG -w $AZURE_WORKSPACE --no-wait
