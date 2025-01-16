// Function to remove rows that are entirely null
removeNullRows:{[t]
    // Create a boolean list where 1 indicates at least one non-null value in the row
    nonNullRows:not all each null each flip t;
    // Filter the table to keep only rows with at least one non-null value
    t where nonNullRows
 };

// Function to remove columns that are entirely null
removeNullCols:{[t]
    // Get column names
    cols:cols t;
    // Create a boolean list where 1 indicates at least one non-null value in the column
    nonNullCols:not all each null each t;
    // Keep only columns that have at least one non-null value
    t:?[t;();0b;cols where nonNullCols!nonNullCols];
    t
 };

// Combined function to remove both null rows and columns
cleanTable:{[t]
    // First remove null rows, then remove null columns
    removeNullCols removeNullRows t
 };

// Example usage:
/ Create a sample table with some null rows and columns
t:([]
    col1:("a";"b";"";" ";());
    col2:(1;0N;0N;0N;0N);
    col3:(0N;0N;0N;0N;0N);  / entirely null column
    col4:(1.1;2.2;0N;4.4;0N)
 );

/ Clean the table
cleanedTable:cleanTable[t];

/ Show results
-1 "Original table:";
show t;
-1 "\nCleaned table:";
show cleanedTable;
