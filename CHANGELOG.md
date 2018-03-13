# 0.2.0
- Add FacturaeRoot signature functionality
  - New methods
    - FacturaeRoot.sign(pkcs12_cert, password) to sign a FacturaeRoot instance
    - FacturaeRoot.sign_verify(signed_root) to verify the already created signature
- Add basic signature tests with a dummy self-signed cert
- Provide Travis-CI integration to validate tests and autodeploy to Pypi on tag
