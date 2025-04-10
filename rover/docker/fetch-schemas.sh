#!/bin/bash
set -e

SUBGRAPHS_FILE="/config/subgraphs.yaml"
SUPERGRAPH_CONFIG="/output/supergraph-config-private.yaml"
SUPERGRAPH="/output/supergraph-private.graphql"
PUBLIC_CONTRACT_SUBGRAPH="/output/public-subgraph.graphql"

# Load subgraphs from YAML
declare -A SUBGRAPHS
while IFS=": " read -r key value; do
  [[ "$key" == "subgraphs" || -z "$key" ]] && continue
  name=$(echo "$key" | sed 's/^[ ]*//;s/[:]$//')
  url=$(echo "$value" | sed 's/^[ ]*//')
  SUBGRAPHS["$name"]=$url
done < <(yq e '.subgraphs' "$SUBGRAPHS_FILE")

# Introspect all subgraphs
for name in "${!SUBGRAPHS[@]}"; do
  url="${SUBGRAPHS[$name]}"
  file="/output/${name}.graphql"
  echo "🔍 Introspecting $name at $url"
  if rover subgraph introspect "$url" > "$file.tmp" 2>/dev/null; then
    mv "$file.tmp" "$file"
    echo "✅ $name introspection successful"
  else
    echo "⚠️  Skipping $name due to introspection failure"
    rm -f "$file.tmp"
  fi
done

# Generate private config
echo "federation_version: 2" > "$SUPERGRAPH_CONFIG"
echo "subgraphs:" >> "$SUPERGRAPH_CONFIG"
for name in "${!SUBGRAPHS[@]}"; do
  echo "  $name:" >> "$SUPERGRAPH_CONFIG"
  echo "    routing_url: ${SUBGRAPHS[$name]}" >> "$SUPERGRAPH_CONFIG"
  echo "    schema:" >> "$SUPERGRAPH_CONFIG"
  echo "      file: /output/${name}.graphql" >> "$SUPERGRAPH_CONFIG"
done

# Compose full private supergraph
echo "🧩 Composing private supergraph..."
rover supergraph compose \
  --elv2-license accept \
  --config "$SUPERGRAPH_CONFIG" \
  > "$SUPERGRAPH"

# Extract public contract (subgraph)
echo "🔐 Extracting public contract subgraph..."
rover contract compose \
  --supergraph "$SUPERGRAPH" \
  --contract-name public \
  --config "$SUPERGRAPH_CONFIG" \
  > "$PUBLIC_CONTRACT_SUBGRAPH"

echo "✅ Done!"
echo "   - Private Supergraph:      $SUPERGRAPH"
echo "   - Public Subgraph (Contract): $PUBLIC_CONTRACT_SUBGRAPH"