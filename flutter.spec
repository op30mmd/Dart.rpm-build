%global debug_package %{nil}
%global __strip /bin/true
%global flutter_version 3.29.0

Name:           flutter
Version:        %{flutter_version}
Release:        1%{?dist}
Summary:        Flutter SDK - Google's UI toolkit for building applications
License:        BSD
URL:            https://flutter.dev/

Source0:        https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{flutter_version}-stable.tar.xz
# Disable analytics during build
Source1:        analytics_disabled

BuildRequires:  tar
BuildRequires:  xz
BuildRequires:  git
BuildRequires:  wget
BuildRequires:  unzip
BuildRequires:  ca-certificates
# Runtime dependencies
Requires:       git
Requires:       curl
Requires:       unzip
Requires:       which
Requires:       xz
Requires:       libglu
Requires:       libstdc++
Requires:       fontconfig
Requires:       cmake
Requires:       clang
Requires:       ninja-build
Requires:       gtk3-devel
# Network is disabled at build time in COPR
BuildRequires:  network-online
%if 0%{?fedora} >= 41
BuildRequires:  kernel-modules-core
%endif
ExclusiveArch:  x86_64

%description
Flutter is Google's UI toolkit for building beautiful, natively compiled 
applications for mobile, web, desktop, and embedded devices from a single 
codebase. Flutter works with existing code, is used by developers and 
organizations around the world, and is free and open source.

%prep
%setup -q -n flutter

# Create a mock config directory to disable analytics
mkdir -p .config

%build
# No traditional build - Flutter is distributed as prebuilt binaries
# We avoid running flutter commands that require network access
# as COPR has limited network connectivity during builds

%install
# Create directories
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}

# Copy the entire Flutter directory
cp -a ./* %{buildroot}%{_datadir}/%{name}/

# Create .config directory with analytics disabled
mkdir -p %{buildroot}%{_datadir}/%{name}/.config
cp -a %{SOURCE1} %{buildroot}%{_datadir}/%{name}/.config/

# Remove unnecessary files for smaller package
rm -rf %{buildroot}%{_datadir}/%{name}/.git
rm -rf %{buildroot}%{_datadir}/%{name}/dev
rm -rf %{buildroot}%{_datadir}/%{name}/.github

# Create symlinks to Flutter executables
ln -sf %{_datadir}/%{name}/bin/flutter %{buildroot}%{_bindir}/flutter
ln -sf %{_datadir}/%{name}/bin/dart %{buildroot}%{_bindir}/flutter-dart

# Create a wrapper script that runs flutter precache on first use
cat > %{buildroot}%{_bindir}/flutter-setup << 'EOF'
#!/bin/bash
echo "Performing first-time Flutter setup..."
flutter precache --linux
flutter doctor
echo "Flutter setup complete!"
EOF
chmod +x %{buildroot}%{_bindir}/flutter-setup

%post
echo "Flutter has been installed. For first-time setup, run 'flutter-setup'"

%files
%license LICENSE
%{_bindir}/flutter
%{_bindir}/flutter-dart
%{_bindir}/flutter-setup
%{_datadir}/%{name}/
