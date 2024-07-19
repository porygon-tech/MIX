#include <windows.h>
#include <iostream>

HHOOK hhkLowLevelKybd = NULL;
bool hookEnabled = false;
HWND hwndButton;

// Low-level keyboard hook procedure
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        KBDLLHOOKSTRUCT* p = (KBDLLHOOKSTRUCT*)lParam;

        // Check if the key is the Windows key (VK_LWIN or VK_RWIN)
        if (p->vkCode == VK_LWIN || p->vkCode == VK_RWIN) {
            // Block the key press
            return 1;
        }
    }
    // Pass the message to the next hook procedure
    return CallNextHookEx(NULL, nCode, wParam, lParam);
}

// Enable the keyboard hook
void EnableHook() {
    if (!hookEnabled) {
        hhkLowLevelKybd = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, 0, 0);
        if (hhkLowLevelKybd != NULL) {
            hookEnabled = true;
            SetWindowText(hwndButton, "Enable Super Key");
        }
    }
}

// Disable the keyboard hook
void DisableHook() {
    if (hookEnabled) {
        UnhookWindowsHookEx(hhkLowLevelKybd);
        hhkLowLevelKybd = NULL;
        hookEnabled = false;
        SetWindowText(hwndButton, "Disable Super Key");
    }
}

// Window procedure to handle messages
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE:
            hwndButton = CreateWindow(
                "BUTTON", "Disable Super Key",
                WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
                10, 10, 200, 30,
                hwnd, (HMENU)1, GetModuleHandle(NULL), NULL
            );
            break;

        case WM_COMMAND:
            if (LOWORD(wParam) == 1) {
                if (hookEnabled) {
                    DisableHook();
                } else {
                    EnableHook();
                }
            }
            break;

        case WM_DESTROY:
            PostQuitMessage(0);
            break;

        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

int main() {
    const char* CLASS_NAME = "SuperKeyDisabler";

    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = CLASS_NAME;

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        "PorygonTech Super Key Disabler",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 250, 100,
        NULL,
        NULL,
        GetModuleHandle(NULL),
        NULL
    );

    if (hwnd == NULL) {
        std::cerr << "Failed to create window!" << std::endl;
        return 1;
    }

    ShowWindow(hwnd, SW_SHOW);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    if (hookEnabled) {
        DisableHook();
    }

    return 0;
}
