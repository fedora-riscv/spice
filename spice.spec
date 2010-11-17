Name:           spice
Version:        0.6.3
Release:        4%{?dist}
Summary:        Implements the SPICE protocol
Group:          User Interface/Desktops
License:        LGPLv2+
URL:            http://www.spice-space.org/
Source0:        http://www.spice-space.org/download/releases/%{name}-%{version}.tar.bz2
# bugfixes from upstream git
Patch1:         0001-spicec-x11-Change-source-of-controller-socket-name-f.patch
Patch2:         0002-client-Interpret-the-title-control-message-as-utf8-i.patch
Patch3:         0003-Remove-no-longer-used-wstring_printf-functions.patch
Patch4:         0004-spicec-x11-Do-not-set-_NET_WM_USER_TIME-to-0-on-star.patch
Patch5:         0005-spicec-x11-Listen-for-selection-owner-window-destroy.patch
Patch6:         0006-spicec-Make-cegui-log-to-app_data_dir-cegui.log.patch
Patch7:         0007-spicec-x11-Add-a-few-missing-XLockDisplay-calls-rhbz.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=613529
ExclusiveArch:  i686 x86_64

BuildRequires:  pkgconfig
BuildRequires:  spice-protocol >= 0.6.3
BuildRequires:  celt051-devel
BuildRequires:  pixman-devel alsa-lib-devel openssl-devel libjpeg-devel
BuildRequires:  libXrandr-devel cegui-devel

%description
The Simple Protocol for Independent Computing Environments (SPICE) is
a remote display system built for virtual environments which allows
you to view a computing 'desktop' environment not only on the machine
where it is running, but from anywhere on the Internet and from a wide
variety of machine architectures.

%package client
Summary:        Implements the client side of the SPICE protocol
Group:          User Interface/Desktops

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%configure --enable-gui
make -C client %{?_smp_mflags}
%ifarch x86_64
make %{?_smp_mflags}
%endif

%install
make DESTDIR=%{buildroot} -C client install
%ifarch x86_64
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/libspice-server.a
rm -f %{buildroot}%{_libdir}/libspice-server.la
%endif

%files client
%defattr(-,root,root,-)
%doc COPYING README NEWS
%{_bindir}/spicec

%ifarch x86_64

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

%endif

%changelog
* Wed Nov 17 2010 Hans de Goede <hdegoede@redhat.com> - 0.6.3-4
- Fix spice client locking up when dealing with XIM input (#654265)

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

