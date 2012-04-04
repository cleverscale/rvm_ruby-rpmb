%define version 2.2
%define release 1.el6_CS
%define installed_rvm_path /usr/local/rvm

%global rvm_group rvm

Name: rvm_ruby
Summary: Ruby Version Manager
Version: %{version}
Release: %{release}
License: ASL 2.0
URL: http://rvm.beginrescueend.com/
Group: Applications/System

#BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-%(%{__id_u} -n)

BuildRequires:  rsync

%description
RVM is the Ruby Version Manager (rvm). It manages Ruby interpreter environments
and switching between them.

This RPM is a simply a packaging of a preinstalled RVM with following rubies and gems:

rvm 1.11.6 (stable)

Rubies in this package:
ruby-1.9.3-p0
    activesupport (3.2.3)
    bundler (1.1.3)
    chronic (0.6.7)
    i18n (0.6.0)
    multi_json (1.2.0)
    rake (0.9.2)
    redis (2.2.2)
    redis-namespace (1.0.3)
    rubygems-bundler (0.3.0)
    whenever (0.7.3)

ruby-1.9.2-p290
    activesupport (3.2.3)
    bundler (1.1.3)
    chronic (0.6.7)
    i18n (0.6.0)
    multi_json (1.2.0)
    rake (0.9.2)
    rubygems-bundler (0.3.0)
    whenever (0.7.3)


%install

test -e %{_sysconfdir}/profile.d/rvm.sh

rm -rf %{buildroot}
mkdir -p %{buildroot}

mkdir -p %{buildroot}%{installed_rvm_path}
rsync -a --exclude=.git --exclude=src --exclude='src-*' %{installed_rvm_path}/* %{buildroot}%{installed_rvm_path}/

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp -a %{_sysconfdir}/rvmrc %{buildroot}%{_sysconfdir}/rvmrc
cp -a %{_sysconfdir}/profile.d/rvm.sh %{buildroot}%{_sysconfdir}/profile.d/rvm.sh

pushd /usr/local/rvm/man
for f in `find . -type f`; do
    mkdir -p %{buildroot}%{_mandir}/`dirname $f`
    ln -s %{installed_rvm_path}/man/$f %{buildroot}%{_mandir}/$f
done
popd

# Strip binaries
find %{buildroot} -type f -print0 |xargs -0 file --no-dereference --no-pad |grep 'not stripped' |cut -f1 -d: |xargs -r strip


%clean
rm -rf %{buildroot}


%pre
rpm --quiet -q %{name}
is_installed=$?
if test -e %{installed_rvm_path} -a $is_installed -ne 0; then
    echo %{installed_rvm_path} already exist
    exit -1
fi

getent group %{rvm_group} >/dev/null || groupadd -r %{rvm_group}

exit 0


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rvmrc
%config(noreplace) %{_sysconfdir}/profile.d/rvm.sh
%attr(-,root,%{rvm_group}) %{installed_rvm_path}
%{_mandir}


%changelog
* Wed Mar 04 2012 Alexandre Fouche 2.2
- added redis and redis-namespace gems to ruby-1.9.3-p0

* Tue Mar 03 2012 Alexandre Fouche 2.1
- added "rvm_project_rvmrc=0" to /etc/rvmrc

* Tue Mar 03 2012 Alexandre Fouche 2.0
- add ruby-1.9.2-p290 with gems

* Tue Mar 03 2012 Alexandre Fouche 1.0
Package existing preinstalled RVM into a RPM
- ruby-1.9.3-p0 with gems
