%define version	0.1.0
%define release	%mkrel 2

%define scim_version	1.4.2

%define libname_orig lib%{name}
%define libname %mklibname %{name} 0

Name:		scim-sinhala
Summary:	An SCIM IMEngine module for Sinhala
Version:		%{version}
Release:		%{release}
Group:		System/Internationalization
License:		GPL
URL:			http://sourceforge.jp/projects/scim-imengine/
Source0:		%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:			%{libname} = %{version}
Requires:			scim >= %{scim_version}
# requires sinhala support
Requires:			locales-si
BuildRequires:		scim-devel >= %{scim_version}
BuildRequires:		automake1.8, libltdl-devel

%description
Scim-sinhala is an SCIM IMEngine module for Sinhala.


%package -n %{libname}
Summary:	Scim-sinhala library
Group:		System/Internationalization
Provides:		%{libname_orig} = %{version}-%{release}

%description -n %{libname}
scim-sinhala library.


%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unneeded files
rm -f %{buildroot}/%{_libdir}/scim-1.0/*/*.{a,la}

# remove empty mo files
for i in %{buildroot}/usr/share/locale/*/LC_MESSAGES/*.mo
do
	msgunfmt $i | LANGUAGE=C msgfmt -v -o /dev/null - 2> tmpfile
	if grep "0 translated messages." tmpfile
	then
		rm -f $i
	fi
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root)
# ChangeLog and NEWS are currently empty.  
%doc AUTHORS COPYING README
%{_datadir}/scim/icons/*

%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/scim-1.0/IMEngine/*.so

