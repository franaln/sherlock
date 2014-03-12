#     # Explore files
#     explore)

#         cd "$HOME"

#         choice=1
#         while [ "$choice" ]; do

#             choice=$((echo ".." ; ls $PWD ; echo "[Open]") | xdmenu "[$(basename $(pwd))]")

#             if [ "$choice" ] ; then

#                 # change dir by hand
#                 if [[ "$choice" == "cd "* ]] ; then
#                     goto=$(echo $choice | cut -d ' ' -f 2)

#                     if [ -d $goto ] ; then
#                         cd $goto
#                     else
#                         exit 1
#                     fi

#                 # Folder -> go inside
#                 elif [[ -d "$choice" ]] ; then
#                     cd "$choice"

#                 # .. -> go up
#                 elif [ "$choice" == ".." ] ; then
#                     cd ..

#                 # [Open] -> open current dir in $fm
#                 elif [ "$choice" == "[Open]" ] ; then
#                     setsid $filemanager "$PWD"
#                     unset file
#                     exit 0

#                 # File -> open
#                 else
#                     $open $choice
#                     unset file
#                     exit 0
#                 fi
#             fi
#         done
#         ;;
