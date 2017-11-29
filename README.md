# Index of Coincidence (IC) Method

The IC method is used to crack polyalphabetic substitution ciphers of unknown key length (e.g. Vigenère cipher).

This simple script exhaustively calculates the aggregate IC for each possible key length, and finds the minimum aggregate IC delta to guess the probable key length.

## Usage

```sh
python ic.py input.txt
```

Try it out with a ciphertext using the [Vigenère cipher](https://www.dcode.fr/vigenere-cipher).

## License

MIT
