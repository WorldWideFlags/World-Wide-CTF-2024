## Mutual TLS

**Flag**: `wwf{n1c3_ch41n_v4l1d4t10n}`

**Author**: `spipm`

**Tag(s)**: `medium`

**Description**: Mutual TLS is best practice, so we created a PoC for an authentication service.
Can you check if this client certificate works at your side?
You can try it out with: `curl --cert client.pem -k "https://mtls.wwctf.com"`