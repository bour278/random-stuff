// Assuming:
// tbl - your table
// weight_col - symbol name of weight column
// pivot_col - symbol name of pivot column

calcWeightedAvgs:{[tbl;weight_col;pivot_col]
    // Get all numeric columns except weight and pivot
    numCols: cols[tbl] where 
        (meta[tbl][`t] in "hijef") and 
        not cols[tbl] in (weight_col;pivot_col);
    
    // For each pivot value, calculate weighted average of each column
    // Returns a table with pivot column and one column per numeric column
    t: 0!select {[w;x] sum[w*x]%sum w}[get[weight_col];get each `$string numCols] by pivot_col from tbl;
    
    // Or alternatively using exec:
    // t: 0!exec {[w;x] sum[w*x]%sum w}[get[weight_col];get each `$string numCols] by pivot_col from tbl;
    
    :t
 };

// Usage:
// result: calcWeightedAvgs[tbl;`weight;`category]
