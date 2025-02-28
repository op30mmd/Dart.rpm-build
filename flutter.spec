%global debug_package %{nil}
%global __strip /bin/true
%global flutter_version 3.19.5

Name:           flutter
Version:        %{flutter_version}
Release:        1%{?dist}
Summary:        Flutter SDK - Google's UI toolkit for building applications
License:        BSD
URL:            https://flutter.dev/

Source0:        https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_%{flutter_version}-stable.tar.xz

# This patch modifies Flutter to use the system Dart if we want to avoid bundled Dart
# Patch0:         flutter-use-system-dart.patch

BuildRequires:  tar
BuildRequires:  xz
# Uncomment if using system Dart instead of bundled Dart
# BuildRequires:  dart >= 3.2.0
Requires:       git
Requires:       curl
Requires:       unzip
Requires:       which
Requires:       xz-utils
Requires:       libglu
Requires:       libstdc++
Requires:       fontconfig
Requires:       cmake
Requires:       clang
Requires:       ninja-build
Requires:       gtk3-devel
ExclusiveArch:  x86_64

%description
Flutter is Google's UI toolkit for building beautiful, natively compiled 
applications for mobile, web, desktop, and embedded devices from a single 
codebase. Flutter works with existing code, is used by developers and 
organizations around the world, and is free and open source.

%prep
%setup -q -n flutter

# If using system Dart, apply the patch
# %patch0 -p1

%build
# Nothing to build initially, Flutter downloads additional components on first run
# We'll pre-download components to include in the package

# Configure Flutter to use the bundled Dart SDK
export FLUTTER_ROOT=$(pwd)
export PATH=$FLUTTER_ROOT/bin:$PATH

# Disable analytics for the build
flutter config --no-analytics

# Pre-download some components (cache Flutter tool, Dart SDK, etc.)
flutter precache --linux

# Download engine artifacts and tools
flutter doctor

%install
# Create directories
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_bindir}

# Copy the entire Flutter directory
cp -a ./* %{buildroot}%{_datadir}/%{name}/

# Remove unnecessary files for smaller package
rm -rf %{buildroot}%{_datadir}/%{name}/.git
rm -rf %{buildroot}%{_datadir}/%{name}/dev
rm -rf %{buildroot}%{_datadir}/%{name}/.github

# Create symlinks to Flutter executables
ln -sf %{_datadir}/%{name}/bin/flutter %{buildroot}%{_bindir}/flutter
ln -sf %{_datadir}/%{name}/bin/dart %{buildroot}%{_bindir}/flutter-dart

%files
%license LICENSE
%{_bindir}/flutter
%{_bindir}/flutter-dart
%{_datadir}/%{name}/
