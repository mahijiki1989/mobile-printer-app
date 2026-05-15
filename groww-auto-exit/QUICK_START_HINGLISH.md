# Groww Auto-Exit - Quick Start (Hinglish)

Yeh ek Windows desktop app hai jo aapke Groww account ki open positions ko
auto-exit karta hai jab aapka P&L threshold hit hota hai.

## Zaroori cheezein (ek baar setup)

1. **Python 3.11** install karo: https://www.python.org/downloads/
   - Install karte waqt "Add Python to PATH" checkbox MUST tick karna hai.
2. **Groww API token** lo: https://groww.in/trade-api
   - Login karke "Generate API Token" se access token banao.

## Install karna (sirf ek baar)

1. `GrowwAutoExit-source.zip` ko extract karo (kahin bhi, jaise `C:\GrowwAutoExit\`).
2. Extract ki hui folder ke andar jao.
3. **`install.bat`** pe double-click karo.
   - Yeh automatically venv banayega aur saari dependencies install karega.
   - 2-5 minutes lag sakte hain (PySide6 thoda heavy hai).
4. Install ke baad `.env` file Notepad mein open karo.
5. Apna Groww access token paste karo:
   ```
   GROWW_ACCESS_TOKEN=yahan_apna_token_paste_karo
   ```
6. Save karo aur close karo.

## App chalana

Bas **`start.bat`** pe double-click karo. Bas itna hi.

Pehli baar app `paper` mode mein khulega - yeh **safe** mode hai, koi real
order place nahi hota. Real prices aate hain Groww se, par exit orders
sirf simulate hote hain.

## Pehli baar kya karein

1. App khulne ke baad **Settings** tab pe jao.
2. Apna access token paste karke "Save credentials to keyring" daba do.
   - Iske baad `.env` se token hata sakte ho - Windows Credential Manager
     mein safe save ho gaya.
3. **Default target/stop** set karo (Settings > Risk caps section nahi,
   Rules tab mein "Default rule for new positions"):
   - Target +INR: jaise 1000
   - Stop -INR: jaise -500
4. Groww app ya web pe manually koi trade lo (jaise hamesha lete ho).
5. **Positions** tab mein wo trade automatic dikhne lagega.
6. Default rule auto-attach ho jayega.
7. Jab MTM +1000 ya -500 cross karega, app khud exit order maar dega.

## Live mode (real money) mein switch karna

Pehle paper mode mein 1-2 din test karo. Phir:

1. Settings tab > Mode dropdown > **live** select karo.
2. "Apply mode" daba do, confirm karo.
3. Top mein laal **LIVE** banner dikhega - matlab real orders jayenge.

LIVE mode mein safety:
- Top right pe red `LIVE` badge hamesha visible
- "Require manual confirmation" ON rakho shuru mein
- **PANIC EXIT ALL** button hamesha kaam karta hai - emergency mein use karo
- Settings mein `Daily max loss` set rakho (default -5000) - itna loss hote
  hi kill switch trip ho jata hai, naye orders block ho jate hain

## Modes ka difference

| Mode  | Prices  | Orders                  | Use kab kare              |
|-------|---------|-------------------------|---------------------------|
| live  | real    | real (paisa lagta hai)  | production                |
| paper | real    | simulate (safe)         | testing / strategy check  |
| mock  | fake    | simulate                | offline UI test           |

## Ekdum standalone .exe banana (optional)

Agar `.exe` file chahiye jo bina Python ke chale:

1. Pehle `install.bat` chala lo.
2. Phir **`build_exe.bat`** double-click karo.
3. 5-10 minute lagega.
4. `dist\GrowwAutoExit\GrowwAutoExit.exe` ban jayega.
5. Pure `dist\GrowwAutoExit\` folder ko distribute karo.

## Common problems

**"Python 3.11 is not installed"**
- Python.org se 3.11 install karo. Custom install karte time "Add to PATH" check karo.

**"Module not found" type errors**
- `install.bat` dobara chala lo.

**App khulta hai par "Disconnected" dikhata hai**
- Token galat hai ya expire ho gaya. Settings tab mein naya paste karo.
- Mode `mock` rakho jab tak token nahi hai - app fir bhi UI test ke liye chalega.

**Trading hours ke bahar test karna hai**
- Settings tab mein `Trading hours start` aur `end` change kar do (jaise
  00:00 se 23:59).

**Notification nahi aa raha**
- Windows mein "Focus assist" off karo.
- Volume on hai check karo.

## Safety reminder

Yeh app aapke paise se trade karta hai LIVE mode mein. Pehle paper mode
mein achhe se test karo. Saari risk caps (daily loss, max positions,
trading hours) settings tab mein set rakho.

App apne aap **naye trades nahi leta** - sirf jo trades aap manually Groww
mein lete ho un par auto-exit lagata hai. Yeh by design hai.
