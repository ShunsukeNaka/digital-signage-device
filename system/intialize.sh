FILES="/home/tns0/service/sec/device_token.enc /home/tns0/service/sec/key.bin /home/tns0/service/sec/update_index.txt /home/tns0/service/content1/* /home/tns0/service/content2/* /home/tns0/service/datas/dirnum.txt"

for f in $FILES; do
   if [ -f "$f" ]; then
     sudo rm -f  "$f"
     echo "$f is deleted."
   fi
done

FILE="/home/tns0/service/sec/update_index.txt"
echo "00000000" > "$FILE"

FILE="/home/tns0/service/datas/dirnum.txt"
echo -n "1" > "$FILE"

FILE="/home/tns0/service/system/TESTIMGAE.png"
sudo cp /home/tns0/service/system/testimg.png /home/tns0/service/content1/

