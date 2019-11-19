#!/bin/sh

. ~/.bash_profile

logger "`dirname \"$0\"`/Cells"

exec "`dirname \"$0\"`/Cells" $@
