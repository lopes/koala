# Koala
IP information for NSOC teams.  Koala was written at [Cemig](http://www.cemig.com.br)'s Network and Security Operations Center (Centro de Operações de Rede e Segurança -- CORS) to assist the team in cybersecurity investigations and network management.

Koala comes with the following modules:

* `subnet`: performs basic IP subnet calculations.
* `whois`: discover many information about an IP address.
* `proxy`: sets OS proxy according to configuration file. _currently works only with Windows_
* `visio`: converts MS-Visio files to PDF or HTML ones. _only works with Windows_
* `abuse`: analyses an abuse box to retrieve header information of messages. _under development_
* `iron`: clean up a proxy domain list. _IronPort compliant_
* `qradar`: performs predefined AQL queries in IBM QRadar.
* `sync`: syncs information between 2 systems (today: Prime to NetBox).


## Usage
First, clone Koala and install its Python dependencies:

```
$ git clone https://github.com/forkd/koala
$ cd koala
$ python -m pip install -r requirements.txt
$ cd koala
```

The list of commands follows:

```
$ koala.py subnet 10.10.56.32/22
$ koala.py whois 888.888.888.888
$ koala.py proxy proxy_id
$ koala.py visio
$ koala.py abuse
$ koala.py iron -i domain_list.txt -o new.txt
$ koala.py qradar query1
$ koala.py sync p2n
```

## License
Licensed under a MIT license --read `LICENSE` file for further information.