# md4

## NAME
md4 - macro processor

## Synopsys
```
md4 [OPTIONs]  FILEs
```

## DESCRIPTION
### Macro
Process macros in text files (FILEs). The following string presents the md4 macro:
```
@macro_name(p0, p1, ...)
```
`p0`, `p1`, ... are parameters for macro. The number of required parameters are defined for each macros which is decided by `macro_name`.

The macro is replaced by the result of macro evaluation.
For example the `@work_dir()` macro will be replaced by the path of the directory where the `md4` command executed.

input:
```
#include "@work_dir()/header_a.h"
```
output:
```
#include "current/dir/header_a.h"
```

#### `@include(file_path)`
Replace this macro by the contents of file in `file_path`. The md4 command searchs the file from
* The include directory which is given by '-I' option
* Relative path from the work directory.

#### `@workdir()`
The path of the directory where the `md4` command is executed.

##  AUTHOR
[Steel Wheels Project](https://github.com/steel-wheels/Project/blob/main/README.md)

## COPYRIGHT
This software is distributed under [GNU General Public License version 2](https://opensource.org/license/GPL-2.0). 

## See also
This software was inspired by the [m4 macro processor](https://www.gnu.org/software/m4/manual/index.html).


