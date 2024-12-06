/ Function to find tables in a q script
findTables:{[script]
    / Split into lines and clean whitespace
    lines:trim each "\n" vs script;
    / Find lines with assignments
    hasColon:where lines like "*:*";
    / Extract variable names (everything before :)
    varNames:distinct trim each first each ":" vs/: lines[hasColon];
    / Execute the script to get variables in memory
    value script;
    / Convert names to symbols and check for table type
    vars:`$varNames;
    / Filter for tables (type 98h) and keyed tables (99h with >1 item)
    tables:vars where {
        $[not `$string[x] in system"v"; :0b;
          t:type get x;
          $[t=98h; :1b;
            t=99h; :1b;
            :0b]
        ]
    } each vars;
    asc tables
 };

/ Example usage:
script:"\n" sv (
    "trade:([] sym:`a`b; price:1 2);";
    "qt:([sym:`x`y] price:3 4);";
    "x:42;";
    "str:\"hello\";"
);

findTables[script]  / Returns `qt`trade
