#include <iostream>
#include"windows.h"
#include<string>
using namespace std;
int main(){
    HANDLE hComm;
    hComm=CreateFile(
            "com7",
            GENERIC_READ | GENERIC_WRITE,
            0,0,OPEN_EXISTING,0,0
            );
    if(hComm){
        cout<<"success"<<endl;
    }
    const char* lpOutBuffer;
    string sbuffer="1 100 100";
    lpOutBuffer=sbuffer.c_str();
    DWORD dwBytesWrite=100;
    COMSTAT ComStat;
    DWORD dwErrorFlags;
    BOOL bWriteStat;
    ClearCommError(hComm,&dwErrorFlags,&ComStat);
    cout<<"send"<<endl;
    bWriteStat = WriteFile(hComm, lpOutBuffer, dwBytesWrite, &dwBytesWrite, NULL);

    PurgeComm(hComm, PURGE_TXABORT|
                    PURGE_RXABORT|PURGE_TXCLEAR|PURGE_RXCLEAR);
    return 0;
}