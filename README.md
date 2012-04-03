This is a script to package a preinstalled RVM into a RPM.

1. On a machine, install RVM, rubies and gems
1. On the same machine, git clone this repo somewhere
1. Edit the file `rvm_ruby.spec` to change the few variables at the top, the description with list of included rubies and gems, and the changelog at the end
1. Run `./package_rvm_rpmb` tp package your preinstalled RVM into a RPM.
    1. It will create a `rpmbuild` directory.
    1. Once finished, RPMs will be in `rpmbuild/RPMS`
1. You can sign the generated rpm manually with `rpm --resign`
