awk -F, '
    # Function to sanitize column 5 for use as a filename
    function sanitize(name) {
        gsub(/[\/<>:"\\|?*]/, "_", name); # Replace problematic symbols with underscore
        gsub(/[\x27\x22]+/, "", name); # Remove single and double quotes
        return name;
    }
    NR == 1 {header = $0; next} # Capture header and skip processing for the header row
    NR > 1 {
        filename = sanitize($5) ".csv"; # Sanitize column 5 value and append .csv
        if (!(filename in fileHeaderWritten)) {
            print header > filename; # Write header to file if not already done
            fileHeaderWritten[filename] = 1; # Mark header as written for this file
        }
        print >> filename; # Append the current line to the file
    }
' cdc_places_data.csv
