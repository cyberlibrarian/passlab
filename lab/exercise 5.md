# Exercise 5
## Using hashcat to crack passwords

### Basic syntax

### Cracking Word hashes
[Extracting Hashes from Password Protected Microsoft Office Documents](https://medium.com/@klockw3rk/extracting-hash-from-password-protected-microsoft-office-files-b206438944d2)

```
./hashcat.bin -m 9600 -o file.txt hash.txt wordlist.txt
```

### Cracking PDF hashes
[Cracking PDF Hashes](https://nicholaslyz.com/blog-posts/2021-07-23-cracking-pdf-hashes/)

```
./hashcat.bin -m 10500 -o file.txt hash.txt wordlist.txt
```

### Cracking NTLM hashes
```
./hashcat.bin -m 1000 -o file.txt --username hash.txt wordlist.txt
```

