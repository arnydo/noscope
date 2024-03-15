# NOSCOPE

![logo](misc/logo.png)

The primary goal of NOSCOPE is to simplify the scoping process for security assessments. By allowing users to specify domains and/or IPs to be checked against a list of in-scope IPs and CIDRs, NOSCOPE helps ensure that the assessment focuses on the intended targets, thereby maximizing efficiency and accuracy.

## Installation

```bash
git clone https://github.com/arnydo/noscope
pip install -r requirements.txt
```

## Usage

To use NOSCOPE, simply provide the tool with the domains and/or IPs you want to scope, along with a file containing the list of in-scope IPs and CIDRs. NOSCOPE will then compare the provided targets against the specified scope and output the results.

## Examples

Using an exampled `scope.txt` with the following content:

```txt
93.184.216.0/24
10.0.0.0/24
```

Here are a few examples of how to use NOSCOPE:

```bash
# Scope domains against a list of in-scope IPs and CIDRs
$ python3 noscope.py --domain example.com subdomain.example.com --scope-file scope.txt

┏━┓╋┏┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃┃┗┓┃┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━━┛
┃┏┓┗┛┃┃╋┃┃┗━━┫┃╋┗┫┃╋┃┃┗━┛┃┗━━┓
┃┃┗┓┃┃┃╋┃┣━━┓┃┃╋┏┫┃╋┃┃┏━━┫┏━━┛
┃┃╋┃┃┃┗━┛┃┗━┛┃┗━┛┃┗━┛┃┃╋╋┃┗━━┓
┗┛╋┗━┻━━━┻━━━┻━━━┻━━━┻┛╋╋┗━━━┛

💾 https://github.com/arnydo/noscope
🐦 https://twitter.com/kyle_parrish_

Domain does not exist: subdomain.example.com
+-----------------+-----------------+
| Domain          | IP              |
+=================+=================+
| example.com     | 93.184.216.34   |
+-----------------+-----------------+

# Scope IPs against a list of in-scope IPs and CIDRs
python3 noscope.py --ip 192.168.0.1 10.0.0.1 --scope-file scope.txt

┏━┓╋┏┳━━━┳━━━┳━━━┳━━━┳━━━┳━━━┓
┃┃┗┓┃┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━┓┃┏━━┛
┃┏┓┗┛┃┃╋┃┃┗━━┫┃╋┗┫┃╋┃┃┗━┛┃┗━━┓
┃┃┗┓┃┃┃╋┃┣━━┓┃┃╋┏┫┃╋┃┃┏━━┫┏━━┛
┃┃╋┃┃┃┗━┛┃┗━┛┃┗━┛┃┗━┛┃┃╋╋┃┗━━┓
┗┛╋┗━┻━━━┻━━━┻━━━┻━━━┻┛╋╋┗━━━┛

💾 https://github.com/arnydo/noscope
🐦 https://twitter.com/kyle_parrish_

10.0.0.1
```

## Changelog

See changes in [CHANGELOG](./CHANGELOG.md)

## Contribution

Contributions to NOSCOPE are welcome! If you encounter any issues, have ideas for new features, or want to contribute code improvements, please feel free to open an issue or submit a pull request on GitHub.

## License

NOSCOPE is licensed under the GPL License. See the [LICENSE](LICENSE.md) file for details.

## Contact

For questions, feedback, or suggestions, you can reach out to the project maintainer at [github@arnydo.com](mailto:github@arnydo.com). We'd love to hear from you!