Name:		robert
# Version from source package name
Version:	0.0.40
Release:	1%{?dist}
Summary:	Robert I2P BitTorrent Client

Group:		Applications/Internet
# License from LICENSES.TXT (and LeoXV.LICENSE.TXT) in src
License:	MIT and read source
URL:		http://bob.i2p/Robert.html
# Stable source URL: http://sponge.i2p/files/Robert-Stable.torrent
# Beta source URL: http://sponge.i2p/files/robert-beta.tar.gz.torrent
Source0:	Robert-%{version}-STABLE.tar.gz
Source1: 	%{name}.desktop
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch: 	noarch

Patch0: change-folders-for-iprediaos.patch
Patch1: set-lang-to-en-us-before-start.patch

# Installation script checks for this
BuildRequires:	python wxPython	

# desktop-file-utils: desktop-file-install
BuildRequires:	desktop-file-utils

# Requires from src/README.txt
# FIXTHIS: Add python-blist to this list.
#          src/README.txt
#          blist: This will boost performance in some areas.
Requires:	python wxPython i2p i2p-plugin-seedless

# Description from http://en.wikipedia.org/wiki/Robert_(P2P_Software)
%description
Robert is a file sharing application that relies upon the security and encryption of peers and tunnels inside of I2P.


%prep
# We must use -qn to tell the source directory name
%setup -qn Robert-src/src
%patch0 -p1
%patch1 -p1


%build
# Build is in the install script


%install
rm -rf $RPM_BUILD_ROOT

# Install in /usr/bin (%{_bindir}) and /usr/share/Robert (%{_datadir}/Robert) 
# Install script must have the bin dir before install
install -d $RPM_BUILD_ROOT%{_bindir}

# Install instructions from src/README.txt
# FIXTHIS: How do we exclude the install prefix from files in /usr/bin?
INSTALL=$RPM_BUILD_ROOT/usr PREFIX=$RPM_BUILD_ROOT/usr ./install

# Remove the prefix from installed files
find $RPM_BUILD_ROOT -type f | xargs sed -i "s|$RPM_BUILD_ROOT||g"

# Install desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{SOURCE1}


%post
# Enable BOB
# In i2p home
sed -i "s|clientApp.5.startOnLoad=false|clientApp.5.startOnLoad=true|g" /usr/local/i2p/.i2p/clients.config
# In i2p installation (needed for fresh installations)
sed -i "s|clientApp.5.startOnLoad=false|clientApp.5.startOnLoad=true|g" %{_bindir}/i2p/clients.config

# Rebuild desktop database
update-desktop-database > /dev/null 2>&1 || :

# Condrestart i2p and return 0
/sbin/service i2p condrestart >/dev/null 2>&1 || :


%postun 
# Update desktop database
update-desktop-database > /dev/null 2>&1 || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{_bindir}/Robert
%{_bindir}/SeaWeed
%{_bindir}/btmakemetafile
%{_bindir}/btshowmetainfo
%{_datadir}/Robert
%{_datadir}/applications/%{name}.desktop


%changelog
* Sat Jan 26 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.40-1
- Update to 0.0.40

* Sun Jan 6 2013 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.37-1
- Update to 0.0.37

* Thu Jul 26 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.35-1
- Update to 0.0.35

* Sat Jul 7 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com>
- Update to 0.0.34-beta5

* Wed Jun 20 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.33-1
- Update to 0.0.33

* Thu Apr 5 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.32-4
- Change settings

* Sat Mar 24 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.32-3
- Add robert-helper

* Sat Mar 24 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.32-2
- Add desktop file

* Sat Mar 24 2012 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 0.0.32-1
- Initial package (Robert 0.0.32-beta2)
