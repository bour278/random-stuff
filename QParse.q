f:{
    a:&[count'[x];&/[":"\:/:x;8h]];  /find assignment rows
    v:`$*'(" "\:*':":"\:x a);         /extract vars (first token before :)
    v@&{(3=@){$[@x;98 99h~\:@!x;0b]}/x}'[v]  /filter for tables
 };

/ Same thing
f2:{`$*''" "\:*':":"\:x@&[#:'x;&/[":"\:/:x;8h]]@&{(3=@){$[@x;98 99h~\:@!x;0b]}/x}'`$*''" "\:*':":"\:x@&[#:'x;&/[":"\:/:x;8h]]};

/ Usage:
/x:("t:([];c:1 2)";"a:42";"s:([k:1]v:2)")
/f[x]
