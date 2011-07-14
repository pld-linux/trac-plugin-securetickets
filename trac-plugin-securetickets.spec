%define		trac_ver	0.12
%define		plugin		securetickets
Summary:	SecureTickets Plugin for Trac
Name:		trac-plugin-%{plugin}
Version:	0.1.4
Release:	0.1
License:	BSD-like / GPL / ...
Group:		Applications/WWW
Source0:	%{plugin}plugin.zip
# Source0-md5:	9f706e733d205d4467ce6534772cb505
URL:		http://trac-hacks.org/wiki/SecureTicketsPlugin
BuildRequires:	python-devel
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This plugin attempts to provide fine-grained permissions for tickets
segmented by component. Specifically, unless a user has
SECURE_TICKET_VIEW permissions, they will only be able to see tickets
of public components. 

%prep
%setup -q -n %{plugin}plugin
mv %{trac_ver}/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

ver=$(awk '$1 == "Version:" {print $2}' *.egg-info/PKG-INFO)
test "$ver" = %{version}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable the %{plugin} plugin, add to conf/trac.ini:

	[components]
	%{plugin}.* = enabled
	...
	[securetickets]
	public_components = customer
	...
	[trac]
	permission_policies = SecureTicketsPolicy, DefaultPermissionPolicy, LegacyAttachmentPolicy
EOF
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{plugin}
%{py_sitescriptdir}/*-*.egg-info
