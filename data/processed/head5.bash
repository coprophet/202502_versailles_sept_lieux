for file in "."/*.csv; do
    if [ -f "$file" ]; then
        echo "===== $file ====="
        head -n 5 "$file"
        echo ""
    fi
done