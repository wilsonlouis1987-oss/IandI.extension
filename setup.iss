[Setup]
AppName=I&I BIM Tools
AppVersion=1.0
DefaultDirName={userappdata}\pyRevit\Extensions
DisableDirPage=yes
OutputBaseFilename=I_and_I_BIM_Tools_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "IandI.extension\\*"; DestDir: "{app}\\I_and_I_BIM_Tools.extension"; Flags: ignoreversion recursesubdirs createallsubdirs; Excludes: "Output*,*.zip"
