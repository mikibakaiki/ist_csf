# First get list of files:
# fls -f ext4 -o 2048 -p -r ./image_disk 573445 | grep -v '^..-' | grep -v '^... \*' > files.lst

# recover all files from directory 575979 -> .thunderbird
#fls -f ext4 -o 2048 -p -r ../../2nd_assignment/sally_disk 575979 | grep -v '^..-' | grep -v '^... \*' > files_thunderbird.lst

#mkdir recovered_thunderbird
mkdir recovered_mozilla

IMAGE=../../2nd_assignment/sally_disk
#LIST=files_thunderbird.lst
LIST=files_mozilla.lst
#DEST=./recovered_thunderbird
DEST=./recovered_mozilla

# thunderbird directory inode -> 575979
# mozilla directory inode -> 575993
MOZILLA=575993
THUNDER=575979

fls -f ext4 -o 2048 -p -r "$IMAGE" "$MOZILLA" | grep -v '^..-' | grep -v '^... \*' > "$LIST"

cat $LIST | while read line; do
   filetype=`echo "$line" | awk {'print $1'}`
   filenode=`echo "$line" | awk {'print $2'}`
   filenode=${filenode%:}
   filename=`echo "$line" | cut -f 2 | grep -v "   "`

   if [ $filetype == "r/r" ]; then
      echo "$filename"
      mkdir -p "`dirname "$DEST/$filename"`"
      icat -f ext4 -o 2048 -r -s "$IMAGE" "$filenode" > "$DEST/$filename"
   fi
done
