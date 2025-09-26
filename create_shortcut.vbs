Set oWS = WScript.CreateObject("WScript.Shell")
userDesktop = oWS.SpecialFolders("Desktop")

Set oLink = oWS.CreateShortcut(userDesktop & "\SOS Assessment Tool.lnk")
oLink.TargetPath = "C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool\Launch_SOS_UI.bat"
oLink.WorkingDirectory = "C:\Users\feket\OneDrive\Desktop\excelsior\r_staff\r_3\Deployed_Code_Op_Locations\SOS-Assessment-Automation-Tool"
oLink.IconLocation = "C:\Users\feket\OneDrive\Desktop\SOS_Tool.ico"
oLink.Description = "Launch SOS Assessment Tool"
oLink.Save

WScript.Echo "Shortcut created on desktop: SOS Assessment Tool"