## 1 Prerequisites
To generate a certificate, you need openssl.
```shell
openssl --help
```
If you get an error, you will need to install openssl.

### 1.1 Install openssl
```shell
choco install openssl
```
If you dont have choco installed you will need to install it.

### 1.2 Install chocolatey 
Windows 11 does not come with Chocolatey (choco) preinstalled. If you want to use Chocolatey as a package manager, you'll need to install it manually. You can follow the official installation guide here or use PowerShell with the following command:

powershell
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
Once installed, you can verify it by running:

cmd
```
choco -v
```
## 2 Generate certificates
First generate the key
```shell
openssl genpkey -algorithm RSA -out .\server.key -pkeyopt rsa_keygen_bits:2048

```
Then generate the certificate signing request file
```shell
openssl req -new -key .\server.key -out .\server.csr
```
You will get a series of prompts like this that you need to fill in:
```
P:\git\grandad-does-stuff\woodpecker-ci>openssl req -new -key .\server.key -out .\server.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:UK
State or Province Name (full name) [Some-State]:England
Locality Name (eg, city) []:Durham
Organization Name (eg, company) [Internet Widgits Pty Ltd]:ownimage
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:Keith Hart
Email Address []:keith@ownimage.co.uk

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
```

Self-sign the certificate:      
```shell
openssl x509 -req -days 365 -in .\server.csr -signkey .\server.key -out .\server.crt
```

# 3 Configure the env file
copy the .env_template to .env and fill in the values

# 4 Fix Webhook

As we have self signed certs GitHub will reject the webhook on a cert error.
You  need to navigate to your repo, and settings, webhook and disable SSL verification.

I also check the box to say send me everything as I was not getting events for pushes to my branch.
