[Setup]
AppName=Clinic Management System
AppVersion=1.0
DefaultDirName={pf}\ClinicCMS
DefaultGroupName=ClinicCMS
OutputBaseFilename=ClinicCMSInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ClinicCMS"; Filename: "{app}\app.exe"
