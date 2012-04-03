%define version 1
%define release 1.el6_CS
%define installed_rvm_path /usr/local/rvm


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

Rubies in this package:
ruby-1.9.3-p0
  bundler
  bluepill
  whenever

ruby-1.9.2-p290
  bundler
  bluepill
  whenever


%install

test -e %{_sysconfdir}/profile.d/rvm.sh

rm -rf %{buildroot}
mkdir -p %{buildroot}

mkdir -p %{buildroot}%{installed_rvm_path}
rsync -a --exclude=.git --exclude=src --exclude='src-*' %{installed_rvm_path}/* %{buildroot}%{installed_rvm_path}/

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
cp -a %{_sysconfdir}/rvmrc %{buildroot}%{_sysconfdir}/rvmrc
cp -a %{_sysconfdir}/profile.d/rvm.sh %{buildroot}%{_sysconfdir}/profile.d/rvm.sh

mkdir -p %{buildroot}%{_mandir}
rsync -av %{installed_rvm_path}/man/* %{buildroot}%{_mandir}
rm -rf %{buildroot}%{installed_rvm_path}/man

# Strip binaries
find %{buildroot} -type f -print0 |xargs -0 file --no-dereference --no-pad |grep 'not stripped' |cut -f1 -d: |xargs -r strip


%clean
rm -rf %{buildroot}


%pre
if test -e %{installed_rvm_path}; then
    echo %{installed_rvm_path} already exist
    exit -1
fi

getent group %{rvm_group} >/dev/null || groupadd -r %{rvm_group}

exit 0


%postun
rm -rf %{installed_rvm_path}
exit 0


%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/rvmrc
%config(noreplace) %{_sysconfdir}/profile.d/rvm.sh
%attr(-,root,%{rvm_group}) %{installed_rvm_path}
%{_mandir}


%changelog
* Tue Mar 03 2012 Alexandre Fouche 1.0
Package existing preinstalled RVM into a RPM
