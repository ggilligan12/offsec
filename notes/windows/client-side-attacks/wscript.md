### WScript

Default apps in Windows are worth being aware of. The default app for files with a `.ps1` extension is notepad. Therefore even if we successfully socially engineer a user into clicking on a malicious `.ps1`, it will not be executed, and will instead just be opened for editing. By contrast, `.js` files default to the Windows-Based Script Host, aka WScript. When executing `.js` files with `cscript` or `wscript` then the runtime in use is the JScript engine, a hilarious old and deprecated piece of shit. `JScript` provides many wonderful features for the attacker, for instance, direct interaction with ActiveX.

```javascript
var shell = new ActiveXObject("WScript.Shell")
var res = shell.Run("cmd.exe");
```