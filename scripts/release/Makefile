.DEFAULT_GOAL: README.md
.SHELLFLAGS := -eu -o pipefail -c
#:Release directory
#:=================
#: 
#:Available `make` targets which can be run inside this directory.
#: 
#:Requirements
#:------------
#:
#:* direnv installed _(optional)_
#:* kubectl installed
#:* kubeseal installed _(including an exported certifcate)_
#:
#:> Note: you need to `source .envrc` manually when `direnv` is not configured on your machine. 
#:
SHELL		:= bash
MAKEFLAGS   += silent warn-undefined-variables no-print-directory
CERTIFICATE := public.pem
#:
#:encrypt-string
#:--------------
#:
#:Encrypt string with a public certificate using kubeseal command
#:
#:* Using exported `NAMESPACE` (see `.envrc` file)
#:
#:```
#:make encrypt-string
#:```
#:* With specified namespace
#:
#:```
#:make encrypt-string NAMESPACE=kube-system
#:``` 
#:
#:Output:
#:
#:> AgA+8TrX....62VA=
#:
#:The consuming `SealedSecret` resource will require a `cluster-wide` annotation (with quoted `true` value):
#:
#: > sealedsecrets.bitnami.com/cluster-wide: "true"
#:
#:```
#:apiVersion: bitnami.com/v1alpha1
#:kind: SealedSecret
#:metadata:
#:  name: somesecret
#:  namespace: example
#:  annotations:
#:    sealedsecrets.bitnami.com/cluster-wide: "true"
#:spec:
#:  encryptedData:
#:	  mykey: AgA+8TrX....62VA=
#: 	  otherkey: AgAVhHnyv....OkyM=
#:```
#:
.PHONY: encrypt-string
encrypt-string:
	tr -d \\n $(cat /dev/stdin)|kubeseal --cert $(CERTIFICATE) --raw --from-file /dev/stdin --scope cluster-wide;echo

.PHONY: encrypt-file
encrypt-file:
	cat /dev/stdin|kubeseal --cert $(CERTIFICATE) --raw --from-file /dev/stdin --scope cluster-wide;echo

#:README.md
#:---------
#:
#:To re-generate this document run:
#:
#:```
#:rm -f README.md; make README.md
#:```
#:
README.md: $(firstword $(MAKEFILE_LIST))
	sed -n 's/^#://p' $< >$@

# vi: ft=make
