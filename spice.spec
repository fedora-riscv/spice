Name:           spice
Version:        0.10.0
Release:        1%{?dist}
Summary:        Implements the SPICE protocol
Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://www.spice-space.org/
Source0:        http://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2
Source1:        spice-xpi-client-spicec

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:  i686 x86_64

BuildRequires:  pkgconfig
BuildRequires:  spice-protocol >= 0.9.1
BuildRequires:  celt051-devel
BuildRequires:  pixman-devel alsa-lib-devel openssl-devel libjpeg-devel
BuildRequires:  libXrandr-devel cegui06-devel
BuildRequires:  libcacard-devel cyrus-sasl-devel

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

%package client
Summary:          Implements the client side of the SPICE protocol
Group:            User Interface/Desktops
Requires(post):   %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description client
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the SPICE client application.

%package server
Summary:        Implements the server side of the SPICE protocol
Group:          System Environment/Libraries

%description server
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

This package contains the run-time libraries for any application that wishes
to be a SPICE server.

%package server-devel
Summary:        Header files, libraries and development documentation for spice-server
Group:          Development/Libraries
Requires:       %{name}-server = %{version}-%{release}
Requires:       pkgconfig

%description server-devel
This package contains the header files, static libraries and development
documentation for spice-server. If you like to develop programs
using spice-server, you will need to install spice-server-devel.

%prep
%setup -q

%build
%configure --enable-gui --enable-smartcard
make -C common WARN_CFLAGS='' %{?_smp_mflags}
make -C client WARN_CFLAGS='' %{?_smp_mflags}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} -C client install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
%endif
mkdir -p %{buildroot}%{_libexecdir}
touch %{buildroot}%{_libexecdir}/spice-xpi-client
install -m 0755 %{_sourcedir}/spice-xpi-client-spicec %{buildroot}%{_libexecdir}/

%files client
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_bindir}/spicec
%ghost %{_libexecdir}/spice-xpi-client
%{_libexecdir}/spice-xpi-client-spicec

%post client
%{_sbindir}/update-alternatives --install %{_libexecdir}/spice-xpi-client \
  spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec 10

%postun client
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove spice-xpi-client %{_libexecdir}/spice-xpi-client-spicec
fi

%files server
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_libdir}/libspice-server.so.1
%{_libdir}/libspice-server.so.1.0.2

%post server -p /sbin/ldconfig

%postun server -p /sbin/ldconfig

%files server-devel
%defattr(-,root,root,-)
%{_includedir}/spice-server
%{_libdir}/libspice-server.so
%{_libdir}/pkgconfig/spice-server.pc

%changelog
* Thu Nov 10 2011 Alon Levy <alevy@redhat.com> - 0.10.0-1
- New upstream release 0.10.0
- support spice-server.i686

* Wed Sep 28 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.1-2
- Provides spice-xpi-client alternative in spice-client

* Thu Aug 25 2011 Hans de Goede <hdegoede@redhat.com> - 0.9.1-1
- New upstream release 0.9.1

* Mon Jul 25 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.9.0-1
- New upstream release 0.9.0

* Wed Apr 20 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.1-1
- New upstream release 0.8.1

* Fri Mar 11 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.0-2
- Fix being unable to send ctrl+alt+key when release mouse is bound to
  ctrl+alt (which can happen when used from RHEV-M)

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.8.0-1
- New upstream release 0.8.0

* Fri Feb 11 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.3-1
- New upstream release 0.7.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.2-1
- New upstream release 0.7.2

* Fri Dec 17 2010 Hans de Goede <hdegoede@redhat.com> - 0.7.1-1
- New upstream release 0.7.1
- Drop all patches (all upstreamed)
- Enable smartcard (CAC) support

* Wed Nov 17 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-4
- Fix the info layer not showing when used through the XPI
- Do not let the connection gui flash by when a hostname has been specified
  on the cmdline
- Fix spice client locking up when dealing with XIM input (#654265)
- Fix modifier keys getting stuck (#655048)
- Fix spice client crashing when dealing with XIM ibus input (#655836)
- Fix spice client only showing a white screen in full screen mode

* Sat Nov  6 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-3
- Log to ~/.spicec/cegui.log rather then to CEGUI.log in the cwd, this
  fixes spicec from aborting when run in a non writable dir (#650253)

* Fri Nov  5 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-2
- Various bugfixes from upstream git:
  - Make spicec work together with the Firefox XPI for RHEV-M
  - Make sure the spicec window gets properly raised when first shown

* Mon Oct 18 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-1
- Update to 0.6.3
- Enable GUI

* Thu Sep 30 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.6.1-1
- Update to 0.6.1.

* Tue Aug 31 2010 Alexander Larsson <alexl@redhat.com> - 0.6.0-1
- Update to 0.6.0 (stable release)

* Tue Jul 20 2010 Alexander Larsson <alexl@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Tue Jul 13 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-4
- Quote %% in changelog to avoid macro expansion.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-3
- %%configure handles CFLAGS automatically, no need to fiddle
  with %%{optflags} manually.

* Mon Jul 12 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-2
- Fix license: LGPL.
- Cleanup specfile, drop bits not needed any more with
  recent rpm versions (F13+).
- Use optflags as-is.
-

* Fri Jul 9 2010 Gerd Hoffmann <kraxel@redhat.com> - 0.5.2-1
- initial package.

