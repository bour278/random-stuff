findTablesInScript:{[script]
    / Split into lines and clean spaces
    lines:trim each "\n" vs script;
    / Get lines with assignments (contains :)
    assignLines:lines where lines like "*:*";
    / Extract first token before : (the variable name)
    varNames:`$trim each first each(" " vs/:first each":" vs/:assignLines);
    / Filter for ones that exist and are tables
    tables:varNames where {(x in system"v") and (type get x) in 98 99h} each varNames;
    asc tables
 };
