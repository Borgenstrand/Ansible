grep -vxFf $1 $2 | sed -r '/^(\s*#|$)/d;'
