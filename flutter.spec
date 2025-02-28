%global _missing_build_ids_terminate_build 0
%global debug_package %{nil}
%global __debugsource_packages %{nil}

Name:           flutter
Version:        3.24.0
Release:        1%{?dist}
Summary:        Google's UI toolkit for building natively compiled applications

License:        BSD-3-Clause
URL:            https://flutter.dev
Source0:        https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{version}-stable.tar.xz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  git
BuildRequires:  clang
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(x11)
Requires:       bash
Requires:       dart
Requires:       git
Requires:       which
Requires:       xz
Requires:       unzip
Requires:       curl
Requires:       mesa-libGL
Requires:       liberation-fonts

%description
Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase.

%prep
%setup -q -n flutter

%build
# Flutter manages its own build process; ensure it’s set up correctly
bin/flutter config --no-analytics
bin/flutter doctor

%install
# Install Flutter to /opt/flutter in the build root
mkdir -p %{buildroot}/opt/flutter
cp -r . %{buildroot}/opt/flutter

# Create a symlink in /usr/bin for system-wide access
mkdir -p %{buildroot}/usr/bin
ln -s /opt/flutter/bin/flutter %{buildroot}/usr/bin/flutter

%files
/opt/flutter/*
/usr/bin/flutter

%changelog
* Wed Sep 18 2024 Your Name <your.email@example.com> - 3.24.0-1
- Initial package for Flutter
