# Koala
IP information for NSOC teams.  Koala was written at [Cemig](http://www.cemig.com.br)'s Network and Security Operations Center (Centro de Operações de Rede e Segurança -- CORS) to assist the team in cybersecurity investigations and network management.

Koala is based in "modules" and the first ones are `update`, `subnet`, `info`, and `rdap`.  The first one downloads databases with IP information used by the `info` module to present them to the user.  `subnet` module performs basic IP subnet calculations, and the `rdap` module does RDAP queries to retrieve IP information.

## Usage
First, clone Koala and install its Python dependencies:

```
$ git clone https://github.com/forkd/koala
$ cd koala
$ python -m pip install -r requirements.txt
$ cd koala
```

After that, the program is ready to be used, but to use the `info` module, first you must install the databases using the `update` module.  A list of common commands follows:

```
$ koala.py update [rir, geo, all]
$ koala.py subnet 10.10.56.32/22
$ koala.py [info, rdap] 100.45.23.89
```

## License
Licensed under a MIT license --read `LICENSE` file for further information.