# Linux Build Instructions

These instructions assume you're running this on a Mac with Vagrant installed,
and that the project directory ends up mounted in the VM at `/vagrant`. (this
should happen automatically)

## One-time setup of Development GPG keys:

To build Linux packages, you will need GPG v1 keys to sign the packages.  Do the following:

```
brew install gpg1
mkdir build-linux/gnupg
chmod 700 build-linux/gnupg
gpg1 --homedir=build-linux/gnupg --gen-key
```

For key generation use the suggested defaults and *no passphrase*. (when
asked to enter a passphrase, just press *Enter*)

If you use a different `gpg-home`, please adjust the `gpg-home` parameter in
the following instructions accordingly.

## Ubuntu

Building the .deb:

```
scons local-repo \
  gpg-home=build-linux/gnupg \
  virt=agent-minimal-ubuntu1204
```

Install & test the .deb:
```
vagrant ssh agent-minimal-ubuntu1204

sudo apt-key add /vagrant/target/tmp/GPG-KEY-pagerduty
sudo sh -c 'echo "deb file:///vagrant/target deb/" \
  >/etc/apt/sources.list.d/pdagent.list'
sudo apt-get update
sudo apt-get install pdagent
sudo service pdagent status
which pd-send
python -c "import pdagent; print pdagent.__file__"
```

Uninstall & test cleanup:
```
sudo apt-get --yes remove pdagent

# ensure that artifacts are no longer present
sudo service pdagent status
which pd-send
```

Rerun the test commands to ensure files are gone

## CentOS / RHEL

Building the .rpm:
```
scons local-repo \
  gpg-home=/gpg/path/used/earlier \
  virt=agent-minimal-centos65
```

Install & test the .rpm:
```
vagrant ssh agent-minimal-centos65

sudo sh -c 'cat >/etc/yum.repos.d/pdagent.repo <<EOF
[pdagent]
name=PDAgent
baseurl=file:///vagrant/target/rpm
enabled=1
gpgcheck=1
gpgkey=file:///vagrant/target/tmp/GPG-KEY-pagerduty
EOF'

sudo yum install -y pdagent
sudo service pdagent status
which pd-send
python -c "import pdagent; print pdagent.__file__"
```

Uninstall & test cleanup:
```
sudo yum remove -y pdagent

# ensure that artifacts are no longer present
sudo service pdagent status
which pd-send
```
