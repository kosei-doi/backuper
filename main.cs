using System;
using System.Diagnostics;

class Program
{
    static void Main()
    {
        ProcessStartInfo psInfo = new ProcessStartInfo("cmd.exe", @"/k D:\ProgramFiles\anaconda\Scripts\activate.bat && python D:\dev\backuper\main.py");
        psInfo.CreateNoWindow = true;
        psInfo.UseShellExecute = false; 

        Process.Start(psInfo);
    }
}