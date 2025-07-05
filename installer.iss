[Setup]
AppName=PyCMS
AppVersion=1.0
DefaultDirName={pf}\PyCMS
DefaultGroupName=PyCMS
OutputBaseFilename=PyCMSInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\app.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\PyCMS"; Filename: "{app}\app.exe"
