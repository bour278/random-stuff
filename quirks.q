calcWeightedAvgs:{[tbl;weight_col;pivot_col]
    // First group by pivot_col
    gb: group tbl[pivot_col];
    
    // Get numeric columns except weight and pivot
    numCols: cols[tbl] where 
        (meta[tbl][`t] in "hijef") and 
        not cols[tbl] in (weight_col;pivot_col);
    
    // Create table with pivot col
    res: flip (enlist pivot_col)!enlist key gb;
    
    // Update each column with its weighted average
    res: res,'flip numCols!{[col;w;gb;t]
        wavg[t[w] gb;t[col] gb]
    }[;weight_col;gb;tbl] each numCols;
    
    res
 };
