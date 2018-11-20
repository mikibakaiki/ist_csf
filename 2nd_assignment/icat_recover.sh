# First get list of files:
# fls -f ext4 -o 2048 -p -r ./image_disk 573445 | grep -v '^..-' | grep -v '^... \*' > files.lst

IMAGE=sally_disk
LIST=files.lst
DEST=./recovered/

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
