#!/usr/bin/env sh

# Define a version (defaults to timestamp if not provided via ENV)
VERSION=${BUILD_VERSION:-"1.0.$(date +%s)"}

echo "Baking version $VERSION into YAMLs..."

# Update placeholders exactly like your GitHub Action
find . -name "*.yaml" -exec sed -i "s/SET_BY_GITHUB_ACTIONS/$VERSION/g" {} +
find . -name "run_pipeline.yaml" -exec sed -i "s/VERSION_PLACEHOLDER/$VERSION/g" {} +

# Register components (simplified loop)
COMPONENTS=("preprocess_text.yaml" "split_data.yaml" "linear_regression.yaml" "train_model.yaml" "score_model.yaml")

for comp in "${COMPONENTS[@]}"; do
    FILE_PATH=$(find . -name "$comp")
    if [ -n "$FILE_PATH" ]; then
        az ml component create --file "$FILE_PATH" -g $AZURE_RG -w $AZURE_WORKSPACE
    fi
done

# Launch the Job
echo "Submitting pipeline..."
az ml job create --file run_pipeline.yaml -g $AZURE_RG -w $AZURE_WORKSPACE --no-wait
