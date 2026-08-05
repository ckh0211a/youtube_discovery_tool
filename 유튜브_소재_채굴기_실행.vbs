Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' EXE 파일 경로 (이 .vbs 파일과 같은 폴더에 있어야 합니다)
strDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
strExe = strDir & "\dist\YouTubeDiscoveryTool.exe"

If objFSO.FileExists(strExe) Then
    ' EXE를 일반 창 모드(1)로 실행. (PyInstaller 자체에서 console=False로 빌드되어 콘솔 창은 안 보입니다)
    objShell.Run Chr(34) & strExe & Chr(34), 1, False
Else
    MsgBox "YouTubeDiscoveryTool.exe 파일을 찾을 수 없습니다." & vbCrLf & _
           "이 .vbs 파일과 같은 폴더에 EXE 파일이 있어야 합니다." & vbCrLf & vbCrLf & _
           "경로: " & strExe, vbCritical, "유튜브 소재 채굴기 — 오류"
End If
