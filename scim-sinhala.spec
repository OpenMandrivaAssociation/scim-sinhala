%define snapdate 20060825
%define scim_version	1.4.7

Name:		scim-sinhala
Summary:	An SCIM IMEngine module for Sinhala
Version:	0.2.0
Release:	%mkrel 4
Group:		System/Internationalization
License:	GPL
URL:		http://sinhala.sourceforge.net
Source0:	%{name}-trans-%{version}-%{snapdate}.tar.gz
Patch1:         scim-sinhala-trans-autogen-automake.patch
Patch2:         scim-sinhala-remove-timeout-206253.patch
Patch3:         scim-sinhala-help-text-206114.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Requires:	scim-client = %{scim_api}
# requires sinhala support
Requires:	locales-si
BuildRequires:	scim-devel >= 1.4.7-4mdk
BuildRequires:	automake, libltdl-devel
Obsoletes:	%{_lib}scim-sinhala0

%description
Scim-sinhala is an SCIM IMEngine module for Sinhala.

%prep
%setup -q -n %{name}-trans-%{version}-%{snapdate}
%patch1 -p1 -b .1-automake17
%patch2 -p1 -b .2-timeout
%patch3 -p1 -b .3-help

%build
autoreconf -fi
%configure2_5x --disable-static
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# remove unneeded files
rm -f %{buildroot}/%{scim_plugins_dir}/*/*.{a,la}

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

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
# ChangeLog and NEWS are currently empty.  
%doc AUTHORS COPYING README
%{_datadir}/scim/icons/*
%{scim_plugins_dir}/IMEngine/*.so
