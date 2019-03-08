# Koala
IP information for NSOC teams.  Koala was written at [Cemig](http://www.cemig.com.br)'s Network and Security Operations Center (Centro de Operações de Rede e Segurança -- CORS) to assist the team in cybersecurity investigations and network management.

Koala comes with the following modules:

* `subnet`: performs basic IP subnet calculations.
* `whois`: discover many information about an IP address.
* `proxy`: sets OS proxy according to configuration file. (currently works only with Windows)
* `iron`: clean up a proxy domain list (IronPort compliant).
* `visio`: converts MS-Visio files to PDF or HTML ones. (only works with Windows)

## Usage
First, clone Koala and install its Python dependencies:

```
$ git clone https://github.com/forkd/koala
$ cd koala
$ python -m pip install -r requirements.txt
$ cd koala
```

A list of common commands follows:

```
$ koala.py subnet 10.10.56.32/22
$ koala.py whois 888.888.888.888
$ koala.py proxy proxy_id
$ koala.py iron domain_list.txt
$ koala.py visio
```

## License
Licensed under a MIT license --read `LICENSE` file for further information.