# Hiding text inside Images using steganography

Uses LSB steganography to hide text in images

# Usage

```bash
git clone https://github.com/wmstack/gci_steganography
cd gci_steganography/

#get some images

#encrypt
python3 hide.py -e /path/to/image.png
Text to hide in image: This is a hidden message
Sucessfully hidden text in file!

#decrypt
python3 hide.py -d /path/to/image.png
The hidden text is : This is a hidden message
```

# Demo

<a href="https://asciinema.org/a/rFQQSYtQvgGKyyfYANVV8LcNA" target="_blank"><img src="https://asciinema.org/a/rFQQSYtQvgGKyyfYANVV8LcNA.png" width="800" /></a>
