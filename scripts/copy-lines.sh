#!/bin/bash
# Copy lines from one file and insert them into another file at a specific position
# Usage: ./copy-lines.sh <source_file> <start_line> <end_line> <target_file> <insert_before_line>

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 <source_file> <start_line> <end_line> <target_file> <insert_before_line>"
    echo ""
    echo "Example: $0 fileA.txt 10 15 fileB.txt 20"
    echo "  This copies lines 10-15 from fileA.txt and inserts them BEFORE line 20 in fileB.txt"
    echo ""
    echo "Parameters:"
    echo "  source_file        - File to copy lines from"
    echo "  start_line         - First line number to copy (inclusive)"
    echo "  end_line           - Last line number to copy (inclusive)"
    echo "  target_file        - File to insert lines into"
    echo "  insert_before_line - Line number where content will be inserted (content becomes this line)"
    exit 1
}

# Check if correct number of arguments provided
if [ "$#" -ne 5 ]; then
    echo -e "${RED}Error: Incorrect number of arguments${NC}"
    usage
fi

SOURCE_FILE="$1"
START_LINE="$2"
END_LINE="$3"
TARGET_FILE="$4"
INSERT_LINE="$5"

# Validate that source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}Error: Source file '$SOURCE_FILE' does not exist${NC}"
    exit 1
fi

# Validate that target file exists
if [ ! -f "$TARGET_FILE" ]; then
    echo -e "${RED}Error: Target file '$TARGET_FILE' does not exist${NC}"
    exit 1
fi

# Validate that line numbers are positive integers
if ! [[ "$START_LINE" =~ ^[0-9]+$ ]] || ! [[ "$END_LINE" =~ ^[0-9]+$ ]] || ! [[ "$INSERT_LINE" =~ ^[0-9]+$ ]]; then
    echo -e "${RED}Error: Line numbers must be positive integers${NC}"
    exit 1
fi

# Validate that start_line <= end_line
if [ "$START_LINE" -gt "$END_LINE" ]; then
    echo -e "${RED}Error: Start line ($START_LINE) must be <= end line ($END_LINE)${NC}"
    exit 1
fi

# Validate that insert_line is positive
if [ "$INSERT_LINE" -lt 1 ]; then
    echo -e "${RED}Error: Insert line must be >= 1${NC}"
    exit 1
fi

# Create temporary file for extracted content
TEMP_FILE=$(mktemp)

# Extract lines from source file
echo -e "${YELLOW}Extracting lines $START_LINE-$END_LINE from '$SOURCE_FILE'...${NC}"
sed -n "${START_LINE},${END_LINE}p" "$SOURCE_FILE" > "$TEMP_FILE"

# Check if extraction was successful
if [ ! -s "$TEMP_FILE" ]; then
    echo -e "${RED}Error: Could not extract lines (file might not have enough lines)${NC}"
    rm "$TEMP_FILE"
    exit 1
fi

# Calculate the line before insertion point
BEFORE_LINE=$((INSERT_LINE - 1))

# Create backup of target file
BACKUP_FILE="${TARGET_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$TARGET_FILE" "$BACKUP_FILE"
echo -e "${YELLOW}Created backup: '$BACKUP_FILE'${NC}"

# Create temporary output file
OUTPUT_FILE=$(mktemp)

# Perform the insertion
if [ "$INSERT_LINE" -eq 1 ]; then
    # Special case: insert at the beginning
    cat "$TEMP_FILE" > "$OUTPUT_FILE"
    cat "$TARGET_FILE" >> "$OUTPUT_FILE"
else
    # Normal case: insert in the middle or end
    head -n "$BEFORE_LINE" "$TARGET_FILE" > "$OUTPUT_FILE"
    cat "$TEMP_FILE" >> "$OUTPUT_FILE"
    tail -n +"$INSERT_LINE" "$TARGET_FILE" >> "$OUTPUT_FILE"
fi

# Replace original file with modified content
mv "$OUTPUT_FILE" "$TARGET_FILE"

# Cleanup temporary files
rm "$TEMP_FILE"

# Success message
LINES_COPIED=$((END_LINE - START_LINE + 1))
echo -e "${GREEN}✓ Successfully copied $LINES_COPIED lines from '$SOURCE_FILE' (lines $START_LINE-$END_LINE)${NC}"
echo -e "${GREEN}✓ Inserted before line $INSERT_LINE in '$TARGET_FILE'${NC}"
echo -e "${GREEN}✓ Backup saved as: '$BACKUP_FILE'${NC}"
