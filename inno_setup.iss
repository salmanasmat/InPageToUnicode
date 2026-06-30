#define MyAppName "InPage Unicode Converter"
#define MyAppVersion "1.0"
#define MyAppExeName "InPage Unicode Converter.exe"
#define MyAppPublisher "Antigravity"
#define MyAppDir "C:\Program Files\InPageUnicodeConverter"

[Setup]
AppId=InPageUnicodeConverter
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={#MyAppDir}
DefaultGroupName={#MyAppName}
OutputDir=.\installer-output
OutputBaseFilename=InPageUnicodeConverter-Setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=assets\icon.ico

[Files]
Source: "dist\InPage Unicode Converter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\fonts\NotoNastaliqUrdu-Regular.ttf"; DestDir: "{app}\assets\fonts"; Flags: ignoreversion
Source: "assets\icon.ico"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: files; Name: "{app}\{#MyAppExeName}"
Type: files; Name: "{app}\assets\icon.ico"
Type: files; Name: "{app}\assets\fonts\NotoNastaliqUrdu-Regular.ttf"
Type: filesandordirs; Name: "{app}\assets"
