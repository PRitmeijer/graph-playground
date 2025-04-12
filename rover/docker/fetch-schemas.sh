#!/bin/bash
set -e

# Input YAML file containing subgraph definitions.
CONFIG_FILE="/config/subgraphs.yaml"

# Root output folder.
OUTPUT_ROOT="/output"

# Folder where introspected subgraph files will be stored.
SUBGRAPHS_DIR="${OUTPUT_ROOT}/subgraphs"

# Folder where the generated config files will be stored.
CONFIG_DIR="${OUTPUT_ROOT}/config"

# Folder where the final composed supergraph files will be stored.
BACKUP_SUPERGRAPH_DIR="${OUTPUT_ROOT}/supergraph"

COMPOSED_DIR="/supergraph"

# Create the output directories.
mkdir -p "${SUBGRAPHS_DIR}"
mkdir -p "${CONFIG_DIR}"
mkdir -p "${BACKUP_SUPERGRAPH_DIR}"

compose_supergraph() {
  local type=$1
  local graph_key="${type}_subgraphs"

  # Directory for storing subgraph introspection files for this type.
  local type_subgraph_dir="${SUBGRAPHS_DIR}/${type}"
  mkdir -p "${type_subgraph_dir}"
  
  # Define the paths for the config and final supergraph output.
  local config_file="${CONFIG_DIR}/${type}-supergraph-config.yaml"
  local graph_output="${BACKUP_SUPERGRAPH_DIR}/${type}-supergraph.graphql"  # backup copy of composed schema
  local composed_output="${COMPOSED_DIR}/${type}-supergraph.graphql"

  echo "📦 Processing ${type} supergraph..."

  # Build an associative array of subgraph names and URLs from the YAML file.
  declare -A SUBGRAPHS=()
  while IFS=": " read -r key value; do
    [[ "$key" == "$graph_key" || -z "$key" ]] && continue
    name=$(echo "$key" | sed 's/^[ ]*//;s/[:]$//')
    url=$(echo "$value" | sed 's/^[ ]*//')
    SUBGRAPHS["$name"]=$url
  done < <(yq e ".${graph_key}" "$CONFIG_FILE")

  # Introspect each subgraph and save the schema in the type-specific folder.
  for name in "${!SUBGRAPHS[@]}"; do
    url="${SUBGRAPHS[$name]}"
    local file="${type_subgraph_dir}/${type}-${name}.graphql"
    echo "🔍 Introspecting ${type} subgraph '$name' at $url"
    if rover subgraph introspect --header "X-Rover-Introspection: 1" "$url" > "$file.tmp" 2>/dev/null; then
      mv "$file.tmp" "$file"
      echo "✅ Introspection for '$name' successful: $file"
    else
      echo "⚠️  Skipping introspection for '$name' due to failure"
      rm -f "$file.tmp"
    fi
  done

  # Generate the supergraph configuration file.
  {
    echo "federation_version: 2"
    echo "subgraphs:"
    for name in "${!SUBGRAPHS[@]}"; do
      echo "  $name:"
      echo "    routing_url: ${SUBGRAPHS[$name]}"
      echo "    schema:"
      echo "      file: ${type_subgraph_dir}/${type}-${name}.graphql"
    done
  } > "$config_file"
  echo "📝 Config file written: $config_file"

  # Compose the full supergraph and write it to both the backup location and final location.
  echo "🧩 Composing ${type} supergraph..."
  rover supergraph compose --elv2-license accept --config "$config_file" \
    | tee "$composed_output" > "$graph_output"
  echo "✅ ${type} supergraph composed!"
  echo "   - Backup schema (saved to): $graph_output"
  echo "   - Final supergraph (used in gateway): $composed_output"
}

compose_supergraph "public"
compose_supergraph "protected"