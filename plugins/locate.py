#     ## Search files
#     search)

#         input=$(xdmenu "search")

#         result=""
#         if [ "$input" != '' ] ; then
#             result=$(echo "$input" | locate -e -r "$input" | xdmenu "result" )
#         else
#             return 1
#         fi

#         if [ "$result" != "" ] ; then
#             $open "$result"
#         else
#             return 1
#         fi
#         ;;
