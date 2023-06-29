# Exercise 1
## Extracting Hashes from Office Documents

```
~/john/run/office2john.py file.docx
```

```
file.docx:$office$*2013*100000*256*16:hash

```
./hashcat.bin -m 9600 -o file.txt hash.txt wordlist.txt
```